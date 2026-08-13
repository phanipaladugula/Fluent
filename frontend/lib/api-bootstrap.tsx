"use client";

import { setApiBase } from "@/lib/api";

type Props = {
  apiUrl: string;
  children: React.ReactNode;
};

export function ApiBootstrap({ apiUrl, children }: Props) {
  if (apiUrl !== "") {
    setApiBase(apiUrl);
  }
  return children;
}
