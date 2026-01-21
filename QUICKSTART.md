# ⚡ Quick Start Guide

**Get your AI Report Scanner running in 10 minutes**

## 🎯 Goal

By the end of this guide, you'll have:
- ✅ Scanner installed and configured
- ✅ Test report generated
- ✅ Email notifications working
- ✅ Ready for weekly automation

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Git installed (`git --version`)
- [ ] Anthropic API key ([Get one here](https://console.anthropic.com))
- [ ] Gmail account with 2FA enabled

⏱️ **Time required:** 10-15 minutes

---

## Step 1️⃣: Install (2 mins)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/AI-Report-Scanner.git
cd AI-Report-Scanner

# Install dependencies
pip install -r requirements.txt
```

**✅ Checkpoint:** Run `python -c "import anthropic"` - should have no errors

---

## Step 2️⃣: Get API Keys (3 mins)

### A. Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Click "API Keys" → "+ Create Key"
4. Copy the key (starts with `sk-ant-...`)

### B. Gmail App Password

1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not already)
3. Go to "App passwords"
4. Select "Mail" → "Other" → Name it "AI Report Scanner"
5. Copy the 16-character password

**✅ Checkpoint:** You have both keys saved somewhere safe

---

## Step 3️⃣: Configure (2 mins)

```bash
# Create .env file from template
cp .env.example .env

# Edit .env file (use nano, vim, or any text editor)
nano .env
```

**Update these values:**

```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
SENDER_EMAIL=your-email@gmail.com
RECIPIENT_EMAIL=your-email@gmail.com  # Can be same as sender
EMAIL_PASSWORD=your-16-char-app-password

# Keep these as-is for testing
LOG_LEVEL=INFO
DRY_RUN=true
SEARCH_DAYS_BACK=7
```

**💡 Tip:** Set `DRY_RUN=true` for first test (uses mock data, no API cost)

Save and exit (Ctrl+O, Enter, Ctrl+X in nano)

**✅ Checkpoint:** Run `cat .env` - should show your values

---

## Step 4️⃣: First Test Run (2 mins)

```bash
# Run in dry-run mode (uses mock data, no API calls)
python main.py
```

**Expected output:**

```
======================================================================
🤖 AI Report Scanner - Weekly Government AI Report Curation
======================================================================

🔍 Searching for reports...
This may take a few minutes...

✅ Report generated successfully!
✅ Report validation passed

📊 Report Summary:
   Generated: 2024-01-15
   Model: mock
   ...

💾 Output files saved to:
   Reading List: reports/reading_list_2024-01-15.md
   NotebookLM: reports/notebooklm_2024-01-15.md
   ...

ℹ️  Email not configured (running in dry-run mode)

======================================================================
✅ AI Report Scanner completed successfully!
======================================================================
```

**✅ Checkpoint:** Check `reports/` folder - should have .md files

---

## Step 5️⃣: Check Output (1 min)

```bash
# View the generated reading list
cat reports/reading_list_*.md
```

You should see a formatted report with:
- Critical reports section
- High priority reports
- Key takeaways and insights
- Weekly synthesis

**✅ Checkpoint:** Report looks good and formatted correctly

---

## Step 6️⃣: Real Run with API (2 mins)

Now let's do a real run that searches actual reports:

```bash
# Edit .env to disable dry-run
nano .env
# Change: DRY_RUN=false
# Save and exit

# Run scanner for real
python main.py
```

**This will:**
1. Call Claude API to search for real reports
2. Generate actual reading list from current sources
3. Send email to your configured address
4. Take 5-8 minutes to complete

**💰 Cost:** ~$3-5 for this run

**✅ Checkpoint:**
- Check your email inbox for the digest
- Check spam folder if not received
- Review the reports for quality

---

## Step 7️⃣: Schedule Weekly Automation (Optional)

### Option A: Railway (Easiest)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
./railway-deploy.sh

# Follow prompts to:
# 1. Login to Railway
# 2. Create new project
# 3. Set environment variables
# 4. Deploy
```

Railway will run automatically every Monday at 9 AM.

### Option B: Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 9 AM)
0 9 * * MON cd /path/to/AI-Report-Scanner && python main.py

# Save and exit
```

### Option C: Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly, Monday, 9:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\AI-Report-Scanner\main.py`
7. Start in: `C:\path\to\AI-Report-Scanner`

**✅ Checkpoint:** Test automation runs once manually

---

## 🎉 Success!

You now have:

✅ Working AI Report Scanner
✅ Automated weekly reports
✅ Email notifications
✅ NotebookLM-ready summaries

## 🔄 What Happens Next?

### Every Monday at 9 AM:

1. Scanner automatically runs
2. Searches 50+ sources for new AI reports
3. Claude analyzes and prioritizes them
4. You receive email digest
5. Files saved to `reports/` folder

### Your Weekly Routine:

1. **Monday 9:30 AM:** Check email for digest
2. **Monday 10:00 AM:** Read Critical reports (20-30 mins)
3. **During week:** Read High priority reports
4. **Optional:** Upload NotebookLM file for audio summary

## 📊 Understanding Your Reports

### Priority Levels:

- 🔥 **CRITICAL** → Read immediately (3-5 reports)
  - Major announcements
  - Policy changes
  - Urgent insights

- 📊 **HIGH** → Read this week (7-10 reports)
  - Important research
  - Government updates
  - Frontier lab developments

- 📚 **MEDIUM** → Read when time allows (10-15 reports)
  - Background research
  - International updates
  - Academic papers

### Each Report Includes:

```markdown
Report Title
Source | Date | Length
Direct Link

Why Critical: [Why you should read this]
Key Takeaways: [3-5 main points]
Relevance: [How it relates to your work]
Actionable Insights: [What to do with this info]
Quote: [Memorable quote for briefings]
```

## 🎙️ Using NotebookLM for Audio

Want to listen instead of read?

1. **Get the file:** `reports/notebooklm_*.md`
2. **Upload to NotebookLM:** https://notebooklm.google.com
3. **Generate Audio:** Click "Audio Overview"
4. **Listen:** Download or play in browser

Perfect for:
- Commuting
- Exercise
- Walking
- Background listening

## ⚙️ Customization

### Change search period:

```bash
# In .env
SEARCH_DAYS_BACK=14  # Last 14 days instead of 7
```

### Adjust max reports:

```bash
# In .env
MAX_REPORTS=50  # Include up to 50 reports
```

### Customize sources:

Edit `search_prompt.txt` to:
- Add your favorite sources
- Remove less relevant ones
- Adjust search terms
- Change priority criteria

### Add Slack notifications:

```bash
# In .env
SLACK_TOKEN=xoxb-your-token
SLACK_CHANNEL=#ai-reports
```

## 🔍 Monitoring & Maintenance

### Check logs:

```bash
# View latest log
cat logs/scanner_$(date +%Y%m%d).log

# Watch in real-time
tail -f logs/scanner_*.log
```

### Check costs:

```bash
# View metadata for token usage
cat output/metadata_*.json
```

### Update scanner:

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 💡 Tips & Tricks

### 1. Organize Reports

Create folders by week:

```bash
mkdir -p archives/week-$(date +%U)
mv reports/*.md archives/week-$(date +%U)/
```

### 2. Share with Team

Forward the email or:

```bash
# Upload to shared drive
cp reports/reading_list_*.md ~/Dropbox/AI-Reports/
```

### 3. Create Notion Database

Import reports to Notion:
1. Copy report content
2. Paste into Notion page
3. Use Notion's database view

### 4. Set Phone Reminder

"Hey Siri, remind me to check AI reports every Monday at 10 AM"

### 5. Quick Mobile Check

Add bookmark on phone:
- Railway Dashboard (to check if ran)
- Gmail (to read digest)
- NotebookLM (to generate audio)

## 🆘 Troubleshooting Quick Fixes

### "Command not found: python"

Try `python3` instead:

```bash
python3 main.py
```

### "Permission denied" on scripts

Make executable:

```bash
chmod +x railway-deploy.sh
chmod +x cron-script.sh
```

### "API error: Invalid key"

Check your key:

```bash
echo $ANTHROPIC_API_KEY
# Or
cat .env | grep ANTHROPIC_API_KEY
```

### "Email not received"

1. Check spam folder
2. Verify app password (not regular password)
3. Check logs: `cat logs/scanner_*.log`

### "No reports found"

- Could be slow news week
- Try increasing `SEARCH_DAYS_BACK=14`
- Check internet connection

## 📚 Next Steps

Ready for more?

1. **[Full Documentation](README.md)** - Complete feature guide
2. **[iPhone Setup](SETUP_IPHONE.md)** - Mobile deployment guide
3. **[Tests](tests/)** - Run test suite
4. **[Customization](search_prompt.txt)** - Modify search logic

## 🎯 Quick Commands Reference

```bash
# Run scanner
python main.py

# Run tests
pytest

# View latest report
cat reports/reading_list_*.md

# Check logs
tail logs/scanner_*.log

# Update scanner
git pull && pip install -r requirements.txt --upgrade
```

## 💬 Get Help

- 📖 Check [README.md](README.md)
- 🐛 Check [Issues](https://github.com/YOUR_USERNAME/AI-Report-Scanner/issues)
- 📧 Open new issue with error logs

---

**🎉 Congratulations! You're now a power user of AI Report Scanner!**

*Questions? Check the full [documentation](README.md) or [open an issue](https://github.com/YOUR_USERNAME/AI-Report-Scanner/issues).*
