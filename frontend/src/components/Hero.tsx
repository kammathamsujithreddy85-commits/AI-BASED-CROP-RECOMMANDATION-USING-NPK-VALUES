export default function Hero() {
    return (
        <section
            className="relative z-10 flex flex-col items-center justify-center text-center px-6"
            style={{ paddingTop: 'calc(8rem - 75px)', paddingBottom: '10rem' }}
        >
            {/* Headline */}
            <h1
                className="text-5xl sm:text-7xl md:text-8xl font-serif font-normal max-w-7xl animate-fade-rise"
                style={{
                    lineHeight: 0.95,
                    letterSpacing: '-2.46px',
                }}
            >
                Empowering Farmers with{' '}
                <span className="italic text-gray-600">Intelligent</span> Crop{' '}
                <span className="italic text-gray-600">Predictions.</span>
            </h1>

            {/* Description */}
            <p
                className="text-base sm:text-lg max-w-2xl mt-8 leading-relaxed text-gray-600 animate-fade-rise-delay"
            >
                AI-powered crop recommendation system helping farmers make data-driven decisions.
                Analyze soil nutrients, climate conditions, and get precise crop predictions for maximum yield.
            </p>

            {/* CTA Button */}
            <button
                onClick={() => window.location.href = 'http://localhost:5000'}
                className="rounded-full px-14 py-5 text-base mt-12 bg-black text-white hover:scale-105 transition-transform animate-fade-rise-delay-2"
            >
                Get Crop Recommendation
            </button>
        </section>
    );
}