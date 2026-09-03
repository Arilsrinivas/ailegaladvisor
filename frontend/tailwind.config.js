/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nyaya: {
          navy: '#0b1329',
          dark: '#111827',
          surface: '#1e293b',
          border: '#334155',
          gold: '#eab308',
          goldhover: '#ca8a04',
          accent: '#3b82f6',
          crimson: '#ef4444',
          emerald: '#10b981'
        }
      }
    },
  },
  plugins: [],
}
