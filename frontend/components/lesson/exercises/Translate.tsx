"use client";

import { OptionPublic } from "@/lib/types";

type Props = {
  options: OptionPublic[];
  selectedWords: string[];
  locked: boolean;
  onChange: (words: string[]) => void;
};

export function Translate({ options, selectedWords, locked, onChange }: Props) {
  function addWord(word: string) {
    if (locked) {
      return;
    }
    const next = selectedWords.slice();
    next.push(word);
    onChange(next);
  }

  function removeAt(index: number) {
    if (locked) {
      return;
    }
    const next = [];
    let i = 0;
    while (i < selectedWords.length) {
      if (i !== index) {
        next.push(selectedWords[i]);
      }
      i = i + 1;
    }
    onChange(next);
  }

  function countUsed(word: string) {
    let count = 0;
    let i = 0;
    while (i < selectedWords.length) {
      if (selectedWords[i] === word) {
        count = count + 1;
      }
      i = i + 1;
    }
    return count;
  }

  function countAvailable(word: string) {
    let count = 0;
    let i = 0;
    while (i < options.length) {
      if (options[i].text === word) {
        count = count + 1;
      }
      i = i + 1;
    }
    return count;
  }

  return (
    <div>
      <div className="answer-line">
        {selectedWords.map(function renderSelected(word, index) {
          return (
            <button
              key={word + "-" + index}
              type="button"
              className="word-chip selected"
              onClick={function remove() {
                removeAt(index);
              }}
            >
              {word}
            </button>
          );
        })}
      </div>
      <div className="bank">
        {options.map(function renderBank(option, index) {
          const used = countUsed(option.text) >= countAvailable(option.text);
          return (
            <button
              key={option.id + "-" + index}
              type="button"
              className={used ? "word-chip used" : "word-chip"}
              disabled={used}
              onClick={function add() {
                addWord(option.text);
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
