"use client";

import { OptionPublic } from "@/lib/types";

type Props = {
  options: OptionPublic[];
  selected: string;
  locked: boolean;
  status: "idle" | "correct" | "incorrect";
  correctAnswer: string;
  onSelect: (value: string) => void;
};

const LETTERS = ["A", "B", "C", "D", "E", "F"];

export function MultipleChoice({
  options,
  selected,
  locked,
  status,
  correctAnswer,
  onSelect,
}: Props) {
  return (
    <div className="choice-list">
      {options.map(function renderChoice(option, index) {
        let className = "choice";
        const isSelected = option.text === selected;
        if (isSelected) {
          className = className + " selected";
        }
        if (status === "incorrect" && isSelected) {
          className = className + " wrong";
        }
        if (status === "incorrect" && option.text === correctAnswer) {
          className = className + " right-hint";
        }
        if (status === "correct" && isSelected) {
          className = className + " right-hint";
        }
        if (locked) {
          className = className + " locked";
        }
        const letter = LETTERS[index] || String(index + 1);
        return (
          <button
            key={option.id}
            type="button"
            className={className}
            disabled={locked}
            onClick={function choose() {
              if (locked) {
                return;
              }
              onSelect(option.text);
            }}
          >
            <span className="choice-letter">{letter}</span>
            <span>{option.text}</span>
          </button>
        );
      })}
    </div>
  );
}
