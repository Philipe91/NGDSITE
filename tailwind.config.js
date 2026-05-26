/** @type {import('tailwindcss').Config}
 *  Config replica EXATAMENTE o que estava inline no base.html (CDN).
 *  Não muda nenhuma cor / typography pra preservar o visual atual.
 */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        background: "#ffffff",
        surface:    "#f7f8fc",
        border:     "#e8eaed",
        primary:    "#003366",
        secondary:  "#00509e",
        textMain:   "#0f172a",
        textMuted:  "#64748b",
        success:    "#10b981",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      letterSpacing: {
        tightest: '-0.04em',
        tighter:  '-0.02em',
        tight:    '-0.01em',
      },
    },
  },
  safelist: [
    // bgColor dos slides do hero (Alpine :class dinâmico)
    'bg-[#f0f4f8]', 'bg-[#fcf5ec]', 'bg-[#f7f2fb]', 'bg-[#f4f7fb]',
    'text-blue-600', 'text-orange-600', 'text-purple-600', 'text-[#0a2553]',
    'bg-blue-300', 'bg-orange-300', 'bg-purple-300', 'bg-blue-200',
    'bg-blue-600', 'hover:bg-blue-700', 'shadow-blue-600/30',
    'bg-orange-500', 'hover:bg-orange-600', 'shadow-orange-500/30',
    'bg-purple-600', 'hover:bg-purple-700', 'shadow-purple-600/30',
    'bg-[#0a2553]', 'hover:bg-[#153e8a]', 'shadow-[#0a2553]/30',
    'text-white',
    // Classes coladas em {% if/else/endif %} (Tailwind JIT às vezes não pega)
    'bg-[#153e8a]/85', 'bg-gray-700/70', 'bg-gray-200', 'bg-emerald-500',
    'bg-amber-500', 'bg-[#0070f3]',
    'opacity-60', 'group-hover/box:opacity-90', 'group-hover/box:scale-[1.03]',
    'filter', 'grayscale',
    // Badges do megamenu (admin pode trocar)
    { pattern: /^(bg|text|ring)-(emerald|amber|gray|blue|red|green)-(50|100|200|300|500|600|700)$/ },
    { pattern: /^(bg|text|ring)-(emerald|amber|gray|blue|red|green)-(50|100|200|300|500|600|700)\/\d+$/ },
  ],
  plugins: [],
}
