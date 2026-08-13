export type UserPublic = {
  id: number;
  username: string;
  display_name: string;
  total_xp: number;
  gems: number;
  hearts: number;
  max_hearts: number;
  streak_count: number;
  last_activity_date: string | null;
  daily_xp: number;
  daily_goal_xp: number;
  seconds_to_next_heart: number;
};

export type SkillPathItem = {
  id: number;
  title: string;
  description: string;
  icon: string;
  order_index: number;
  max_crowns: number;
  crowns: number;
  is_unlocked: boolean;
  is_completed: boolean;
  lesson_id: number | null;
};

export type UnitPathItem = {
  id: number;
  title: string;
  description: string;
  color: string;
  order_index: number;
  skills: SkillPathItem[];
};

export type CoursePath = {
  id: number;
  language_code: string;
  title: string;
  from_language: string;
  units: UnitPathItem[];
};

export type OptionPublic = {
  id: number;
  text: string;
  side: string | null;
};

export type ExercisePublic = {
  id: number;
  type: string;
  prompt: string;
  order_index: number;
  options: OptionPublic[];
};

export type LessonPublic = {
  id: number;
  skill_id: number;
  title: string;
  xp_reward: number;
  exercises: ExercisePublic[];
};

export type AnswerResponse = {
  is_correct: boolean;
  correct_answer: string;
  hearts: number;
  out_of_hearts: boolean;
};

export type LessonStartResponse = {
  lesson_id: number;
  hearts: number;
  can_start: boolean;
  message: string;
};

export type LessonCompleteResponse = {
  xp_earned: number;
  total_xp: number;
  daily_xp: number;
  daily_goal_xp: number;
  streak_count: number;
  crowns: number;
  new_achievements: string[];
  hearts: number;
};

export type LeaderboardEntry = {
  rank: number;
  user_id: number;
  display_name: string;
  username: string;
  total_xp: number;
  streak_count: number;
  is_current_user: boolean;
};

export type AchievementPublic = {
  id: number;
  code: string;
  title: string;
  description: string;
  icon: string;
  earned: boolean;
  earned_at: string | null;
};

export type ProfileResponse = {
  user: UserPublic;
  completed_lessons: number;
  unlocked_skills: number;
  achievements: AchievementPublic[];
};
