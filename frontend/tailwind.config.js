/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0d1117',
          cyan: '#00f2fe',
          blue: '#4facfe',
          panel: '#161b22',
        }
      }
    },
  },
  plugins: [],
}
