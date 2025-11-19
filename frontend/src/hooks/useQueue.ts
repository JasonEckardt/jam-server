import { useEffect, useState } from "react";
import { fetch } from "@/services/fetch";
import { useMutation } from "@tanstack/react-query";

interface UseQueueHookProps {
  url: string;
  queue: any;
  setUrl: (url: string) => void;
  handleAddTrack: () => void;
  handleRemoveTrack: (trackId: string) => void;
}

const useQueue = (): UseQueueHookProps => {
  const [url, setUrl] = useState<string>("");

  const queueId = "main";

  const { data: queue, mutate: getQueue } = useMutation({
    mutationKey: ["queue"],
    mutationFn: () => fetch(`api/queues/${queueId}`),
  });

  const { mutate: addToQueue } = useMutation({
    mutationKey: ["addToQueue"],
    mutationFn: () =>
      fetch(`/queues/${queueId}/tracks`, {
        method: "POST",
        body: JSON.stringify({ url }),
      }),
    onSuccess: () => {
      setUrl("");
      // getQueue();
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
    // getQueue();
  }, []);

  return {
    url,
    queue,
    setUrl,
    handleAddTrack,
    handleRemoveTrack,
  };
};

export default useQueue;
