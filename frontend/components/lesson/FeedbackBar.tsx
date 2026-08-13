"use client";

type Props = {
  status: "idle" | "correct" | "incorrect";
  correctAnswer: string;
  canCheck: boolean;
  checking: boolean;
  onCheck: () => void;
  onContinue: () => void;
  onTryAgain: () => void;
};

export function FeedbackBar({
  status,
  correctAnswer,
  canCheck,
  checking,
  onCheck,
  onContinue,
  onTryAgain,
}: Props) {
  if (status === "idle") {
    return (
      <div className="feedback-bar">
        <div className="feedback-inner">
          <div />
          <button
            className={canCheck ? "btn btn-green" : "btn btn-idle"}
            type="button"
            disabled={!canCheck || checking}
            onClick={onCheck}
            style={{ minWidth: 160 }}
          >
            {checking ? "Checking" : "Check"}
          </button>
        </div>
      </div>
    );
  }

  if (status === "correct") {
    return (
      <div className="feedback-bar correct">
        <div className="feedback-inner">
          <div className="feedback-copy">
            <h3>Nice!</h3>
            <p>Keep going.</p>
          </div>
          <button
            className="btn btn-green"
            type="button"
            onClick={onContinue}
            style={{ minWidth: 160 }}
          >
            Continue
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="feedback-bar incorrect">
      <div className="feedback-inner">
        <div className="feedback-copy">
          <h3>Not quite</h3>
          <p>
            The answer is <strong>{correctAnswer}</strong>
          </p>
          <p className="muted">Pick another choice and check again.</p>
        </div>
        <div className="feedback-actions">
          <button
            className="btn btn-red"
            type="button"
            onClick={onTryAgain}
            style={{ minWidth: 140 }}
          >
            Try again
          </button>
          <button
            className="btn btn-ghost"
            type="button"
            onClick={onContinue}
            style={{ minWidth: 120 }}
          >
            Skip
          </button>
        </div>
      </div>
    </div>
  );
}
