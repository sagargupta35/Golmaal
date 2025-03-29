import mongoose from 'mongoose';

const statsSchema = new mongoose.Schema({
  totalVisits: {
    type: Number,
    default: 0
  },
  totalRickrolls: {
    type: Number,
    default: 0
  },
  lastUpdated: {
    type: Date,
    default: Date.now
  }
});

// Static method to get or create stats document
statsSchema.statics.getStats = async function() {
  let stats = await this.findOne();
  if (!stats) {
    stats = await this.create({});
  }
  return stats;
};

export default mongoose.model('Stats', statsSchema); 