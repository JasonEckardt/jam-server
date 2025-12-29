import { useEffect, useState, useRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { io, Socket } from "socket.io-client";

interface UseQueueHookProps {
  url: string;
  queue: any;
  setUrl: (url: string) => void;
  handleAddTrack: () => void;
  handleRemoveTrack: (trackId: string) => void;
  isConnected: boolean;
  isLoading: boolean; // Added this so UI knows when we are checking auth
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
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [url, setUrl] = useState<string>("");
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true); // New loading state

  const socketRef = useRef<Socket | null>(null);
  const queryClient = useQueryClient();

  const queueId = "main";
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:5000";

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/token`, {
          credentials: "include", // CRITICAL: Sends the cookie to Flask
        });

        if (res.ok) {
          const data = await res.json();
          console.log("Session found for user:", data.user_id);
          setAccessToken(data.access_token);
        } else {
          console.log("No active session found");
        }
      } catch (err) {
        console.error("Failed to fetch session:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSession();
  }, [BACKEND_URL]);

  // 2. socket logic (Now depends on accessToken)
  useEffect(() => {
    // Stop here if we don't have a token yet
    if (!accessToken) return;

    console.log("Initializing socket with token...");

    const socket = io(BACKEND_URL, {
      transports: ["websocket"],
      // Optional: Standard way to pass auth in SocketIO
      auth: { token: accessToken },
    });

    socketRef.current = socket;

    socket.on("connect", () => {
      console.log("WebSocket connected");
      setIsConnected(true);

      // Join the queue room (passing token as your backend expects)
      socket.emit("join_queue", {
        queue_id: queueId,
        access_token: accessToken,
      });
    });

    socket.on("disconnect", () => {
      console.log("WebSocket disconnected");
      setIsConnected(false);
    });

    socket.on("queue_snapshot", (data) => {
      console.log("Received queue snapshot:", data);
      queryClient.setQueryData(["queue", queueId], data);
    });

    socket.on("queue_patch", (patch) => {
      // ... (Your existing patch logic remains exactly the same) ...
      console.log("Received queue patch:", patch);
      queryClient.setQueryData(["queue", queueId], (old: any) => {
        if (!old) return old;
        switch (patch.event) {
          case "add":
            const tracksWithoutPending = old.tracks.filter((t: Track) => !t.pending);
            return { ...old, tracks: [...tracksWithoutPending, patch.track] };
          case "remove":
            return { ...old, tracks: old.tracks.filter((t: Track) => t.id !== patch.track_id) };
          case "skip":
            return { ...old, tracks: old.tracks.slice(1) };
          case "move":
            const newTracks = [...old.tracks];
            const [movedTrack] = newTracks.splice(patch.from, 1);
            newTracks.splice(patch.to, 0, movedTrack);
            return { ...old, tracks: newTracks };
          case "clear":
            return { ...old, tracks: [], };
          default:
            return old;
        }
      });
    });

    socket.on("error", (error) => {
      console.error("Socket error:", error.error);
      queryClient.setQueryData(["queue", queueId], (old: any) => {
        if (!old) return old;
        return { ...old, tracks: old.tracks.filter((t: Track) => !t.pending) };
      });
    });

    return () => {
      console.log("Cleaning up WebSocket connection");
      socket.emit("leave_queue", { queue_id: queueId });
      socket.disconnect();
    };
  }, [queueId, accessToken, queryClient, BACKEND_URL]); // Add accessToken dependency

  // ... (Your existing handleAddTrack/handleRemoveTrack logic) ...

  // Read queue from cache
  const queue = queryClient.getQueryData(["queue", queueId]);

  const handleAddTrack = () => {
    if (!socketRef.current || !url || !isConnected) {
      console.warn("Cannot add track: socket not connected or no URL");
      return;
    }

    const tempId = `temp-${Date.now()}`;
    const optimisticTrack: Track = {
      name: "Loading...",
      artists: [],
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

    socketRef.current.emit("add_track", {
      queue_id: queueId,
      url: url,
      access_token: accessToken, // Now uses the fetched token
    });

    setUrl("");
  };

  const handleRemoveTrack = (trackId: string) => {
    if (!socketRef.current || !isConnected) return;
    socketRef.current.emit("remove_track", {
      queue_id: queueId,
      track_id: trackId,
    });
  };

  useEffect(() => {
    const currentQueue = queryClient.getQueryData<any>(["queue", queueId]);
    const hasPending = currentQueue?.tracks?.some((t: Track) => t.pending);
    if (!hasPending) return;

    const timeout = setTimeout(() => {
      console.log("Removing pending tracks (timeout)");
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
    isConnected,
    isLoading, // Return this so UI can show a spinner
  };
};

export default useQueue;
