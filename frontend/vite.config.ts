import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const pagesBase = process.env.GITHUB_PAGES === "true" ? "/PROSPECTiA/" : "/";

export default defineConfig({
  base: pagesBase,
  plugins: [react()],
  server: {
    port: 4173,
    host: true,
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
  preview: {
    port: 4173,
    host: true,
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
  },
});
