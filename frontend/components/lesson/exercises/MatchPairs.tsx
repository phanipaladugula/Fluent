"use client";

import { useEffect, useState } from "react";
import { OptionPublic } from "@/lib/types";

type Props = {
  options: OptionPublic[];
  locked: boolean;
  resetKey: number;
  onChange: (value: string) => void;
};

type Pair = {
  left: string;
  right: string;
};

function shuffle(list: OptionPublic[]) {
  const copy = list.slice();
  let i = copy.length - 1;
  while (i > 0) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = copy[i];
    copy[i] = copy[j];
    copy[j] = temp;
    i = i - 1;
  }
  return copy;
}

export function MatchPairs({ options, locked, resetKey, onChange }: Props) {
  const left: OptionPublic[] = [];
  const rightSource: OptionPublic[] = [];
  let i = 0;
  while (i < options.length) {
    if (options[i].side === "right") {
      rightSource.push(options[i]);
    } else {
      left.push(options[i]);
    }
    i = i + 1;
  }

  const [right, setRight] = useState<OptionPublic[]>([]);
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
  const [pairs, setPairs] = useState<Pair[]>([]);

  useEffect(
    function shuffleRight() {
      setRight(shuffle(rightSource));
      setPairs([]);
      setSelectedLeft(null);
      onChange("");
    },
    [resetKey]
  );

  function isMatched(text: string, side: string) {
    let p = 0;
    while (p < pairs.length) {
      if (side === "left" && pairs[p].left === text) {
        return true;
      }
      if (side === "right" && pairs[p].right === text) {
        return true;
      }
      p = p + 1;
    }
    return false;
  }

  function publish(nextPairs: Pair[]) {
    const parts = [];
    let p = 0;
    while (p < nextPairs.length) {
      parts.push(nextPairs[p].left + "=" + nextPairs[p].right);
      p = p + 1;
    }
    onChange(parts.join(";"));
  }

  function chooseLeft(text: string) {
    if (locked) {
      return;
    }
    if (isMatched(text, "left")) {
      return;
    }
    setSelectedLeft(text);
  }

  function chooseRight(text: string) {
    if (locked) {
      return;
    }
    if (isMatched(text, "right")) {
      return;
    }
    if (selectedLeft === null) {
      return;
    }
    const next = pairs.slice();
    next.push({ left: selectedLeft, right: text });
    setPairs(next);
    setSelectedLeft(null);
    publish(next);
  }

  return (
    <div className="match-board">
      <div className="match-col">
        {left.map(function renderLeft(option) {
          let className = "match-card";
          if (isMatched(option.text, "left")) {
            className = "match-card matched";
          } else if (selectedLeft === option.text) {
            className = "match-card selected";
          }
          return (
            <button
              key={option.id}
              type="button"
              className={className}
              onClick={function onLeft() {
                chooseLeft(option.text);
              }}
            >
              {option.text}
            </button>
          );
        })}
      </div>
      <div className="match-col">
        {right.map(function renderRight(option) {
          let className = "match-card";
          if (isMatched(option.text, "right")) {
            className = "match-card matched";
          }
          return (
            <button
              key={option.id}
              type="button"
              className={className}
              onClick={function onRight() {
                chooseRight(option.text);
              }}
            >
              {option.text}
            </button>
          );
        })}
      </div>
    </div>
  );
}
