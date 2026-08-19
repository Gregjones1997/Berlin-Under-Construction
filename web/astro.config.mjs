import { defineConfig } from "astro/config";

export default defineConfig({
  output: "static",
  publicDir: "./site-public",
  build: {
    format: "directory",
  },
});
