const API_BASE_URL = 'http://localhost:5000/api';

// Helper function to get session ID
const getSessionId = () => {
  return localStorage.getItem('sessionId');
};

// Helper function to get headers with session ID
const getHeaders = () => {
  const sessionId = getSessionId();
  return {
    'Content-Type': 'application/json',
    'x-session-id': sessionId
  };
};

// Stats related API calls
export const getStats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch stats');
    return await response.json();
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export const trackRickroll = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stats/rickroll`, {
      method: 'POST',
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to track rickroll');
    const data = await response.json();
    return data.stats;
  } catch (error) {
    console.error('Error tracking rickroll:', error);
    throw error;
  }
};

// User session related API calls
export const createSession = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) throw new Error('Failed to create session');
    const data = await response.json();
    localStorage.setItem('sessionId', data.sessionId);
    return data;
  } catch (error) {
    console.error('Error creating session:', error);
    throw error;
  }
};

export const updateSession = async (editorContent) => {
  try {
    const sessionId = getSessionId();
    if (!sessionId) throw new Error('No active session');

    const response = await fetch(`${API_BASE_URL}/user/session/${sessionId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({ editorContent })
    });
    if (!response.ok) throw new Error('Failed to update session');
    return await response.json();
  } catch (error) {
    console.error('Error updating session:', error);
    throw error;
  }
};

export const updateReached300s = async () => {
  try {
    const sessionId = getSessionId();
    if (!sessionId) throw new Error('No active session');

    const response = await fetch(`${API_BASE_URL}/user/session/${sessionId}/reached300s`, {
      method: 'PUT',
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to update reached300s status');
    return await response.json();
  } catch (error) {
    console.error('Error updating reached300s status:', error);
    throw error;
  }
};

export const executeCode = async (code) => {
  try {
    const response = await fetch(`${API_BASE_URL}/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-session-id': getSessionId()
      },
      body: JSON.stringify({ "code":code })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.output || errorData.error || 'Failed to execute code');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error executing code:', error);
    throw error;
  }
};

export const getSessionData = async () => {
  try {
    const sessionId = getSessionId();
    if (!sessionId) throw new Error('No active session');

    const response = await fetch(`${API_BASE_URL}/user/session/${sessionId}`, {
      headers: getHeaders()
    });
    
    if (response.status === 404) {
      const error = new Error('Session not found');
      error.name = 'SessionNotFoundError';
      throw error;
    }
    
    if (!response.ok) throw new Error('Failed to get session data');
    return await response.json();
  } catch (error) {
    console.error('Error getting session data:', error);
    throw error;
  }
};

// Cleanup session data
export const cleanupSession = async () => {
  try {
    const sessionId = getSessionId();
    if (!sessionId) return;

    const response = await fetch(`${API_BASE_URL}/user/session/${sessionId}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    
    if (!response.ok) throw new Error('Failed to cleanup session');
    
    // Clear session ID from localStorage
    localStorage.removeItem('sessionId');
    
    return await response.json();
  } catch (error) {
    console.error('Error cleaning up session:', error);
    throw error;
  }
}; 