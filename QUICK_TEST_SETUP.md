# 🚀 Quick Test & Setup Guide

**Goal**: Test the monthly scanner, iterate on quality, then deploy to Railway

**Time**: 30-45 minutes
**Cost**: £3-5 for initial test

---

## 📱 Step 1: Set Up for Testing (5 minutes)

### A. If Testing Locally

```bash
# 1. Make sure you have latest code
git pull origin claude/automated-report-curator-SigTE

# 2. Install dependencies (if not done)
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Edit .env with your API key
nano .env
# Add: ANTHROPIC_API_KEY=your_key_here
# Leave email/slack blank for now
```

### B. If Testing on Railway

```bash
# 1. Make sure Railway has latest code
# (It auto-deploys from GitHub, or manually redeploy)

# 2. Check Railway variables:
ANTHROPIC_API_KEY=your_key_here
SEARCH_DAYS_BACK=30
MAX_REPORTS=15
```

---

## 🧪 Step 2: Run Initial Test with Cache (£3-5 cost)

This runs a real monthly scan and saves results for free iteration.

### Locally:

```bash
# Edit .env
CACHE_MODE=true
REPLAY_MODE=false

# Run scanner
python main.py
```

### Railway:

```bash
# Add to Railway variables:
CACHE_MODE=true
REPLAY_MODE=false

# Trigger manual run:
railway run python main.py

# Or click "Redeploy" in Railway dashboard
```

**Wait 5-10 minutes** for completion.

---

## 📊 Step 3: Review Results (10 minutes)

### Check Output Files:

**Locally:**
```bash
# Reading list
cat reports/reading_list_*.md

# Check report count
grep "## 🔥 CRITICAL" reports/reading_list_*.md
grep "## 📊 HIGH" reports/reading_list_*.md

# View in browser
open reports/reading_list_*.md
```

**Railway:**
```bash
# View reports
railway run ls reports/
railway run cat reports/reading_list_*.md

# Or download
railway run cat reports/reading_list_*.md > monthly_report.md
open monthly_report.md
```

### Quality Checklist:

Ask yourself:
- [ ] Are there 10-15 reports (not 25+)?
- [ ] Are all reports from past 30 days?
- [ ] Are all reports truly significant?
- [ ] Would I reference these in senior meetings?
- [ ] Is there good source diversity (labs, gov, think tanks)?
- [ ] Is the synthesis insightful?

---

## 🔧 Step 4: Adjust Quality Criteria (FREE iterations)

If reports aren't quite right, adjust the selection criteria:

### A. Too Many Reports (>20)

**Edit `search_prompt.txt`:**

```markdown
## QUALITY FILTERS

### ✅ INCLUDE ONLY if report:
2. Substantial and significant (40+ pages instead of 30+)
```

Or increase strictness:
```markdown
6. **Would be discussed in Cabinet meetings** (higher bar)
```

### B. Too Few Reports (<8)

**Edit `search_prompt.txt`:**

```markdown
## QUALITY FILTERS

### ✅ INCLUDE ONLY if report:
2. Substantial and significant (20+ pages instead of 30+)
```

Or relax criteria slightly:
```markdown
6. **Would be discussed in DG or ministerial meetings**
```

### C. Wrong Type of Reports

**Adjust priority definitions:**

```markdown
### 🔥 **CRITICAL** - Must Read This Month (aim for 3-5 reports)
- [Add or remove criteria based on what you want]
```

---

## 🔄 Step 5: Test Changes for FREE

After editing `search_prompt.txt`:

```bash
# Switch to replay mode
CACHE_MODE=false
REPLAY_MODE=true

# Run again (FREE - uses cached search results)
python main.py
```

**Check results again**. Repeat steps 4-5 until satisfied.

---

## ✅ Step 6: Deploy to Production

Once happy with quality:

### A. Update Railway Variables

```bash
# Production settings
CACHE_MODE=false
REPLAY_MODE=false
SEARCH_DAYS_BACK=30
MAX_REPORTS=15

# Make sure these are set:
ANTHROPIC_API_KEY=your_key
SLACK_TOKEN=xoxb-your-real-token  # Not placeholder!
SLACK_CHANNEL=#ai-reports
```

### B. Confirm Cron Schedule

Railway should already have:
```toml
schedule = "0 9 1 * *"  # 1st of each month at 9 AM
```

### C. Test Production Run

```bash
# Manually trigger to test
railway run python main.py

# Check Slack #ai-reports channel
# Should see high-quality monthly digest
```

---

## 📅 Step 7: Monitor First Month

After deployment:

### 1st of Next Month:
- Check Slack at 9 AM for automatic digest
- Review report quality
- Note any adjustments needed

### During Month:
- Track which reports you actually read
- Note if anything critical was missed
- Consider if 10-15 is right number

### End of Month:
- Review usefulness
- Adjust criteria if needed
- Re-cache and test adjustments

---

## 🎯 Expected Results

### Successful Monthly Setup:

**What you should see:**

1. **Critical Section (3-5 reports)**
   - Major announcements from frontier labs
   - Significant government policy reports
   - Cross-government strategic documents

2. **High Priority (5-8 reports)**
   - Leading think tank comprehensive analysis
   - Major consultancy research with evidence
   - International governance developments

3. **Medium (2-3 reports, if any)**
   - Only truly exceptional additional reports
   - Clear policy implications
   - International exemplars worth studying

4. **Total: 10-16 reports**
   - All highly relevant
   - All from authoritative sources
   - All merit senior-level discussion

5. **Synthesis Section**
   - 3-5 major monthly themes
   - Strategic insights
   - Cross-cutting analysis
   - Action items

### Red Flags:

🚩 **More than 20 reports** → Criteria too loose
🚩 **Routine/incremental reports** → Need stricter filters
🚩 **Reports you skip** → Wrong relevance criteria
🚩 **Missing major developments** → Searches too narrow

---

## 💡 Pro Tips

### Tip 1: Test Multiple Months

```bash
# Cache different months
CACHE_FILE=cache/january.json CACHE_MODE=true python main.py
CACHE_FILE=cache/february.json CACHE_MODE=true python main.py

# Test criteria against both
CACHE_FILE=cache/january.json REPLAY_MODE=true python main.py
CACHE_FILE=cache/february.json REPLAY_MODE=true python main.py
```

**Cost**: £6-10 for 2 months
**Benefit**: Test criteria robustness across different months

### Tip 2: A/B Test Selection Criteria

```bash
# Test strict criteria
# Edit search_prompt.txt (strict version)
REPLAY_MODE=true python main.py
cp reports/reading_list_*.md reports/strict_version.md

# Test loose criteria
# Edit search_prompt.txt (loose version)
REPLAY_MODE=true python main.py
cp reports/reading_list_*.md reports/loose_version.md

# Compare
diff reports/strict_version.md reports/loose_version.md
```

### Tip 3: Track Quality Over Time

```bash
# Create tracking file
echo "Month | Reports | Critical | High | Quality (1-5) | Notes" > quality_tracking.md
echo "------|---------|----------|------|---------------|------" >> quality_tracking.md

# After each month, add row:
echo "Jan 2024 | 14 | 4 | 8 | 4.5 | Good balance, one routine report" >> quality_tracking.md
```

---

## ⚡ Quick Reference Commands

### Local Testing

```bash
# Initial test (costs £3-5)
CACHE_MODE=true REPLAY_MODE=false python main.py

# Iterate on criteria (FREE)
CACHE_MODE=false REPLAY_MODE=true python main.py

# View results
cat reports/reading_list_*.md
```

### Railway Testing

```bash
# Initial test
railway run python main.py

# View results
railway run cat reports/reading_list_*.md > report.md

# Check logs
railway logs
```

### Edit Criteria

```bash
# Open prompt
nano search_prompt.txt

# Key sections to adjust:
# - QUALITY FILTERS (lines 66-90)
# - RELEVANCE SCORING (lines 100-130)
# - SELECTION CRITERIA (line 7)
```

---

## 🐛 Troubleshooting

### "Report is empty or useless"

**Likely cause**: Web search not working

**Solution**: Check that web_search fix is applied:
```python
# In scanner.py, should have:
tools=[{
    "type": "web_search_20250305",
    "name": "web_search"
}]
```

### "Too many/few reports"

**Solution**: Adjust MAX_REPORTS or quality filters

```bash
# Try different values
MAX_REPORTS=10   # Fewer
MAX_REPORTS=20   # More

# Or adjust in search_prompt.txt
```

### "Cache not found in replay mode"

**Solution**: Run with cache mode first

```bash
# Must cache before replay
CACHE_MODE=true python main.py
# Then can use replay
REPLAY_MODE=true python main.py
```

### "Slack not receiving reports"

**Solution**: Check token is real (not placeholder)

```bash
# Token should be long:
SLACK_TOKEN=xoxb-1234567890123-1234567890123-abcdefg...

# Not placeholder:
SLACK_TOKEN=xoxb-your-slack-bot-token  # ❌ Won't work
```

---

## ✅ Success Checklist

Before considering setup complete:

- [ ] Ran initial test successfully
- [ ] Reviewed and approved report quality
- [ ] Tested iteration with replay mode
- [ ] Adjusted criteria to satisfaction
- [ ] Deployed to Railway
- [ ] Confirmed Slack is working
- [ ] Verified cron schedule (1st of month)
- [ ] Documented any custom criteria choices

---

## 📞 Getting Help

**If stuck:**

1. Check the specific guide:
   - [TESTING_GUIDE.md](TESTING_GUIDE.md) - Cache/replay help
   - [MONTHLY_GUIDE.md](MONTHLY_GUIDE.md) - Monthly scanning details
   - [RAILWAY_EMAIL_FIX.md](RAILWAY_EMAIL_FIX.md) - Slack setup

2. Check Railway logs:
   ```bash
   railway logs
   ```

3. Enable debug mode:
   ```bash
   LOG_LEVEL=DEBUG python main.py
   ```

---

## 🎉 You're Done!

**Once you complete these steps:**

✅ Monthly scanner configured and tested
✅ Quality criteria adjusted to your needs
✅ Railway running automatic monthly scans
✅ Slack delivering high-quality reports
✅ Costing only £3-5/month (75% savings!)

**Next monthly scan**: 1st of next month at 9 AM
**What you'll get**: 10-15 exceptional reports, curated from 30-day search
**Your time saved**: 3-4 hours of manual curation per month

**Enjoy your automated, cost-effective AI intelligence briefing! 🚀**
