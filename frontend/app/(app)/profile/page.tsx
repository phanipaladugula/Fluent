"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";
import { ProfileResponse } from "@/lib/types";
import { OwlMascot, FireIcon, StarIcon } from "@/components/icons";

export default function ProfilePage() {
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(function loadProfile() {
    apiGet<ProfileResponse>("/profile")
      .then(function onOk(data) {
        setProfile(data);
      })
      .catch(function onErr() {
        setError("Could not load your profile.");
      });
  }, []);

  if (error !== "") {
    return <p className="muted">{error}</p>;
  }
  if (profile === null) {
    return <p className="muted">Loading profile...</p>;
  }

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 24 }}>
        <OwlMascot size={88} mood="idle" />
        <div>
          <h1 className="page-title">{profile.user.display_name}</h1>
          <p className="muted">@{profile.user.username} · Spanish</p>
        </div>
      </div>

      <div className="choice-grid" style={{ marginBottom: 24 }}>
        <div className="card">
          <div className="muted">Total XP</div>
          <h2>{profile.user.total_xp}</h2>
        </div>
        <div className="card">
          <div className="muted">Streak</div>
          <h2 style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <FireIcon /> {profile.user.streak_count}
          </h2>
        </div>
        <div className="card">
          <div className="muted">Lessons</div>
          <h2>{profile.completed_lessons}</h2>
        </div>
        <div className="card">
          <div className="muted">Skills unlocked</div>
          <h2>{profile.unlocked_skills}</h2>
        </div>
      </div>

      <h3>Achievements</h3>
      <div className="badge-grid">
        {profile.achievements.map(function renderBadge(item) {
          return (
            <div key={item.id} className={item.earned ? "badge earned" : "badge"}>
              <StarIcon />
              <h4 style={{ margin: "8px 0 4px" }}>{item.title}</h4>
              <p className="muted">{item.description}</p>
              <p className="muted">{item.earned ? "Earned" : "Locked"}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
