"""
Steam-Only Automation Pipeline

This script:
1. Fetches recent games from Steam
2. Gets top 100 most helpful reviews for each game
3. Generates consensus tags from reviews
4. Can be run manually or scheduled with cron
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from database import SessionLocal
from steam_service import fetch_steam_games_and_reviews
from tag_analyzer import TagAnalyzer

load_dotenv()


def run_full_pipeline(
    days_back: int = 9000,
    games_limit: int = 5,
    reviews_per_game: int = 50
):
    """
    Run the complete automation pipeline with Steam
    
    Args:
        days_back: How many days back to fetch games from Steam
        games_limit: Maximum games to fetch
        reviews_per_game: How many top reviews to get per game (max 100)
    """
    
    print("="*70)
    print("ðŸš€ GAME REVIEW AGGREGATOR - STEAM-ONLY PIPELINE")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    db = SessionLocal()
    
    try:
        # STEP 1 & 2: Fetch games and reviews from Steam
        print("\n" + "="*70)
        print("STEP 1 & 2: FETCHING GAMES & REVIEWS FROM STEAM")
        print("="*70)
        
        result = fetch_steam_games_and_reviews(
            db,
            days_back=days_back,
            games_limit=games_limit,
            reviews_per_game=reviews_per_game
        )
        
        print(f"\nâœ… Games added: {result['games']}")
        print(f"âœ… Reviews collected: {result['reviews']}")
        
        # STEP 3: Generate consensus tags
        print("\n" + "="*70)
        print("STEP 3: GENERATING CONSENSUS TAGS")
        print("="*70)
        
        analyzer = TagAnalyzer()
        analyzer.analyze_all_games(db, limit=result['games'])
        
        # Summary
        print("\n" + "="*70)
        print("ðŸ“Š PIPELINE SUMMARY")
        print("="*70)
        print(f"âœ… New games added: {result['games']}")
        print(f"âœ… Reviews scraped: {result['reviews']}")
        print(f"âœ… Games analyzed for tags: {result['games']}")
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        return {
            'success': True,
            'games_added': result['games'],
            'reviews_scraped': result['reviews'],
            'games_analyzed': result['games']
        }
        
    except Exception as e:
        print(f"\nâŒ ERROR IN PIPELINE: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}
        
    finally:
        db.close()


def run_quick_update():
    """
    Quick update mode - fetch just a few recent games
    Good for daily/hourly cron jobs
    """
    print("ðŸ”„ Running quick update (last 9000 days, 5 games max)...\n")
    return run_full_pipeline(
        days_back=9000,
        games_limit=5,
        reviews_per_game=50
    )


def run_full_update():
    """
    Full update mode - comprehensive fetch
    Good for weekly cron jobs
    """
    print("ðŸ”„ Running full update (last 90 days, 20 games max)...\n")
    return run_full_pipeline(
        days_back=90,
        games_limit=20,
        reviews_per_game=100
    )


def get_database_stats():
    """
    Print current database statistics
    """
    from models import Game, Review, Tag
    
    db = SessionLocal()
    
    try:
        total_games = db.query(Game).count()
        games_with_reviews = db.query(Game).join(Review).distinct().count()
        total_reviews = db.query(Review).count()
        total_tags = db.query(Tag).count()
        
        print("\n" + "="*70)
        print("ðŸ“Š DATABASE STATISTICS")
        print("="*70)
        print(f"Total games: {total_games}")
        print(f"Games with reviews: {games_with_reviews}")
        print(f"Total reviews: {total_reviews}")
        print(f"Total unique tags: {total_tags}")
        if games_with_reviews > 0:
            print(f"Average reviews per game: {total_reviews / games_with_reviews:.1f}")
        print("="*70)
        
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "quick":
            run_quick_update()
        elif command == "full":
            run_full_update()
        elif command == "stats":
            get_database_stats()
        else:
            print("Unknown command. Available commands:")
            print("  python automation_pipeline.py quick  # Quick update (5 recent games)")
            print("  python automation_pipeline.py full   # Full update (20 games)")
            print("  python automation_pipeline.py stats  # Show database statistics")
    else:
        # Default: show help
        print("ðŸŽ® Game Review Aggregator - Steam-Only Automation")
        print("\nAvailable commands:")
        print("  python automation_pipeline.py quick  # Quick update (5 recent games)")
        print("  python automation_pipeline.py full   # Full update (20 games)")
        print("  python automation_pipeline.py stats  # Show database statistics")
        print("\nRunning quick update by default...\n")
        run_quick_update()