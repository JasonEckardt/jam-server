import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { useEffect, useState } from "react";

interface Track {
  name: string;
  artists: string[];
  album: string;
  duration_ms: number;
  images: { url: string }[];
  id: string;
}

const Player = () => {
  const [track, setTrack] = useState<Track | null>(null);

  useEffect(() => {
    fetch("/api/queues/main")
      .then(res => res.json())
      .then(data => setTrack(data.tracks[0]))
      .catch(err => console.error(err));
  }, []);

  /*TODO
    Returns the track at the top of the queue,
    this should probably use the useQueue hook that we set up earlier
    also this probably does not update when the song ends.
  */
  return (
    <Card className="max-w-xl">
      <CardHeader>
        <CardTitle>Now playing...</CardTitle>
      </CardHeader>
      <CardContent>
        {track && (
          <div className="flex gap-4">
            <img
              src={track.images[0]?.url}
              alt={`${track.album} album cover`}
              className="w-32 h-32 rounded-md object-cover"
            />
            <div className="flex flex-col justify-center">
              <p className="font-semibold text-lg">{track.name}</p>
              <p className="text-gray-600">{track.artists.join(", ")}</p>
              <p className="text-sm text-gray-500 mt-1">{track.album}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
export default Player;
