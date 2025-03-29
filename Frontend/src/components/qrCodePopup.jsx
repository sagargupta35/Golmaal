import React from 'react';

const QRCodePopup = ({ onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Blurred Background */}
      <div 
        className="absolute inset-0 bg-black/70 backdrop-blur-md"
        onClick={onClose}
      ></div>

      {/* Popup Content */}
      <div className="relative bg-gray-900/90 backdrop-blur-md rounded-2xl p-12 border border-[#e8984a]/30 shadow-xl shadow-[#e8984a]/20">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 text-gray-400 hover:text-[#e8984a] transition-colors"
        >
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* QR Code Image */}
        <div className="flex flex-col items-center space-y-6">
          <img 
            src="/qr.png" 
            alt="QR Code" 
            className="w-60 h-60 rounded-lg"
          />
          <p className="text-[#e8984a] text-xl font-medium">Scan to help us drink Chai 😉!</p>
        </div>
      </div>
    </div>
  );
};

export default QRCodePopup;