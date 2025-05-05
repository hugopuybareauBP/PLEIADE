/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
        extend: {
            animation: {
                fadeIn: "fadeIn 1.2s ease-out forwards",
                pulseSlow: "pulseSlow 2s ease-in-out infinite",
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: 0, transform: 'scale(0.96)' },
                    '100%': { opacity: 1, transform: 'scale(1)' },
                },
                pulseSlow: {
                    '0%, 100%': { opacity: 1 },
                    '50%': { opacity: 0.6 },
                },
            },
        },
    },
    plugins: [],
};
