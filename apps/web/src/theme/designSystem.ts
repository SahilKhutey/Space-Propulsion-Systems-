export const theme = {
  space: {
    50: '#f0f4ff', 100: '#dde6ff', 200: '#b9c8ff', 300: '#8ea3ff',
    400: '#6478ff', 500: '#4451ec', 600: '#2f3bbf', 700: '#1f2a99',
    800: '#141c6e', 900: '#0a1142', 950: '#050828',
  },
  thrust:  { 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706' },
  plasma:  { 400: '#22d3ee', 500: '#06b6d4', 600: '#0891b2' },
  burn:    { 500: '#ef4444', 600: '#dc2626' },
  ok:      { 500: '#10b981' },
  warn:    { 500: '#f59e0b' },
  crit:    { 500: '#ef4444' },
};

export const thrusterColors: Record<string, string> = {
  hall_thruster:    '#22d3ee',
  ion_thruster:     '#a78bfa',
  VASIMR:           '#f472b6',
  MPD:              '#fb923c',
  arcjet:           '#fbbf24',
  resistojet:       '#fde68a',
  PPT:              '#34d399',
  chemical:         '#94a3b8',
  NTR:              '#60a5fa',
  NEP:              '#c084fc',
};

export const chartPalette = [
  '#06b6d4', '#f59e0b', '#a78bfa', '#10b981', '#f472b6',
  '#fb923c', '#60a5fa', '#fbbf24', '#34d399', '#fb7185',
];
