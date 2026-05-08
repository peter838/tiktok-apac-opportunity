#!/bin/bash
# Setup script for production Convex deployment
# Run this after: npx convex login

set -e

echo "=== Convex Production Setup ==="
echo ""

# Check if logged in
if ! npx convex login status > /dev/null 2>&1; then
    echo "❌ Not logged in to Convex. Please run: npx convex login"
    exit 1
fi

echo "✅ Logged in to Convex"
echo ""

# Create production deployment
echo "Creating production deployment..."
npx convex deploy

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Get your production URL from the output above (looks like: https://your-project.convex.cloud)"
echo "2. Update all HTML files with the production URL"
echo "3. Deploy to Vercel"
echo ""
echo "To update HTML files, run:"
echo "  npm run update-convex-url https://your-project.convex.cloud"
