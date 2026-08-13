"use client";

import { useState } from "react";
import Link from "next/link";
import { FireIcon, GemIcon, HeartIcon, SpainFlag } from "@/components/icons";
import { useUser } from "@/lib/user-context";

function formatHeartWait(seconds: number) {
  const minutes = Math.ceil(seconds / 60);
  if (minutes <= 1) {
    return "+1 in 1m";
  }
  return "+1 in " + minutes + "m";
}

export function TopStats() {
  const context = useUser();
  const user = context.user;

  if (user === null) {
    return <div className="stats-row" />;
  }

  return (
    <div className="stats-row">
      <div className="stat-chip">
        <SpainFlag />
        <span>ES</span>
      </div>
      <div className="stat-chip gold">
        <FireIcon />
        {user.streak_count}
      </div>
      <div className="stat-chip blue">
        <GemIcon />
        {user.gems}
      </div>
      <Link href="/practice" className="stat-chip red" title="Practice to refill a heart">
        <HeartIcon />
        {user.hearts}
        {user.hearts < user.max_hearts && user.seconds_to_next_heart > 0 ? (
          <span className="muted" style={{ fontSize: 12, color: "inherit" }}>
            {formatHeartWait(user.seconds_to_next_heart)}
          </span>
        ) : null}
      </Link>
    </div>
  );
}

export function RightRail() {
  const context = useUser();
  const user = context.user;
  const [superNote, setSuperNote] = useState(false);

  let goalPercent = 0;
  if (user !== null && user.daily_goal_xp > 0) {
    goalPercent = Math.round((user.daily_xp / user.daily_goal_xp) * 100);
    if (goalPercent > 100) {
      goalPercent = 100;
    }
  }

  function showSuperNote() {
    setSuperNote(true);
  }

  return (
    <aside className="right-rail">
      <TopStats />

      <section className="card">
        <h3>Daily Quests</h3>
        <p className="muted">Earn {user ? user.daily_goal_xp : 20} XP</p>
        <div className="progress-track">
          <div className="progress-fill" style={{ width: goalPercent + "%" }} />
        </div>
        <p className="muted" style={{ marginTop: 10 }}>
          {user ? user.daily_xp : 0} / {user ? user.daily_goal_xp : 20} XP
        </p>
        {user && user.daily_xp >= user.daily_goal_xp ? (
          <p className="muted" style={{ marginTop: 8, color: "#58a700" }}>
            Daily goal complete!
          </p>
        ) : null}
      </section>

      <section className="card">
        <h3>Leaderboard</h3>
        <p className="muted">Climb the league by earning XP today.</p>
        <Link href="/leaderboard" className="btn btn-blue btn-block" style={{ marginTop: 12 }}>
          View league
        </Link>
      </section>

      <section className="card">
        <h3>Super Fluent</h3>
        <p className="muted">Unlimited hearts, legendary challenges, and no ads.</p>
        <button className="btn btn-gold btn-block" type="button" onClick={showSuperNote} style={{ marginTop: 12 }}>
          Try Super
        </button>
        {superNote ? (
          <p className="muted" style={{ marginTop: 10 }}>
            Super Fluent is coming soon. Shop is not part of this demo.
          </p>
        ) : null}
      </section>
    </aside>
  );
}
