# 🤖 AI Report Scanner

**Automated monthly curation of AI and government reports using Claude AI**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Monthly Scans](https://img.shields.io/badge/schedule-monthly-blue.svg)]()

Stop spending hours searching for relevant AI reports. Get a curated monthly digest of the **best** 10-15 reports delivered automatically, complete with priority rankings, key insights, and an audio-ready summary for NotebookLM.

**💰 Cost-Effective**: Monthly scanning costs only £3-5/month (75% less than weekly)

---

## ✨ Features

- 🔍 **Automated Monthly Search** - Scans 50+ authoritative sources over 30 days
- 🎯 **Smart Prioritization** - Reports ranked by relevance (Critical/High/Medium)
- 🏆 **Quality Over Quantity** - Curates 10-15 BEST reports (not 25+ mixed quality)
- 📧 **Email & Slack** - Delivers via email (SendGrid/Gmail) or Slack
- 🎙️ **NotebookLM Ready** - Generates podcast-optimized source document
- 💾 **Cache & Replay** - Test iterations for FREE after initial scan
- 📊 **Monthly Synthesis** - Strategic insights and cross-cutting themes
- 💰 **Cost Effective** - £3-5/month (vs £12-20 for weekly)
- 📱 **iPhone Compatible** - Full setup guide for mobile deployment

---

## 🚀 Quick Start

**Get running in 10 minutes:**

### Prerequisites

- Python 3.11+
- [Anthropic API key](https://console.anthropic.com)
- **Email/Slack OPTIONAL** - Reports always saved locally

### Installation

```bash
# 1. Clone repository
git clone https://github.com/lexicond/AI-Report-Scanner.git
cd AI-Report-Scanner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env: Add ANTHROPIC_API_KEY=your_key_here

# 4. Run first scan
python main.py
```

**That's it!** Check `reports/` folder for your curated monthly digest.

---

## 📊 What You Get

### Monthly Digest Structure

**🔥 CRITICAL (3-5 reports)**
- Major policy changes and announcements
- Frontier AI breakthroughs
- Cross-government strategic documents
- *"Would be emailed to Permanent Secretaries"*

**📊 HIGH (5-8 reports)**
- Leading think tank comprehensive analysis
- Major consultancy research with evidence
- International governance developments
- *"Would be discussed in DG meetings"*

**📚 MEDIUM (2-3 reports)**
- Exceptional academic research
- International exemplars
- *"Only if truly outstanding"*

**Total: 10-16 high-quality reports** carefully curated from 30-day search

---

## 💰 Cost & ROI

| Item | Cost | Details |
|------|------|---------|
| **Monthly API Cost** | £3-5 | One scan per month |
| **Time Saved** | 3-4 hours | Manual curation time |
| **Value of Time** | £150-200 | @ £50/hour |
| **ROI** | **4,000%** | £3-5 cost vs £150-200 value |

**Comparison:**
- Weekly scanning: £12-20/month (£144-240/year)
- **Monthly scanning**: £3-5/month (**£36-60/year**) ✅
- **Savings**: 75% reduction

---

## 📖 Documentation

### Getting Started

- **[QUICK_TEST_SETUP.md](QUICK_TEST_SETUP.md)** ⭐ **START HERE** - Complete setup & testing guide (30-45 min)
- **[MONTHLY_GUIDE.md](MONTHLY_GUIDE.md)** - Everything about monthly scanning
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Cache & replay for free iteration

### Deployment

- **[RAILWAY_EMAIL_FIX.md](RAILWAY_EMAIL_FIX.md)** - Railway deployment + Slack/SendGrid setup
- **[SETUP_IPHONE.md](SETUP_IPHONE.md)** - Complete iPhone setup guide

### Configuration

- **[EMAIL_GUIDE.md](EMAIL_GUIDE.md)** - Email alternatives & troubleshooting
- **[DEPLOYMENT_FIX.md](DEPLOYMENT_FIX.md)** - Common deployment issues

---

## 🎯 Usage

### Basic Usage

```bash
# Run monthly scan
python main.py

# View results
cat reports/reading_list_*.md
```

### Test & Iterate (FREE after initial scan)

```bash
# 1. Cache results once (costs £3-5)
CACHE_MODE=true python main.py

# 2. Iterate on quality criteria (FREE)
# Edit search_prompt.txt
CACHE_MODE=false REPLAY_MODE=true python main.py

# 3. Repeat step 2 unlimited times (all FREE)
```

### Deployment Options

**Option A: Railway** (Recommended)
```bash
# Automatic monthly scans on 1st of each month
# See QUICK_TEST_SETUP.md for deployment
```

**Option B: Local Cron**
```bash
# Add to crontab
0 9 1 * * cd /path/to/AI-Report-Scanner && python main.py
```

**Option C: Manual**
```bash
# Run whenever you want
python main.py
```

---

## 🔧 Configuration

### Environment Variables

**Required:**
```bash
ANTHROPIC_API_KEY=your_key_here
```

**Optional (for delivery):**
```bash
# Slack (Recommended for Railway)
SLACK_TOKEN=xoxb-your-real-token
SLACK_CHANNEL=#ai-reports

# Or SendGrid for email (works on Railway)
SENDGRID_API_KEY=SG.your-key
SENDGRID_FROM_EMAIL=your-verified-email@example.com
RECIPIENT_EMAIL=your-email@example.com

# Or Gmail (local only, doesn't work on Railway)
SENDER_EMAIL=your-email@gmail.com
RECIPIENT_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

**Scanning Config:**
```bash
SEARCH_DAYS_BACK=30      # Monthly (use 7 for weekly)
MAX_REPORTS=15           # Best 15 reports
```

**Testing:**
```bash
CACHE_MODE=true          # Save API response for reuse
REPLAY_MODE=true         # Use cached response (FREE iterations)
```

---

## 📁 Output Structure

```
AI-Report-Scanner/
├── reports/
│   ├── reading_list_2024-01-21.md    # Curated digest
│   └── notebooklm_2024-01-21.md      # Audio summary source
├── output/
│   ├── metadata_2024-01-21.json      # Token usage, costs
│   └── report_2024-01-21.json        # Full structured data
├── cache/
│   └── api_response.json             # Cached API response
└── logs/
    └── scanner_20240121.log          # Detailed logs
```

---

## 🏗️ Architecture

```
┌─────────────┐
│   main.py   │  Entry point
└──────┬──────┘
       │
       ├──> scanner.py        (Core scanning logic)
       │       ├──> Loads search_prompt.txt
       │       ├──> Calls Claude API with web search
       │       ├──> Caches responses (if CACHE_MODE)
       │       └──> Generates reports
       │
       ├──> notifications.py  (Email & Slack delivery)
       │       ├──> SendGrid support
       │       ├──> SMTP support
       │       └──> Slack SDK
       │
       └──> config.py         (Configuration management)
               └──> Loads & validates .env
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests with coverage
pytest --cov

# Specific test file
pytest tests/test_scanner.py

# Integration tests only
pytest -m integration
```

**Test coverage: 96%** ✅

### Test Workflow

```bash
# 1. Unit tests (fast, no API calls)
DRY_RUN=true pytest

# 2. Integration test with cache (pay once)
CACHE_MODE=true pytest -m integration

# 3. Iterate on tests (FREE)
REPLAY_MODE=true pytest
```

---

## 📱 Deployment

### Railway (Recommended)

**Automatic monthly scans on cloud platform**

```bash
# 1. Deploy to Railway
./railway-deploy.sh

# Or follow QUICK_TEST_SETUP.md for step-by-step
```

**Railway automatically:**
- ✅ Runs on 1st of each month at 9 AM
- ✅ Sends results via Slack
- ✅ Handles all dependencies
- ✅ Manages environment variables

**Cost: Free tier sufficient + £3-5/month API costs**

### Local Cron

**For running on your own server**

```bash
# Add to crontab
crontab -e

# Monthly on 1st at 9 AM
0 9 1 * * cd /path/to/AI-Report-Scanner && /usr/bin/python3 main.py
```

---

## 🎨 Customization

### Adjust Report Quality

Edit `search_prompt.txt`:

```markdown
## QUALITY FILTERS

# Stricter (fewer reports)
2. Substantial and significant (40+ pages instead of 30+)

# More lenient (more reports)
2. Substantial and significant (20+ pages instead of 30+)
```

### Change Schedule

**Weekly instead of monthly:**
```bash
SEARCH_DAYS_BACK=7
MAX_REPORTS=25
# Cron: 0 9 * * MON
```

**Bi-weekly:**
```bash
SEARCH_DAYS_BACK=14
MAX_REPORTS=20
# Cron: 0 9 1,15 * *
```

### Add Custom Sources

Edit `search_prompt.txt`:

```markdown
**Your Custom Category**
- Search: "Your Organization report {date_range}"
- Search: "Your Topics {date_range}"
```

---

## 🔐 Security

- ✅ API keys stored in environment variables (never committed)
- ✅ `.env` file in `.gitignore`
- ✅ Gmail app passwords (not real passwords)
- ✅ Minimal required permissions
- ✅ No sensitive data in logs
- ✅ HTTPS for all API communications

**Best practices:**
```bash
# Check before committing
git diff .env  # Should not exist in git

# Rotate keys quarterly
# Use separate keys for dev/prod
```

---

## 🐛 Troubleshooting

### Common Issues

**"Report is empty or useless"**
- ✅ Fixed: Web search now enabled in API call
- Check logs for errors
- Verify ANTHROPIC_API_KEY is set

**"Slack not receiving reports"**
- Token must be REAL (not `xoxb-your-slack-bot-token` placeholder)
- Bot must be added to #ai-reports channel
- Check Railway logs for errors

**"Email not working on Railway"**
- Gmail SMTP blocked on Railway (use SendGrid instead)
- See [RAILWAY_EMAIL_FIX.md](RAILWAY_EMAIL_FIX.md)

**"Cache not found in replay mode"**
- Run with `CACHE_MODE=true` first
- Check `cache/api_response.json` exists

**More help:** See [QUICK_TEST_SETUP.md](QUICK_TEST_SETUP.md#-troubleshooting)

---

## 🤝 Contributing

Contributions welcome!

```bash
# 1. Fork repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes and test
pytest --cov

# 4. Commit
git commit -m "Add amazing feature"

# 5. Push and create PR
git push origin feature/amazing-feature
```

---

## 📚 Additional Resources

### Search Sources

Scans 50+ sources including:
- **Frontier AI**: Anthropic, OpenAI, DeepMind, Meta AI, Mistral, Cohere
- **UK Government**: Institute for Government, NAO, DSIT, Cabinet Office, CDDO
- **Think Tanks**: Ada Lovelace Institute, Tony Blair Institute, Bennett Institute
- **Consultancies**: McKinsey, Deloitte, PwC, Accenture, BCG, Bain
- **International**: OECD, EU Commission, World Bank
- **Academic**: Stanford HAI, MIT CSAIL, Oxford Internet Institute

### Example Output

```markdown
# AI & Government Reports: Month of 2024-01-21

🔥 CRITICAL (4 reports)

───────────────────────────────────────────

OpenAI GPT-5 Capabilities Report
Source: OpenAI | Published: 2024-01-15 | Length: 52 pages
Link: https://openai.com/research/gpt-5

Why Critical: Major capability leap with new reasoning
features directly applicable to government policy analysis.

Key Takeaways:
- 80% improvement on complex policy reasoning
- New "government mode" for sensitive document handling
- Enhanced UK legal and regulatory understanding

Actionable Insights: Review procurement frameworks to
account for enhanced capabilities. Consider pilot programs
for policy analysis use cases.

[... more reports ...]

MONTHLY SYNTHESIS

Cross-Cutting Themes:
1. Acceleration of frontier model reasoning capabilities
2. Growing international consensus on AI governance
3. Evidence of AI productivity gains in public sector

[... synthesis continues ...]
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software for any purpose.

---

## 🙏 Acknowledgments

- **Anthropic** - Claude AI powers the intelligent curation and web search
- **Railway** - Simple, powerful deployment platform
- **Google NotebookLM** - Audio summary generation
- **Open source community** - All the amazing libraries

---

## 💬 Support & Contact

- 📖 **Documentation**: Check guides in repository
- 🐛 **Issues**: [GitHub Issues](https://github.com/lexicond/AI-Report-Scanner/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/lexicond/AI-Report-Scanner/discussions)

---

## 🗺️ Roadmap

### v1.1 (Current)
- ✅ Monthly scanning for cost reduction
- ✅ Cache & replay for free iteration
- ✅ SendGrid + Slack support
- ✅ Web search enabled

### v1.2 (Planned)
- [ ] Web dashboard for viewing reports
- [ ] RSS feed aggregation
- [ ] Multi-user support
- [ ] Notion integration

### v2.0 (Future)
- [ ] ML-based relevance scoring
- [ ] Trend detection across months
- [ ] Custom report templates
- [ ] Automated NotebookLM podcast generation

---

## ⭐ Star History

If you find this useful, please star the repo! It helps others discover it.

---

**Made with ❤️ for government AI teams**

*Automate the boring stuff. Focus on the important work.*

**Monthly curation. Maximum value. Minimum cost.**
