"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiGet, apiPost } from "@/lib/api";
import { speakText } from "@/lib/speech";
import { playCorrectSound, playWrongSound } from "@/lib/sounds";
import { useUser } from "@/lib/user-context";
import {
  AnswerResponse,
  ExercisePublic,
  LessonCompleteResponse,
  LessonPublic,
  LessonStartResponse,
} from "@/lib/types";
import { HeartIcon, OwlMascot, VolumeIcon } from "@/components/icons";
import { FeedbackBar } from "@/components/lesson/FeedbackBar";
import { LessonCompleteModal, OutOfHeartsModal } from "@/components/lesson/Modals";
import { MultipleChoice } from "@/components/lesson/exercises/MultipleChoice";
import { FillBlank } from "@/components/lesson/exercises/FillBlank";
import { Translate } from "@/components/lesson/exercises/Translate";
import { MatchPairs } from "@/components/lesson/exercises/MatchPairs";
import { TypeAnswer } from "@/components/lesson/exercises/TypeAnswer";

type Props = {
  lessonId: number;
  mode: "lesson" | "practice" | "legendary";
  skillId?: number;
};

type AnswerStatus = "idle" | "correct" | "incorrect";

function countLeftOptions(exercise: ExercisePublic) {
  let count = 0;
  let i = 0;
  while (i < exercise.options.length) {
    if (exercise.options[i].side !== "right") {
      count = count + 1;
    }
    i = i + 1;
  }
  return count;
}

function canSubmit(exercise: ExercisePublic, answer: string) {
  if (answer.trim() === "") {
    return false;
  }
  if (exercise.type === "match_pairs") {
    const needed = countLeftOptions(exercise);
    const parts = answer.split(";");
    return parts.length === needed;
  }
  return true;
}

function owlMoodFor(status: AnswerStatus) {
  if (status === "correct") {
    return "happy";
  }
  if (status === "incorrect") {
    return "sad";
  }
  return "idle";
}

export function LessonPlayer({ lessonId, mode, skillId }: Props) {
  const router = useRouter();
  const userContext = useUser();
  const [lesson, setLesson] = useState<LessonPublic | null>(null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [words, setWords] = useState<string[]>([]);
  const [status, setStatus] = useState<AnswerStatus>("idle");
  const [correctAnswer, setCorrectAnswer] = useState("");
  const [checking, setChecking] = useState(false);
  const [hearts, setHearts] = useState(5);
  const [heartsLost, setHeartsLost] = useState(0);
  const [outOfHearts, setOutOfHearts] = useState(false);
  const [complete, setComplete] = useState<LessonCompleteResponse | null>(null);
  const [error, setError] = useState("");
  const [seconds, setSeconds] = useState(60);
  const [pairReset, setPairReset] = useState(0);

  useEffect(
    function loadLesson() {
      async function run() {
        try {
          let data: LessonPublic;
          if (mode === "practice") {
            data = await apiGet<LessonPublic>("/practice");
          } else {
            data = await apiGet<LessonPublic>("/lessons/" + lessonId);
            if (mode === "lesson") {
              const start = await apiPost<LessonStartResponse>("/lessons/" + lessonId + "/start");
              setHearts(start.hearts);
              if (!start.can_start) {
                if (start.message.indexOf("hearts") !== -1) {
                  setOutOfHearts(true);
                } else {
                  setError(start.message);
                }
              }
            }
          }
          setLesson(data);
        } catch (err) {
          setError("Could not load the lesson. Is the Fluent backend running?");
        }
      }
      run();
    },
    [lessonId, mode]
  );

  useEffect(
    function legendaryTimer() {
      if (mode !== "legendary") {
        return;
      }
      if (complete !== null || outOfHearts) {
        return;
      }
      const timer = window.setInterval(function tick() {
        setSeconds(function update(current) {
          if (current <= 1) {
            window.clearInterval(timer);
            setError("Time is up. Try legendary again!");
            return 0;
          }
          return current - 1;
        });
      }, 1000);
      return function stop() {
        window.clearInterval(timer);
      };
    },
    [mode, complete, outOfHearts]
  );

  useEffect(
    function keyboardShortcuts() {
      function onKey(event: KeyboardEvent) {
        if (event.key !== "Enter") {
          if (status !== "idle" || lesson === null) {
            return;
          }
          const exercise = lesson.exercises[index];
          const isChoice = exercise.type === "multiple_choice" || exercise.type === "fill_blank";
          if (!isChoice) {
            return;
          }
          const number = parseInt(event.key, 10);
          if (number >= 1 && number <= exercise.options.length) {
            onPickAnswer(exercise.options[number - 1].text);
          }
          return;
        }
        if (checking) {
          return;
        }
        if (status === "idle") {
          if (lesson === null) {
            return;
          }
          const exercise = lesson.exercises[index];
          if (!canSubmit(exercise, answer)) {
            return;
          }
          onCheck();
          return;
        }
        if (status === "correct") {
          onContinue();
          return;
        }
        onTryAgain();
      }
      window.addEventListener("keydown", onKey);
      return function cleanup() {
        window.removeEventListener("keydown", onKey);
      };
    },
    [status, lesson, index, answer, checking]
  );

  function resetLocalAnswer() {
    setAnswer("");
    setWords([]);
    setStatus("idle");
    setCorrectAnswer("");
    setPairReset(function bump(current) {
      return current + 1;
    });
  }

  function onPickAnswer(value: string) {
    if (status === "incorrect") {
      setStatus("idle");
      setCorrectAnswer("");
    }
    setAnswer(value);
  }

  function onWordsChange(next: string[]) {
    if (status === "incorrect") {
      setStatus("idle");
      setCorrectAnswer("");
    }
    setWords(next);
    setAnswer(next.join(" "));
  }

  function onMatchChange(value: string) {
    if (status === "incorrect") {
      setStatus("idle");
      setCorrectAnswer("");
    }
    setAnswer(value);
  }

  function onTryAgain() {
    resetLocalAnswer();
  }

  function isLocked(exerciseType: string) {
    if (checking) {
      return true;
    }
    if (status === "correct") {
      return true;
    }
    if (status === "incorrect") {
      if (exerciseType === "multiple_choice" || exerciseType === "fill_blank") {
        return false;
      }
      return true;
    }
    return false;
  }

  async function onCheck() {
    if (lesson === null) {
      return;
    }
    const exercise = lesson.exercises[index];
    setChecking(true);
    try {
      const response = await apiPost<AnswerResponse>(
        mode === "practice" ? "/practice/answer" : "/lessons/" + lessonId + "/answer",
        {
          exercise_id: exercise.id,
          answer: answer,
        }
      );
      applyAnswer(response);
    } catch (err) {
      setError("Could not check the answer.");
    }
    setChecking(false);
  }

  function applyAnswer(response: AnswerResponse) {
    setHearts(response.hearts);
    setCorrectAnswer(response.correct_answer);
    if (response.is_correct) {
      setStatus("correct");
      playCorrectSound();
    } else {
      setStatus("incorrect");
      setHeartsLost(function bump(current) {
        return current + 1;
      });
      playWrongSound();
    }
    if (response.out_of_hearts) {
      setOutOfHearts(true);
    }
  }

  async function finishLesson() {
    if (mode === "practice") {
      await apiPost("/practice/complete");
      await userContext.refresh();
      router.push("/");
      return;
    }
    if (mode === "legendary" && skillId !== undefined) {
      const result = await apiPost<LessonCompleteResponse>("/legendary/" + skillId + "/complete");
      setComplete(result);
      await userContext.refresh();
      return;
    }
    const result = await apiPost<LessonCompleteResponse>("/lessons/" + lessonId + "/complete", {
      hearts_lost: heartsLost,
    });
    setComplete(result);
    await userContext.refresh();
  }

  async function onContinue() {
    if (lesson === null) {
      return;
    }
    if (index + 1 >= lesson.exercises.length) {
      await finishLesson();
      return;
    }
    setIndex(index + 1);
    resetLocalAnswer();
  }

  if (error !== "") {
    return (
      <div className="lesson-shell">
        <div className="lesson-body">
          <p className="muted">{error}</p>
          <button className="btn btn-green" type="button" onClick={function go() { router.push("/"); }}>
            Back to path
          </button>
        </div>
      </div>
    );
  }

  if (lesson === null) {
    return (
      <div className="lesson-shell">
        <div className="lesson-body lesson-loading">
          <OwlMascot size={88} mood="idle" />
          <p className="muted">Loading lesson...</p>
        </div>
      </div>
    );
  }

  const exercise = lesson.exercises[index];
  const percent = Math.round(((index + (status === "correct" ? 1 : 0)) / lesson.exercises.length) * 100);
  const locked = isLocked(exercise.type);

  return (
    <div className="lesson-shell">
      <div className="lesson-top">
        <button className="lesson-close" type="button" onClick={function close() { router.push("/"); }}>
          ×
        </button>
        <div className="lesson-progress">
          <span style={{ width: percent + "%" }} />
        </div>
        {mode === "legendary" ? <div className="timer">{seconds}s</div> : null}
        <div className="lesson-hearts">
          <HeartIcon />
          {hearts}
        </div>
      </div>

      <div className="lesson-body">
        <div className="prompt-row">
          <div className="lesson-coach">
            <OwlMascot size={72} mood={owlMoodFor(status)} />
          </div>
          <button
            className="speak-btn"
            type="button"
            onClick={function speak() {
              speakText(exercise.prompt);
            }}
          >
            <VolumeIcon />
          </button>
          <h1 className="prompt-text">{exercise.prompt}</h1>
        </div>

        {exercise.type === "multiple_choice" ? (
          <MultipleChoice
            key={exercise.id}
            options={exercise.options}
            selected={answer}
            locked={locked}
            status={status}
            correctAnswer={correctAnswer}
            onSelect={onPickAnswer}
          />
        ) : null}
        {exercise.type === "fill_blank" ? (
          <FillBlank
            key={exercise.id}
            options={exercise.options}
            selected={answer}
            locked={locked}
            status={status}
            correctAnswer={correctAnswer}
            onSelect={onPickAnswer}
          />
        ) : null}
        {exercise.type === "translate" ? (
          <Translate
            key={exercise.id}
            options={exercise.options}
            selectedWords={words}
            locked={locked}
            onChange={onWordsChange}
          />
        ) : null}
        {exercise.type === "match_pairs" ? (
          <MatchPairs
            key={exercise.id}
            options={exercise.options}
            locked={locked}
            resetKey={pairReset}
            onChange={onMatchChange}
          />
        ) : null}
        {exercise.type === "type_answer" ? (
          <TypeAnswer
            key={exercise.id}
            value={answer}
            locked={locked}
            onChange={onPickAnswer}
          />
        ) : null}
      </div>

      <FeedbackBar
        status={status}
        correctAnswer={correctAnswer}
        canCheck={canSubmit(exercise, answer)}
        checking={checking}
        onCheck={onCheck}
        onContinue={onContinue}
        onTryAgain={onTryAgain}
      />

      {complete !== null ? (
        <LessonCompleteModal
          result={complete}
          onExit={function exit() {
            router.push("/");
          }}
        />
      ) : null}

      {outOfHearts ? (
        <OutOfHeartsModal
          onPractice={function goPractice() {
            router.push("/practice");
          }}
          onRefill={function refill() {
            userContext.refillHearts().then(function done() {
              setOutOfHearts(false);
              setHearts(5);
            });
          }}
          onExit={function exit() {
            router.push("/");
          }}
        />
      ) : null}
    </div>
  );
}
