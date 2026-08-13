"use client";

import { useEffect, useState, MouseEvent } from "react";
import Link from "next/link";
import { apiGet } from "@/lib/api";
import { CoursePath, SkillPathItem, UnitPathItem } from "@/lib/types";
import { SkillNode } from "@/components/path/SkillNode";
import { useUser } from "@/lib/user-context";

function getOffset(index: number) {
  const pattern = [0, 48, 80, 48];
  return pattern[index % 4];
}

function findCurrentSkill(units: UnitPathItem[]) {
  for (const unit of units) {
    for (const skill of unit.skills) {
      if (skill.is_unlocked && !skill.is_completed) {
        return skill;
      }
    }
  }
  if (units.length > 0 && units[0].skills.length > 0) {
    return units[0].skills[0];
  }
  return null;
}

export function LearningPath() {
  const userContext = useUser();
  const [course, setCourse] = useState<CoursePath | null>(null);
  const [error, setError] = useState("");
  const [openSkillId, setOpenSkillId] = useState<number | null>(null);
  const [guideUnitId, setGuideUnitId] = useState<number | null>(null);

  let xpStamp = 0;
  if (userContext.user !== null) {
    xpStamp = userContext.user.total_xp;
  }

  function loadPath() {
    apiGet<CoursePath>("/course/path")
      .then(function onOk(data) {
        setCourse(data);
        setError("");
      })
      .catch(function onErr() {
        setError("Could not load the learning path. Is the Fluent backend running?");
      });
  }

  useEffect(
    function loadWhenProgressChanges() {
      loadPath();
    },
    [xpStamp]
  );

  useEffect(function reloadWhenVisible() {
    function onVisible() {
      if (document.visibilityState === "visible") {
        loadPath();
      }
    }
    document.addEventListener("visibilitychange", onVisible);
    return function cleanup() {
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, []);

  useEffect(function closeOnOutsideClick() {
    function onDocClick(event: Event) {
      const target = event.target;
      if (!(target instanceof Element)) {
        setOpenSkillId(null);
        return;
      }
      const insideNode = target.closest(".skill-node-wrap");
      if (insideNode === null) {
        setOpenSkillId(null);
      }
    }
    document.addEventListener("click", onDocClick);
    return function cleanup() {
      document.removeEventListener("click", onDocClick);
    };
  }, []);

  function onToggle(skillId: number) {
    if (openSkillId === skillId) {
      setOpenSkillId(null);
      return;
    }
    setOpenSkillId(skillId);
  }

  function openGuide(event: MouseEvent<HTMLButtonElement>, unitId: number) {
    event.stopPropagation();
    setGuideUnitId(unitId);
    setOpenSkillId(null);
  }

  if (error !== "") {
    return <p className="muted">{error}</p>;
  }
  if (course === null) {
    return <p className="muted">Loading your path...</p>;
  }

  const currentSkill = findCurrentSkill(course.units);
  let currentId: number | null = null;
  if (currentSkill !== null) {
    currentId = currentSkill.id;
  }

  let globalIndex = 0;
  let guideUnit: UnitPathItem | null = null;
  for (const unit of course.units) {
    if (unit.id === guideUnitId) {
      guideUnit = unit;
    }
  }

  let continueHref = "";
  if (currentSkill !== null && currentSkill.lesson_id !== null) {
    continueHref = "/lesson/" + currentSkill.lesson_id;
  }

  return (
    <div>
      {currentSkill !== null && continueHref !== "" ? (
        <div className="continue-card">
          <div>
            <div className="unit-kicker" style={{ color: "var(--text-secondary)" }}>
              Jump back in
            </div>
            <strong>{currentSkill.title}</strong>
            <div className="muted">{currentSkill.description}</div>
          </div>
          <Link className="btn btn-green" href={continueHref}>
            Start
          </Link>
        </div>
      ) : null}

      {course.units.map(function renderUnit(unit) {
        return (
          <section key={unit.id}>
            <div className="unit-banner" style={{ background: unit.color }}>
              <div>
                <div className="unit-kicker">Section 1, {unit.title}</div>
                <h2>{unit.description}</h2>
              </div>
              <button
                className="guidebook"
                type="button"
                onClick={function handleGuide(event: MouseEvent<HTMLButtonElement>) {
                  openGuide(event, unit.id);
                }}
              >
                Guidebook
              </button>
            </div>
            <div className="path-list">
              {unit.skills.map(function renderSkill(skill: SkillPathItem) {
                const offset = getOffset(globalIndex);
                const showMascot = skill.id === currentId;
                globalIndex = globalIndex + 1;
                return (
                  <SkillNode
                    key={skill.id}
                    skill={skill}
                    offset={offset}
                    showMascot={showMascot}
                    isOpen={openSkillId === skill.id}
                    onToggle={onToggle}
                  />
                );
              })}
            </div>
          </section>
        );
      })}

      {guideUnit !== null ? (
        <div
          className="modal-backdrop"
          onClick={function closeGuide() {
            setGuideUnitId(null);
          }}
        >
          <div
            className="modal"
            onClick={function stop(event: MouseEvent<HTMLDivElement>) {
              event.stopPropagation();
            }}
          >
            <h2>{guideUnit.title} guidebook</h2>
            <p className="muted">{guideUnit.description}</p>
            {guideUnit.skills.map(function renderGuideSkill(skill) {
              let state = "Locked";
              let lessonHref = "";
              if (skill.is_completed) {
                state = "Crowned";
              } else if (skill.is_unlocked) {
                state = "Ready";
              }
              if (skill.is_unlocked && skill.lesson_id !== null) {
                lessonHref = "/lesson/" + skill.lesson_id;
              }
              return (
                <div key={skill.id} className="list-row">
                  <div style={{ flex: 1, textAlign: "left" }}>
                    <strong>{skill.title}</strong>
                    <div className="muted">{skill.description}</div>
                  </div>
                  {lessonHref !== "" ? (
                    <Link className="btn btn-green" href={lessonHref} style={{ minWidth: 110 }}>
                      {state === "Crowned" ? "Review" : "Start"}
                    </Link>
                  ) : (
                    <span className="muted">{state}</span>
                  )}
                </div>
              );
            })}
            <button
              className="btn btn-green btn-block"
              type="button"
              style={{ marginTop: 16 }}
              onClick={function closeGuide() {
                setGuideUnitId(null);
              }}
            >
              Close
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
