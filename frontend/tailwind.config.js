/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#831C1C',
        accent: '#B73E3E',
        accentSoft: '#F0EDE9',
        neutralbg: '#F9F6F4',
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'serif'],
      }
    },
  },
  plugins: [],
}