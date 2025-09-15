import { useState, useEffect } from "react";

export default function Player() {
  const [status, setStatus] = useState("");
  const [player, setPlayer] = useState(null);

  const sendAction = async (action) => {
    try {
      const res = await fetch(`/api/player/${action}`, { method: "POST" });
      const data = await res.json();

      // Update status
      if (data.error) {
        setStatus(data.error.message || "Error");
      } else {
        setStatus(data.status || "");
      }

      // Update player only if returned
      if (data.player) {
        setPlayer(data.player);
      }
      // if no player returned, keep existing player to avoid UI disappearing
    } catch (err) {
      setStatus("Network or server error");
    }
  };

  const fetchPlayer = async () => {
    try {
      const res = await fetch("/api/player");
      const data = await res.json();
      if (data) setPlayer(data);
    } catch (err) {
      setStatus("Failed to fetch player");
    }
  };

  useEffect(() => {
    fetchPlayer();
    const interval = setInterval(fetchPlayer, 5000); // update every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
      fontFamily: "sans-serif",
      gap: "15px"
    }}>
      {player && player.item && (
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "15px",
          width: "400px",
          padding: "10px",
          backgroundColor: "#181818",
          borderRadius: "8px",
          color: "white"
        }}>
          <img
            src={player.item.album.images[0].url}
            alt="cover"
            style={{ width: "50px", height: "50px", borderRadius: "4px" }}
          />
          <div style={{ flexGrow: 1 }}>
            <div style={{ fontWeight: "bold" }}>{player.item.name}</div>
            <div style={{ fontSize: "0.8em", color: "#b3b3b3" }}>
              {player.item.artists.map(a => a.name).join(", ")}
            </div>
            <div style={{ height: "4px", background: "#535353", borderRadius: "2px", marginTop: "5px" }}>
              <div style={{
                width: `${(player.progress_ms / player.item.duration_ms) * 100}%`,
                height: "100%",
                background: "#1db954",
                borderRadius: "2px"
              }}></div>
            </div>
          </div>

          <button onClick={() => sendAction(player.is_playing ? "pause" : "play")} style={{
            marginLeft: "10px",
            background: "none",
            border: "none",
            color: "white",
            fontSize: "1.2em",
            cursor: "pointer"
          }}>
            {player.is_playing ? "⏸" : "▶"}
          </button>

          <button onClick={() => sendAction("next")} style={{
            marginLeft: "5px",
            background: "none",
            border: "none",
            color: "white",
            fontSize: "1.2em",
            cursor: "pointer"
          }}>
            ⏭
          </button>
        </div>
      )}

      <div style={{ color: "#b3b3b3", fontSize: "0.9em" }}>Status: {status}</div>
    </div>
  );
}
