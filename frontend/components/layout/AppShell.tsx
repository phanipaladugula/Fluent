"use client";

import { Sidebar, MobileNav } from "@/components/layout/Sidebar";
import { RightRail } from "@/components/layout/RightRail";
import { useUser } from "@/lib/user-context";

export function AppShell({ children }: { children: React.ReactNode }) {
  const userContext = useUser();

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-wrap">
        {userContext.apiError !== "" ? (
          <div className="offline-banner">
            <span>{userContext.apiError}</span>
            <button className="btn btn-green" type="button" onClick={userContext.refresh}>
              Retry
            </button>
          </div>
        ) : null}
        <div className="main-col">{children}</div>
        <RightRail />
      </div>
      <MobileNav />
    </div>
  );
}
