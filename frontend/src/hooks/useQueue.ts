import { useEffect, useState } from "react";
import { fetch } from "@/services/fetch";
import { useMutation, useQuery } from "@tanstack/react-query";

interface UseQueueHookProps {
  url: string;
  queue: any;
  setUrl: (url: string) => void;
  handleAddTrack: () => void;
  handleRemoveTrack: (trackId: string) => void;
}

const useQueue = (): UseQueueHookProps => {
  const [url, setUrl] = useState<string>("");

  const { data: queue, mutate: getQueue } = useMutation({
    mutationKey: ["queue"],
    mutationFn: () => fetch("/queue"),
  });

  const { mutate: addToQueue } = useMutation({
    mutationKey: ["addToQueue"],
    mutationFn: () =>
      fetch("/queue", {
        method: "POST",
        body: { url },
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
