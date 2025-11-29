import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import useQueue from "@/hooks/useQueue";
import { Loader2 } from "lucide-react";

interface Track {
  name: string;
  artists: string[];
  album: string;
  duration_ms: number;
  images: { url: string }[];
  id: string;
  pending?: boolean;
}

const Player = () => {
  const { queue } = useQueue();

  const nowPlaying: Track | null = queue?.tracks?.[0] || null;
  const upNext: Track[] = queue?.tracks?.slice(1) || [];

  return (
    <div className="space-y-4 max-w-xl">
      {/* Now Playing Card */}
      <Card>
        <CardHeader>
          <CardTitle>Now playing...</CardTitle>
        </CardHeader>
        <CardContent>
          {nowPlaying ? (
            <div className="flex gap-4">
              <div className="relative">
                <img
                  src={nowPlaying.images[0]?.url || '/placeholder-album.png'}
                  alt={`${nowPlaying.album} album cover`}
                  className={`w-32 h-32 rounded-md object-cover ${nowPlaying.pending ? 'opacity-50' : ''
                    }`}
                />
                {nowPlaying.pending && (
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
                  {nowPlaying.artists.join(", ")}
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
                  className={`flex gap-3 items-center ${track.pending ? 'opacity-60' : ''
                    }`}
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
                    <p className={`font-medium truncate ${track.pending ? 'text-gray-400' : ''
                      }`}>
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
  );
};

export default Player;
