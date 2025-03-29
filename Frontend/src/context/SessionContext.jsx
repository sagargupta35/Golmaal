import React, { createContext, useContext, useState, useEffect } from 'react';
import { createSession, updateSession, getSessionData, cleanupSession, getStats } from '../services/api';

const SessionContext = createContext();

export const useSession = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};

export const SessionProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [editorContent, setEditorContent] = useState('');

  // Handle cleanup on window close
  useEffect(() => {
    const handleBeforeUnload = async () => {
      try {
        await cleanupSession();
      } catch (error) {
        console.error('Failed to cleanup session:', error);
      }
    };

    const handleVisibilityChange = async () => {
      if (document.visibilityState === 'hidden') {
        try {
          await cleanupSession();
        } catch (error) {
          console.error('Failed to cleanup session:', error);
        }
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  // Initialize session and update visit count
  useEffect(() => {
    const initSession = async () => {
      try {
        // First create a session
        const data = await createSession();
        setSessionId(data.sessionId);
        
        // Only update visit count for new sessions
        await getStats();
      } catch (error) {
        console.error('Failed to initialize session:', error);
      }
    };

    const checkAndUpdateSession = async () => {
      // Check if we already have a session
      const existingSessionId = localStorage.getItem('sessionId');
      if (!existingSessionId) {
        // Only create new session and update visit count if no session exists
        await initSession();
      } else {
        // For existing sessions, verify if it's still valid
        try {
          const sessionData = await getSessionData();
          if (!sessionData) {
            // If session is invalid, create a new one
            localStorage.removeItem('sessionId'); // Clear invalid session ID
            await initSession();
          } else {
            setSessionId(existingSessionId);
          }
        } catch (error) {
          // Handle session not found error
          if (error.name === 'SessionNotFoundError') {
            console.log('Session not found, creating new session');
            localStorage.removeItem('sessionId'); // Clear invalid session ID
            await initSession();
          } else {
            // Handle other errors
            console.error('Error checking session:', error);
            // Optionally create a new session on other errors
            localStorage.removeItem('sessionId');
            await initSession();
          }
        }
      }
    };

    checkAndUpdateSession();
  }, []);

  // Update editor content
  const updateContent = async (content) => {
    try {
      setEditorContent(content);
      if (sessionId) {
        await updateSession(content);
      }
    } catch (error) {
      console.error('Failed to update content:', error);
    }
  };

  const value = {
    sessionId,
    editorContent,
    updateContent
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
}; 