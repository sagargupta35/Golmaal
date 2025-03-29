import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';
import Stats from './models/Stats.js';
import TempUserData from './models/TempUserData.js';
import fetch from 'node-fetch';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: '*', 
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'x-session-id'],
  credentials: true
}));
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/golmaal')
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

// Routes

// 1. Track visit and get stats
app.get('/api/stats', async (req, res) => {
  try {
    const stats = await Stats.getStats();
    const ratio = stats.totalRickrolls / stats.totalVisits;
    res.json({
      totalVisits: stats.totalVisits,
      totalRickrolls: stats.totalRickrolls,
      ratio: ratio
    });
  } catch (error) {
    console.error('Error in /api/stats:', error);
    res.status(500).json({ error: 'Failed to update stats' });
  }
});

// 2. Track rickroll
app.post('/api/stats/rickroll', async (req, res) => {
  try {
    console.log('Received rickroll request');
    const sessionId = req.headers['x-session-id'];
    
    if (!sessionId) {
      return res.status(400).json({ error: 'No session ID provided' });
    }

    // Check if rickroll has been counted for this session
    const userData = await TempUserData.findOne({ sessionId });
    if (!userData) {
      return res.status(404).json({ error: 'Session not found' });
    }

    const stats = await Stats.getStats();
    console.log('Current stats before update:', stats);

    // Only increment the count if this session hasn't counted a rickroll yet and hasn't reached 300s
    if (!userData.hasCountedRickroll && !userData.hasReached300s) {
      stats.totalRickrolls += 1;
      await stats.save();
      console.log('Updated stats after rickroll:', stats);
      
      // Mark this session as having counted a rickroll
      userData.hasCountedRickroll = true;
      await userData.save();
    }
    
    // Return updated stats
    const ratio = stats.totalRickrolls / stats.totalVisits;
    res.json({
      success: true,
      stats: {
        totalVisits: stats.totalVisits,
        totalRickrolls: stats.totalRickrolls,
        ratio: ratio
      }
    });
  } catch (error) {
    console.error('Error in /api/stats/rickroll:', error);
    res.status(500).json({ error: 'Failed to update rickroll count' });
  }
});

// 3. Create temporary user session
app.post('/api/user/session', async (req, res) => {
  try {
    const sessionId = uuidv4();
    const userData = await TempUserData.create({
      sessionId
    });

    // Increment visit count when creating a new session
    const stats = await Stats.getStats();
    stats.totalVisits += 1;
    await stats.save();

    res.json({ sessionId: userData.sessionId });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create session' });
  }
});

// 4. Get temporary user data
app.get('/api/user/session/:sessionId', async (req, res) => {
  try {
    const userData = await TempUserData.findOne({ sessionId: req.params.sessionId });
    if (!userData) {
      return res.status(404).json({ error: 'Session not found' });
    }
    res.json(userData);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get user data' });
  }
});

// 5. Cleanup temporary user data
app.delete('/api/user/session/:sessionId', async (req, res) => {
  try {
    const result = await TempUserData.findOneAndDelete({ sessionId: req.params.sessionId });
    if (!result) {
      return res.status(404).json({ error: 'Session not found' });
    }
    res.json({ message: 'Session data cleaned up successfully' });
  } catch (error) {
    console.error('Error cleaning up session:', error);
    res.status(500).json({ error: 'Failed to cleanup session data' });
  }
});

// 6. Update hasReached300s status
app.put('/api/user/session/:sessionId/reached300s', async (req, res) => {
  try {
    const userData = await TempUserData.findOne({ sessionId: req.params.sessionId });
    if (!userData) {
      return res.status(404).json({ error: 'Session not found' });
    }
    
    userData.hasReached300s = true;
    await userData.save();
    
    res.json({ success: true, message: 'Updated hasReached300s status' });
  } catch (error) {
    console.error('Error updating hasReached300s status:', error);
    res.status(500).json({ error: 'Failed to update hasReached300s status' });
  }
});

// 7. Proxy code execution to external service
app.post('/api/execute', async (req, res) => {
  try {
    const { code } = req.body;
    //console.log(code);
    if (!code) {
      return res.status(400).json({ error: 'No code provided' });
    }

    const response = await fetch(process.env.CODEURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "code": code
      })
    });

    if (!response.ok) {
      throw new Error('Failed to execute code on external service');
    }

    const data = await response.json();
    //console.log(data);
    // Format the response to match the expected structure
    res.json({
      "output": data.Output  || null,
      "error": data.Error  || null
    });
  } catch (error) {
    console.error('Error executing code:', error);
    res.status(500).json({ 
      output: `Error: ${error.message || 'Failed to execute code'}`
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
}); 