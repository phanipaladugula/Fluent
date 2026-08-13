"use client";

import { LessonCompleteResponse } from "@/lib/types";
import { HeartIcon, OwlMascot } from "@/components/icons";

type Props = {
  result: LessonCompleteResponse;
  onExit: () => void;
};

export function LessonCompleteModal({ result, onExit }: Props) {
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <OwlMascot size={96} mood="celebrate" />
        <h2>Lesson complete!</h2>
        <p className="muted">You crushed that one. Keep the streak alive.</p>
        <div>
          <span className="xp-pill">+{result.xp_earned} XP</span>
          <span className="xp-pill">{result.streak_count} day streak</span>
          <span className="xp-pill">{result.crowns} crowns</span>
        </div>
        {result.new_achievements.length > 0 ? (
          <p className="muted">Badge unlocked: {result.new_achievements.join(", ")}</p>
        ) : null}
        <button className="btn btn-green btn-block" type="button" onClick={onExit} style={{ marginTop: 20 }}>
          Continue
        </button>
      </div>
    </div>
  );
}

type HeartsProps = {
  onPractice: () => void;
  onRefill: () => void;
  onExit: () => void;
};

export function OutOfHeartsModal({ onPractice, onRefill, onExit }: HeartsProps) {
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 8 }}>
          <HeartIcon size={48} />
        </div>
        <h2>You ran out of hearts!</h2>
        <p className="muted">Practice to earn a heart back, or refill to keep learning.</p>
        <button className="btn btn-green btn-block" type="button" onClick={onPractice}>
          Practice
        </button>
        <button
          className="btn btn-gold btn-block"
          type="button"
          onClick={onRefill}
          style={{ marginTop: 10 }}
        >
          Refill hearts
        </button>
        <button
          className="btn btn-ghost btn-block"
          type="button"
          onClick={onExit}
          style={{ marginTop: 10 }}
        >
          End lesson
        </button>
      </div>
    </div>
  );
}
