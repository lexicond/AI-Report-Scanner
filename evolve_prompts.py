#!/usr/bin/env python3
"""
CLI tool for managing prompt evolution

Usage:
    python evolve_prompts.py init              # Initialize population from current prompt
    python evolve_prompts.py evolve            # Run one generation of evolution
    python evolve_prompts.py status            # Show current generation status
    python evolve_prompts.py test A B          # Start A/B test between variants
    python evolve_prompts.py analyze TEST_ID   # Analyze A/B test results
    python evolve_prompts.py promote ID        # Promote variant to production
"""

import argparse
import sys
from pathlib import Path
from anthropic import Anthropic

from prompt_evolution import (
    PromptBreeder,
    InteractionTracker,
    RewardFunction,
    ABTester,
    ReportMetrics,
    PromptPerformance
)
from config import get_settings


def init_population(args):
    """Initialize population from current search_prompt.txt"""
    print("🧬 Initializing PromptBreeder population...")

    # Load current prompt
    prompt_file = Path("search_prompt.txt")
    if not prompt_file.exists():
        print("❌ Error: search_prompt.txt not found")
        sys.exit(1)

    with open(prompt_file) as f:
        seed_prompt = f.read()

    # Initialize breeder
    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)
    breeder = PromptBreeder(client, population_size=args.population_size)

    # Create initial population
    population = breeder.initialize_population(seed_prompt)

    print(f"✅ Created initial population of {len(population)} variants")
    print(f"📁 Saved to data/prompts/generation_0.json")

    # Show variants
    for i, prompt in enumerate(population[:3]):
        print(f"\n{'='*60}")
        print(f"Variant {i}: {prompt.prompt_id}")
        print(f"Mutation: {prompt.mutation_type or 'seed'}")
        print(f"Preview: {prompt.prompt_text[:200]}...")


def evolve_generation(args):
    """Run one generation of evolution"""
    print("🧬 Evolving prompt generation...")

    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)

    # Load components
    breeder = PromptBreeder(client)
    tracker = InteractionTracker()
    reward_fn = RewardFunction()

    # Load current population
    population = breeder.load_latest_population()
    if not population:
        print("❌ No population found. Run 'init' first.")
        sys.exit(1)

    print(f"📊 Current generation: {population[0].generation}")
    print(f"🧪 Population size: {len(population)}")

    # Calculate fitness for each variant
    print("\n🎯 Calculating fitness scores...")
    fitness_scores = []

    for prompt in population:
        # Load reports generated with this prompt
        # (In practice, you'd tag reports with prompt_id)
        report_metrics = _load_report_metrics_for_prompt(prompt.prompt_id, tracker)

        if not report_metrics:
            # No data yet, use default low fitness
            fitness = 0.3
            print(f"  {prompt.prompt_id}: {fitness:.3f} (no data yet)")
        else:
            # Calculate performance from prompt
            fitness = reward_fn.calculate_fitness(prompt, report_metrics)
            print(f"  {prompt.prompt_id}: {fitness:.3f}")

        fitness_scores.append(fitness)
        prompt.fitness_score = fitness

    # Evolve new generation
    print("\n🧬 Creating next generation...")
    new_population = breeder.evolve_generation(population, fitness_scores)

    print(f"\n✅ Generated {len(new_population)} new variants")
    print(f"📁 Saved to data/prompts/generation_{new_population[0].generation}.json")

    # Show top performers
    sorted_pop = sorted(zip(new_population, fitness_scores),
                       key=lambda x: x[1], reverse=True)

    print("\n🏆 Top 3 performers:")
    for i, (prompt, fitness) in enumerate(sorted_pop[:3]):
        print(f"  {i+1}. {prompt.prompt_id}: {fitness:.3f}")
        if prompt.mutation_type:
            print(f"     Mutation: {prompt.mutation_type}")


def show_status(args):
    """Show status of current generation"""
    print("📊 PromptBreeder Status\n")

    # Load latest generation
    breeder = PromptBreeder(None)  # Don't need client for loading
    population = breeder.load_latest_population()

    if not population:
        print("❌ No population found. Run 'init' first.")
        return

    print(f"Generation: {population[0].generation}")
    print(f"Population size: {len(population)}")
    print(f"Created: {population[0].created_at}")

    # Show variants sorted by fitness
    sorted_pop = sorted(population, key=lambda p: p.fitness_score, reverse=True)

    print("\n🏆 Variant Rankings:\n")
    print(f"{'Rank':<6} {'Prompt ID':<20} {'Fitness':<10} {'Mutation':<15} {'Usage':<8}")
    print("-" * 70)

    for i, prompt in enumerate(sorted_pop):
        mutation = prompt.mutation_type or 'seed'
        print(f"{i+1:<6} {prompt.prompt_id:<20} {prompt.fitness_score:<10.3f} "
              f"{mutation:<15} {prompt.usage_count:<8}")

    # Show current production prompt
    prod_file = Path("search_prompt.txt")
    if prod_file.exists():
        print("\n📌 Current production prompt:")
        print(f"   File: search_prompt.txt")
        print(f"   Size: {prod_file.stat().st_size} bytes")


def start_ab_test(args):
    """Start A/B test between two variants"""
    print(f"🧪 Starting A/B test: {args.variant_a} vs {args.variant_b}")

    # Load variants
    breeder = PromptBreeder(None)
    population = breeder.load_latest_population()

    variant_a = next((p for p in population if p.prompt_id == args.variant_a), None)
    variant_b = next((p for p in population if p.prompt_id == args.variant_b), None)

    if not variant_a or not variant_b:
        print("❌ Error: One or both variants not found")
        sys.exit(1)

    # Start test
    tester = ABTester(test_duration_days=args.duration)
    test_id = tester.start_test(variant_a, variant_b, traffic_split=args.split)

    print(f"\n✅ Started A/B test: {test_id}")
    print(f"📊 Duration: {args.duration} days")
    print(f"🔀 Traffic split: {args.split:.0%} to variant B")
    print(f"\nTo check results later:")
    print(f"  python evolve_prompts.py analyze {test_id}")


def analyze_test(args):
    """Analyze A/B test results"""
    print(f"📊 Analyzing A/B test: {args.test_id}\n")

    tracker = InteractionTracker()
    reward_fn = RewardFunction()
    tester = ABTester()

    results = tester.analyze_test(args.test_id, tracker, reward_fn)

    print(f"Test ID: {results['test_id']}")
    print(f"Duration: {results['duration_days']} days")
    print(f"\nResults:")
    print(f"  Variant A fitness: {results['variant_a_fitness']:.3f}")
    print(f"  Variant B fitness: {results['variant_b_fitness']:.3f}")
    print(f"\n🏆 Winner: Variant {results['winner'].upper()}")
    print(f"📈 Confidence: {results['confidence']:.1%}")
    print(f"\nRecommendation: {results['recommendation']}")

    if results['winner'] == 'b':
        print(f"\nTo promote variant B to production:")
        print(f"  python evolve_prompts.py promote {results['test_id']}_b")


def promote_variant(args):
    """Promote a variant to production"""
    print(f"🚀 Promoting variant to production: {args.variant_id}\n")

    # Load variant
    breeder = PromptBreeder(None)
    population = breeder.load_latest_population()

    variant = next((p for p in population if p.prompt_id == args.variant_id), None)

    if not variant:
        print("❌ Error: Variant not found")
        sys.exit(1)

    # Backup current prompt
    current_prompt = Path("search_prompt.txt")
    if current_prompt.exists():
        backup_file = Path(f"search_prompt.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        current_prompt.rename(backup_file)
        print(f"💾 Backed up current prompt to: {backup_file}")

    # Write new prompt
    with open(current_prompt, 'w') as f:
        f.write(variant.prompt_text)

    print(f"✅ Promoted {variant.prompt_id} to production")
    print(f"📁 Updated: search_prompt.txt")
    print(f"\nNext steps:")
    print(f"  1. Test locally: python main.py")
    print(f"  2. Deploy to Railway")
    print(f"  3. Monitor performance for next week")


def _load_report_metrics_for_prompt(prompt_id: str,
                                    tracker: InteractionTracker) -> list:
    """
    Load report metrics for reports generated with a specific prompt

    In practice, you'd need to tag each report with the prompt_id
    that was used to generate it. This is a placeholder.
    """
    # This would load actual report data
    # For now, return empty to indicate no data
    return []


def main():
    parser = argparse.ArgumentParser(
        description="PromptBreeder - Evolutionary prompt optimization"
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize population')
    init_parser.add_argument('--population-size', type=int, default=10,
                            help='Initial population size')
    init_parser.set_defaults(func=init_population)

    # Evolve command
    evolve_parser = subparsers.add_parser('evolve', help='Evolve one generation')
    evolve_parser.set_defaults(func=evolve_generation)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show current status')
    status_parser.set_defaults(func=show_status)

    # Test command
    test_parser = subparsers.add_parser('test', help='Start A/B test')
    test_parser.add_argument('variant_a', help='Control variant ID')
    test_parser.add_argument('variant_b', help='Test variant ID')
    test_parser.add_argument('--duration', type=int, default=7,
                            help='Test duration in days')
    test_parser.add_argument('--split', type=float, default=0.5,
                            help='Traffic split (0.0 to 1.0)')
    test_parser.set_defaults(func=start_ab_test)

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze A/B test')
    analyze_parser.add_argument('test_id', help='Test ID to analyze')
    analyze_parser.set_defaults(func=analyze_test)

    # Promote command
    promote_parser = subparsers.add_parser('promote', help='Promote variant to production')
    promote_parser.add_argument('variant_id', help='Variant ID to promote')
    promote_parser.set_defaults(func=promote_variant)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    from datetime import datetime, timedelta
    main()
