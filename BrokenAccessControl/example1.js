/* app.get('/profile/:userId', (req, res) => {
    User.findById(req.params.userId, (err, user) => {
        if (err) return res.status(500).send(err);
        res.json(user);
    });
}); */
const auth = require('./middleware/auth');
const { Types } = require('mongoose');
app.get('/profile/:userId', auth, async (req, res) => {
  if (!Types.ObjectId.isValid(req.params.userId))
    return res.status(400).json({ error: 'Invalid ID' });
  if (req.user.id !== req.params.userId)
    return res.status(403).json({ error: 'Forbidden' });
  try {
    const user = await user.findById(req.params.userId)
      .select('-password -resetToken -__v');
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json(user);
  } catch (err) {
    console.error('[profile]', err);
    res.status(500).json({ error: 'Server error' });
  }
});