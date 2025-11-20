import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "neon-blue": "#00F0FF",
        "neon-pink": "#FF00F5",
        "neon-green": "#39FF14",
        "neon-purple": "#9D00FF",
        "neon-orange": "#FF6600",
        "dark-bg": "#0A0A0F",
        "dark-card": "#12121A",
        "dark-hover": "#1A1A25",
      },
    },
  },
};

export default config;