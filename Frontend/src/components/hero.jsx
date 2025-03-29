import React, { useState, useEffect, useRef } from "react";
import MonacoEditor from "./monaco";
import { executeCode } from "../services/api";

const HeroSection = () => {
  const [editorContent, setEditorContent] = useState("");
  const [outputContent, setOutputContent] = useState("");
  const [showWelcome, setShowWelcome] = useState(false);
  const [countdown, setCountdown] = useState(3);
  const [buttonsSwapped, setButtonsSwapped] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const editorRef = useRef(null);

  useEffect(() => {
    // Check if this is the first visit or new session
    const hasSeenWelcome = localStorage.getItem('hasSeenWelcome');
    const sessionId = localStorage.getItem('sessionId');
    
    if (!hasSeenWelcome || !sessionId) {
      setShowWelcome(true);
      localStorage.setItem('hasSeenWelcome', 'true');
    }
  }, []);

  useEffect(() => {
    if (countdown > 0 && showWelcome) {
      const timer = setInterval(() => {
        setCountdown(prev => prev - 1);
      }, 1000);
      return () => clearInterval(timer);
    } else if (countdown === 0) {
      setShowWelcome(false);
    }
  }, [countdown, showWelcome]);

  // Add button swap effect
  useEffect(() => {
    const swapInterval = setInterval(() => {
      setButtonsSwapped(prev => !prev);
    }, 15000);

    return () => clearInterval(swapInterval);
  }, []);

  const handleClear = () => {
    setEditorContent("");
    setOutputContent("");
    if (editorRef.current) {
      editorRef.current.setValue("");
    }
  };

  const handleWelcomeOK = () => {
    setShowWelcome(false);
  };

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  const getRandomInt = () => Math.floor(Math.random() * 10) + 1;

  const handleRunCode = async () => {
    try {
      setIsRunning(true);
      
      // Create a timeout promise that rejects after 5 seconds
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('timeout')), 5000);
      });

      // Race between the code execution and the timeout
      const response = await Promise.race([
        executeCode(editorContent),
        timeoutPromise
      ]);

      const randomInt = getRandomInt();
      if(randomInt === 7 && response.error === null){
        setOutputContent(`Chud Gye Guru!  Chud Gyi Chud Gyi Chud Gyi!!!!`);
        await sleep(3000);
      }
      let stringResponse = "";
      if(response.output) {
        stringResponse = response.output.join("\n");
      }
      if(response.error){
        stringResponse = stringResponse + "\nError:";
        if(Array.isArray(response.error)){
          const stringError = response.error.join("\n");
          stringResponse = stringResponse + "\n" + stringError;
        }
        else{
          stringResponse = stringResponse + "\n" + response.error;
        }
      }
      stringResponse = stringResponse + "\n\n\n\n\n\n\n\n\n\n\n";
      setOutputContent(stringResponse);
    } catch (error) {
      if (error.message === 'timeout') {
        setOutputContent("It took too long, try running again\n\n\n\n\n\n\n\n\n\n\n");
      } else {
        setOutputContent(`Error: ${error.message}\n\n\n\n\n\n\n\n\n\n\n`);
      }
    } finally {
      setIsRunning(false);
    }
  };

  const WelcomePopup = () => (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Blurred Background */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-md"></div>
      
      {/* Popup Content */}
      <div className="relative bg-gray-900/90 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-700/50 p-8 flex flex-col items-center space-y-6">
        {/* Welcome Heading */}
        <h1 className="text-2xl font-bold text-white mb-2">Welcome to Golmaal!</h1>
        <p className="text-gray-300 mb-4">Try not to get Rickrolled for 5 minutes!</p>
        {/* Dancing Emoji */}
        <div className="text-8xl animate-bounce">🕺</div>

        {/* OK Button */}
        <button
          onClick={handleWelcomeOK}
          className="px-8 py-3 rounded-lg text-white font-medium bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 shadow-lg hover:shadow-green-500/25 transition-all duration-300 transform hover:scale-105 active:scale-95"
        >
          OK
        </button>

        {/* Countdown Timer */}
        <div className="text-3xl font-mono text-green-400 animate-pulse">
          {countdown}
        </div>
      </div>
    </div>
  );

  const RunButton = () => (
    <button 
      onClick={handleRunCode}
      disabled={isRunning}
      className={`px-2.5 py-1.5 bg-transparent backdrop-blur-md hover:bg-gray-800/30 transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-green-500/25 group flex items-center space-x-1.5 border border-[#1e1e1e] hover:border-green-500/30 rounded-lg ${isRunning ? 'opacity-50 cursor-not-allowed' : ''}`}
      title="Run Code"
    >
      <svg 
        className="w-4 h-4 text-green-500 group-hover:text-green-400" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
        />
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <span className="text-sm text-gray-300 group-hover:text-green-400">
        {isRunning ? 'Running...' : 'Run'}
      </span>
    </button>
  );

  const ClearButton = () => (
    <button 
      onClick={handleClear}
      className="px-2.5 py-1.5 bg-transparent backdrop-blur-md hover:bg-gray-800/30 rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-500/25 group flex items-center space-x-1.5 border border-[#1e1e1e] hover:border-red-500/30 rounded-lg"
      title="Clear Output"
    >
      <svg 
        className="w-4 h-4 text-red-500 group-hover:text-red-400" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
        />
      </svg>
      <span className="text-sm text-gray-300 group-hover:text-red-400">Clear</span>
    </button>
  );

  return (
    <section className="w-full h-screen flex bg-black">
      {/* Welcome Popup */}
      {showWelcome && <WelcomePopup />}

      {/* Left Part */}
      <div className="w-1/2 relative flex flex-col justify-center bg-black">
        {/* Action Buttons */}
        <div className="flex justify-center space-x-3 mb-5 mt-5.5">
          {buttonsSwapped ? (
            <>
              <ClearButton />
              <RunButton />
            </>
          ) : (
            <>
              <RunButton />
              <ClearButton />
            </>
          )}
        </div>

        {/* Editor Container */}
        <div className='overflow-hidden shadow-2xl border border-gray-700/50'>
          <MonacoEditor 
            ref={editorRef}
            value={editorContent}
            onChange={setEditorContent}
          />
        </div>
      </div>

      {/* Right Part */}
      <div className="w-1/2 flex flex-col justify-center bg-gradient-to-br from-gray-900 to-gray-800">
        {/* Output Container */}
        <div className="h-full overflow-hidden shadow-2xl border-l border-gray-700/50">
          <div className="bg-black p-2 border-b border-gray-700/50 flex justify-center items-center">
            <span className="text-gray-300 h-15 text-xl font-medium flex items-center justify-center">Output</span>
          </div>
          <textarea
            value={outputContent}
            onChange={(e) => setOutputContent(e.target.value)}
            readOnly
            className="w-full h-full p-6 bg-black backdrop-blur-sm text-white font-mono text-lg resize-none border-none focus:outline-none placeholder-gray-500"
          ></textarea>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
