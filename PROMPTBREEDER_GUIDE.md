# 🧬 PromptBreeder Integration Guide

**Evolutionary Prompt Optimization for AI Report Scanner**

This guide explains how to use PromptBreeder to automatically improve your report-finding prompts over time based on user feedback and engagement metrics.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Setup](#setup)
4. [Tracking User Interactions](#tracking-user-interactions)
5. [Reward Functions](#reward-functions)
6. [Running Evolution](#running-evolution)
7. [A/B Testing](#ab-testing)
8. [Best Practices](#best-practices)
9. [Examples](#examples)

---

## Overview

### What is PromptBreeder?

PromptBreeder is an evolutionary algorithm for prompt optimization that:
- Generates prompt variants through mutation
- Evaluates performance using reward functions
- Selects best performers for next generation
- Continuously improves over time

### How It Works

```
1. Generate prompt variants (mutations)
2. Run reports with each variant
3. Track user interactions (clicks, ratings, time)
4. Calculate fitness scores
5. Select best performers
6. Create new generation
7. Repeat
```

### Key Benefits

- ✅ **Automatic improvement** - No manual prompt engineering
- ✅ **Data-driven** - Based on actual user behavior
- ✅ **Adaptive** - Learns what works for YOUR audience
- ✅ **Multi-objective** - Optimizes multiple metrics at once

---

## Architecture

### Components

```
┌─────────────────────────────────────────────────┐
│          AI Report Scanner                       │
│  (Generates reports with different prompts)      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│       Interaction Tracker                        │
│  - Click tracking                                │
│  - Dwell time monitoring                         │
│  - Rating collection                             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│       Reward Function                            │
│  - Calculate fitness scores                      │
│  - Multi-signal aggregation                      │
│  - Weighted scoring                              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│       PromptBreeder                              │
│  - Mutation strategies                           │
│  - Selection algorithm                           │
│  - Population management                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│       A/B Tester                                 │
│  - Test variants before promotion                │
│  - Statistical significance                      │
│  - Safe rollout                                  │
└─────────────────────────────────────────────────┘
```

---

## Setup

### 1. Install Dependencies

```bash
pip install flask flask-cors numpy anthropic
```

### 2. Initialize PromptBreeder

```bash
# Create initial population from your current prompt
python evolve_prompts.py init --population-size 10
```

This creates 10 variants of your search prompt:
- 1 seed (your current prompt)
- 9 mutations (variations)

### 3. Start Tracking Server

```bash
python tracking_server.py
```

Access dashboard at: http://localhost:5000

---

## Tracking User Interactions

### Method 1: Manual Tracking (Simple)

Add tracking links to your reports:

```markdown
# Your Report

[UK AI Strategy](http://localhost:5000/api/track/click?report=report_001&url=https://gov.uk/ai-strategy)
```

### Method 2: Web Dashboard (Recommended)

Users rate reports through web interface:
1. View report at `/report/report_001`
2. Automatic dwell time tracking
3. Click "Helpful" or "Not Helpful"

### Method 3: API Integration

Track programmatically:

```python
from prompt_evolution import InteractionTracker

tracker = InteractionTracker()

# Track click
tracker.track_click(
    report_id="report_001",
    user_id="user_123"
)

# Track reading time
tracker.track_dwell_time(
    report_id="report_001",
    user_id="user_123",
    seconds=245.5
)

# Track rating
tracker.track_rating(
    report_id="report_001",
    user_id="user_123",
    rating=1  # 1 = positive, -1 = negative
)
```

### Method 4: Email Click Tracking

Add tracking pixels to email reports:

```html
<!-- In your email template -->
<img src="http://your-domain.com/api/track/open?report=report_001&user=user_123"
     width="1" height="1" />

<!-- Track clicks -->
<a href="http://your-domain.com/api/track/click?report=report_001&redirect=https://actual-url.com">
  Read Report
</a>
```

---

## Reward Functions

### Overview

Reward functions calculate how "good" a prompt is based on multiple signals:

```python
fitness_score = Σ (signal_score × weight)
```

### Default Signals

| Signal | Weight | Description |
|--------|--------|-------------|
| **Click Rate** | 0.25 | How often reports are clicked |
| **Dwell Time** | 0.20 | How long users spend reading |
| **Rating Score** | 0.20 | Positive vs negative ratings |
| **Source Diversity** | 0.15 | Variety of sources |
| **Priority Distribution** | 0.10 | Good mix of priorities |
| **Freshness** | 0.10 | How recent reports are |

### Customizing Weights

Create your own reward function:

```python
from prompt_evolution import RewardFunction

# Prioritize engagement over diversity
custom_weights = {
    'click_rate': 0.35,         # ↑ More important
    'dwell_time': 0.30,         # ↑ More important
    'rating_score': 0.20,
    'source_diversity': 0.05,   # ↓ Less important
    'priority_distribution': 0.05,
    'freshness': 0.05
}

reward_fn = RewardFunction(weights=custom_weights)
```

### Adding Custom Signals

Extend the RewardFunction class:

```python
class CustomRewardFunction(RewardFunction):
    def __init__(self):
        super().__init__()
        # Add new signal
        self.weights['actionability'] = 0.15

    def _score_actionability(self, reports):
        """Score based on actionable insights"""
        # Count reports with "Actionable Insights" section
        actionable = sum(
            1 for r in reports
            if 'Actionable Insights' in r.content
        )
        return actionable / len(reports)

    def calculate_fitness(self, prompt_performance, report_metrics):
        # Call parent method
        base_fitness = super().calculate_fitness(
            prompt_performance, report_metrics
        )

        # Add custom signal
        actionability_score = self._score_actionability(report_metrics)

        return base_fitness + (actionability_score * 0.15)
```

---

## Running Evolution

### Step-by-Step Workflow

#### 1. Initialize Population

```bash
python evolve_prompts.py init --population-size 10
```

**Output:**
```
🧬 Initializing PromptBreeder population...
✅ Created initial population of 10 variants
📁 Saved to data/prompts/generation_0.json

Variant 0: prompt_gen0_id0 (seed)
Variant 1: prompt_gen0_id1 (hypermutation)
Variant 2: prompt_gen0_id2 (fine_tuning)
...
```

#### 2. Run Reports with Different Variants

**Option A: Manual Testing**

Test each variant manually:

```bash
# Use variant 1's prompt
cp data/prompts/variant_1.txt search_prompt.txt
python main.py

# Use variant 2's prompt
cp data/prompts/variant_2.txt search_prompt.txt
python main.py

# Repeat for all variants
```

**Option B: Automated A/B Testing**

Run multiple variants in rotation:

```python
# Auto-rotate through variants
from prompt_evolution import PromptBreeder

breeder = PromptBreeder(client)
population = breeder.load_latest_population()

# Run reports with each variant
for prompt in population:
    # Update search_prompt.txt
    with open('search_prompt.txt', 'w') as f:
        f.write(prompt.prompt_text)

    # Generate report
    os.system('python main.py')

    # Tag reports with prompt_id
    # (Implementation depends on your setup)
```

#### 3. Collect Feedback

Let users interact with reports for 7-14 days:
- Click on interesting reports
- Read reports (dwell time tracked)
- Rate reports (helpful/not helpful)

#### 4. Evolve Next Generation

```bash
python evolve_prompts.py evolve
```

**Output:**
```
🧬 Evolving prompt generation...
📊 Current generation: 0
🧪 Population size: 10

🎯 Calculating fitness scores...
  prompt_gen0_id0: 0.725
  prompt_gen0_id1: 0.812  ← Best
  prompt_gen0_id2: 0.634
  ...

🧬 Creating next generation...
✅ Generated 10 new variants
📁 Saved to data/prompts/generation_1.json

🏆 Top 3 performers:
  1. prompt_gen0_id1: 0.812 (fine_tuning)
  2. prompt_gen0_id4: 0.789 (expand_sources)
  3. prompt_gen0_id0: 0.725 (seed)
```

#### 5. Check Status

```bash
python evolve_prompts.py status
```

**Output:**
```
📊 PromptBreeder Status

Generation: 1
Population size: 10
Created: 2026-01-21T15:30:00

🏆 Variant Rankings:

Rank   Prompt ID              Fitness    Mutation        Usage
----------------------------------------------------------------------
1      prompt_gen1_id2        0.856      fine_tuning     3
2      prompt_gen1_id1        0.823      hypermutation   2
3      prompt_gen0_id1        0.812      fine_tuning     5
...
```

#### 6. Repeat

Continue evolving:
- Run generation 1 variants
- Collect more feedback
- Evolve to generation 2
- Keep iterating!

---

## A/B Testing

### Why A/B Test?

Before promoting a new prompt to production, test it safely:
- Compare against current production prompt
- Measure statistical significance
- Reduce risk of regression

### Start A/B Test

```bash
python evolve_prompts.py test \
    prompt_gen0_id0 \
    prompt_gen1_id2 \
    --duration 7 \
    --split 0.5
```

Parameters:
- `prompt_gen0_id0`: Control (current production)
- `prompt_gen1_id2`: Test variant (challenger)
- `--duration 7`: Test for 7 days
- `--split 0.5`: 50% traffic to each

### Monitor Test

```bash
python evolve_prompts.py analyze test_20260121_153000
```

**Output:**
```
📊 Analyzing A/B test: test_20260121_153000

Test ID: test_20260121_153000
Duration: 7 days

Results:
  Variant A fitness: 0.725
  Variant B fitness: 0.856

🏆 Winner: Variant B
📈 Confidence: 95.0%

Recommendation: promote_b
```

### Promote Winner

```bash
python evolve_prompts.py promote prompt_gen1_id2
```

This:
1. Backs up current `search_prompt.txt`
2. Promotes winner to production
3. Logs promotion for tracking

---

## Best Practices

### 1. Start Small

- Begin with population of 5-10 variants
- Test for 1-2 weeks before evolving
- Increase population as you scale

### 2. Balance Exploration vs Exploitation

```python
# More exploration (risky but innovative)
breeder = PromptBreeder(
    population_size=15,
    mutation_rate=0.5  # Higher mutation
)

# More exploitation (safe but incremental)
breeder = PromptBreeder(
    population_size=10,
    mutation_rate=0.2  # Lower mutation
)
```

### 3. Monitor for Drift

Watch for prompt "drift" away from goals:

```bash
# Check recent prompts
cat data/prompts/generation_5.json | jq '.prompts[0].prompt_text' | head -20
```

If prompts diverge too much, re-seed with original.

### 4. Use Multi-Objective Optimization

Don't optimize for clicks alone:

```python
weights = {
    'click_rate': 0.25,       # Engagement
    'rating_score': 0.25,     # Quality
    'source_diversity': 0.20, # Coverage
    'freshness': 0.15,        # Timeliness
    'actionability': 0.15     # Value
}
```

### 5. Track Metadata

Tag each report with:
- `prompt_id`: Which prompt generated it
- `generation`: Which generation
- `mutation_type`: How it was created

This enables proper attribution:

```python
# In your scanner.py
report_metadata = {
    'prompt_id': current_prompt.prompt_id,
    'generation': current_prompt.generation,
    'mutation_type': current_prompt.mutation_type,
    'timestamp': datetime.now().isoformat()
}
```

### 6. Regular Evaluation

Schedule evolution runs:

```bash
# Weekly cron job
0 0 * * MON python evolve_prompts.py evolve
```

### 7. Human Review

Don't automate blindly:
- Review top performers manually
- Check for quality issues
- Verify prompts still align with goals
- Use A/B tests before promoting

---

## Examples

### Example 1: Basic Evolution Loop

```python
from anthropic import Anthropic
from prompt_evolution import (
    PromptBreeder,
    InteractionTracker,
    RewardFunction
)

# Initialize
client = Anthropic(api_key="your-key")
breeder = PromptBreeder(client, population_size=10)
tracker = InteractionTracker()
reward_fn = RewardFunction()

# Load current prompt
with open('search_prompt.txt') as f:
    seed_prompt = f.read()

# Create initial population
population = breeder.initialize_population(seed_prompt)

# Simulate tracking (in practice, this happens over time)
# ... users interact with reports ...

# Calculate fitness
fitness_scores = []
for prompt in population:
    # Get metrics for this prompt's reports
    reports = get_reports_for_prompt(prompt.prompt_id)
    report_metrics = [
        get_metrics_for_report(r, tracker)
        for r in reports
    ]

    # Calculate fitness
    fitness = reward_fn.calculate_fitness(prompt, report_metrics)
    fitness_scores.append(fitness)

# Evolve
new_population = breeder.evolve_generation(population, fitness_scores)

print(f"Best fitness: {max(fitness_scores):.3f}")
```

### Example 2: Custom Reward Function

```python
class GovernmentFocusedReward(RewardFunction):
    """Reward function optimized for government reports"""

    def __init__(self):
        super().__init__()
        # Adjust weights for government context
        self.weights = {
            'click_rate': 0.20,
            'dwell_time': 0.15,
            'rating_score': 0.15,
            'source_authority': 0.25,  # New: Official sources
            'policy_relevance': 0.15,  # New: Policy impact
            'freshness': 0.10
        }

    def _score_source_authority(self, reports):
        """Prioritize official government sources"""
        official_sources = [
            'gov.uk',
            'DSIT',
            'Cabinet Office',
            'NAO',
            'PAC'
        ]

        official_count = sum(
            1 for r in reports
            if any(src in r.source for src in official_sources)
        )

        return official_count / len(reports)

    def _score_policy_relevance(self, reports):
        """Score based on policy keywords"""
        policy_keywords = [
            'strategy',
            'framework',
            'policy',
            'legislation',
            'regulation'
        ]

        relevant_count = sum(
            1 for r in reports
            if any(kw in r.title.lower() for kw in policy_keywords)
        )

        return relevant_count / len(reports)

    def calculate_fitness(self, prompt_performance, report_metrics):
        """Override to add custom signals"""
        # Base fitness
        fitness = super().calculate_fitness(prompt_performance, report_metrics)

        # Add custom signals
        authority_score = self._score_source_authority(report_metrics)
        relevance_score = self._score_policy_relevance(report_metrics)

        # Weighted combination
        fitness += authority_score * self.weights['source_authority']
        fitness += relevance_score * self.weights['policy_relevance']

        return min(fitness, 1.0)  # Cap at 1.0
```

### Example 3: Automated Evolution Pipeline

```bash
#!/bin/bash
# evolution_pipeline.sh

# 1. Run reports with all variants in current generation
echo "📊 Running reports with all variants..."
python run_all_variants.py

# 2. Wait for user feedback (run this script weekly)
echo "⏳ Collecting user feedback..."
sleep 604800  # 1 week

# 3. Evolve next generation
echo "🧬 Evolving next generation..."
python evolve_prompts.py evolve

# 4. Check if we have a clear winner
BEST_FITNESS=$(python evolve_prompts.py status | grep -oP 'Fitness: \K[0-9.]+' | head -1)

if (( $(echo "$BEST_FITNESS > 0.85" | bc -l) )); then
    echo "🏆 Strong performer found! Starting A/B test..."

    BEST_ID=$(python get_best_prompt_id.py)
    CURRENT_ID=$(python get_current_prompt_id.py)

    python evolve_prompts.py test $CURRENT_ID $BEST_ID --duration 7
else
    echo "📈 Continue evolving..."
fi
```

---

## FAQ

### Q: How long until I see improvements?

**A:** Typically 3-5 generations (3-5 weeks with weekly evolution).

Early generations explore broadly. Later generations fine-tune.

### Q: What if fitness scores decrease?

**A:** This can happen due to:
1. **Insufficient data** - Need more user interactions
2. **Drift** - Prompts diverging from goal
3. **Changing preferences** - User needs evolving

Solutions:
- Collect more data before evolving
- Re-seed with original prompt
- Adjust reward function weights

### Q: Can I run multiple reward functions?

**A:** Yes! Use ensemble approach:

```python
fitness_ensemble = (
    0.4 * fitness_engagement +
    0.3 * fitness_quality +
    0.3 * fitness_diversity
)
```

### Q: How to handle cold start (no data)?

**A:** Use synthetic metrics initially:

```python
if not user_data_available:
    # Use LLM-based evaluation
    fitness = llm_evaluate_prompt(prompt_text)
else:
    # Use real user data
    fitness = calculate_from_user_interactions()
```

### Q: What population size is optimal?

**A:**
- **Small** (5-10): Faster iteration, less diversity
- **Medium** (10-20): Balanced
- **Large** (20-50): Slower but more exploration

Start with 10, increase if plateauing.

---

## Advanced Topics

### Multi-Armed Bandits

Use MAB for exploration-exploitation:

```python
import numpy as np

class EpsilonGreedy:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon
        self.counts = {}
        self.values = {}

    def select_prompt(self, prompts):
        # Explore
        if np.random.random() < self.epsilon:
            return np.random.choice(prompts)

        # Exploit
        return max(prompts, key=lambda p: self.values.get(p.prompt_id, 0))
```

### Contextual Bandits

Adapt prompt based on context:

```python
# Different prompts for different user segments
if user.role == "policy_maker":
    prompts = policy_focused_prompts
elif user.role == "researcher":
    prompts = research_focused_prompts
else:
    prompts = general_prompts
```

### Novelty Search

Prevent premature convergence:

```python
def novelty_score(prompt, archive):
    """Reward prompts that are different from archive"""
    similarities = [
        embedding_similarity(prompt, archived)
        for archived in archive
    ]
    return 1 - max(similarities)
```

---

## Integration Checklist

- [ ] Installed dependencies (`pip install -r requirements_evolution.txt`)
- [ ] Initialized population (`python evolve_prompts.py init`)
- [ ] Set up tracking server (`python tracking_server.py`)
- [ ] Added tracking to reports (links/API/web interface)
- [ ] Customized reward function (optional)
- [ ] Ran first generation with multiple variants
- [ ] Collected user feedback (1-2 weeks)
- [ ] Evolved next generation (`python evolve_prompts.py evolve`)
- [ ] Set up automated evolution (cron job)
- [ ] Configured A/B testing before promotions
- [ ] Documented reward function rationale
- [ ] Set up monitoring dashboard

---

## Next Steps

1. **Week 1:** Initialize and run first generation
2. **Week 2:** Collect user feedback
3. **Week 3:** Evolve to generation 2
4. **Week 4:** A/B test top performer
5. **Week 5:** Promote winner to production
6. **Ongoing:** Continuous evolution

---

## Resources

- Original PromptBreeder paper: [ArXiv](https://arxiv.org/abs/2309.16797)
- GitHub implementation: https://github.com/vaughanlove/PromptBreeder
- Multi-armed bandits: [Sutton & Barto](http://incompleteideas.net/book/the-book.html)
- A/B testing: [Evan Miller's guides](https://www.evanmiller.org/ab-testing/)

---

**Questions?** Open an issue or check the `prompt_evolution.py` code for implementation details!
