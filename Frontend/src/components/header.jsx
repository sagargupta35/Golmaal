import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import QRCodePopup from "./qrCodePopup.jsx";

const Header = () => {
  const [showQRCode, setShowQRCode] = useState(false);

  return (
    <>
      <header className="w-full flex justify-between items-center px-4 py-3 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.3)] bg-[#1e1e1e] h-16">
        <NavLink to="/">
          <div className="text-3xl font-bold">
            <img src="../../public/logo.png" alt="" height='105px' width='130px' className="hover:opacity-80 transition-all duration-300 hover:scale-105 ml-2" />
          </div>
        </NavLink>
        <nav className="flex space-x-6">
          <button 
            onClick={() => setShowQRCode(true)}
            className="relative text-[#e8984a] hover:text-[#ec625d] transition-all duration-300 font-medium active:scale-95 active:opacity-80 group"
          >
            <span className="relative z-10">Chai Pilao</span>
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#ec625d] transition-all duration-300 group-hover:w-full"></span>
          </button>
          <NavLink 
            to="/AboutUs" 
            className="relative text-[#e8984a] hover:text-[#ec625d] transition-all duration-300 font-medium active:scale-95 active:opacity-80 group mr-2"
          >
            <span className="relative z-10">About Us</span>
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#ec625d] transition-all duration-300 group-hover:w-full"></span>
          </NavLink>
        </nav>
      </header>

      {showQRCode && <QRCodePopup onClose={() => setShowQRCode(false)} />}
    </>
  );
};

export default Header;