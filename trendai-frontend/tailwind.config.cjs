module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
    extend: {
      colors: {
        'bg-dark': '#0b0f17',
        'panel': '#0f1720',
        'muted': '#94a3b8'
      },
      fontFamily: {
        sans: ['Inter','ui-sans-serif','system-ui']
      },
      borderRadius: {
        xl2: '14px'
      }
    }
  },
  plugins: []
};
