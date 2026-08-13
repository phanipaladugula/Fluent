"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
import { UserPublic } from "@/lib/types";

type UserContextValue = {
  user: UserPublic | null;
  loading: boolean;
  apiError: string;
  refresh: () => Promise<void>;
  simulateDay: () => Promise<void>;
  refillHearts: () => Promise<void>;
};

const UserContext = createContext<UserContextValue>({
  user: null,
  loading: true,
  apiError: "",
  refresh: async function emptyRefresh() {},
  simulateDay: async function emptyDay() {},
  refillHearts: async function emptyRefill() {},
});

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserPublic | null>(null);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState("");

  async function refresh() {
    try {
      const data = await apiGet<UserPublic>("/users/me");
      setUser(data);
      setApiError("");
    } catch (err) {
      setApiError("Could not reach the Fluent API. Start the backend on port 8000.");
    }
    setLoading(false);
  }

  async function simulateDay() {
    const data = await apiPost<UserPublic>("/users/me/simulate-day");
    setUser(data);
  }

  async function refillHearts() {
    const data = await apiPost<UserPublic>("/users/me/refill-hearts");
    setUser(data);
  }

  useEffect(function loadUser() {
    refresh();
  }, []);

  useEffect(function pollUser() {
    const timer = window.setInterval(function tick() {
      refresh();
    }, 20000);
    return function stop() {
      window.clearInterval(timer);
    };
  }, []);

  useEffect(function reloadOnFocus() {
    function onVisible() {
      if (document.visibilityState === "visible") {
        refresh();
      }
    }
    document.addEventListener("visibilitychange", onVisible);
    window.addEventListener("focus", refresh);
    return function cleanup() {
      document.removeEventListener("visibilitychange", onVisible);
      window.removeEventListener("focus", refresh);
    };
  }, []);

  return (
    <UserContext.Provider
      value={{
        user: user,
        loading: loading,
        apiError: apiError,
        refresh: refresh,
        simulateDay: simulateDay,
        refillHearts: refillHearts,
      }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}
