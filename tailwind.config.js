/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F172A', // Navy Gelap
        primary: '#EAB308',    // Kuning Gold (Yellow-500)
        accent: '#FACC15',     // Kuning Terang (Yellow-400)
        secondary: '#1E293B',  // Slate-800
      },
      boxShadow: {
        'neo-yellow': '0 0 0 2px #0F172A, 4px 4px 0 0 #EAB308',
        'neo-yellow-hover': '0 0 0 2px #0F172A, 2px 2px 0 0 #EAB308',
      }
    },
  },
  plugins: [],
}