/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
      },
      colors: {
        brand: {
          50: "#eef6ff",
          500: "#2563eb",
          600: "#1d4ed8",
          900: "#0f172a",
        },
      },
    },
  },
  plugins: [],
};
