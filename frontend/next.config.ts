import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Docker needs a standalone server. Vercel sets VERCEL=1 and uses its own build.
  ...(process.env.VERCEL ? {} : { output: "standalone" as const }),
  poweredByHeader: false,
  async rewrites() {
    if (process.env.NEXT_PUBLIC_API_URL) {
      return [];
    }
    const backend = process.env.API_PROXY_TARGET || "http://127.0.0.1:8000";
    const isLoopback =
      backend.indexOf("127.0.0.1") !== -1 || backend.indexOf("localhost") !== -1;
    if (process.env.NODE_ENV === "production" && isLoopback) {
      return [];
    }
    return [
      {
        source: "/api/:path*",
        destination: backend + "/api/:path*",
      },
    ];
  },
};

export default nextConfig;
