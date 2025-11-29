import { useEffect, useState, useRef } from "react";
import { fetch } from "@/services/fetch";
import { useMutation, useQueryClient } from "@tanstack/react-query";

interface UseQueueHookProps {
  url: string;
  queue: any;
  setUrl: (url: string) => void;
  handleAddTrack: () => void;
  handleRemoveTrack: (trackId: string) => void;
}

export interface Track {
  name: string;
  artists: string[];
  album: string;
  duration_ms: number;
  images: { url: string }[];
  id: string;
  pending?: boolean;
  tempId?: string;
}

const useQueue = (): UseQueueHookProps => {
  const [url, setUrl] = useState<string>("");
  const eventSourceRef = useRef<EventSource | null>(null);
  const queryClient = useQueryClient();

  const queueId = "main";

  const { mutate: getQueue } = useMutation({
    mutationKey: ["queue"],
    mutationFn: () => fetch(`/queues/${queueId}`),
    onSuccess: (data) => {
      // Update the cache when we fetch the queue
      queryClient.setQueryData(["queue", queueId], data);
    },
  });

  // Read queue from cache to get optimistic updates
  const queue = queryClient.getQueryData(["queue", queueId]);

  const { mutate: addToQueue } = useMutation({
    mutationKey: ["addToQueue"],
    mutationFn: () =>
      fetch(`/queues/${queueId}/tracks`, {
        method: "POST",
        body: JSON.stringify({ url }),
      }),
    onMutate: async () => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["queue", queueId] });

      // Snapshot the previous value
      const previousQueue = queryClient.getQueryData(["queue", queueId]);

      // Optimistically update with pending track
      const tempId = `temp-${Date.now()}`;
      const optimisticTrack: Track = {
        name: "Loading...",
        artists: [""],
        album: "",
        duration_ms: 0,
        images: [{ url: "" }],
        id: tempId,
        pending: true,
        tempId: tempId,
      };

      queryClient.setQueryData(["queue", queueId], (old: any) => ({
        ...old,
        tracks: [...(old?.tracks || []), optimisticTrack],
      }));

      // Return context for potential rollback
      return { previousQueue, tempId };
    },
    onSuccess: () => {
      setUrl("");
      // SSE will trigger getQueue() with real data
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousQueue) {
        queryClient.setQueryData(["queue", queueId], context.previousQueue);
      }
      console.error("Failed to add track:", err);
    },
  });

  const { mutate: removeFromQueue } = useMutation({
    mutationKey: ["removeFromQueue"],
    mutationFn: (trackId: string) =>
      fetch(`/queue/${trackId}`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      // getQueue();
    },
  });

  const handleAddTrack = () => {
    addToQueue();
  };

  const handleRemoveTrack = (trackId: string) => {
    removeFromQueue(trackId);
  };

  useEffect(() => {
    // Set up SSE connection - it will send initial snapshot once
    const eventSource = new EventSource(`/api/queues/${queueId}/update`);
    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      console.log("Queue update received:", event.data);
      const data = JSON.parse(event.data);

      if (data.type === 'snapshot') {
        // Initial snapshot on connect - load once, fast
        console.log("Received initial queue snapshot");
        queryClient.setQueryData(["queue", queueId], data.queue);
      } else if (data.type === 'update') {
        // Lightweight notification - refetch to get changes
        console.log("Queue changed, refetching...");
        getQueue();
      }
    };

    eventSource.onerror = (error) => {
      console.error("SSE connection error:", error);
    };

    eventSource.onopen = () => {
      console.log("SSE connection established");
    };

    // Cleanup on unmount
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        console.log("SSE connection closed");
      }
    };
  }, [queueId, getQueue, queryClient]);

  // Remove pending tracks after 15 seconds (timeout fallback)
  useEffect(() => {
    const currentQueue = queryClient.getQueryData<any>(["queue", queueId]);
    const hasPending = currentQueue?.tracks?.some((t: Track) => t.pending);

    if (!hasPending) return;

    const timeout = setTimeout(() => {
      queryClient.setQueryData(["queue", queueId], (old: any) => ({
        ...old,
        tracks: old?.tracks?.filter((t: Track) => !t.pending) || [],
      }));
    }, 15000);

    return () => clearTimeout(timeout);
  }, [queue, queueId, queryClient]);

  return {
    url,
    queue,
    setUrl,
    handleAddTrack,
    handleRemoveTrack,
  };
};

export default useQueue;
