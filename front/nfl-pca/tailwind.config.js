/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        nfl: {
          blue: "#013369",
          red: "#D50A0A",
          gold: "#FFB612",
          dark: "#0a0a0f",
          gray: "#1a1a2e",
        },
      },
      fontFamily: {
        display: ["'Anton'", "sans-serif"],
        body: ["'Barlow Condensed'", "sans-serif"],
      },
    },
  },
  plugins: [],
};