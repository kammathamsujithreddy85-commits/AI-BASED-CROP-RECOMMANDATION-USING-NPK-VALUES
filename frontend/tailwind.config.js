/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                serif: ['Instrument Serif', 'serif'],
                sans: ['Inter', 'sans-serif'],
            },
            colors: {
                background: '#FFFFFF',
                primary: '#000000',
                secondary: '#6F6F6F',
            },
            keyframes: {
                'fade-rise': {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
            animation: {
                'fade-rise': 'fade-rise 0.8s ease-out forwards',
                'fade-rise-delay': 'fade-rise 0.8s ease-out 0.2s forwards',
                'fade-rise-delay-2': 'fade-rise 0.8s ease-out 0.4s forwards',
            },
        },
    },
    plugins: [],
}