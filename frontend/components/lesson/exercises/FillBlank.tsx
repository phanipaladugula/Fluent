"use client";

import { OptionPublic } from "@/lib/types";
import { MultipleChoice } from "@/components/lesson/exercises/MultipleChoice";

type Props = {
  options: OptionPublic[];
  selected: string;
  locked: boolean;
  status: "idle" | "correct" | "incorrect";
  correctAnswer: string;
  onSelect: (value: string) => void;
};

export function FillBlank({
  options,
  selected,
  locked,
  status,
  correctAnswer,
  onSelect,
}: Props) {
  return (
    <MultipleChoice
      options={options}
      selected={selected}
      locked={locked}
      status={status}
      correctAnswer={correctAnswer}
      onSelect={onSelect}
    />
  );
}
