(function initConvexTaskClient(global) {
  const isLocalhost = global.location && global.location.hostname.includes('localhost');
  
  // For localhost, use direct Convex connection from window.CONVEX_URL or default
  // For production, use window.CONVEX_URL which should be set to the production deployment
  const convexUrl = global.CONVEX_URL || (isLocalhost ? 'http://127.0.0.1:3210' : null);

  let clientPromise = null;
  let connectionFailed = false;

  async function getClient() {
    if (!convexUrl) {
      throw new Error('Convex URL is not configured. Set window.CONVEX_URL before loading shared.js.');
    }
    
    if (!clientPromise) {
      clientPromise = import('https://esm.sh/convex@1.22.0/browser').then((mod) => {
        return new mod.ConvexHttpClient(convexUrl);
      }).catch(err => {
        connectionFailed = true;
        throw err;
      });
    }
    return clientPromise;
  }

  async function query(name, args) {
    if (!convexUrl || connectionFailed) {
      throw new Error('Convex not available');
    }
    const client = await getClient();
    return client.query(name, args || {});
  }

  async function mutation(name, args) {
    if (!convexUrl || connectionFailed) {
      throw new Error('Convex not available');
    }
    const client = await getClient();
    return client.mutation(name, args || {});
  }

  global.TikTokConvexClient = {
    url: convexUrl,
    isConfigured: Boolean(convexUrl) && !connectionFailed,
    isLocalhost,
    query,
    mutation,
  };
})(window);
