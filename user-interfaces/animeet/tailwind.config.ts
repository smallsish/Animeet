import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        'appWhite': '#ffffff',
        'appBlack': '#000000',
        'appPurple': '#8d67ff',
        'appRed': '#ff6767'
      },
    },
  },
  plugins: [require('daisyui')],
};
export default config;
