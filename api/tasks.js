module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.end();
    return;
  }

  return res.status(410).json({
    ok: false,
    error: 'Supabase task API has been deprecated. Task Tracker now reads/writes through Convex client functions.',
  });
};
