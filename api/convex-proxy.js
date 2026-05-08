// Convex proxy API route - forwards requests to anonymous Convex deployment
// This bypasses CORS restrictions by proxying through the same origin

const CONVEX_URL = process.env.CONVEX_URL || 'http://127.0.0.1:3210';

module.exports = async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { path, body } = req.body;
    
    if (!path) {
      return res.status(400).json({ error: 'Missing path' });
    }

    // Forward to Convex
    // Convex expects: { path: "tasks:getTasksByCountry", args: {...}, format: "json" }
    const convexBody = {
      path: body?.path || path,
      args: body?.args || body || {},
      format: 'json'
    };

    const convexResponse = await fetch(`${CONVEX_URL}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(convexBody),
    });

    const data = await convexResponse.json();
    
    return res.status(convexResponse.status).json(data);
  } catch (error) {
    console.error('Convex proxy error:', error);
    return res.status(500).json({ 
      error: 'Proxy error', 
      message: error.message,
      convexUrl: CONVEX_URL 
    });
  }
}
