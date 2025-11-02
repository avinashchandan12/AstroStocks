import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    optimizePackageImports: ['@prisma/client'],
  },
  // Turbopack handles path aliases automatically from tsconfig.json
  // No additional configuration needed
};

export default nextConfig;
