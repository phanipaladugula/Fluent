"use client";

import { useEffect, useState } from "react";
import { apiGet, getStreamUrl } from "@/lib/api";
import { LeaderboardEntry } from "@/lib/types";

export default function LeaderboardPage() {
  const [rows, setRows] = useState<LeaderboardEntry[]>([]);
  const [error, setError] = useState("");
  const [live, setLive] = useState(false);

  function applyRows(data: LeaderboardEntry[]) {
    setRows(data);
    setError("");
  }

  useEffect(function connectLive() {
    apiGet<LeaderboardEntry[]>("/leaderboard")
      .then(function onOk(data) {
        applyRows(data);
      })
      .catch(function onErr() {
        setError("Could not load the leaderboard.");
      });

    const source = new EventSource(getStreamUrl("/leaderboard/stream"));

    source.onopen = function onOpen() {
      setLive(true);
    };

    source.onmessage = function onMessage(event) {
      try {
        const payload = JSON.parse(event.data);
        if (payload.entries) {
          applyRows(payload.entries);
        }
      } catch (err) {
        setError("Could not read a live leaderboard update.");
      }
    };

    source.onerror = function onError() {
      setLive(false);
    };

    return function stop() {
      source.close();
    };
  }, []);

  return (
    <div>
      <h1 className="page-title">Leaderboard</h1>
      <p className="muted">
        <span className="live-dot" />
        {live ? "Live via server-sent events" : "Connecting to live league..."}
      </p>
      <div className="card" style={{ marginTop: 20 }}>
        {error !== "" ? <p className="muted">{error}</p> : null}
        {rows.map(function renderRow(row) {
          const className = row.is_current_user ? "list-row me" : "list-row";
          return (
            <div key={row.user_id} className={className}>
              <div className="rank">{row.rank}</div>
              <div className="avatar">{row.display_name.charAt(0)}</div>
              <div style={{ flex: 1 }}>
                <strong>{row.display_name}</strong>
                {row.is_current_user ? <span className="muted"> · you</span> : null}
                <div className="muted">{row.streak_count} day streak</div>
              </div>
              <strong>{row.total_xp} XP</strong>
            </div>
          );
        })}
      </div>
      <p className="muted" style={{ marginTop: 16 }}>
        Keep this page open. Finish a lesson in another tab. Alex&apos;s XP and rank update as soon
        as the lesson completes — no timer and no refresh.
      </p>
    </div>
  );
}
