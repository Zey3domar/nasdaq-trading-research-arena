#!/usr/bin/env python3
"""Run the trading tournament"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🏆 STARTING TRADING TOURNAMENT")
    print("=" * 50)
    
    try:
        # Import core modules
        from orchestration.ray_arena import DistributedArenaManager
        from strategies.generator import StrategyGenerator
        
        print("Generating 1,000 strategies...")
        generator = StrategyGenerator()
        strategies = generator.generate_population(1000)
        
        print(f"✅ Generated {len(strategies)} strategies")
        print("Starting distributed evaluation...")
        
        # This runs the actual tournament
        arena = DistributedArenaManager(strategies)
        results = arena.evaluate_generation()
        
        print("🎉 Tournament completed!")
        print(f"Top strategy: {results[0]['strategy_id']}")
        print(f"Best Sharpe: {results[0]['metrics']['sharpe_ratio']:.2f}")
        
    except ImportError as e:
        print(f"❌ Setup required: {e}")
        print("Run: python simple_run.py first")

if __name__ == "__main__":
    main()
