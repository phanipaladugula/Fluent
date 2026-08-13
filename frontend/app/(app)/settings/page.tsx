"use client";

import { useEffect, useState } from "react";
import { useUser } from "@/lib/user-context";

export default function SettingsPage() {
  const userContext = useUser();
  const [dark, setDark] = useState(false);

  useEffect(function readTheme() {
    const theme = localStorage.getItem("fluent-theme") || localStorage.getItem("lingo-theme");
    setDark(theme === "dark");
  }, []);

  function toggleTheme() {
    const next = !dark;
    setDark(next);
    if (next) {
      document.documentElement.setAttribute("data-theme", "dark");
      localStorage.setItem("fluent-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
      localStorage.setItem("fluent-theme", "light");
    }
  }

  return (
    <div>
      <h1 className="page-title">Settings</h1>
      <p className="muted">Preferences for your Fluent account.</p>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="settings-row">
          <div>
            <div>Dark mode</div>
            <div className="muted">Night owl friendly</div>
          </div>
          <button
            className={dark ? "toggle on" : "toggle"}
            type="button"
            onClick={toggleTheme}
            aria-label="Toggle dark mode"
          >
            <span />
          </button>
        </div>

        <div className="settings-row">
          <div>
            <div>Simulate next day</div>
            <div className="muted">
              Moves your last activity back one day so you can test streaks.
            </div>
          </div>
          <button className="btn btn-blue" type="button" onClick={userContext.simulateDay}>
            Simulate
          </button>
        </div>

        <div className="settings-row">
          <div>
            <div>Refill hearts</div>
            <div className="muted">Mocked Super refill for demos.</div>
          </div>
          <button className="btn btn-red" type="button" onClick={userContext.refillHearts}>
            Refill
          </button>
        </div>

        <div className="settings-row">
          <div>
            <div>Speech recognition</div>
            <div className="muted">Pronunciation exercises.</div>
          </div>
          <span className="muted">Coming soon</span>
        </div>

        <div className="settings-row">
          <div>
            <div>Friends</div>
            <div className="muted">Follow learners and add friends.</div>
          </div>
          <span className="muted">Coming soon</span>
        </div>
      </div>
    </div>
  );
}
