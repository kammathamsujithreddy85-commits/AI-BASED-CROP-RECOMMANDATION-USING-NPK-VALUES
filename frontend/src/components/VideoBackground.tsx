import { useRef, useEffect } from 'react';

interface VideoBackgroundProps {
    videoUrl: string;
    className?: string;
}

export default function VideoBackground({ videoUrl, className = '' }: VideoBackgroundProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const fadeRef = useRef<number>(0);
    const animationFrameRef = useRef<number>();
    const isFadingRef = useRef<boolean>(false);

    useEffect(() => {
        const video = videoRef.current;
        if (!video) return;

        video.muted = true;
        video.playsInline = true;
        video.preload = 'auto';

        const fadeIn = () => {
            if (isFadingRef.current) return;
            isFadingRef.current = true;
            const startTime = performance.now();
            const duration = 500;

            const animate = (currentTime: number) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                if (videoRef.current) {
                    videoRef.current.style.opacity = progress.toString();
                    fadeRef.current = progress;
                }

                if (progress < 1) {
                    animationFrameRef.current = requestAnimationFrame(animate);
                } else {
                    isFadingRef.current = false;
                }
            };

            animationFrameRef.current = requestAnimationFrame(animate);
        };

        const fadeOut = () => {
            if (isFadingRef.current) return;
            isFadingRef.current = true;
            const startTime = performance.now();
            const duration = 500;

            const animate = (currentTime: number) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                if (videoRef.current) {
                    videoRef.current.style.opacity = (1 - progress).toString();
                    fadeRef.current = 1 - progress;
                }

                if (progress < 1) {
                    animationFrameRef.current = requestAnimationFrame(animate);
                } else {
                    isFadingRef.current = false;
                }
            };

            animationFrameRef.current = requestAnimationFrame(animate);
        };

        const handleTimeUpdate = () => {
            if (!video) return;
            const { currentTime, duration } = video;

            if (duration - currentTime <= 0.5 && fadeRef.current > 0.5) {
                fadeOut();
            }
        };

        const handleEnded = () => {
            if (videoRef.current) {
                videoRef.current.style.opacity = '0';
                fadeRef.current = 0;
            }

            setTimeout(() => {
                if (videoRef.current) {
                    videoRef.current.currentTime = 0;
                    videoRef.current.play().catch(err => {
                        console.warn('Video replay failed:', err);
                    });
                    fadeIn();
                }
            }, 100);
        };

        video.addEventListener('timeupdate', handleTimeUpdate);
        video.addEventListener('ended', handleEnded);

        video.play().catch(err => {
            console.warn('Video autoplay failed:', err);
            const retry = () => {
                video.play().then(() => {
                    fadeIn();
                    document.removeEventListener('click', retry);
                    document.removeEventListener('touchstart', retry);
                });
            };
            document.addEventListener('click', retry, { once: true });
            document.addEventListener('touchstart', retry, { once: true });
        });

        setTimeout(fadeIn, 300);

        return () => {
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            video.removeEventListener('timeupdate', handleTimeUpdate);
            video.removeEventListener('ended', handleEnded);
        };
    }, [videoUrl]);

    return (
        <div className={`absolute inset-0 z-0 overflow-hidden ${className}`}>
            <video
                ref={videoRef}
                src={videoUrl}
                className="absolute inset-0 w-full h-full object-cover"
                style={{
                    top: '300px',
                    inset: 'auto 0 0 0',
                    opacity: 0,
                    transition: 'opacity 0.1s linear'
                }}
                loop={false}
                muted
                playsInline
            />

            <div className="absolute inset-0 bg-gradient-to-b from-background via-transparent to-background pointer-events-none" />

            <div className="absolute inset-0 bg-background/5 pointer-events-none" />
        </div>
    );
}