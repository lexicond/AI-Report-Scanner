# 🧪 Testing & Iteration Guide

**Problem**: Running the scanner costs $3-5 each time due to web searches and AI processing. Testing prompt variations would be expensive!

**Solution**: Cache & Replay modes let you pay once, iterate unlimited times for free.

---

## 💰 Cost Comparison

| Mode | API Calls | Web Searches | Cost | Use Case |
|------|-----------|--------------|------|----------|
| **Normal** | Yes | Yes | $3-5 | Production runs |
| **Cache Mode** | Yes | Yes | $3-5 | Run once, save results |
| **Replay Mode** | No | No | FREE | Iterate on cached results |
| **Dry Run** | No | No | FREE | Mock data for development |

---

## 🚀 Quick Start: Test & Iterate Workflow

### Step 1: Run Once with Cache Mode (Costs $3-5)

This performs real web searches and saves the results:

```bash
# Edit .env
CACHE_MODE=true
REPLAY_MODE=false

# Run scanner
python main.py
```

**What happens:**
- ✅ Real web searches performed
- ✅ Claude processes results
- ✅ Response saved to `cache/api_response.json`
- ✅ Normal reports generated
- 💰 Costs $3-5

### Step 2: Iterate Unlimited Times (FREE)

Now use the cached results to test different configurations:

```bash
# Edit .env
CACHE_MODE=false
REPLAY_MODE=true

# Run scanner - uses cached data
python main.py
```

**What happens:**
- ✅ Loads cached response
- ✅ Re-processes with current prompt
- ✅ Generates reports with new formatting
- ✅ Tests different priorities
- 💰 FREE - no API calls!

### Step 3: Iterate on Improvements

You can now modify:
- `search_prompt.txt` - Change output format, priorities, synthesis
- Priority criteria - Adjust what's Critical vs High
- Output formatting - Test different report structures
- NotebookLM formatting - Optimize for audio

Each iteration is **FREE** using the same cached search results!

---

## 📝 Detailed Workflow Examples

### Example 1: Testing Report Format Changes

**Goal**: Test different report formatting without paying each time.

```bash
# 1. Initial run with cache (pay once)
echo "CACHE_MODE=true" >> .env
echo "REPLAY_MODE=false" >> .env
python main.py

# 2. Modify search_prompt.txt
# Change output format, add new sections, etc.

# 3. Test formatting (free)
echo "CACHE_MODE=false" >> .env
echo "REPLAY_MODE=true" >> .env
python main.py

# 4. Iterate as many times as needed (all free)
# Edit search_prompt.txt
python main.py

# Edit again
python main.py

# And again...
python main.py
```

### Example 2: Testing Priority Criteria

**Goal**: Adjust what reports are marked as "Critical" vs "High".

```bash
# 1. Get real reports (cache them)
CACHE_MODE=true REPLAY_MODE=false python main.py

# 2. Edit search_prompt.txt - modify priority rules:
#    - Change Critical criteria
#    - Adjust scoring logic
#    - Test different thresholds

# 3. Re-run with new priorities (free)
CACHE_MODE=false REPLAY_MODE=true python main.py

# 4. Compare outputs, iterate
```

### Example 3: A/B Testing Output Formats

**Goal**: Test multiple output formats to see which works best.

```bash
# 1. Cache real data once
python main.py  # With CACHE_MODE=true

# 2. Test format A
#    Edit search_prompt.txt with format A
REPLAY_MODE=true python main.py
# Rename output: mv reports/reading_list_*.md reports/format_a.md

# 3. Test format B
#    Edit search_prompt.txt with format B
REPLAY_MODE=true python main.py
# Rename output: mv reports/reading_list_*.md reports/format_b.md

# 4. Compare format_a.md vs format_b.md
# Choose the better one, iterate more
```

---

## 🎯 Common Use Cases

### Use Case 1: Perfecting the Search Prompt

**Scenario**: You want to optimize how reports are summarized and formatted.

**Workflow**:
1. Run once with `CACHE_MODE=true` to get real report data
2. Edit `search_prompt.txt`:
   - Adjust summary length
   - Change priority definitions
   - Modify synthesis section
   - Tweak NotebookLM formatting
3. Test each change with `REPLAY_MODE=true` (free)
4. Iterate until perfect

**Cost**: $3-5 for initial cache, then unlimited free iterations.

### Use Case 2: Testing with Different Date Ranges

**Scenario**: You want to test how the scanner handles different weeks.

**Workflow**:
1. Run Week 1 with `CACHE_MODE=true`, save as `cache/week1.json`
2. Run Week 2 with `CACHE_MODE=true`, save as `cache/week2.json`
3. Test prompt changes against both:
   ```bash
   CACHE_FILE=cache/week1.json REPLAY_MODE=true python main.py
   CACHE_FILE=cache/week2.json REPLAY_MODE=true python main.py
   ```

**Cost**: $3-5 per week cached, then unlimited testing across all weeks.

### Use Case 3: Developing New Features

**Scenario**: You're adding a new section to the report (e.g., "Industry Trends").

**Workflow**:
1. Use existing cache: `REPLAY_MODE=true`
2. Edit `search_prompt.txt` to add new section
3. Test immediately (free)
4. Iterate on the new section until it looks right
5. Only pay again when you need fresh data

**Cost**: Free development using cached data, only pay for production runs.

---

## 🔧 Advanced Techniques

### Technique 1: Multiple Cache Files

Save different weeks or topics:

```bash
# Cache different scenarios
CACHE_FILE=cache/normal_week.json CACHE_MODE=true python main.py
CACHE_FILE=cache/busy_week.json CACHE_MODE=true python main.py
CACHE_FILE=cache/quiet_week.json CACHE_MODE=true python main.py

# Test against all scenarios
CACHE_FILE=cache/normal_week.json REPLAY_MODE=true python main.py
CACHE_FILE=cache/busy_week.json REPLAY_MODE=true python main.py
CACHE_FILE=cache/quiet_week.json REPLAY_MODE=true python main.py
```

### Technique 2: Version Control for Prompts

Track prompt iterations:

```bash
# Save current version
git commit -m "v1: Initial prompt format"

# Cache data for this version
CACHE_MODE=true python main.py
cp cache/api_response.json cache/v1_response.json

# Iterate on prompt
# Edit search_prompt.txt
git commit -m "v2: Improved summary format"

# Test v2 against v1 data
CACHE_FILE=cache/v1_response.json REPLAY_MODE=true python main.py

# If v2 is better, update cache for future tests
CACHE_MODE=true python main.py
```

### Technique 3: Automated Testing

Create test script:

```bash
#!/bin/bash
# test_formats.sh

echo "Testing format variations..."

for format in compact detailed bullet narrative
do
  echo "Testing $format format..."

  # Update prompt with format
  sed -i "s/OUTPUT_FORMAT=.*/OUTPUT_FORMAT=$format/" search_prompt.txt

  # Run with cached data
  REPLAY_MODE=true python main.py

  # Save output
  mv reports/reading_list_*.md reports/test_${format}.md
done

echo "All formats tested! Check reports/test_*.md"
```

---

## 📊 Cache File Structure

The cache file (`cache/api_response.json`) contains:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Full report content from Claude..."
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 2899,
    "output_tokens": 8500
  },
  "cached_at": "2026-01-21T10:30:00"
}
```

**Benefits**:
- Can inspect the raw response
- Can manually edit if needed
- Can share with others for testing
- Timestamp shows when data was collected

---

## ⚠️ Important Notes

### When to Recache

You need to run with `CACHE_MODE=true` again when:
- ✅ You want fresh reports from current week
- ✅ You're testing changes to search queries
- ✅ You want to test against different data
- ✅ Cache is more than a week old

You DON'T need to recache when:
- ❌ Only changing output formatting
- ❌ Only adjusting priorities
- ❌ Only modifying synthesis logic
- ❌ Testing different report structures

### Cache Mode vs Replay Mode

**Never enable both at the same time!**

| Setting | Behavior |
|---------|----------|
| `CACHE_MODE=false, REPLAY_MODE=false` | Normal production run |
| `CACHE_MODE=true, REPLAY_MODE=false` | Run once, save results |
| `CACHE_MODE=false, REPLAY_MODE=true` | Use cached results |
| `CACHE_MODE=true, REPLAY_MODE=true` | ❌ ERROR - conflicts! |

### Cache Freshness

The cache includes a `cached_at` timestamp. Consider recaching if:
- More than 1 week old (data is stale)
- Testing current week's reports (need fresh data)
- Significant world events happened (data context changed)

---

## 🎓 Best Practices

### 1. Cache Representative Data

Cache a "typical" week's results for general testing:
```bash
# Wait for a normal week (not holiday, not major news event)
CACHE_MODE=true python main.py
# Use this cache for most iterations
```

### 2. Version Your Prompts

```bash
git commit -m "Prompt version X" search_prompt.txt
# Now you can always go back to working versions
```

### 3. Document Your Iterations

```bash
# Keep notes on what you tried
echo "v1: Too verbose, 12k tokens" >> iteration_notes.txt
echo "v2: Better, 8k tokens, clearer priorities" >> iteration_notes.txt
echo "v3: Perfect! Clean format, good NotebookLM" >> iteration_notes.txt
```

### 4. Test Edge Cases

Cache multiple scenarios:
- Light week (few reports)
- Heavy week (many reports)
- Mixed quality (some good, some meh)
- Specific topic (e.g., all frontier AI)

### 5. Share Cache Files

Team testing:
```bash
# Person A caches data
CACHE_MODE=true python main.py
git add cache/api_response.json
git commit -m "Cache: Week of Jan 21"

# Person B uses same data
git pull
REPLAY_MODE=true python main.py
# Both testing against identical data
```

---

## 🐛 Troubleshooting

### "No cached response found"

**Problem**: Trying to use `REPLAY_MODE=true` but no cache exists.

**Solution**:
```bash
# Run once with cache mode first
CACHE_MODE=true REPLAY_MODE=false python main.py

# Then use replay mode
CACHE_MODE=false REPLAY_MODE=true python main.py
```

### "Cache file corrupted"

**Problem**: Cache file is invalid JSON or incomplete.

**Solution**:
```bash
# Delete cache and regenerate
rm cache/api_response.json
CACHE_MODE=true python main.py
```

### "Results differ from production"

**Problem**: Replay mode output differs from normal runs.

**Solution**: This is expected! Replay mode uses cached web search results. The prompt may have changed, so processing is different. This is the point - testing prompt changes without new searches.

---

## 💡 Pro Tips

### Tip 1: Quick Iteration Loop

```bash
# One-line iteration
while true; do
  nano search_prompt.txt  # Edit prompt
  REPLAY_MODE=true python main.py  # Test
  read -p "Continue? (y/n) " -n 1 -r
  [[ ! $REPLY =~ ^[Yy]$ ]] && break
done
```

### Tip 2: Diff Checking

```bash
# Compare two iterations
REPLAY_MODE=true python main.py
cp reports/reading_list_*.md reports/version1.md

# Edit prompt
REPLAY_MODE=true python main.py
cp reports/reading_list_*.md reports/version2.md

# See what changed
diff reports/version1.md reports/version2.md
```

### Tip 3: Metrics Tracking

Track improvements:
```bash
# Count output tokens
REPLAY_MODE=true python main.py | grep "Output tokens"

# Track report quality metrics
wc -l reports/reading_list_*.md  # Length
grep "CRITICAL" reports/reading_list_*.md | wc -l  # Critical reports
```

---

## 🎯 Summary

**Testing without cache**: $3-5 per test × 10 iterations = **$30-50**

**Testing with cache**: $3-5 once + FREE × 10 iterations = **$3-5**

**Savings**: Up to 90% cost reduction during development!

**Workflow**:
1. Cache once: `CACHE_MODE=true` ($3-5)
2. Iterate forever: `REPLAY_MODE=true` (FREE)
3. Recache when needed (fresh data, new week)

**Perfect for**:
- Prompt optimization
- Format testing
- Feature development
- A/B testing
- Quality improvements

---

## 📚 Related Guides

- [README.md](README.md) - Main documentation
- [EMAIL_GUIDE.md](EMAIL_GUIDE.md) - Email configuration
- [RAILWAY_EMAIL_FIX.md](RAILWAY_EMAIL_FIX.md) - Railway deployment
- [SETUP_IPHONE.md](SETUP_IPHONE.md) - iPhone setup

---

**Happy testing! Iterate fearlessly with zero cost! 🚀**
