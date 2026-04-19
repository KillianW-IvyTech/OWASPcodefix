/* app.get('/user', (req, res) => {
      // Directly trusting query parameters can lead to NoSQL injection
      db.collection('users').findOne({ username: req.query.username }, (err, user) => {
          if (err) throw err;
          res.json(user);
      });
  }); */
import express from 'express';
import { authenticate } from './middleware/authenticate.js';
const app = express();
app.get('/user', authenticate, async (req, res, next) => {
    try {
        const username = req.query.username;
        if (!username || typeof username !== 'string' || username.length > 50) {
            return res.status(400).json({ error: 'Invalid username' });
        }
        if (username !== req.user.username) {
            return res.status(403).json({ error: 'Forbidden' });
        }
        const user = await db.collection('users').findOne(
            { username: String(username) },
            { projection: { password: 0, resetToken: 0, internalFlags: 0 } }
        );
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        res.status(200).json(user);
    } catch (err) {
        next(err);
    }
});
app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({ error: 'An internal error occurred' });
});