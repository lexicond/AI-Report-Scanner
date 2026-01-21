# 📱 iPhone Setup Guide for AI Report Scanner

**Complete step-by-step guide to set up your automated monthly AI report curator on iPhone**

This guide will help you set up the AI Report Scanner entirely from your iPhone. No computer required! ✨

---

## 📋 What You'll Need

- ✅ iPhone with iOS 14 or later
- ✅ Internet connection
- ✅ Gmail account (for receiving reports)
- ✅ Anthropic API key (we'll show you how to get one)
- ✅ Railway account (free tier available)
- ✅ 30-45 minutes

---

## 🎯 What You'll Get

On the 1st of each month at 9 AM, you'll automatically receive:

1. **📧 Email digest** with curated AI & government reports
2. **📄 Reading list** organized by priority (Critical/High/Medium)
3. **🎙️ NotebookLM source** ready for AI podcast generation
4. **📊 Monthly synthesis** with key themes and insights

---

## Step 1️⃣: Get Your Anthropic API Key

### On iPhone Safari:

1. **Open Safari** and go to: `https://console.anthropic.com`

2. **Create account or log in**
   - Tap "Sign Up" if new
   - Or "Log In" if you have an account

3. **Navigate to API Keys**
   - Tap menu icon (☰) in top right
   - Select "API Keys"

4. **Create new key**
   - Tap "+ Create Key"
   - Name it: "AI Report Scanner"
   - Tap "Create"

5. **Copy your API key**
   - Tap the key to select all
   - Tap "Copy"
   - **⚠️ IMPORTANT**: Save this somewhere safe! You'll need it later.

   **💡 Tip**: Paste it in Notes app temporarily:
   ```
   Open Notes → New Note → Paste → Title it "API Keys"
   ```

### Pricing Info:
- Claude Sonnet 4: ~£3-5 per monthly report
- Free credits available for new accounts
- Reports run monthly, so ~£3-5/month (75% cheaper than weekly!)

---

## Step 2️⃣: Set Up Gmail App Password

You need this so the app can send you emails.

### On iPhone Safari:

1. **Go to Google Account Settings**
   - Open Safari: `https://myaccount.google.com`
   - Sign in to your Gmail account

2. **Navigate to Security**
   - Scroll down to "Security"
   - Tap "2-Step Verification"
   - **If not enabled**: Enable it first (required for app passwords)

3. **Create App Password**
   - Go back to Security
   - Scroll to "App passwords"
   - Tap "App passwords"

4. **Generate password**
   - Select app: "Mail"
   - Select device: "Other"
   - Type: "AI Report Scanner"
   - Tap "Generate"

5. **Copy the 16-character password**
   - It looks like: `abcd efgh ijkl mnop`
   - Copy it (remove spaces)
   - **Save in Notes** with your API key

---

## Step 3️⃣: Set Up Railway (Where the App Runs)

### On iPhone Safari:

1. **Go to Railway**
   - Open Safari: `https://railway.app`

2. **Sign Up**
   - Tap "Start a New Project"
   - Sign up with GitHub (recommended)
   - Or use email

3. **Verify account**
   - Check your email
   - Tap verification link

4. **Add payment method (for free trial)**
   - Railway requires a card for free $5 credit
   - Go to Account Settings
   - Add card (you won't be charged unless you exceed free tier)

---

## Step 4️⃣: Deploy to Railway

### Option A: Using Railway Mobile

1. **Install Railway CLI (via working-copy.app)**

   Actually, Railway's web interface is easier on iPhone! Continue to Option B.

### Option B: Using Railway Web Dashboard ✅ RECOMMENDED

1. **Open Railway Dashboard**
   - Safari: `https://railway.app/dashboard`

2. **Create New Project**
   - Tap "+ New Project"
   - Select "Deploy from GitHub repo"

3. **Connect GitHub**
   - Tap "Connect GitHub"
   - Authorize Railway

4. **Fork the Repository First**

   You need to fork the repo to your GitHub account:

   a. **Go to the original repository**
      - Safari: `https://github.com/YOUR_USERNAME/AI-Report-Scanner`
      - Or wherever this code is hosted

   b. **Fork it**
      - Tap the "Fork" button (top right)
      - Wait for fork to complete

   c. **Go back to Railway**
      - Select your forked repository
      - Select branch: `main`

5. **Configure Environment Variables**

   Tap "Variables" tab and add these one by one:

   ```
   ANTHROPIC_API_KEY=your_key_from_step_1
   SENDER_EMAIL=your-gmail@gmail.com
   RECIPIENT_EMAIL=your-email@example.com
   EMAIL_PASSWORD=your_app_password_from_step_2
   LOG_LEVEL=INFO
   DRY_RUN=false
   ```

   **💡 How to add each variable:**
   - Tap "+ New Variable"
   - Type variable name (e.g., `ANTHROPIC_API_KEY`)
   - Tap "Value" field
   - Paste value
   - Tap "Add"
   - Repeat for each variable

6. **Deploy**
   - Tap "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - You'll see "Success ✓" when done

7. **Set Up Cron Schedule**

   - In your project, tap "Settings"
   - Scroll to "Cron"
   - Tap "Add Cron Job"
   - Enter: `0 9 * * MON` (every Monday 9 AM)
   - Tap "Add"

---

## Step 5️⃣: Test Your Setup

### Run Manually First:

1. **In Railway Dashboard**
   - Go to your project
   - Tap "Deployments"
   - Tap latest deployment
   - Tap "View Logs"

2. **Trigger Manual Run**
   - Tap "⋮" (three dots)
   - Select "Redeploy"
   - Watch logs in real-time

3. **Check Your Email**
   - Should receive email within 5-10 minutes
   - Check spam folder if not received

---

## Step 6️⃣: Using the Reports

### Reading the Weekly Digest:

1. **Open Email on iPhone**
   - Look for: "📊 Weekly AI Reports Digest"
   - Opens in Mail app

2. **Navigate by Priority**
   - 🔥 **CRITICAL**: Read immediately
   - 📊 **HIGH**: Read this week
   - 📚 **MEDIUM**: Read when time allows

3. **Tap Links to Read Reports**
   - Links open in Safari
   - Can save to Reading List
   - Or save to Notion/Notes

### Using NotebookLM for Audio:

1. **Download NotebookLM Attachment**
   - Open email
   - Tap the `notebooklm_*.md` attachment
   - Tap share icon
   - Save to Files app

2. **Go to NotebookLM**
   - Safari: `https://notebooklm.google.com`
   - Sign in with Google

3. **Create New Notebook**
   - Tap "+ New"
   - Tap "Upload"

4. **Upload the File**
   - Browse to Files app
   - Select the notebooklm file
   - Tap "Upload"

5. **Generate Audio Overview**
   - Tap "Audio Overview" button
   - Wait 2-3 minutes
   - Tap "Play" to listen

6. **Listen On-The-Go**
   - Download the audio
   - Play in Podcasts app
   - Or listen while commuting

---

## 🔍 Troubleshooting

### "No email received"

**Check these:**

1. **Look in Spam folder**
   - Open Gmail app
   - Menu → Spam
   - Mark as "Not Spam" if found

2. **Verify environment variables**
   - Railway Dashboard → Variables
   - Make sure all are set correctly
   - No typos in email addresses

3. **Check Railway logs**
   - Railway Dashboard → Deployments → View Logs
   - Look for errors in red

4. **Verify Gmail app password**
   - Must be 16 characters
   - No spaces
   - Generated from Google Account settings

### "API Error" in logs

**Possible issues:**

1. **Invalid API key**
   - Verify key is copied correctly
   - No extra spaces
   - Not expired

2. **Insufficient credits**
   - Check Anthropic Console
   - Add payment method if needed

3. **Rate limits**
   - Wait 5 minutes
   - Try again

### "Build failed" on Railway

**Try these:**

1. **Check repository structure**
   - Make sure all files are committed
   - Especially `requirements.txt`

2. **Redeploy**
   - Railway Dashboard
   - Tap "Redeploy"

3. **Check Python version**
   - Railway uses Python 3.11 by default
   - Our app is compatible

---

## 🎨 Customization Options

### Change Scan Frequency

In Railway Dashboard → Settings → Cron (current: monthly):

- **Monthly (default)**: `0 9 1 * *` - 1st of month at 9 AM
- **Weekly (more expensive)**: `0 9 * * MON` - Every Monday
- **Bi-weekly**: `0 9 1,15 * *` - 1st and 15th of month
- **Daily (not recommended)**: `0 9 * * *` - Every day

### Change Search Period

Add environment variable:
```
SEARCH_DAYS_BACK=14
```

For bi-weekly (14 days) instead of monthly (30 days).

### Add Slack Notifications

1. Create Slack Bot:
   - `https://api.slack.com/apps`
   - Create New App
   - Add Bot Token Scope: `chat:write`
   - Install to workspace

2. Add to Railway:
   ```
   SLACK_TOKEN=xoxb-your-token
   SLACK_CHANNEL=#ai-reports
   ```

### Change Priority Sources

Edit `search_prompt.txt` in repository:
- Add your preferred sources
- Remove less relevant ones
- Adjust search terms

---

## 📊 Understanding Your Reports

### Email Structure:

```
📊 Weekly AI Reports Digest - 2024-01-15

┌─────────────────────────┐
│  🔥 CRITICAL (3 reports)│  ← Read immediately
└─────────────────────────┘

┌─────────────────────────┐
│  📊 HIGH (7 reports)    │  ← Read this week
└─────────────────────────┘

┌─────────────────────────┐
│  📚 MEDIUM (12 reports) │  ← Read when time allows
└─────────────────────────┘

┌─────────────────────────┐
│  WEEKLY SYNTHESIS       │  ← Big picture insights
└─────────────────────────┘
```

### Each Report Includes:

- **Title** and **Source**
- **Publication Date**
- **Why Critical**: Why you should read it
- **Key Takeaways**: Main findings
- **Relevance**: How it relates to your work
- **Actionable Insights**: What to do with this info
- **Quote**: Memorable quote for briefings

---

## 🚀 Advanced: Using iPhone Shortcuts

### Create Shortcut to Check Latest Report:

1. **Open Shortcuts app**

2. **Create New Shortcut**
   - Tap "+"
   - Name it: "Check AI Reports"

3. **Add Actions**:
   ```
   1. Open URL: https://railway.app/project/YOUR_PROJECT_ID
   2. Wait 1 second
   3. Get Contents of URL
   4. Show Result
   ```

4. **Add to Home Screen**
   - Tap "⋮" → "Add to Home Screen"
   - Now one tap to check status!

---

## 💡 Tips for Maximum Value

### For Reading:

1. **Monday Morning Routine**
   - Coffee + Critical reports
   - 20-30 minutes
   - Note key quotes in Notes app

2. **Use Reading List**
   - Save report PDFs to Safari Reading List
   - Read offline during commute

3. **Share with Team**
   - Forward relevant reports
   - Add your commentary

### For NotebookLM Audio:

1. **Queue for Commute**
   - Download Monday morning
   - Listen on drive/train

2. **2x Speed**
   - NotebookLM audio works great at 1.5-2x
   - Saves time

3. **Take Notes**
   - Use Voice Memos for key insights
   - Review later

---

## 🔐 Security Best Practices

1. **Keep API Keys Secret**
   - Never share your keys
   - Don't commit to public repos
   - Store securely in Notes app

2. **Use Strong Password**
   - For Railway account
   - Enable 2FA

3. **Review Permissions**
   - Railway can only access your repo
   - Email can only send (not read)

4. **Monitor Usage**
   - Check Anthropic Console monthly
   - Railway free tier: $5/month

---

## 📞 Getting Help

### If stuck:

1. **Check logs first**
   - Railway Dashboard → Logs
   - Usually shows the issue

2. **Review this guide**
   - Most issues covered in Troubleshooting

3. **GitHub Issues**
   - Open issue in repository
   - Include error logs
   - Describe what you tried

4. **Railway Discord**
   - Active community
   - Fast responses

---

## 🎉 Success Checklist

Before you finish, verify:

- ✅ Anthropic API key working
- ✅ Gmail app password created
- ✅ Railway project deployed
- ✅ Cron schedule set (Monday 9 AM)
- ✅ Environment variables configured
- ✅ Test email received
- ✅ NotebookLM audio generated

**Congratulations! You're now receiving automated weekly AI report digests! 🎊**

---

## 📅 What Happens Next

### Every Monday:

1. **9:00 AM**: Scanner runs automatically
2. **9:05 AM**: AI analyzes reports (2-5 mins)
3. **9:10 AM**: Email sent to your inbox
4. **Your time**: Review and read reports

### Monthly Maintenance:

- **Check costs**: Anthropic Console + Railway
- **Update preferences**: Edit search_prompt.txt if needed
- **Review quality**: Are reports relevant?

---

## 🔄 Updating the System

### To modify search criteria:

1. **Edit in GitHub**
   - Open your forked repo
   - Navigate to `search_prompt.txt`
   - Tap "Edit" (pencil icon)
   - Make changes
   - Commit

2. **Railway auto-redeploys**
   - Watches for changes
   - Rebuilds automatically

---

## 💰 Cost Breakdown

### Monthly costs:

- **Anthropic API**: £3-5/month (1 monthly report)
  - £3-5 per monthly scan
  - Varies by number of reports found
  - 75% cheaper than weekly scanning!

- **Railway**: Free tier
  - $5 credit monthly
  - Usually sufficient for this app
  - Only pay if exceeded

- **Gmail**: Free
- **NotebookLM**: Free

**Total: ~£3-5/month** for automated curation that would take 3-4 hours manually!

---

## 🎯 ROI Calculation

### Time saved:

- **Manual search**: 3 hours/month
- **Reading scattered sources**: 1 hour/month
- **Organizing reports**: 30 mins/month

**Total saved: 4.5 hours/month**

At £50/hour value: **£225/month saved** for £3-5/month cost.

**ROI: 4,500-7,500%** 🚀 (Even better than weekly!)

---

## 📱 iPhone Productivity Tips

### Optimize for mobile:

1. **Use Safari Reader Mode**
   - Tap "AA" in address bar
   - Select "Show Reader"
   - Cleaner reading experience

2. **Save to Reading List**
   - Share → Add to Reading List
   - Syncs across devices

3. **Use Speak Screen**
   - Settings → Accessibility → Spoken Content
   - Enable "Speak Screen"
   - Two-finger swipe down to listen

4. **Set Reminders**
   - "Hey Siri, remind me to read AI reports Monday 10 AM"

---

## 🎓 Next Level Features

Once comfortable, try:

### 1. Notion Integration
- Forward emails to Notion
- Create automatic database

### 2. Multi-user Setup
- Deploy once
- Add multiple recipients
- Share across team

### 3. Custom RSS Feeds
- Add organization RSS feeds
- Faster than web search
- Edit scanner.py

### 4. Priority Alerts
- Critical reports → SMS
- High reports → Email
- Medium → Weekly digest

---

## ✅ You're All Set!

Your AI Report Scanner is now running on autopilot!

**Every Monday you'll get:**
- Curated report list
- Priority rankings
- Key insights
- Audio summary ready

**Enjoy your automated AI intelligence briefing! 🎉**

Questions? Check Troubleshooting section or GitHub Issues.

---

*Last updated: January 2024*
*Compatible with: iPhone iOS 14+, Railway v2, Anthropic Claude API*
