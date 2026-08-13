function trimSlash(value: string) {
  if (value.endsWith("/")) {
    return value.slice(0, value.length - 1);
  }
  return value;
}

let apiBase = trimSlash(process.env.NEXT_PUBLIC_API_URL || "");

export function setApiBase(url: string) {
  apiBase = trimSlash(url);
}

export function getApiBase() {
  return apiBase;
}

async function request<T>(path: string, method: string, body?: unknown): Promise<T> {
  const options: RequestInit = {
    method: method,
    cache: "no-store",
    headers: {},
    credentials: "omit",
  };

  if (body !== undefined) {
    options.headers = {
      "Content-Type": "application/json",
    };
    options.body = JSON.stringify(body);
  }

  const response = await fetch(getApiBase() + "/api" + path, options);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Request failed");
  }
  return response.json();
}

export function apiGet<T>(path: string): Promise<T> {
  return request<T>(path, "GET");
}

export function apiPost<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, "POST", body || {});
}

function getBrowserOrigin() {
  if (typeof window === "undefined") {
    return "";
  }
  return window.location.origin;
}

export function getStreamUrl(path: string) {
  const base = getApiBase();
  if (base !== "") {
    return base + "/api" + path;
  }
  const origin = getBrowserOrigin();
  if (origin !== "") {
    return origin + "/api" + path;
  }
  return "/api" + path;
}
