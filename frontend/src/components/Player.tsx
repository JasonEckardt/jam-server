import { useState, useEffect } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Slider } from "./ui/slider";
import useQueue, { type Track } from "@/hooks/useQueue";
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  Users,
  Maximize2,
  Loader2
} from "lucide-react";

interface PlayerProps {
  isAdmin?: boolean;
}

const Player = ({ isAdmin = false }: PlayerProps) => {
  const { queue } = useQueue();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [volume, setVolume] = useState(80);
  const [showGuests, setShowGuests] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const track: Track | null = queue?.tracks?.[0] || null;
  const duration = track?.duration_ms ? track.duration_ms / 1000 : 0;

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Simulate time progress (in real app, sync with Spotify playback)
  useEffect(() => {
    if (!isPlaying || !track) return;

    const interval = setInterval(() => {
      setCurrentTime(prev => {
        if (prev >= duration) {
          setIsPlaying(false);
          return 0;
        }
        return prev + 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isPlaying, duration, track]);

  const handlePlayPause = () => {
    if (!isAdmin) return;
    setIsPlaying(!isPlaying);
    // TODO: Call Spotify API to play/pause
  };

  const handlePrevious = () => {
    if (!isAdmin) return;
    setCurrentTime(0);
    // TODO: Call backend to go to previous track
  };

  const handleNext = () => {
    if (!isAdmin) return;
    // TODO: Call backend to skip to next track
  };

  const handleSeek = (value: number[]) => {
    if (!isAdmin) return;
    setCurrentTime(value[0]);
    // TODO: Call Spotify API to seek
  };

  const handleVolumeChange = (value: number[]) => {
    if (!isAdmin) return;
    setVolume(value[0]);
    // TODO: Call Spotify API to set volume
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
    // TODO: Implement fullscreen jukebox view
  };

  if (!track) {
    return (
      <Card className="fixed bottom-0 left-0 right-0 bg-black text-white border-t border-gray-800">
        <div className="flex items-center justify-center h-24">
          <p className="text-gray-400">No track playing</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="fixed bottom-0 left-0 right-0 bg-black text-white border-t border-gray-800 shadow-2xl">
      <div className="px-4 py-3">
        <div className="flex items-center gap-4">
          {/* Left Section: Album Art + Track Info */}
          <div className="flex items-center gap-3 min-w-[240px] w-[30%]">
            <div className="relative">
              <img
                src={track.images?.[0]?.url || '/placeholder-album.png'}
                alt={`${track.album} cover`}
                className="w-14 h-14 rounded shadow-lg"
              />
              {track.pending && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/50 rounded">
                  <Loader2 className="w-5 h-5 animate-spin" />
                </div>
              )}
            </div>
            <div className="flex flex-col min-w-0">
              <a
                href={`https://open.spotify.com/track/${track.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-sm hover:underline truncate"
              >
                {track.name}
              </a>
              <a
                href={`https://open.spotify.com/artist/${track.artists[0]}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-gray-400 hover:underline truncate"
              >
                {track.artists.join(", ")}
              </a>
            </div>
          </div>

          {/* Center Section: Playback Controls + Progress */}
          <div className="flex-1 flex flex-col items-center gap-2 max-w-[40%]">
            {/* Control Buttons */}
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="icon"
                className={`h-8 w-8 ${!isAdmin ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-800'}`}
                onClick={handlePrevious}
                disabled={!isAdmin}
              >
                <SkipBack className="h-4 w-4" />
              </Button>

              <Button
                variant="ghost"
                size="icon"
                className={`h-10 w-10 rounded-full ${!isAdmin
                  ? 'opacity-50 cursor-not-allowed'
                  : 'bg-white hover:bg-gray-200 hover:scale-105'
                  }`}
                onClick={handlePlayPause}
                disabled={!isAdmin}
              >
                {isPlaying ? (
                  <Pause className="h-5 w-5 text-black fill-black" />
                ) : (
                  <Play className="h-5 w-5 text-black fill-black ml-0.5" />
                )}
              </Button>

              <Button
                variant="ghost"
                size="icon"
                className={`h-8 w-8 ${!isAdmin ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-800'}`}
                onClick={handleNext}
                disabled={!isAdmin}
              >
                <SkipForward className="h-4 w-4" />
              </Button>
            </div>

            {/* Progress Bar */}
            <div className="flex items-center gap-2 w-full">
              <span className="text-xs text-gray-400 w-10 text-right">
                {formatTime(currentTime)}
              </span>
              <Slider
                value={[currentTime]}
                max={duration}
                step={1}
                className={`flex-1 ${!isAdmin ? 'cursor-not-allowed' : ''}`}
                onValueChange={handleSeek}
                disabled={!isAdmin}
              />
              <span className="text-xs text-gray-400 w-10">
                {formatTime(duration)}
              </span>
            </div>
          </div>

          {/* Right Section: Volume + Controls */}
          <div className="flex items-center gap-2 min-w-[240px] w-[30%] justify-end">
            {/* Guests Button */}
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 hover:bg-gray-800 relative"
              onClick={() => setShowGuests(!showGuests)}
            >
              <Users className="h-4 w-4" />
            </Button>

            {/* Volume Control */}
            <div className="flex items-center gap-2 w-32">
              <Button
                variant="ghost"
                size="icon"
                className={`h-8 w-8 ${!isAdmin ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-800'}`}
                disabled={!isAdmin}
              >
                <Volume2 className="h-4 w-4" />
              </Button>
              <Slider
                value={[volume]}
                max={100}
                step={1}
                className={`flex-1 ${!isAdmin ? 'cursor-not-allowed' : ''}`}
                onValueChange={handleVolumeChange}
                disabled={!isAdmin}
              />
            </div>

            {/* Fullscreen Button */}
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 hover:bg-gray-800"
              onClick={toggleFullscreen}
            >
              <Maximize2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Guests Popup (simple version) */}
      {showGuests && (
        <div className="absolute bottom-full right-4 mb-2 bg-gray-900 border border-gray-700 rounded-lg shadow-xl p-4 min-w-[200px]">
          <h3 className="font-semibold mb-2 text-sm">Current Guests</h3>
          <div className="space-y-2 text-sm text-gray-300">
            <div>👤 Guest 1</div>
            <div>👤 Guest 2</div>
            <div>👤 Guest 3</div>
          </div>
        </div>
      )}
    </Card>
  );
};

export default Player;
