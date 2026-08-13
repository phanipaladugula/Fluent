"use client";

import Link from "next/link";
import { MouseEvent } from "react";
import { SkillPathItem } from "@/lib/types";
import { LockIcon, OwlMascot, SkillGlyph, StarIcon } from "@/components/icons";

type SkillNodeProps = {
  skill: SkillPathItem;
  offset: number;
  showMascot: boolean;
  isOpen: boolean;
  onToggle: (skillId: number) => void;
};

function getButtonClass(skill: SkillPathItem) {
  if (!skill.is_unlocked) {
    return "skill-button locked";
  }
  if (skill.crowns >= 5) {
    return "skill-button legendary";
  }
  if (skill.is_completed) {
    return "skill-button completed";
  }
  return "skill-button available";
}

export function SkillNode({ skill, offset, showMascot, isOpen, onToggle }: SkillNodeProps) {
  function handleToggle(event: MouseEvent<HTMLButtonElement>) {
    event.stopPropagation();
    onToggle(skill.id);
  }

  const ringPercent = (skill.crowns / skill.max_crowns) * 100;
  let rowClass = "skill-row";
  if (isOpen) {
    rowClass = "skill-row open";
  }

  let startHref = "";
  if (skill.lesson_id !== null) {
    startHref = "/lesson/" + skill.lesson_id;
  }

  let wrapClass = "skill-node-wrap";
  if (isOpen) {
    wrapClass = wrapClass + " open";
  }
  if (showMascot) {
    wrapClass = wrapClass + " current";
  }

  return (
    <div className={rowClass} style={{ marginLeft: offset + "px" }}>
      <div className={wrapClass}>
        {showMascot ? (
          <div className="mascot">
            <OwlMascot mood="idle" />
          </div>
        ) : null}

        <div className="skill-hit">
          <svg className="crown-ring" viewBox="0 0 90 90" aria-hidden="true">
            <circle cx="45" cy="45" r="40" stroke="#e5e5e5" strokeWidth="6" fill="none" />
            <circle
              cx="45"
              cy="45"
              r="40"
              stroke="#ffc800"
              strokeWidth="6"
              fill="none"
              strokeDasharray="251"
              strokeDashoffset={251 - (251 * ringPercent) / 100}
              strokeLinecap="round"
              transform="rotate(-90 45 45)"
            />
          </svg>
          <button
            className={getButtonClass(skill)}
            onClick={handleToggle}
            type="button"
            aria-label={skill.title}
          >
            {skill.is_unlocked ? <SkillGlyph name={skill.icon} /> : <LockIcon />}
          </button>
        </div>

        <p className="skill-title">{skill.title}</p>
        {skill.crowns > 0 ? (
          <p className="skill-crowns">
            <StarIcon size={14} /> {skill.crowns}/{skill.max_crowns}
          </p>
        ) : null}

        {isOpen ? (
          <div
            className="skill-pop"
            onClick={function stopBubble(event: MouseEvent<HTMLDivElement>) {
              event.stopPropagation();
            }}
          >
            <h4>{skill.title}</h4>
            <p className="muted">{skill.description}</p>
            {!skill.is_unlocked ? (
              <p className="muted">Complete the previous skill to unlock this one.</p>
            ) : (
              <div>
                {startHref !== "" ? (
                  <Link className="btn btn-green btn-block" href={startHref}>
                    Start +10 XP
                  </Link>
                ) : null}
                {skill.is_completed ? (
                  <Link
                    className="btn btn-gold btn-block"
                    href={"/legendary/" + skill.id}
                    style={{ marginTop: 8 }}
                  >
                    Legendary
                  </Link>
                ) : null}
              </div>
            )}
          </div>
        ) : null}
      </div>
    </div>
  );
}
