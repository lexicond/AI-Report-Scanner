# 🚨 Urgent Fix Guide - After First Run

## What Happened

Your scanner ran successfully and **spent ~$3-5** calling the Claude API. However:

1. ❌ **Using 7 days instead of 30** - Railway variables not set for monthly
2. ⚠️ **Slack message truncated** - Only showing header
3. ⚠️ **Email not received** - Sent successfully but not in inbox
4. ✅ **Reports generated successfully** - Saved to Railway container

---

## 🎯 IMMEDIATE ACTIONS (No Additional Cost)

### 1. View Your Generated Reports

Your reports are already generated! You just need to access them from Railway:

**Option A: Download from Railway (Easiest)**

1. Go to Railway Dashboard: https://railway.app
2. Click your AI-Report-Scanner project
3. Click on the deployment
4. Go to "Deployments" tab → Latest deployment
5. Click "View Logs"
6. Scroll to find the file paths:
   ```
   📄 Reading List: reports/reading_list_2026-01-21.md
   ```

**Option B: Use Railway CLI to Download Files**

```bash
# Install Railway CLI (if not already)
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Download the reports
railway run cat reports/reading_list_2026-01-21.md > reading_list.md
railway run cat output/metadata_2026-01-21.json > metadata.json
```

**Option C: Check Railway Volume (if mounted)**

Railway deployments are ephemeral, but you can mount a volume to persist files.

---

### 2. Enable CACHE MODE (Most Important!)

This will let you test improvements **for FREE** using the API response you just paid for.

**In Railway Dashboard:**

1. Go to your project → Variables
2. Add these variables:
   ```
   CACHE_MODE=true
   ```

3. Click "Redeploy"

**What this does:**
- First run (ALREADY DONE ✅): Calls API and saves response to `cache/api_response.json`
- Next runs (FREE 🆓): Uses cached response instead of calling API

**Now you can test unlimited changes to:**
- Slack formatting
- Email formatting
- Report structure
- Output files

**All for FREE!** 🎉

---

### 3. Fix Railway Configuration for Monthly Scanning

Your Railway variables are using **weekly** defaults (7 days). Let's fix that:

**In Railway Dashboard → Variables, UPDATE these:**

```bash
# Change from 7 to 30 for monthly
SEARCH_DAYS_BACK=30

# Ensure monthly report count
MAX_REPORTS=15

# Keep cache mode ON for testing
CACHE_MODE=true
```

**Redeploy after changing.**

---

### 4. Check Email (Spam Folder)

SendGrid shows the email was sent successfully to `Alex.m.deville@gmail.com`.

**Check:**
1. 📬 **Spam/Junk folder** in Gmail
2. 🔍 Search Gmail for: `from:noreply@railway.app` or subject: `Weekly AI Reports`
3. 📧 Check SendGrid dashboard: https://app.sendgrid.com/

**If still not there:**
- SendGrid might need domain verification
- Check SendGrid Activity Feed for bounce/delivery status
- Verify `SENDGRID_FROM_EMAIL` is verified in SendGrid

---

### 5. Fix Slack Notification Format

The Slack message is too short. Let's improve it in the next (FREE) cache run.

I'll create a fix for this below.

---

## 📊 Your Current Report Stats

From the logs:
```
Model: claude-sonnet-4-20250514
Input tokens: 609,711
Output tokens: 5,587
Cost: ~$3-5
```

**Good news:** This response is now cached! You can iterate on formatting for free.

---

## 🔄 Test Workflow (After Enabling CACHE_MODE)

### Step 1: Manual Trigger with Cache (FREE)

```bash
# Trigger deployment manually in Railway
# Or wait for next cron run
```

The scanner will:
1. ✅ Use cached API response (no API call)
2. ✅ Generate reports
3. ✅ Send to Slack/Email
4. ✅ Show improved formatting

**Cost: $0.00** 🆓

### Step 2: View Reports Locally

If you want to iterate locally:

```bash
# Pull the code
git pull

# Set up .env
cp .env.example .env

# Add these to .env:
REPLAY_MODE=true
CACHE_MODE=false

# Copy cache from Railway (if you have it)
# Or run once with CACHE_MODE=true locally

# Run locally for free
python main.py
```

---

## 🛠️ Improvements to Make (Next Steps)

### A. Better Slack Formatting

The Slack code extracts only the CRITICAL section. Let's improve this.

**I'll create a fix in a separate commit.**

### B. Email in Spam - Domain Authentication

If emails keep going to spam, you need to:

1. **Verify your domain in SendGrid**:
   - Add SPF/DKIM records
   - Use a custom domain (not @gmail.com)

2. **Or use a verified SendGrid sender**:
   - SendGrid → Settings → Sender Authentication
   - Verify an email address

### C. Add Volume for Report Persistence

Railway deployments are ephemeral. To persist reports:

```bash
# In railway.toml, add:
[volumes]
mount = "/app/reports"
```

This keeps reports between deployments.

---

## ⚡ Quick Commands Reference

### View cached response (locally):
```bash
cat cache/api_response.json | jq '.content[0].text[:500]'
```

### Force new API call (costs $3-5):
```bash
# In Railway, set:
CACHE_MODE=false
REPLAY_MODE=false
```

### Use cache for testing (FREE):
```bash
# In Railway, set:
CACHE_MODE=true  # Saves responses
REPLAY_MODE=true # Uses cached responses
```

### Download reports from Railway:
```bash
railway run cat reports/reading_list_2026-01-21.md
```

---

## 🎯 Recommended Next Steps

1. **Enable CACHE_MODE=true in Railway** ← DO THIS NOW
2. **Redeploy to save cache**
3. **Download the reading_list file to view results**
4. **Check Gmail spam folder for email**
5. **Wait for improved Slack formatting** (I'll fix this)
6. **Set SEARCH_DAYS_BACK=30 for monthly**

---

## 💡 Understanding the Modes

| Mode | API Call? | Cost | Use Case |
|------|-----------|------|----------|
| **Normal** | ✅ Yes | $3-5 | Production monthly run |
| **CACHE_MODE=true** | ✅ Yes + Save | $3-5 once | First run, save response |
| **REPLAY_MODE=true** | ❌ No (uses cache) | $0 | Testing/iterating format |
| **DRY_RUN=true** | ❌ No (mock data) | $0 | Initial setup testing |

---

## 🚨 Common Issues

### "Cache file not found"

If you enable REPLAY_MODE but don't have a cache:

**Solution:** Run once with `CACHE_MODE=true` first to create the cache.

### "Report looks wrong"

If the report format is bad:

**Solution:** With CACHE_MODE enabled, you can iterate on `search_prompt.txt` and `notifications.py` for free!

### "I want to test with NEW reports"

If you need fresh results:

**Solution:** Disable both cache modes:
```bash
CACHE_MODE=false
REPLAY_MODE=false
```
This will cost $3-5 for a new API call.

---

## 📞 Need Help?

1. Check logs in Railway Dashboard
2. Download and review the actual report file
3. Verify SendGrid Activity Feed
4. Check Slack channel for any error messages

**Remember:** With CACHE_MODE, you can iterate and fix issues for FREE! 🎉
