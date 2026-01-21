# 📅 Monthly Scanning Guide

## Why Monthly Instead of Weekly?

**Cost Savings**: Monthly scanning reduces costs by **75%**

| Frequency | Runs/Month | Cost/Month | Annual Cost |
|-----------|------------|------------|-------------|
| **Weekly** | 4 | £12-20 | £144-240 |
| **Monthly** | 1 | £3-5 | £36-60 |
| **Savings** | -75% | **£9-15/month** | **£108-180/year** |

**Quality**: With monthly scanning, we focus on **best reports only**
- 10-15 exceptional reports vs 25+ mixed quality
- Higher signal-to-noise ratio
- More strategic focus

---

## What's Changed

### 1. Search Period
- **Before**: Last 7 days
- **After**: Last 30 days

### 2. Report Selection
- **Before**: 25 reports, varied quality
- **After**: 10-15 reports, highly selective

### 3. Schedule
- **Before**: Every Monday (4x per month)
- **After**: 1st of each month (1x per month)

### 4. Selection Criteria
**Much stricter quality filters:**
- Must be 30+ pages (vs 20+ pages for weekly)
- Only from highly authoritative sources
- Would be discussed in ministerial/DG meetings
- Cross-government relevance required
- Excludes routine/incremental reports

---

## Monthly Report Structure

### 🔥 CRITICAL (3-5 reports)
**"Would be emailed to Permanent Secretaries"**
- Major policy changes
- Frontier breakthroughs with government impact
- Cross-government strategic implications

### 📊 HIGH (5-8 reports)
**"Would be discussed in DG meetings"**
- Substantial transformation insights
- Major governance developments
- Leading think tank comprehensive analysis

### 📚 MEDIUM (2-3 reports maximum)
**"Exceptional only"**
- Only included if truly outstanding
- Clear policy implications
- International exemplars

### 📋 BACKGROUND
**Excluded from monthly digest**
- Monthly is high-signal only

---

## Testing Your Monthly Setup

### Step 1: Test with Cache Mode (Costs £3-5)

This tests monthly scanning with real data:

```bash
# Set monthly configuration
SEARCH_DAYS_BACK=30
MAX_REPORTS=15
CACHE_MODE=true
REPLAY_MODE=false

# Run scanner
python main.py
```

**What to check:**
- Reports cover 30-day period
- 10-15 high-quality reports (not 25+)
- Only truly significant reports included
- Good mix of sources (labs, government, think tanks)

### Step 2: Iterate on Quality Criteria (FREE)

Now fine-tune the selection criteria:

```bash
# Use cached results
CACHE_MODE=false
REPLAY_MODE=true

# Edit search_prompt.txt to adjust:
# - Priority thresholds
# - Selection criteria
# - Quality filters

# Test changes (free)
python main.py
```

### Step 3: Deploy to Railway

Once satisfied:

```bash
# Update Railway variables
SEARCH_DAYS_BACK=30
MAX_REPORTS=15
CACHE_MODE=false
REPLAY_MODE=false

# Cron schedule already set to monthly: 0 9 1 * *
```

---

## What to Expect

### Monthly Digest Size

**Typical monthly report:**
- 3-5 Critical reports
- 5-8 High priority reports
- 2-3 Medium reports (if exceptional)
- **Total: 10-16 reports**

### Content Quality

**Higher bar for inclusion:**
- All reports are significant
- Cross-government relevance
- Actionable insights
- Authoritative sources

### Monthly Synthesis

**More strategic focus:**
- Broader trends over the month
- Pattern identification
- Strategic implications
- Cross-cutting themes

---

## Adjusting Selectivity

### Too Few Reports (< 8)

If monthly scan finds too few reports, adjust in `search_prompt.txt`:

```markdown
## QUALITY FILTERS

### ✅ INCLUDE ONLY if report:
2. Substantial and significant (20+ pages instead of 30+)
```

### Too Many Reports (> 20)

If monthly scan finds too many reports, increase strictness:

```markdown
## QUALITY FILTERS

### ✅ INCLUDE ONLY if report:
2. Substantial and significant (40+ pages, or major policy announcement)
```

---

## Cost-Benefit Analysis

### Monthly Scanning

**Costs:**
- £3-5/month = £36-60/year
- 1 cache for testing = £3-5 one-time

**Benefits:**
- High-quality curated reports
- Strategic monthly view
- Still covers all major developments
- Better signal-to-noise ratio

**Time saved:**
- Still saves 3-4 hours/month of manual curation
- More focused reading (10-15 reports vs 25+)
- Better for NotebookLM consumption

### ROI Calculation

**Manual monthly curation:**
- 4 hours × £50/hour = £200/month

**Automated monthly:**
- £3-5/month

**ROI: 4,000%** (even better than weekly due to lower costs!)

---

## Monthly vs Weekly: When to Use Each

### Use Monthly If:
- ✅ Budget-conscious (75% cost savings)
- ✅ Want strategic overview
- ✅ Prefer curated "best of" approach
- ✅ Read 10-15 reports/month is sufficient
- ✅ Don't need immediate breaking news

### Use Weekly If:
- Fast-moving policy area
- Need to catch everything quickly
- Budget allows £12-20/month
- Time-sensitive decisions
- Regulatory environment

**Recommendation: Start with monthly**, upgrade to weekly only if needed.

---

## Calendar Integration

### Monthly Schedule

**1st of each month at 9:00 AM:**
- Scan previous 30 days
- Generate curated digest
- Send via email/Slack

**Perfect timing:**
- Review over first week of month
- Inform monthly planning meetings
- Update stakeholders

### Manual Runs

Can also trigger manually anytime:

```bash
# Railway
railway run python main.py

# Locally
python main.py
```

---

## Monitoring Quality

### Monthly Review Checklist

After each monthly scan, ask:

- [ ] Are all reports truly significant?
- [ ] Would I reference these in senior meetings?
- [ ] Is anything routine/incremental included?
- [ ] Are sources authoritative?
- [ ] Does synthesis provide strategic insights?

### Adjusting Over Time

Track monthly:
- Number of reports found
- Time spent reading
- Usefulness rating (1-5)
- Reports referenced in meetings

Adjust `search_prompt.txt` based on feedback.

---

## Advanced: Quarterly Deep Dives

### Hybrid Approach

**Monthly**: Standard curated digest (10-15 reports)

**Quarterly**: Comprehensive scan (20-30 reports)

Implementation:
```bash
# Monthly (1st of most months)
SEARCH_DAYS_BACK=30
MAX_REPORTS=15

# Quarterly (1st of Jan/Apr/Jul/Oct)
SEARCH_DAYS_BACK=90
MAX_REPORTS=30
```

**Railway cron for quarterly:**
```toml
# Monthly: 1st day of month
schedule = "0 9 1 * *"

# Add separate quarterly job
# (requires separate deployment or manual trigger)
```

---

## FAQ

**Q: Will I miss important reports with monthly scanning?**

A: No - monthly scanning covers 30 days, so it catches everything. The difference is we're more selective about which reports make the final digest.

**Q: What if something urgent happens mid-month?**

A: You can always trigger a manual scan anytime via Railway dashboard or locally. Monthly is the scheduled cadence, not a limitation.

**Q: Can I switch back to weekly?**

A: Yes, just change:
```bash
SEARCH_DAYS_BACK=7
MAX_REPORTS=25
# Cron: 0 9 * * MON
```

**Q: How do I know if monthly is working well?**

A: After 2-3 months, check:
- Are you reading all the reports?
- Do they feel relevant and high-quality?
- Are you referencing them in work?
- If yes to all, it's working!

---

## Summary

**Monthly scanning is now configured and ready to go!**

**Changes made:**
- ✅ Default search period: 30 days (was 7)
- ✅ Default max reports: 15 (was 25)
- ✅ Railway cron: 1st of month (was every Monday)
- ✅ Stricter quality filters
- ✅ Higher selection bar
- ✅ Monthly-optimized prompt

**Benefits:**
- 💰 75% cost reduction (£3-5/month vs £12-20/month)
- 📊 Higher quality reports
- 🎯 More strategic focus
- ⏱️ Better use of reading time

**Next steps:**
1. Test with `CACHE_MODE=true` (costs £3-5)
2. Review report quality
3. Adjust criteria if needed using `REPLAY_MODE=true` (free)
4. Deploy to Railway for automatic monthly scans

**You're all set for cost-effective monthly AI report curation! 🎉**
