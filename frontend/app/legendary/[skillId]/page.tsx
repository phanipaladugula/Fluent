"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { apiGet } from "@/lib/api";
import { CoursePath } from "@/lib/types";
import { LessonPlayer } from "@/components/lesson/LessonPlayer";

export default function LegendaryPage() {
  const params = useParams();
  let raw = params.skillId;
  if (Array.isArray(raw)) {
    raw = raw[0];
  }
  const skillId = Number(raw);
  const [lessonId, setLessonId] = useState<number | null>(null);
  const [error, setError] = useState("");

  useEffect(
    function loadSkill() {
      apiGet<CoursePath>("/course/path")
        .then(function onOk(path) {
          let found: number | null = null;
          let u = 0;
          while (u < path.units.length) {
            let s = 0;
            while (s < path.units[u].skills.length) {
              if (path.units[u].skills[s].id === skillId) {
                found = path.units[u].skills[s].lesson_id;
              }
              s = s + 1;
            }
            u = u + 1;
          }
          if (found === null) {
            setError("That skill was not found.");
            return;
          }
          setLessonId(found);
        })
        .catch(function onErr() {
          setError("Could not start legendary.");
        });
    },
    [skillId]
  );

  if (error !== "") {
    return <p className="muted" style={{ padding: 40 }}>{error}</p>;
  }
  if (lessonId === null) {
    return <p className="muted" style={{ padding: 40 }}>Loading legendary...</p>;
  }
  return <LessonPlayer lessonId={lessonId} mode="legendary" skillId={skillId} />;
}
