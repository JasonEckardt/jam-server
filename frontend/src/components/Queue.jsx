import { useState, useEffect } from "react";

export default function Queue() {
  const [queue, setQueue] = useState([]);
  const [url, setUrl] = useState("");

  const fetchQueue = async () => {
    const res = await fetch("/api/queue"); // adjust prefix if backend is on another port
    const data = await res.json();
    setQueue(data.queue || []);
  };

  const addTrack = async () => {
    if (!url) return;
    await fetch("/api/queue", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    setUrl("");
    fetchQueue();
  };

  const removeTrack = async (id) => {
    await fetch(`/api/queue/${id}`, { method: "DELETE" });
    fetchQueue();
  };

  useEffect(() => {
    fetchQueue();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Queue</h2>
      <div className="flex mb-4">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Spotify track URL"
          className="border p-2 flex-1"
        />
        <button onClick={addTrack} className="ml-2 px-4 py-2 bg-blue-500 text-white">
          Add
        </button>
      </div>
      <ul>
        {queue.map((track) => (
          <li key={track.id} className="flex items-center mb-2">
            {track.images?.[0] && (
              <img src={track.images[0].url} alt="" className="w-12 h-12 mr-2" />
            )}
            <div className="flex-1">
              <div>{track.name}</div>
              <div className="text-sm text-gray-600">
                {track.artists?.join(", ")} — {track.album}
              </div>
            </div>
            <button
              onClick={() => removeTrack(track.id)}
              className="ml-2 px-2 py-1 bg-red-500 text-white"
            >
              Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

