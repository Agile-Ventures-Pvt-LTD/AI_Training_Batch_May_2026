import React from 'react';

interface SleepsiaLogoProps {
  className?: string;
  variant?: 'full' | 'icon' | 'dark';
}

export const SleepsiaLogo: React.FC<SleepsiaLogoProps> = ({ className = 'h-8 w-auto', variant = 'full' }) => {
  if (variant === 'icon') {
    return (
      <div className={`flex items-center justify-center font-serif font-black text-[#027dae] ${className}`}>
        <span className="text-xl font-bold tracking-tight">S</span>
      </div>
    );
  }

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 420 160"
      className={className}
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <linearGradient id="sleepsiaBrandBlue" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#015b85" />
          <stop offset="50%" stopColor="#027dae" />
          <stop offset="100%" stopColor="#0494cf" />
        </linearGradient>
      </defs>

      {/* Top Swoosh */}
      <path
        d="M 45,44 C 70,27 135,21 210,23 C 285,25 350,36 395,48 C 345,34 275,23 205,23 C 135,23 75,29 45,44 Z"
        fill="url(#sleepsiaBrandBlue)"
      />

      {/* SLEEPSIA Serif Wordmark */}
      <text
        x="210"
        y="108"
        textAnchor="middle"
        fontFamily="'Playfair Display', 'Baskerville', 'Times New Roman', 'Georgia', serif"
        fontSize="64"
        fontWeight="700"
        letterSpacing="6"
        fill="#027dae"
        style={{ letterSpacing: '0.12em' }}
      >
        SLEEPSIA
      </text>

      {/* Bottom Swoosh */}
      <path
        d="M 15,116 C 50,132 120,143 200,145 C 265,146 310,143 325,142 C 280,146 220,146 155,143 C 85,138 40,127 15,116 Z"
        fill="url(#sleepsiaBrandBlue)"
      />
    </svg>
  );
};

export default SleepsiaLogo;
