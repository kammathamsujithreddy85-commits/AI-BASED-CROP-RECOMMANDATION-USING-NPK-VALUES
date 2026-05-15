export default function Navigation() {
    return (
        <nav className="relative z-10 px-8 py-6">
            <div className="max-w-7xl mx-auto flex justify-between items-center">
                {/* Logo */}
                <div className="text-3xl tracking-tight font-serif text-black">
                    Aethera<sup className="text-sm">®</sup>
                </div>

                {/* Menu Items */}
                <div className="flex items-center gap-10">
                    <a href="#" className="text-sm text-black transition-colors hover:text-gray-600">
                        Home
                    </a>
                    <a href="#" className="text-sm text-gray-600 transition-colors hover:text-black">
                        Studio
                    </a>
                    <a href="#" className="text-sm text-gray-600 transition-colors hover:text-black">
                        About
                    </a>
                    <a href="#" className="text-sm text-gray-600 transition-colors hover:text-black">
                        Journal
                    </a>
                    <a href="#" className="text-sm text-gray-600 transition-colors hover:text-black">
                        Reach Us
                    </a>

                    {/* CTA Button - Links to your Flask app */}
                    <button
                        onClick={() => window.location.href = 'http://localhost:5000/chat'}
                        className="rounded-full px-6 py-2.5 text-sm bg-black text-white hover:scale-105 transition-transform"
                    >
                        Begin Journey
                    </button>
                </div>
            </div>
        </nav>
    );
}