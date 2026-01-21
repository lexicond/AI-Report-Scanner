# 🔧 Deployment Fixes Applied

## Issues Fixed

### 1. ❌ KeyError: 'date' - FIXED ✅

**Problem:** The search_prompt.txt template had `{date}` placeholders that Python's `.format()` method tried to replace, but also had placeholders meant for Claude (like `{count}`, `{Title}`) which caused conflicts.

**Solution:** Changed from `.format()` to string `.replace()` method which only replaces our specific date placeholders and leaves Claude's placeholders intact.

**Files Changed:**
- `scanner.py` line 77-88: Updated `_format_prompt()` method
- `tests/test_scanner.py` line 68-86: Updated tests to verify fix

### 2. ❌ Gmail Confusion - FIXED ✅

**Problem:** Email appeared required, but Gmail setup is complex (app passwords, 2FA).

**Solution:** Made email **completely optional**. Reports are always saved locally. Email is just for automatic delivery.

**Files Changed:**
- `.env.example`: Commented out email by default, clear REQUIRED vs OPTIONAL sections
- `main.py`: Better messaging about email being optional
- `README.md`: Prominent notes that email is optional
- **NEW:** `EMAIL_GUIDE.md` - Complete guide to email alternatives

---

## How to Deploy (Updated)

### Option 1: No Email (Simplest) ✅ RECOMMENDED

1. **Set only your API key in Railway:**
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

2. **Deploy - that's it!**

3. **Access reports:**
   - Railway logs will show when scan completes
   - Download reports from Railway's file browser
   - Or use Railway CLI: `railway run cat reports/reading_list_*.md`

### Option 2: With Email (If You Want It)

Only add email if you specifically want automatic delivery:

1. **Get Gmail App Password:**
   - Enable 2FA: https://myaccount.google.com/security
   - Generate App Password: Security → App passwords
   - Copy the 16-character password

2. **Set in Railway environment:**
   ```
   ANTHROPIC_API_KEY=your_key_here
   SENDER_EMAIL=you@gmail.com
   RECIPIENT_EMAIL=you@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop
   ```

3. **Deploy**

### Option 3: With Slack (Best for Teams)

1. **Create Slack Bot:**
   - https://api.slack.com/apps
   - "Create New App" → "From scratch"
   - Add `chat:write` scope
   - Install to workspace

2. **Set in Railway:**
   ```
   ANTHROPIC_API_KEY=your_key_here
   SLACK_TOKEN=xoxb-your-token
   SLACK_CHANNEL=#ai-reports
   ```

3. **Deploy**

---

## Testing the Fix

### Test Locally First:

```bash
# 1. Pull latest changes
git pull origin claude/automated-report-curator-SigTE

# 2. Set only API key (no email)
cp .env.example .env
# Edit .env:
#   ANTHROPIC_API_KEY=your_key_here
#   Leave email lines commented out

# 3. Test run
python main.py

# 4. Check output
cat reports/reading_list_*.md
```

**Expected output:**
```
======================================================================
🤖 AI Report Scanner - Monthly Government AI Report Curation
======================================================================

Configuration loaded successfully
Mode: PRODUCTION
Search period: Last 30 days

🔍 Searching for reports...
This may take a few minutes...

✅ Report generated successfully!

📊 Report Summary:
   Generated: 2024-01-19
   Model: claude-sonnet-4-20250514
   Input tokens: 2,500
   Output tokens: 8,500

💾 Output files saved to:
   📄 Reading List: reports/reading_list_2024-01-19.md
   🎙️  NotebookLM: reports/notebooklm_2024-01-19.md
   Metadata: output/metadata_2024-01-19.json

ℹ️  Email not configured - reports saved locally to reports/ folder
   To enable email: Set SENDER_EMAIL, RECIPIENT_EMAIL, EMAIL_PASSWORD
   Alternative: Check reports/ folder for markdown files

======================================================================
✅ AI Report Scanner completed successfully!
======================================================================

📁 Your reports are ready:
   📄 Reading List: reports/reading_list_2024-01-19.md
   🎙️  NotebookLM: reports/notebooklm_2024-01-19.md

Next steps:
1. Open reports/ folder to read your curated report
2. Upload notebooklm_*.md to NotebookLM for audio summary
3. Optional: Configure email to receive automatic delivery
```

---

## Railway Deployment (Updated)

### Via Railway Dashboard:

1. **Go to your Railway project**

2. **Update Environment Variables:**
   - Remove `SENDER_EMAIL`, `RECIPIENT_EMAIL`, `EMAIL_PASSWORD` if you don't want email
   - Or update them with correct values if you do

3. **Redeploy:**
   - Settings → "Redeploy"
   - Or: Automatic redeploy if connected to Git

4. **Check Logs:**
   - View Logs tab
   - Should see "Report generated successfully"
   - Look for "reports saved locally" message

### Via Railway CLI:

```bash
# 1. Update to latest code
git pull origin claude/automated-report-curator-SigTE

# 2. Set variables (only API key required)
railway variables set ANTHROPIC_API_KEY=your_key_here

# Optional: Remove email variables
railway variables delete SENDER_EMAIL
railway variables delete RECIPIENT_EMAIL
railway variables delete EMAIL_PASSWORD

# 3. Deploy
railway up

# 4. Check logs
railway logs

# 5. Download reports (once run completes)
railway run ls reports/
railway run cat reports/reading_list_*.md > latest_report.md
```

---

## Verifying the Fix

### Check 1: No More KeyError

Old error in logs:
```
KeyError: 'date'
```

✅ Should be gone now!

### Check 2: Works Without Email

Old behavior:
- Crashed or complained if email not set

New behavior:
- ✅ Works perfectly without email
- ✅ Clear message: "reports saved locally"
- ✅ Shows file paths

### Check 3: Template Variables

Test the template formatting:
```python
# This should work now
python -c "
from scanner import ReportScanner
from config import get_settings

settings = get_settings()
scanner = ReportScanner(settings)

# This would have failed before
template = 'Week of {date}, Count: {count}'
result = scanner._format_prompt(template, '2024-01-19', '2024-01-12', '2024-01-19')

print('✅ Template formatted successfully!')
print(result)
assert '{date}' not in result  # Our placeholder replaced
assert '{count}' in result     # Claude's placeholder preserved
"
```

---

## FAQ

**Q: Do I need to reconfigure anything?**
A: No! If you already had it working, nothing changes. If you had the KeyError, just redeploy with latest code.

**Q: I don't want email. What do I do?**
A: Just remove/comment the email variables in Railway. That's it!

**Q: I want email. How do I set it up properly?**
A: See [EMAIL_GUIDE.md](EMAIL_GUIDE.md) for detailed instructions. Gmail requires an "app password" (not your regular password).

**Q: Can I test without using my API credits?**
A: Yes! Set `DRY_RUN=true` in environment variables. It generates a mock report without calling the API.

**Q: Where are reports saved in Railway?**
A: In the `reports/` folder in your Railway container. Download via CLI or logs.

**Q: Can I use other email providers?**
A: Yes! See [EMAIL_GUIDE.md](EMAIL_GUIDE.md) for Outlook, Yahoo, ProtonMail, and custom SMTP.

**Q: Should I use email or Slack?**
A:
- Solo user: Local files (no email needed)
- Want mobile access: Email
- Team sharing: Slack
- High security: Local files only

---

## Support

**Still having issues?**

1. **Check Railway logs:**
   - Logs tab in Railway dashboard
   - Look for the exact error message

2. **Test locally first:**
   ```bash
   git pull origin claude/automated-report-curator-SigTE
   python main.py
   ```

3. **Enable debug logging:**
   ```bash
   LOG_LEVEL=DEBUG python main.py
   ```

4. **Check files:**
   - Is `search_prompt.txt` present?
   - Is `.env` configured?
   - Are directories created?

5. **Open GitHub issue:**
   - Include error logs
   - Mention Railway or local deployment
   - Describe what you tried

---

## Summary of Changes

```diff
# scanner.py
- return template.format(...)  # Old way - conflicts with Claude placeholders
+ return template.replace(...)  # New way - only replaces our variables

# .env.example
- SENDER_EMAIL=your-email@gmail.com  # Required-looking
+ #SENDER_EMAIL=your-email@gmail.com  # Clearly optional

# main.py
- print("Email not configured")  # Confusing
+ print("Email not configured - reports saved locally")  # Clear

# NEW: EMAIL_GUIDE.md
Complete guide to:
- Using without email (recommended)
- Gmail app password setup
- Alternative email providers
- Slack integration
- File-based workflows
```

---

**✅ Both issues are now fixed. Email is optional, and the template formatting works correctly!**

Deploy with confidence! 🚀
