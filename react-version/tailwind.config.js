module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#FFFFFF',
        'secondary': '#f7f7f8',
        'tertiary': '#ececec',
        'text-primary': '#202123',
        'text-secondary': '#64666B',
        'border': '#d9d9e0',
      },
      fontFamily: {
        sans: ['"PingFangSC-Thin"', '"PingFang SC"', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
} 