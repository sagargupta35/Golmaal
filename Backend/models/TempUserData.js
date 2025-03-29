import mongoose from 'mongoose';

const tempUserDataSchema = new mongoose.Schema({
  sessionId: {
    type: String,
    required: true,
    unique: true
  },
  hasCountedRickroll: {
    type: Boolean,
    default: false
  },
  hasReached300s: {
    type: Boolean,
    default: false
  },
  createdAt: {
    type: Date,
    default: Date.now,
    expires: 3600 // Document will be automatically deleted after 1 hour
  }
});

export default mongoose.model('TempUserData', tempUserDataSchema); 