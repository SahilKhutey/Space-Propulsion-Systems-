/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Mission Control palette
        space: {
          50:  '#f0f4ff',
          100: '#dde6ff',
          200: '#b9c8ff',
          300: '#8ea3ff',
          400: '#6478ff',
          500: '#4451ec',
          600: '#2f3bbf',
          700: '#1f2a99',
          800: '#141c6e',
          900: '#0a1142',
          950: '#050828',
        },
        thrust: {
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
        },
        plasma: {
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
        },
        burn: {
          500: '#ef4444',
          600: '#dc2626',
        },
        ok: { 500: '#10b981' },
        warn: { 500: '#f59e0b' },
        crit: { 500: '#ef4444' },
        panel: {
          DEFAULT: 'rgba(15, 23, 42, 0.7)',
          border: 'rgba(148, 163, 184, 0.12)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
        display: ['Space Grotesk', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'flow': 'flow 2s linear infinite',
        'pulse-glow': 'glow 2s ease-in-out infinite',
        'spin-slow': 'spin 8s linear infinite',
      },
      keyframes: {
        flow: { '0%': { backgroundPosition: '0% 50%' }, '100%': { backgroundPosition: '100% 50%' } },
        glow: { '0%,100%': { boxShadow: '0 0 8px rgba(6,182,212,0.4)' }, '50%': { boxShadow: '0 0 24px rgba(6,182,212,0.8)' } },
      },
      backdropBlur: { xs: '2px' },
    },
  },
  plugins: [],
}
