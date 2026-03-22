export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#020617',
        panel: '#0f172a',
        muted: '#94a3b8',
        accent: '#22c55e',
      },
      boxShadow: {
        glow: '0 20px 45px rgba(34, 197, 94, 0.15)',
      },
    },
  },
  plugins: [],
}
