#!/usr/bin/env node
/**
 * Migration script: GitHub Issues → Supabase
 * 
 * This script migrates existing task tracker state from GitHub Issues to Supabase.
 * Run this once after setting up Supabase to preserve existing data.
 * 
 * Usage:
 *   node scripts/migrate-to-supabase.js
 * 
 * Required environment variables:
 *   - SUPABASE_URL
 *   - SUPABASE_SERVICE_KEY
 *   - GITHUB_TOKEN (to read from GitHub Issues)
 *   - TASK_TRACKER_STATE_REPO (e.g., "owner/repo")
 *   - TASK_TRACKER_STATE_ISSUE (e.g., "123")
 */

const { createClient } = require('@supabase/supabase-js');

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
const STATE_REPO = process.env.TASK_TRACKER_STATE_REPO || process.env.GITHUB_STATE_REPO;
const STATE_ISSUE = process.env.TASK_TRACKER_STATE_ISSUE || process.env.GITHUB_STATE_ISSUE;
const STATE_MARKER = '<!-- TikTok_TASK_TRACKER_STATE -->';
const API_BASE = 'https://api.github.com';
const TABLE_NAME = 'task_tracker_state';

function checkEnv() {
  const missing = [];
  if (!SUPABASE_URL) missing.push('SUPABASE_URL');
  if (!SUPABASE_SERVICE_KEY) missing.push('SUPABASE_SERVICE_KEY');
  if (!GITHUB_TOKEN) missing.push('GITHUB_TOKEN');
  if (!STATE_REPO) missing.push('TASK_TRACKER_STATE_REPO');
  if (!STATE_ISSUE) missing.push('TASK_TRACKER_STATE_ISSUE');
  
  if (missing.length > 0) {
    console.error('Missing required environment variables:');
    missing.forEach(v => console.error(`  - ${v}`));
    process.exit(1);
  }
}

function extractJsonFromComment(body) {
  if (!body || typeof body !== 'string' || !body.includes(STATE_MARKER)) return null;
  const match = body.match(/```json\s*([\s\S]*?)\s*```/);
  if (!match) return null;
  try {
    return JSON.parse(match[1]);
  } catch (error) {
    return null;
  }
}

async function githubRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`GitHub API ${response.status} ${response.statusText}: ${text}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

async function loadFromGitHub() {
  console.log(`Loading from GitHub: ${STATE_REPO}/issues/${STATE_ISSUE}`);
  const comments = await githubRequest(`/repos/${STATE_REPO}/issues/${STATE_ISSUE}/comments?per_page=100`);
  const latest = Array.isArray(comments) && comments.length ? comments[comments.length - 1] : null;
  const parsed = latest ? extractJsonFromComment(latest.body) : null;
  
  if (!parsed) {
    console.log('No existing state found in GitHub Issues');
    return null;
  }
  
  console.log(`Found state: version ${parsed.version || 1}, updated at ${parsed.updatedAt || 'unknown'}`);
  return parsed;
}

async function migrate() {
  checkEnv();
  
  console.log('Starting migration from GitHub Issues to Supabase...\n');
  
  // Initialize Supabase client
  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
  
  // Check if Supabase already has data
  const { data: existing, error: checkError } = await supabase
    .from(TABLE_NAME)
    .select('*')
    .eq('id', 1)
    .single();
  
  if (checkError && checkError.code !== 'PGRST116') {
    console.error('Error checking Supabase:', checkError);
    process.exit(1);
  }
  
  if (existing) {
    console.log('Supabase already has data:');
    console.log(`  - Version: ${existing.state?.version || 1}`);
    console.log(`  - Updated at: ${existing.updated_at || 'unknown'}`);
    console.log('\nMigration skipped: Supabase already contains data.');
    console.log('If you want to force migration, delete the existing row first.');
    process.exit(0);
  }
  
  // Load from GitHub
  const doc = await loadFromGitHub();
  
  if (!doc) {
    console.log('No data to migrate. Creating empty state in Supabase.');
    const emptyDoc = {
      version: 1,
      updatedAt: new Date().toISOString(),
      countries: {}
    };
    
    const { error } = await supabase
      .from(TABLE_NAME)
      .insert({
        id: 1,
        state: emptyDoc,
        updated_at: new Date().toISOString()
      });
    
    if (error) {
      console.error('Error creating empty state:', error);
      process.exit(1);
    }
    
    console.log('\n✓ Created empty state in Supabase');
    process.exit(0);
  }
  
  // Save to Supabase
  console.log('\nSaving to Supabase...');
  const { error } = await supabase
    .from(TABLE_NAME)
    .insert({
      id: 1,
      state: doc,
      updated_at: new Date().toISOString()
    });
  
  if (error) {
    console.error('Error saving to Supabase:', error);
    process.exit(1);
  }
  
  console.log('\n✓ Migration complete!');
  console.log(`  - Migrated version: ${doc.version || 1}`);
  console.log(`  - Countries: ${Object.keys(doc.countries || {}).join(', ') || 'none'}`);
  console.log(`  - Last updated: ${doc.updatedAt || 'unknown'}`);
  console.log('\nYour task tracker is now using Supabase for persistence.');
}

migrate().catch(err => {
  console.error('Migration failed:', err);
  process.exit(1);
});
