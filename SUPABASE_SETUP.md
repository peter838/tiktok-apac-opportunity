# Supabase Setup Guide for DHL Task Tracker

This guide walks you through setting up Supabase as the persistence backend for the Task Tracker.

## Overview

The Task Tracker now supports **Supabase** as the primary persistence layer, with **GitHub Issues** as a fallback. This provides:
- Faster reads/writes
- Better reliability
- Easier querying and debugging
- Simpler backup/restore

## Required Environment Variables

Add these to your Vercel project settings (Settings → Environment Variables):

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
```

The following GitHub variables are still used as fallback and for migration:

```
GITHUB_TOKEN=your-github-token
TASK_TRACKER_STATE_REPO=owner/repo-name
TASK_TRACKER_STATE_ISSUE=123
```

## Supabase Database Setup

### 1. Create the Table

Run this SQL in your Supabase SQL Editor:

```sql
-- Create the task_tracker_state table
CREATE TABLE IF NOT EXISTS task_tracker_state (
    id INTEGER PRIMARY KEY DEFAULT 1,
    state JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ensure only one row exists (singleton pattern)
CREATE UNIQUE INDEX IF NOT EXISTS task_tracker_state_single_row 
ON task_tracker_state ((id = 1));

-- Add comment for documentation
COMMENT ON TABLE task_tracker_state IS 'Stores global task tracker state for all countries';
```

### 2. Enable Row Level Security (Optional but Recommended)

```sql
-- Enable RLS
ALTER TABLE task_tracker_state ENABLE ROW LEVEL SECURITY;

-- Create policy to allow service role full access
CREATE POLICY "Service role has full access" 
ON task_tracker_state 
FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);
```

### 3. Create the Initial Row

```sql
-- Insert initial empty state
INSERT INTO task_tracker_state (id, state, updated_at)
VALUES (1, '{"version": 1, "updatedAt": "' || NOW()::text || '", "countries": {}}', NOW())
ON CONFLICT (id) DO NOTHING;
```

## Migration from GitHub Issues

If you have existing data in GitHub Issues, migrate it to Supabase:

### Option 1: Automatic Migration (via API)

Call the migration endpoint with your GitHub token:

```bash
curl -X POST https://your-vercel-app.vercel.app/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"action": "migrate"}'
```

### Option 2: Local Migration Script

1. Set environment variables locally:
```bash
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_SERVICE_KEY=your-service-role-key
export GITHUB_TOKEN=your-github-token
export TASK_TRACKER_STATE_REPO=owner/repo-name
export TASK_TRACKER_STATE_ISSUE=123
```

2. Run the migration script:
```bash
cd /data/.openclaw/workspace-vibe-agent/dhl-singapore-opportunity
npm install
node scripts/migrate-to-supabase.js
```

## Verification

After setup, verify everything works:

1. **Check the API returns Supabase backend:**
```bash
curl https://your-vercel-app.vercel.app/api/tasks?country=sg
```

Look for `"backend": "supabase"` in the response.

2. **Make a test edit** on any country page and verify it persists after refresh.

3. **Check Supabase Dashboard** → Table Editor → `task_tracker_state` to see the data.

## Troubleshooting

### "Supabase not configured" error
- Verify `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` are set in Vercel
- Redeploy after adding environment variables

### Migration fails
- Check that GitHub token has `repo` scope
- Verify the issue number and repo name are correct
- Check that the Supabase table exists

### Data not persisting
- Check Vercel logs for errors
- Verify Supabase service key has full access (not anon key)
- Check RLS policies if enabled

## Rollback

To revert to GitHub Issues:
1. Remove `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` from Vercel
2. Redeploy
3. The API will automatically fall back to GitHub Issues

## Data Structure

The state document stored in Supabase:

```json
{
  "version": 42,
  "updatedAt": "2026-04-13T09:30:00.000Z",
  "countries": {
    "sg": {
      "nextId": 15,
      "tasks": [...],
      "history": [...],
      "past": [...]
    },
    "hk": { ... },
    "my": { ... },
    "th": { ... }
  }
}
```

## Support

For issues:
1. Check Vercel function logs
2. Check Supabase logs (Dashboard → Logs)
3. Verify environment variables are set correctly
