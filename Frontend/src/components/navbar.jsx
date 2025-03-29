import React, { useState, useEffect } from "react";
import { Router } from "react-router-dom";
import { NavLink, useNavigate } from "react-router-dom";
import Rickroll from "./pages/Rickroll";
import { updateReached300s } from "../services/api";

const Navbar = () => {
  const [time1, setTime1] = useState(60);
  const [time2, setTime2] = useState(0);
  const [canBeRickrolled, setCanBeRickrolled] = useState(true);
  const [time2Stopped, setTime2Stopped] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      if (!time2Stopped) {
        setTime1(prev => (prev > 0 ? prev - 1 : 0));
        setTime2(prev => {
          const newTime = prev + 1;
          // If time2 reaches 300 seconds for the first time, stop it and disable rickroll
          if (newTime === 300 && canBeRickrolled) {
            setTime2Stopped(true);
            setCanBeRickrolled(false);
            // Update the backend about reaching 300s
            updateReached300s().catch(error => {
              console.error('Failed to update reached300s status:', error);
            });
            return 300;
          }
          return newTime;
        });
      }
      else{
        setTime1(prev => 60);
        setTime2(prev => 300);
      }
      if (time1 === 0 && canBeRickrolled) {
        navigate('/rickroll');
      }
    }, 1000);

    const resetTimer = () => setTime1(60);
    
    const handleUserActivity = () => {
      resetTimer();
    };

    window.addEventListener("click", handleUserActivity);
    window.addEventListener("keydown", handleUserActivity);

    return () => {
      clearInterval(interval);
      window.removeEventListener("click", handleUserActivity);
      window.removeEventListener("keydown", handleUserActivity);
    };
  }, [time1, navigate, canBeRickrolled, time2Stopped]);

  const resetTime2 = () => setTime2(0);

  return (
    <nav className="w-full flex justify-between items-center py-2 px-4 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.3)] bg-black border-t border-b border-gray-500/50 h-24">
      <div className="flex space-x-8 text-xl font-mono">
        <div className="flex flex-col items-center group">
          <div className={`w-16 h-10 flex items-center justify-center rounded-lg bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700/50 shadow-inner transition-all duration-300 group-hover:border-[#ec625d9e] group-hover:shadow-lg group-hover:shadow-[#ec625d7e] relative overflow-hidden`}>
            <div className="absolute inset-0 bg-gradient-to-r from-green-500/0 via-green-500/10 to-green-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-shimmer"></div>
            <span className="text-gray-300 group-hover:text-[#e8984a] transition-colors duration-300 font-bold tracking-wider text-base">{time1}s</span>
            <div className="absolute inset-0 border-2 border-transparent rounded-lg group-hover:border-[#ec625d9e] transition-all duration-300"></div>
          </div>
          <span className="mt-1 text-white group-hover:text-[#e8984a] transition-colors duration-300 text-xs tracking-wide">
            {canBeRickrolled ? 'Rickroll In' : 'Rickroll Disabled'}
          </span>
        </div>
        <div className="flex flex-col items-center group">
          <div className="w-20 h-10 flex items-center justify-center rounded-lg bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700/50 shadow-inner transition-all duration-300 group-hover:border-[#ec625d9e] group-hover:shadow-lg group-hover:shadow-[#ec625d7e] relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-green-500/0 via-green-500/10 to-green-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-shimmer"></div>
            <span className="text-white group-hover:text-[#e8984a] transition-colors duration-300 tracking-wider text-base">{time2}s</span>
            <div className="absolute inset-0 border-2 border-transparent rounded-lg group-hover:border-[#ec625d9e] transition-all duration-300"></div>
          </div>
          <span className="mt-1 text-white group-hover:text-[#e8984a] transition-colors duration-300 text-xs tracking-wide">Last Rickroll</span>
        </div>
      </div>

      <div className="flex space-x-3">
        <NavLink 
          to="/rickroll"
          className={`px-4.5 py-2.5 bg-[#e8984a] text-black font-semibold rounded-lg hover:bg-[#ec625d] transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-[#ec625d7e] text-sm`}
        >
          Tutorial 
        </NavLink>
        <button
          onClick={() => navigate('/tutorial')}
          className="px-4 py-1.5 bg-[#e8984a] text-black font-semibold rounded-lg hover:bg-[#ec625d] transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-[#ec625d7e] text-sm text-center"
        >
          Rickroll
        </button>
      </div>
    </nav>
  );
};

export default Navbar;