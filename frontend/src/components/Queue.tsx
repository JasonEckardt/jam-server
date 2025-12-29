import useQueue, { type Track } from "@/hooks/useQueue";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Loader2 } from "lucide-react";

const Queue = () => {
  // Access token is handled by Flask session on the backend
  // The backend checks: session.get("access_token") or data.get("access_token")
  const accessToken = undefined;

  const {
    url,
    queue,
    setUrl,
    handleAddTrack,
    handleRemoveTrack,
    isConnected
  } = useQueue(accessToken);

  const nowPlaying: Track | null = queue?.tracks?.[0] || null;
  const upNext: Track[] = queue?.tracks?.slice(1) || [];

  // Optional: Add skip track functionality to the hook if needed
  // For now, we can just remove the first track
  const handleSkipTrack = () => {
    if (nowPlaying) {
      handleRemoveTrack(nowPlaying.id);
    }
  };

  return (
    <div className="space-y-4">
      {/* Connection status indicator (optional) */}
      {!isConnected && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-2 rounded">
          Connecting to server...
        </div>
      )}

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
          disabled={!url || !isConnected}
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
                disabled={!isConnected}
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
                      {track.images?.[0]?.url ? (
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
                        {track.artists?.join(", ") || "Unknown Artist"}
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
                      disabled={!isConnected}
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
