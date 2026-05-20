import Navigation from './components/Navigation';
import Hero from './components/Hero';
import VideoBackground from './components/VideoBackground';

function App() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-white">
      <VideoBackground
        videoUrl="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_083109_283f3553-e28f-428b-a723-d639c617eb2b.mp4"
      />

      <Navigation />
      <Hero />
    </div>
  );
}

export default App;