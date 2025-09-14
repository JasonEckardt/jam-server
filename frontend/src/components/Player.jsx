import { useState } from "react";

export default function Player() {
  const [status, setStatus] = useState("");

  const play = async () => {
    const res = await fetch("/api/player/play", { method: "POST" });
    const data = await res.json();
    setStatus(data.status || data.error?.message);
  };

  const pause = async () => {
    const res = await fetch("/api/player/pause", { method: "POST" });
    const data = await res.json();
    setStatus(data.status || data.error?.message);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Player</h2>
      <div className="flex space-x-2">
        <button onClick={play} className="px-4 py-2 bg-green-500 text-white">
          Play
        </button>
        <button onClick={pause} className="px-4 py-2 bg-yellow-500 text-white">
          Pause
        </button>
      </div>
      <div className="mt-2 text-gray-700">Status: {status}</div>
    </div>
  );
}

