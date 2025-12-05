/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './vgm_source_database/templates/**/*.html',
    './vgm_source_database/**/*.py',
    './config/**/*.py',
    './templates/**/*.html',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Modern dark theme color palette
        dark: {
          bg: '#111827',      // gray-900
          surface: '#1f2937',  // gray-800
          card: '#374151',     // gray-700
          border: '#4b5563',   // gray-600
        },
        accent: {
          primary: '#3b82f6',   // blue-500
          success: '#10b981',    // emerald-500
          info: '#06b6d4',       // cyan-500
          danger: '#ef4444',     // red-500
          warning: '#f59e0b',   // amber-500
        },
      },
      boxShadow: {
        'soft': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'medium': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'large': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  plugins: [],
}
