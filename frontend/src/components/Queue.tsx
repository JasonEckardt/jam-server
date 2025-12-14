import { useEffect, useState } from "react";
import useQueue, { type Track } from "@/hooks/useQueue";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Loader2 } from "lucide-react";
import { io, Socket } from "socket.io-client";

const Queue = () => {
  const { url, queue, setUrl, setQueue } = useQueue();
  const [socket, setSocket] = useState<Socket | null>(null);
  const [queueId] = useState("some_queue"); // Could be dynamic based on session

  const nowPlaying: Track | null = queue?.tracks?.[0] || null;
  const upNext: Track[] = queue?.tracks?.slice(1) || [];

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io("/api/queues", {
      transports: ["websocket", "polling"]
    });

    setSocket(newSocket);

    // Join the queue
    newSocket.emit("join_queue", { queue_id: queueId });

    // Handle initial queue snapshot
    newSocket.on("queue_snapshot", (snapshot: { tracks: Track[] }) => {
      setQueue({ tracks: snapshot.tracks });
    });

    // Handle queue patches (real-time updates)
    newSocket.on("queue_patch", (patch: any) => {
      switch (patch.event) {
        case "add":
          setQueue((currentQueue) => ({
            tracks: [...(currentQueue?.tracks || []), patch.track]
          }));
          break;

        case "remove":
          setQueue((currentQueue) => ({
            tracks: (currentQueue?.tracks || []).filter(
              (track) => track.id !== patch.track_id
            )
          }));
          break;

        case "move":
          setQueue((currentQueue) => {
            const tracks = [...(currentQueue?.tracks || [])];
            const [movedTrack] = tracks.splice(patch.from, 1);
            tracks.splice(patch.to, 0, movedTrack);
            return { tracks };
          });
          break;

        case "clear":
          setQueue({ tracks: [] });
          break;

        case "skip":
          setQueue((currentQueue) => ({
            tracks: (currentQueue?.tracks || []).slice(1)
          }));
          break;

        default:
          console.warn("Unknown patch event:", patch.event);
      }
    });

    // Handle full queue updates (fallback)
    newSocket.on("queue_updated", (data: { queue: Track[] }) => {
      setQueue({ tracks: data.queue });
    });

    // Cleanup on unmount
    return () => {
      newSocket.emit("leave_queue", { queue_id: queueId });
      newSocket.close();
    };
  }, [queueId, setQueue]);

  // Send add track request to server
  const handleAddTrack = () => {
    if (!socket || !url) return;

    // Add optimistic update (optional)
    const tempTrack: Track = {
      id: `temp-${Date.now()}`,
      tempId: `temp-${Date.now()}`,
      name: "Loading...",
      artists: [],
      album: "",
      duration_ms: 0,
      images: [],
      pending: true
    };

    setQueue((currentQueue) => ({
      tracks: [...(currentQueue?.tracks || []), tempTrack]
    }));

    // Send mutation request to server
    socket.emit("add_track", {
      queue_id: queueId,
      url: url
    });

    setUrl("");
  };

  const handleSkipTrack = () => {
    if (!socket) return;

    socket.emit("skip_track", {
      queue_id: queueId
    });
  };

  const handleRemoveTrack = (trackId: string) => {
    if (!socket) return;

    socket.emit("remove_track", {
      queue_id: queueId,
      track_id: trackId
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex max-w-4xl gap-2">
        <Input
          type="text"
          placeholder="Enter the song URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAddTrack()}
        />
        <Button
          className="bg-green-500 hover:bg-green-600"
          onClick={handleAddTrack}
          disabled={!url || !socket}
        >
          Add to Queue
        </Button>
      </div>

      <div className="space-y-4 max-w-xl">
        {/* Now Playing Card */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Now playing...</CardTitle>
            {nowPlaying && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleSkipTrack}
              >
                Skip
              </Button>
            )}
          </CardHeader>
          <CardContent>
            {nowPlaying ? (
              <div className="flex gap-4">
                <div className="relative">
                  <img
                    src={nowPlaying?.images?.[0]?.url || '/placeholder-album.png'}
                    alt={`${nowPlaying?.album || 'Album'} cover`}
                    className={`w-32 h-32 rounded-md object-cover ${nowPlaying?.pending ? 'opacity-50' : ''}`}
                  />
                  {nowPlaying?.pending && (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Loader2 className="w-8 h-8 text-white animate-spin" />
                    </div>
                  )}
                </div>
                <div className="flex flex-col justify-center">
                  <p className={`font-semibold text-lg ${nowPlaying.pending ? 'text-gray-400' : ''}`}>
                    {nowPlaying.name}
                  </p>
                  <p className={`text-gray-600 ${nowPlaying.pending ? 'text-gray-400' : ''}`}>
                    {nowPlaying?.artists?.join(", ") || "Unknown Artist"}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">{nowPlaying.album}</p>
                </div>
              </div>
            ) : (
              <div className="text-gray-500 text-center py-8">
                No track currently playing
              </div>
            )}
          </CardContent>
        </Card>

        {/* Queue Card */}
        <Card>
          <CardHeader>
            <CardTitle>Up Next ({upNext.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {upNext.length > 0 ? (
              <div className="space-y-3">
                {upNext.map((track, index) => (
                  <div
                    key={track.tempId || track.id}
                    className={`flex gap-3 items-center ${track.pending ? 'opacity-60' : ''}`}
                  >
                    <span className="text-gray-400 text-sm font-medium w-6">
                      {index + 1}
                    </span>
                    <div className="relative">
                      {track.images[0]?.url ? (
                        <img
                          src={track.images[0].url}
                          alt={`${track.album} album cover`}
                          className="w-12 h-12 rounded object-cover"
                        />
                      ) : (
                        <div className="w-12 h-12 rounded bg-gray-200 flex items-center justify-center">
                          <span className="text-gray-400 text-xs">♪</span>
                        </div>
                      )}
                      {track.pending && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/30 rounded">
                          <Loader2 className="w-6 h-6 text-white animate-spin" />
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`font-medium truncate ${track.pending ? 'text-gray-400' : ''}`}>
                        {track.name}
                      </p>
                      <p className="text-sm text-gray-600 truncate">
                        {track.artists.join(", ")}
                      </p>
                    </div>
                    <span className="text-sm text-gray-500">
                      {track.duration_ms > 0 ? (
                        <>
                          {Math.floor(track.duration_ms / 60000)}:
                          {String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, "0")}
                        </>
                      ) : (
                        <span className="text-gray-400">--:--</span>
                      )}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveTrack(track.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      ✕
                    </Button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 text-center py-8">
                Queue is empty
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Queue;
