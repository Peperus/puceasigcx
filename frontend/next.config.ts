import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  devIndicators: false,
  turbopack: {},
  webpack(config, { dev, isServer }) {
    if (dev && !isServer) {
      config.resolve.alias["next/dist/compiled/next-devtools"] = path.resolve(
        process.cwd(),
        "lib/next-devtools-shim.ts",
      );
    }

    return config;
  },
};

export default nextConfig;
