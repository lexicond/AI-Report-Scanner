"""
PromptBreeder Integration for AI Report Scanner

This module implements evolutionary prompt optimization using:
1. User interaction tracking (clicks, ratings, dwell time)
2. Multi-signal reward functions
3. PromptBreeder-style evolutionary optimization
4. A/B testing of prompt variants

Based on: https://github.com/vaughanlove/PromptBreeder
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from anthropic import Anthropic


@dataclass
class ReportMetrics:
    """Metrics for a single report"""
    report_id: str
    title: str
    source: str
    url: str
    priority: str  # CRITICAL, HIGH, MEDIUM

    # User interaction metrics
    clicks: int = 0
    unique_users: int = 0
    avg_time_spent: float = 0.0  # seconds
    ratings_positive: int = 0
    ratings_negative: int = 0

    # Search quality metrics
    search_position: int = 0  # Position in search results
    relevance_score: float = 0.0

    # Metadata
    discovered_date: str = ""
    prompt_version: str = ""


@dataclass
class PromptPerformance:
    """Performance metrics for a prompt variant"""
    prompt_id: str
    prompt_text: str
    version: int

    # Aggregate metrics
    total_reports: int = 0
    avg_click_rate: float = 0.0
    avg_rating_score: float = 0.0  # -1 to 1
    avg_dwell_time: float = 0.0

    # Quality metrics
    critical_reports: int = 0
    high_reports: int = 0
    source_diversity: float = 0.0  # 0 to 1

    # Evolution metadata
    parent_id: Optional[str] = None
    mutation_type: Optional[str] = None
    generation: int = 0
    fitness_score: float = 0.0

    # Timestamps
    created_at: str = ""
    last_used: str = ""
    usage_count: int = 0


class InteractionTracker:
    """Track user interactions with reports"""

    def __init__(self, data_dir: Path = Path("data/interactions")):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("InteractionTracker")

    def track_click(self, report_id: str, user_id: str, timestamp: str = None):
        """Track when a user clicks on a report"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        event = {
            "event": "click",
            "report_id": report_id,
            "user_id": user_id,
            "timestamp": timestamp
        }

        self._save_event(event)
        self.logger.info(f"Tracked click: {report_id} by {user_id}")

    def track_dwell_time(self, report_id: str, user_id: str, seconds: float):
        """Track how long a user spent reading a report"""
        event = {
            "event": "dwell",
            "report_id": report_id,
            "user_id": user_id,
            "seconds": seconds,
            "timestamp": datetime.now().isoformat()
        }

        self._save_event(event)
        self.logger.info(f"Tracked dwell: {report_id} for {seconds}s")

    def track_rating(self, report_id: str, user_id: str, rating: int):
        """Track user rating (1 = positive, -1 = negative)"""
        event = {
            "event": "rating",
            "report_id": report_id,
            "user_id": user_id,
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        }

        self._save_event(event)
        self.logger.info(f"Tracked rating: {report_id} = {rating}")

    def _save_event(self, event: Dict):
        """Save event to daily log file"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.data_dir / f"events_{date_str}.jsonl"

        with open(log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def get_report_metrics(self, report_id: str, days: int = 30) -> Dict:
        """Aggregate metrics for a report over last N days"""
        events = self._load_events(days)

        clicks = 0
        unique_users = set()
        dwell_times = []
        ratings_pos = 0
        ratings_neg = 0

        for event in events:
            if event.get('report_id') != report_id:
                continue

            if event['event'] == 'click':
                clicks += 1
                unique_users.add(event['user_id'])
            elif event['event'] == 'dwell':
                dwell_times.append(event['seconds'])
            elif event['event'] == 'rating':
                if event['rating'] > 0:
                    ratings_pos += 1
                else:
                    ratings_neg += 1

        return {
            'clicks': clicks,
            'unique_users': len(unique_users),
            'avg_dwell_time': np.mean(dwell_times) if dwell_times else 0.0,
            'ratings_positive': ratings_pos,
            'ratings_negative': ratings_neg
        }

    def _load_events(self, days: int = 30) -> List[Dict]:
        """Load events from last N days"""
        events = []

        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            log_file = self.data_dir / f"events_{date_str}.jsonl"

            if log_file.exists():
                with open(log_file) as f:
                    for line in f:
                        events.append(json.loads(line.strip()))

        return events


class RewardFunction:
    """Calculate reward scores for prompt performance"""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        # Default weights for different signals
        self.weights = weights or {
            'click_rate': 0.25,          # How often reports are clicked
            'dwell_time': 0.20,          # How long users spend reading
            'rating_score': 0.20,        # Positive vs negative ratings
            'source_diversity': 0.15,    # Variety of sources
            'priority_distribution': 0.10,  # Good mix of priorities
            'freshness': 0.10            # How recent the reports are
        }

        self.logger = logging.getLogger("RewardFunction")

    def calculate_fitness(self, prompt_performance: PromptPerformance,
                         report_metrics: List[ReportMetrics]) -> float:
        """
        Calculate overall fitness score for a prompt variant

        Returns: float between 0.0 and 1.0
        """
        scores = {}

        # 1. Click Rate Score
        scores['click_rate'] = self._score_click_rate(report_metrics)

        # 2. Dwell Time Score
        scores['dwell_time'] = self._score_dwell_time(report_metrics)

        # 3. Rating Score
        scores['rating_score'] = self._score_ratings(report_metrics)

        # 4. Source Diversity Score
        scores['source_diversity'] = self._score_source_diversity(report_metrics)

        # 5. Priority Distribution Score
        scores['priority_distribution'] = self._score_priority_distribution(report_metrics)

        # 6. Freshness Score
        scores['freshness'] = self._score_freshness(report_metrics)

        # Calculate weighted average
        fitness = sum(scores[key] * self.weights[key]
                     for key in scores.keys())

        self.logger.info(f"Fitness scores: {scores}")
        self.logger.info(f"Overall fitness: {fitness:.3f}")

        return fitness

    def _score_click_rate(self, reports: List[ReportMetrics]) -> float:
        """Score based on click-through rate"""
        if not reports:
            return 0.0

        total_clicks = sum(r.clicks for r in reports)
        avg_clicks_per_report = total_clicks / len(reports)

        # Normalize: assume 5+ clicks per report is excellent
        return min(avg_clicks_per_report / 5.0, 1.0)

    def _score_dwell_time(self, reports: List[ReportMetrics]) -> float:
        """Score based on average time spent reading"""
        if not reports:
            return 0.0

        avg_dwell = np.mean([r.avg_time_spent for r in reports if r.clicks > 0])

        # Normalize: 300 seconds (5 min) is excellent
        return min(avg_dwell / 300.0, 1.0)

    def _score_ratings(self, reports: List[ReportMetrics]) -> float:
        """Score based on positive vs negative ratings"""
        total_pos = sum(r.ratings_positive for r in reports)
        total_neg = sum(r.ratings_negative for r in reports)

        if total_pos + total_neg == 0:
            return 0.5  # Neutral if no ratings

        # Score from -1 to 1, normalize to 0 to 1
        ratio = (total_pos - total_neg) / (total_pos + total_neg)
        return (ratio + 1) / 2

    def _score_source_diversity(self, reports: List[ReportMetrics]) -> float:
        """Score based on variety of sources"""
        if not reports:
            return 0.0

        unique_sources = len(set(r.source for r in reports))

        # Normalize: 10+ unique sources is excellent
        return min(unique_sources / 10.0, 1.0)

    def _score_priority_distribution(self, reports: List[ReportMetrics]) -> float:
        """Score based on good mix of priority levels"""
        if not reports:
            return 0.0

        critical = sum(1 for r in reports if r.priority == 'CRITICAL')
        high = sum(1 for r in reports if r.priority == 'HIGH')
        medium = sum(1 for r in reports if r.priority == 'MEDIUM')

        total = len(reports)

        # Ideal distribution: 30% critical, 50% high, 20% medium
        ideal = [0.3, 0.5, 0.2]
        actual = [critical/total, high/total, medium/total]

        # Calculate distance from ideal (lower is better)
        distance = sum(abs(a - i) for a, i in zip(actual, ideal))

        # Convert to score (0 to 1, higher is better)
        return max(1.0 - distance, 0.0)

    def _score_freshness(self, reports: List[ReportMetrics]) -> float:
        """Score based on how recent the reports are"""
        if not reports:
            return 0.0

        # This would need actual publication dates
        # For now, assume all reports are recent (placeholder)
        return 0.8


class PromptBreeder:
    """Evolutionary prompt optimization using PromptBreeder techniques"""

    def __init__(self, anthropic_client: Anthropic,
                 population_size: int = 10,
                 mutation_rate: float = 0.3):
        self.client = anthropic_client
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.logger = logging.getLogger("PromptBreeder")

        self.prompt_dir = Path("data/prompts")
        self.prompt_dir.mkdir(parents=True, exist_ok=True)

    def initialize_population(self, seed_prompt: str) -> List[PromptPerformance]:
        """Create initial population from seed prompt"""
        population = []

        # Add seed prompt
        seed = PromptPerformance(
            prompt_id=f"prompt_gen0_id0",
            prompt_text=seed_prompt,
            version=0,
            generation=0,
            created_at=datetime.now().isoformat()
        )
        population.append(seed)

        # Generate variants through mutations
        for i in range(1, self.population_size):
            variant = self._mutate_prompt(seed, i)
            population.append(variant)

        # Save population
        self._save_population(population)

        return population

    def _mutate_prompt(self, parent: PromptPerformance,
                      child_id: int) -> PromptPerformance:
        """
        Generate a mutated version of the prompt using Claude

        Mutation strategies:
        1. Hypermutation: Significant changes to search strategy
        2. Fine-tuning: Small refinements to existing prompt
        3. Crossover: Combine elements from multiple parents
        4. Zero-order: Complete rewrite while maintaining goal
        """
        mutation_type = np.random.choice([
            'hypermutation',
            'fine_tuning',
            'add_context',
            'simplify',
            'expand_sources'
        ])

        self.logger.info(f"Mutating prompt with strategy: {mutation_type}")

        mutation_prompts = {
            'hypermutation': f"""
Given this prompt for finding AI government reports:

{parent.prompt_text}

Create a SIGNIFICANTLY DIFFERENT version that:
- Uses different search strategies
- Targets different sources or keywords
- Changes the priority criteria
- Maintains the same output format

Return ONLY the new prompt text, no explanation.
""",
            'fine_tuning': f"""
Given this prompt for finding AI government reports:

{parent.prompt_text}

Make SMALL IMPROVEMENTS to:
- Improve search precision
- Better filter criteria
- Clearer instructions
- More specific examples

Return ONLY the improved prompt text, no explanation.
""",
            'add_context': f"""
Given this prompt for finding AI government reports:

{parent.prompt_text}

Add MORE CONTEXT about:
- Current AI policy landscape
- Important government initiatives
- Key stakeholders to prioritize
- Recent trends in AI governance

Return ONLY the enhanced prompt text, no explanation.
""",
            'simplify': f"""
Given this prompt for finding AI government reports:

{parent.prompt_text}

SIMPLIFY by:
- Removing redundant instructions
- Focusing on core search criteria
- Making it more concise
- Keeping essential elements only

Return ONLY the simplified prompt text, no explanation.
""",
            'expand_sources': f"""
Given this prompt for finding AI government reports:

{parent.prompt_text}

EXPAND the sources section to include:
- More international organizations
- Additional UK think tanks
- Frontier AI lab research centers
- Government innovation hubs

Return ONLY the expanded prompt text, no explanation.
"""
        }

        # Call Claude to mutate the prompt
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": mutation_prompts[mutation_type]
            }]
        )

        mutated_text = response.content[0].text

        return PromptPerformance(
            prompt_id=f"prompt_gen{parent.generation + 1}_id{child_id}",
            prompt_text=mutated_text,
            version=parent.version + 1,
            generation=parent.generation + 1,
            parent_id=parent.prompt_id,
            mutation_type=mutation_type,
            created_at=datetime.now().isoformat()
        )

    def evolve_generation(self, current_population: List[PromptPerformance],
                         fitness_scores: List[float]) -> List[PromptPerformance]:
        """
        Create next generation through selection and mutation

        Uses tournament selection to pick parents based on fitness
        """
        # Sort by fitness
        sorted_pop = sorted(zip(current_population, fitness_scores),
                           key=lambda x: x[1], reverse=True)

        new_population = []

        # Elitism: Keep top 20% unchanged
        elite_count = max(1, self.population_size // 5)
        for prompt, score in sorted_pop[:elite_count]:
            prompt.usage_count += 1
            new_population.append(prompt)

        # Generate rest through mutation of top performers
        parent_pool = [p for p, s in sorted_pop[:self.population_size // 2]]

        while len(new_population) < self.population_size:
            parent = np.random.choice(parent_pool)
            child = self._mutate_prompt(parent, len(new_population))
            new_population.append(child)

        # Save new generation
        self._save_population(new_population)

        self.logger.info(f"Evolved generation {new_population[0].generation + 1}")

        return new_population

    def _save_population(self, population: List[PromptPerformance]):
        """Save current population to disk"""
        gen = population[0].generation
        output_file = self.prompt_dir / f"generation_{gen}.json"

        data = {
            'generation': gen,
            'population_size': len(population),
            'timestamp': datetime.now().isoformat(),
            'prompts': [asdict(p) for p in population]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        self.logger.info(f"Saved generation {gen} to {output_file}")

    def load_latest_population(self) -> Optional[List[PromptPerformance]]:
        """Load most recent generation"""
        gen_files = list(self.prompt_dir.glob("generation_*.json"))

        if not gen_files:
            return None

        latest_file = max(gen_files, key=lambda p: p.stat().st_mtime)

        with open(latest_file) as f:
            data = json.load(f)

        return [PromptPerformance(**p) for p in data['prompts']]


class ABTester:
    """A/B test prompt variants before promoting to production"""

    def __init__(self, test_duration_days: int = 7):
        self.test_duration_days = test_duration_days
        self.logger = logging.getLogger("ABTester")
        self.test_dir = Path("data/ab_tests")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def start_test(self, variant_a: PromptPerformance,
                   variant_b: PromptPerformance,
                   traffic_split: float = 0.5) -> str:
        """
        Start A/B test between two variants

        Args:
            variant_a: Control prompt
            variant_b: Test prompt
            traffic_split: Fraction of traffic to send to variant_b

        Returns:
            test_id
        """
        test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        test_config = {
            'test_id': test_id,
            'start_date': datetime.now().isoformat(),
            'duration_days': self.test_duration_days,
            'traffic_split': traffic_split,
            'variant_a': asdict(variant_a),
            'variant_b': asdict(variant_b),
            'status': 'running'
        }

        test_file = self.test_dir / f"{test_id}.json"
        with open(test_file, 'w') as f:
            json.dump(test_config, f, indent=2)

        self.logger.info(f"Started A/B test: {test_id}")
        return test_id

    def get_variant(self, test_id: str) -> str:
        """
        Randomly select a variant based on traffic split

        Returns:
            'a' or 'b'
        """
        test_file = self.test_dir / f"{test_id}.json"

        with open(test_file) as f:
            test_config = json.load(f)

        if np.random.random() < test_config['traffic_split']:
            return 'b'
        return 'a'

    def analyze_test(self, test_id: str,
                    tracker: InteractionTracker,
                    reward_fn: RewardFunction) -> Dict:
        """
        Analyze results of A/B test

        Returns:
            Dictionary with variant performances and winner
        """
        test_file = self.test_dir / f"{test_id}.json"

        with open(test_file) as f:
            test_config = json.load(f)

        # Get metrics for each variant
        # (This would need report IDs tagged with variant in practice)

        results = {
            'test_id': test_id,
            'duration_days': test_config['duration_days'],
            'variant_a_fitness': 0.0,  # Placeholder
            'variant_b_fitness': 0.0,  # Placeholder
            'winner': 'b',  # Placeholder
            'confidence': 0.95,  # Placeholder - would use statistical test
            'recommendation': 'promote_b'
        }

        return results


# Example usage
if __name__ == "__main__":
    # Initialize components
    tracker = InteractionTracker()
    reward_fn = RewardFunction()

    # Simulate tracking some interactions
    tracker.track_click("report_001", "user_123")
    tracker.track_dwell_time("report_001", "user_123", 245.5)
    tracker.track_rating("report_001", "user_123", 1)

    # Get metrics
    metrics = tracker.get_report_metrics("report_001")
    print(f"Report metrics: {metrics}")
