type IconProps = {
  size?: number;
  color?: string;
};

export function HomeIcon({ size = 28, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path
        d="M4 10.5L12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1v-9.5z"
        stroke={color}
        strokeWidth="2.2"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function DumbbellIcon({ size = 28, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path
        d="M4 9v6M7 7v10M17 7v10M20 9v6M7 12h10"
        stroke={color}
        strokeWidth="2.4"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function ShieldIcon({ size = 28, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path
        d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"
        stroke={color}
        strokeWidth="2.2"
      />
    </svg>
  );
}

export function ShopIcon({ size = 28, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path
        d="M5 8h14l-1 12H6L5 8zM8 8V6a4 4 0 0 1 8 0v2"
        stroke={color}
        strokeWidth="2.2"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function UserIcon({ size = 28, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="8" r="3.2" stroke={color} strokeWidth="2.2" />
      <path
        d="M5 19c1.2-3.2 3.7-5 7-5s5.8 1.8 7 5"
        stroke={color}
        strokeWidth="2.2"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function GearIcon({ size = 28, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="3" stroke={color} strokeWidth="2.2" />
      <path
        d="M12 3.5v2.2M12 18.3V20.5M4.8 7.2l1.8 1.2M17.4 15.6l1.8 1.2M4.8 16.8l1.8-1.2M17.4 8.4l1.8-1.2"
        stroke={color}
        strokeWidth="2.2"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function FireIcon({ size = 22 }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="#ff9600">
      <path d="M12 2s3 4 3 7c0 1.4-.6 2.6-1.5 3.5 1.8-.2 4.5-2 4.5-6 3 3.2 4 6.4 4 9.2C22 19.4 17.5 22 12 22S2 19.4 2 15.7C2 10.4 7 6.2 12 2z" />
    </svg>
  );
}

export function GemIcon({ size = 22 }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="#1cb0f6">
      <path d="M7 3h10l5 7-10 11L2 10l5-7zm2.2 2L6.4 10h11.2L14.8 5H9.2z" />
    </svg>
  );
}

export function HeartIcon({ size = 22 }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="#ff4b4b">
      <path d="M12 21s-7.2-4.5-9.3-8.4C.8 9.4 2.4 6 5.7 6c1.9 0 3.2 1 4.3 2.4C11.1 7 12.4 6 14.3 6c3.3 0 4.9 3.4 3 6.6C19.2 16.5 12 21 12 21z" />
    </svg>
  );
}

export function LockIcon({ size = 26, color = "#afafaf" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <rect x="5" y="10" width="14" height="10" rx="2" fill={color} />
      <path d="M8 10V8a4 4 0 0 1 8 0v2" stroke={color} strokeWidth="2.2" />
    </svg>
  );
}

export function StarIcon({ size = 26 }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 3l2.4 6.5H21l-5.3 4 2 6.5L12 16.8 6.3 20l2-6.5L3 9.5h6.6L12 3z" />
    </svg>
  );
}

export function VolumeIcon({ size = 22, color = "currentColor" }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path d="M4 10v4h4l5 4V6L8 10H4z" fill={color} />
      <path d="M16 9.5a4 4 0 0 1 0 5" stroke={color} strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

type OwlMood = "idle" | "happy" | "sad" | "celebrate";

export function OwlMascot({ size = 78, mood = "idle" }: IconProps & { mood?: OwlMood }) {
  return (
    <div className={"owl-mascot owl-" + mood} style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox="0 0 78 78" fill="none" aria-hidden="true">
        <g className="owl-body">
          <ellipse cx="39" cy="44" rx="24" ry="26" fill="#58CC02" />
          <ellipse cx="39" cy="48" rx="16" ry="16" fill="#FFFFFF" />
          <g className="owl-pupils">
            <circle cx="31" cy="34" r="10" fill="#FFFFFF" />
            <circle cx="47" cy="34" r="10" fill="#FFFFFF" />
            <circle cx="31" cy="34" r="5" fill="#1B1B1B" />
            <circle cx="47" cy="34" r="5" fill="#1B1B1B" />
            <circle cx="33" cy="32" r="1.6" fill="#FFFFFF" />
            <circle cx="49" cy="32" r="1.6" fill="#FFFFFF" />
          </g>
          <path d="M35 42l4 5 4-5" fill="#FFC800" />
          <path d="M18 28c6-12 14-16 21-16" stroke="#46A302" strokeWidth="5" strokeLinecap="round" />
          <path d="M60 28c-6-12-14-16-21-16" stroke="#46A302" strokeWidth="5" strokeLinecap="round" />
          <ellipse cx="30" cy="66" rx="6" ry="3" fill="#FFC800" />
          <ellipse cx="48" cy="66" rx="6" ry="3" fill="#FFC800" />
        </g>
      </svg>
    </div>
  );
}

export function SpainFlag() {
  return (
    <svg width="24" height="18" viewBox="0 0 24 18">
      <rect width="24" height="18" rx="2" fill="#C60B1E" />
      <rect y="5" width="24" height="8" fill="#FFC400" />
    </svg>
  );
}

export function BrandMark() {
  return (
    <span className="owl-mascot owl-idle brand-owl">
      <svg className="brand-mark" viewBox="0 0 42 42" fill="none">
        <circle cx="21" cy="21" r="21" fill="#58CC02" />
        <g className="owl-pupils">
          <circle cx="15" cy="18" r="5" fill="#fff" />
          <circle cx="27" cy="18" r="5" fill="#fff" />
          <circle cx="15" cy="18" r="2.2" fill="#1b1b1b" />
          <circle cx="27" cy="18" r="2.2" fill="#1b1b1b" />
        </g>
        <path d="M18 26l3 3 3-3" fill="#FFC800" />
      </svg>
    </span>
  );
}

export function SkillGlyph({ name }: { name: string }) {
  if (name === "wave") {
    return (
      <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
        <path d="M4 14c2-6 4-8 6-8 1 4 2 8 2 8s1-6 3-8c3 1 5 5 5 9-2 4-8 6-12 4-2-1-3-3-4-5z" />
      </svg>
    );
  }
  if (name === "id") {
    return (
      <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
        <rect x="3" y="5" width="18" height="14" rx="2" />
        <circle cx="9" cy="12" r="2.2" fill="#fff" />
        <rect x="13" y="10" width="5" height="1.6" fill="#fff" />
        <rect x="13" y="13" width="4" height="1.6" fill="#fff" />
      </svg>
    );
  }
  if (name === "chat") {
    return (
      <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
        <path d="M4 5h16v11H8l-4 3V5z" />
      </svg>
    );
  }
  if (name === "apple") {
    return (
      <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 6c3 0 7 3 7 8s-3 7-7 7-7-2-7-7 4-8 7-8z" />
        <path d="M12 6c1-3 4-4 5-4" stroke="currentColor" strokeWidth="2" fill="none" />
      </svg>
    );
  }
  if (name === "paw") {
    return (
      <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
        <circle cx="7" cy="8" r="2.2" />
        <circle cx="17" cy="8" r="2.2" />
        <circle cx="9" cy="4.5" r="1.8" />
        <circle cx="15" cy="4.5" r="1.8" />
        <ellipse cx="12" cy="15" rx="5" ry="4" />
      </svg>
    );
  }
  return (
    <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 3l6 8H6l6-8z" />
      <circle cx="12" cy="17" r="4" />
    </svg>
  );
}
