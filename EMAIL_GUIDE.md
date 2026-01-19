# Email Configuration Guide

## Don't Want to Use Gmail? No Problem!

The AI Report Scanner works perfectly fine **without email**. Reports are always saved locally to the `reports/` folder.

---

## Option 1: No Email (Simplest) ✅ RECOMMENDED

**Just leave email settings blank and use local files:**

1. Don't set `SENDER_EMAIL`, `RECIPIENT_EMAIL`, or `EMAIL_PASSWORD` in `.env`
2. Run the scanner normally
3. Find your reports in `reports/` folder
4. Open them in any text editor or markdown viewer

**Advantages:**
- ✅ No setup required
- ✅ No passwords needed
- ✅ Works offline
- ✅ Full control over files
- ✅ Easy to share via any method you want

---

## Option 2: Gmail with App Password

If you DO want email, Gmail is the easiest but requires an "App Password" (not your regular password).

### What is a Gmail App Password?

It's a 16-character password Google generates specifically for apps. Your real password stays secure.

### Steps:

1. **Enable 2-Factor Authentication first** (required)
   - Go to: https://myaccount.google.com/security
   - Turn on 2-Step Verification

2. **Generate App Password**
   - Same page → "App passwords"
   - Select "Mail" and "Other (Custom name)"
   - Type: "AI Report Scanner"
   - Copy the 16-character password

3. **Add to .env file:**
   ```bash
   SENDER_EMAIL=your-email@gmail.com
   RECIPIENT_EMAIL=your-email@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop  # The 16-char app password
   ```

**Advantages:**
- ✅ Automatic delivery
- ✅ Email archive
- ✅ Mobile access

**Disadvantages:**
- ⚠️ Requires 2FA setup
- ⚠️ Gmail-specific password management

---

## Option 3: Other Email Services

### Outlook/Office 365

```bash
SENDER_EMAIL=your-email@outlook.com
RECIPIENT_EMAIL=your-email@outlook.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Yahoo Mail

```bash
SENDER_EMAIL=your-email@yahoo.com
RECIPIENT_EMAIL=your-email@yahoo.com
EMAIL_PASSWORD=your_app_password  # Generate at account.yahoo.com
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

### ProtonMail

```bash
SENDER_EMAIL=your-email@protonmail.com
RECIPIENT_EMAIL=your-email@protonmail.com
EMAIL_PASSWORD=your_bridge_password  # Requires ProtonMail Bridge
SMTP_SERVER=127.0.0.1
SMTP_PORT=1025
```

### Custom SMTP Server

```bash
SENDER_EMAIL=you@yourdomain.com
RECIPIENT_EMAIL=you@yourdomain.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
```

---

## Option 4: Slack Instead of Email

Don't like email at all? Use Slack!

### Setup:

1. **Create Slack Bot**
   - Go to: https://api.slack.com/apps
   - Click "Create New App"
   - Choose "From scratch"
   - Name it "AI Report Scanner"

2. **Add Permissions**
   - OAuth & Permissions
   - Add scope: `chat:write`
   - Install to workspace

3. **Get Token**
   - Copy "Bot User OAuth Token" (starts with `xoxb-`)

4. **Configure .env:**
   ```bash
   SLACK_TOKEN=xoxb-your-token-here
   SLACK_CHANNEL=#ai-reports
   ```

**Advantages:**
- ✅ Team sharing
- ✅ Threading/discussions
- ✅ Mobile notifications
- ✅ No email passwords

---

## Option 5: File-Based Workflows

### A. Automatic File Sync

**Dropbox/Google Drive:**
```bash
# After running scanner, copy to cloud folder
cp reports/reading_list_*.md ~/Dropbox/AI-Reports/
```

**Add to cron-script.sh:**
```bash
python main.py && cp reports/reading_list_*.md ~/Dropbox/AI-Reports/
```

### B. Git Repository Archive

```bash
# Auto-commit reports to Git
git add reports/
git commit -m "Weekly report $(date +%Y-%m-%d)"
git push
```

### C. Notion Integration

Use Notion's email-to-page feature:
1. Get your Notion email address
2. Forward reports via email
3. Or use Notion API (more complex)

---

## Recommended Setup by Use Case

### Solo User, Local Machine
**Best:** No email, just use local files
```bash
# Don't set email variables
# Check reports/ folder weekly
```

### Solo User, Remote Server
**Best:** Email or Slack
```bash
# Email to yourself
# Or Slack DM to yourself
```

### Team/Organization
**Best:** Slack channel
```bash
# Shared #ai-reports channel
# Everyone gets updates
```

### Government/High Security
**Best:** No email, file-based with encrypted storage
```bash
# Save to encrypted directory
# Manual distribution via secure channels
```

---

## Troubleshooting Email

### "SMTP Authentication Failed"

**Gmail:**
- Check 2FA is enabled
- Verify app password (not regular password)
- Check for typos in password

**Other providers:**
- Verify SMTP server address
- Check port number (usually 587 or 465)
- Some providers block automated emails

### "Connection Refused"

- Firewall blocking SMTP ports
- Incorrect SMTP_SERVER setting
- Network issues

### "SSL Certificate Error"

- Update Python's SSL certificates
- Some corporate networks intercept SSL

---

## Testing Email Configuration

Before running full scan, test email:

```python
python -c "
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Test from AI Report Scanner')
msg['Subject'] = 'Test Email'
msg['From'] = 'your-email@gmail.com'
msg['To'] = 'your-email@gmail.com'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login('your-email@gmail.com', 'your-app-password')
server.send_message(msg)
server.quit()

print('✅ Email sent successfully!')
"
```

---

## FAQ

**Q: Is email required?**
A: No! Reports are always saved locally to `reports/` folder.

**Q: Can I use my regular Gmail password?**
A: No, you must use an App Password (16 characters from Google).

**Q: Why not support attachments in Slack?**
A: Slack API requires different scopes. We send formatted text instead.

**Q: Can I send to multiple recipients?**
A: Set `RECIPIENT_EMAIL=person1@example.com,person2@example.com`

**Q: How do I disable email after setting it up?**
A: Comment out lines in `.env`:
```bash
# SENDER_EMAIL=...
# RECIPIENT_EMAIL=...
# EMAIL_PASSWORD=...
```

**Q: Will my email password be exposed in logs?**
A: No, passwords are never logged.

---

## Recommended: Start Without Email

**For first-time users, we recommend:**

1. ✅ Skip email configuration entirely
2. ✅ Run scanner with `DRY_RUN=false`
3. ✅ Check `reports/` folder for output
4. ✅ Read the markdown files locally
5. ✅ Decide later if you want email

This way you can test the scanner without any email complexity!

---

## Quick Reference

```bash
# .env file examples

# NO EMAIL (recommended for testing)
ANTHROPIC_API_KEY=sk-ant-...
# Leave other fields blank or commented

# WITH GMAIL
ANTHROPIC_API_KEY=sk-ant-...
SENDER_EMAIL=you@gmail.com
RECIPIENT_EMAIL=you@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop  # 16-char app password

# WITH SLACK INSTEAD
ANTHROPIC_API_KEY=sk-ant-...
SLACK_TOKEN=xoxb-...
SLACK_CHANNEL=#ai-reports

# WITH BOTH
ANTHROPIC_API_KEY=sk-ant-...
SENDER_EMAIL=you@gmail.com
RECIPIENT_EMAIL=you@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
SLACK_TOKEN=xoxb-...
SLACK_CHANNEL=#ai-reports
```

---

**Bottom line: Email is 100% optional. Use local files, Slack, or any distribution method you prefer!**
