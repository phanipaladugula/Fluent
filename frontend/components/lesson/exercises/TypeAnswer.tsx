"use client";

type Props = {
  value: string;
  locked: boolean;
  onChange: (value: string) => void;
};

export function TypeAnswer({ value, locked, onChange }: Props) {
  return (
    <input
      className="type-input"
      value={value}
      placeholder="Type your answer"
      disabled={locked}
      onChange={function handle(event) {
        onChange(event.target.value);
      }}
    />
  );
}
