#!/usr/bin/env node
// Update all HTML files with the production Convex URL
// Usage: node scripts/update-convex-url.js https://your-project.convex.cloud

const fs = require('fs');
const path = require('path');

const NEW_URL = process.argv[2];

if (!NEW_URL) {
  console.error('Usage: node scripts/update-convex-url.js https://your-project.convex.cloud');
  process.exit(1);
}

const filesToUpdate = [
  'index.html',
  'sg/index.html',
  'hk/index.html',
  'cn/index.html',
  'jp/index.html',
  'au/index.html',
  'my/index.html',
  'id/index.html',
  'in/index.html',
  'th/index.html',
];

let updatedCount = 0;

filesToUpdate.forEach(file => {
  const filePath = path.join(__dirname, '..', file);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  Skipping ${file} (not found)`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Check if file has the Convex URL script
  if (!content.includes('window.CONVEX_URL')) {
    console.log(`⚠️  Skipping ${file} (no CONVEX_URL found)`);
    return;
  }
  
  // Replace the URL - handle both anonymous and localhost URLs
  const oldPattern = /window\.CONVEX_URL\s*=\s*"[^"]+";/;
  const newScript = `window.CONVEX_URL = "${NEW_URL}";`;
  
  if (oldPattern.test(content)) {
    content = content.replace(oldPattern, newScript);
    fs.writeFileSync(filePath, content);
    console.log(`✅ Updated ${file}`);
    updatedCount++;
  } else {
    console.log(`⚠️  Could not find pattern in ${file}`);
  }
});

console.log('');
console.log(`Updated ${updatedCount} files with Convex URL: ${NEW_URL}`);
console.log('');
console.log('Next: Deploy to Vercel with:');
console.log('  vercel --prod');
