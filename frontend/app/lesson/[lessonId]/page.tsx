"use client";

import { useParams } from "next/navigation";
import { LessonPlayer } from "@/components/lesson/LessonPlayer";

export default function LessonPage() {
  const params = useParams();
  let raw = params.lessonId;
  if (Array.isArray(raw)) {
    raw = raw[0];
  }
  const lessonId = Number(raw);
  return <LessonPlayer lessonId={lessonId} mode="lesson" />;
}
