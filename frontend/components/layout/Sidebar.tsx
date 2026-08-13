"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BrandMark,
  DumbbellIcon,
  GearIcon,
  HomeIcon,
  ShieldIcon,
  UserIcon,
} from "@/components/icons";

function isActive(pathname: string, href: string) {
  if (href === "/") {
    return pathname === "/";
  }
  return pathname.startsWith(href);
}

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <Link href="/" className="brand">
        <BrandMark />
        <span className="brand-name">fluent</span>
      </Link>

      <Link className={isActive(pathname, "/") ? "nav-item active" : "nav-item"} href="/">
        <HomeIcon />
        Learn
      </Link>
      <Link
        className={isActive(pathname, "/practice") ? "nav-item active" : "nav-item"}
        href="/practice"
      >
        <DumbbellIcon />
        Practice
      </Link>
      <Link
        className={isActive(pathname, "/leaderboard") ? "nav-item active" : "nav-item"}
        href="/leaderboard"
      >
        <ShieldIcon />
        Leaderboards
      </Link>
      <Link
        className={isActive(pathname, "/profile") ? "nav-item active" : "nav-item"}
        href="/profile"
      >
        <UserIcon />
        Profile
      </Link>

      <div className="sidebar-spacer" />

      <Link
        className={isActive(pathname, "/settings") ? "nav-item active" : "nav-item"}
        href="/settings"
      >
        <GearIcon />
        Settings
      </Link>
    </aside>
  );
}

export function MobileNav() {
  const pathname = usePathname();
  return (
    <nav className="mobile-nav">
      <Link className={pathname === "/" ? "active" : ""} href="/">
        <HomeIcon size={22} />
        Learn
      </Link>
      <Link className={pathname.startsWith("/practice") ? "active" : ""} href="/practice">
        <DumbbellIcon size={22} />
        Practice
      </Link>
      <Link className={pathname.startsWith("/leaderboard") ? "active" : ""} href="/leaderboard">
        <ShieldIcon size={22} />
        League
      </Link>
      <Link className={pathname.startsWith("/profile") ? "active" : ""} href="/profile">
        <UserIcon size={22} />
        Profile
      </Link>
    </nav>
  );
}
