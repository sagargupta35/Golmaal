import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { trackRickroll, getStats } from '../../services/api';

const Rickroll = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatsAndTrack = async () => {
      try {
        setLoading(true);
        // First track the rickroll
        await trackRickroll();
        // Then fetch updated stats
        const statsData = await getStats();
        setStats(statsData);
      } catch (error) {
        console.error('Failed to fetch stats or track rickroll:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatsAndTrack();
  }, []);

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-black relative">
      {/* Back Button */}
      <button
        onClick={() => navigate('/')}
        className="absolute top-4 left-4 px-4 py-2 bg-[#e8984a] text-black font-semibold rounded-lg hover:bg-[#ec625d] transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-[#ec625d7e] flex items-center space-x-2"
      >
        <svg 
          className="w-5 h-5" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
        <span>Back to Home</span>
      </button>

      {/* Stats Display */}
      {stats && (
        <div className="absolute top-4 right-4 bg-gray-800/80 backdrop-blur-md p-4 rounded-lg text-white">
          <h3 className="text-lg font-semibold mb-2">Rickroll Stats</h3>
          <p>Total Visits: {stats.totalVisits}</p>
          <p>Total Rickrolls: {stats.totalRickrolls}</p>
          <p>Rickroll Ratio: {(stats.ratio * 100).toFixed(2)}%</p>
        </div>
      )}

      {/* Tutorial Link Heading */}
      <div className="mb-8 text-center">
        <h2 className="text-2xl font-bold text-white mb-2">Got Rickrolled?</h2>
        <Link 
          to="/tutorial" 
          className="text-[#e8984a] hover:text-[#ec625d] transition-colors duration-300 text-lg font-medium"
        >
          Click here to go to tutorial (Not Kidding this time!😉) →
        </Link>
      </div>

      {/* Video Container */}
      <div className="w-full max-w-4xl aspect-video rounded-lg">
        <iframe
          className="w-full h-full"
          src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
          title="Rickroll"
          allow="accelerometer; autoplay; clipboard-write; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>
    </div>
  );
};

export default Rickroll;
