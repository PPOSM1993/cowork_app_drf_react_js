/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}', // <-- esto es clave
  ],
  theme: {
    extend: {},
  },
  plugins: [
    ('tailwind-scrollbar-hide'),
  ]
}
