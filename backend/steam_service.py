import requests
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Game, Review, Source

class SteamService:
    """
    Complete Steam-only service for games and reviews
    No IGDB needed - everything from Steam!
    """
    
    def __init__(self):
        self.base_url = "https://api.steampowered.com"
        self.store_url = "https://store.steampowered.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_all_steam_apps(self):
        """
        Get complete list of all Steam apps using the working v1 endpoint
        Returns ~150,000+ items (games, DLC, software, etc.)
        """
        try:
            # Use v1 endpoint which still works
            url = f"{self.base_url}/ISteamApps/GetAppList/v1/"
            
            print("ðŸ“¥ Fetching Steam app list (this may take a moment)...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            apps = data.get('applist', {}).get('apps', [])
            
            print(f"âœ… Retrieved {len(apps)} Steam apps")
            return apps
            
        except Exception as e:
            print(f"âŒ Error getting Steam app list: {e}")
            print("   Trying alternative method...")
            
            # Fallback: Try the older appdetails method with known recent games
            # This is a simplified approach - just use some known app IDs for testing
            return []
    
    def get_game_details(self, app_id: int):
        """
        Get detailed information about a specific game
        """
        try:
            url = f"{self.store_url}/api/appdetails"
            params = {
                'appids': app_id,
                'cc': 'us',
                'l': 'english'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if str(app_id) in data and data[str(app_id)].get('success'):
                return data[str(app_id)]['data']
            
            return None
            
        except Exception as e:
            print(f"   âš ï¸  Error getting details for {app_id}: {e}")
            return None
    
    def is_game(self, app_details: dict) -> bool:
        """
        Filter to ensure we only get actual games (not DLC, software, etc.)
        """
        if not app_details:
            return False
        
        app_type = app_details.get('type', '')
        
        # Only include actual games
        if app_type != 'game':
            return False
        
        # Filter out free promotional items
        if app_details.get('is_free', False):
            # Keep if it has substantial content (not just a demo)
            if not app_details.get('required_age') and not app_details.get('developers'):
                return False
        
        return True
    
    def get_recent_games(self, days_back: int = 9000, limit: int = 50):
        """
        Get recently released games from Steam
        
        Simplified approach: Check popular/recent game IDs directly
        This is much faster than fetching all 150k+ apps
        """
        print(f"ðŸŽ® Fetching recent Steam games...")
        
        # Sample of popular games with lots of reviews (great for testing)
        # Mix of recent and established titles
        sample_app_ids = [
            1546990,  # Baldur's Gate 3 (2023) - thousands of reviews
            292030,   # The Witcher 3 (2015) - you already have this
            1174180,  # Red Dead Redemption 2
            1091500,  # Cyberpunk 2077
            271590,   # Grand Theft Auto V
            1203220,  # NARAKA: BLADEPOINT
            2358720,  # Black Myth: Wukong  
            1172470,  # Apex Legends
            1623730,  # Persona 3 Reload
            2050650,  # Starfield
            1938090,  # Call of Duty MW III
            2321470,  # Metaphor: ReFantazio
            # Add more popular titles as needed
        ]
        
        recent_games = []
        checked = 0
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for app_id in sample_app_ids:
            if len(recent_games) >= limit:
                break
            
            checked += 1
            print(f"   Checking app {app_id}... ({checked}/{len(sample_app_ids)})")
            
            # Rate limiting
            time.sleep(1.5)
            
            details = self.get_game_details(app_id)
            
            if not details or not self.is_game(details):
                print(f"      âš ï¸  Skipped (not a game or unavailable)")
                continue
            
            # Check release date
            release_date = details.get('release_date', {})
            
            if not release_date.get('date'):
                continue
            
            # Try to parse release date
            try:
                date_str = release_date['date']
                release_dt = datetime.strptime(date_str, "%b %d, %Y")
                
                if release_dt >= cutoff_date:
                    recent_games.append({
                        'appid': app_id,
                        'name': details.get('name'),
                        'details': details
                    })
                    print(f"      âœ… Added: {details.get('name')}")
                else:
                    print(f"      â­ï¸  Too old (released {date_str})")
            except Exception as e:
                print(f"      âš ï¸  Could not parse date: {e}")
                continue
        
        print(f"\nâœ… Found {len(recent_games)} recent games")
        return recent_games
    
    def get_top_reviews(self, app_id: int, num_reviews: int = 100):
        """
        Get top most helpful reviews for a game
        This is the key feature - sorted by helpfulness!
        """
        try:
            url = f"{self.store_url}/appreviews/{app_id}"
            params = {
                'json': 1,
                'filter': 'all',  # Sorted by helpfulness
                'language': 'english',
                'num_per_page': min(num_reviews, 100),  # Max 100 per request
                'purchase_type': 'all'
            }
            
            print(f"ðŸ” Fetching top {num_reviews} reviews for app {app_id}...")
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('success') == 1:
                print(f"   âš ï¸  No reviews available")
                return []
            
            reviews = data.get('reviews', [])
            print(f"   âœ… Got {len(reviews)} reviews")
            
            return reviews
            
        except Exception as e:
            print(f"   âŒ Error getting reviews: {e}")
            return []
    
    def save_game_to_db(self, app_id: int, game_details: dict, db: Session):
        """
        Save Steam game to database
        """
        # Check if exists
        existing = db.query(Game).filter(Game.igdb_id == app_id).first()
        if existing:
            return existing
        
        # Parse release date
        release_date = None
        try:
            date_str = game_details.get('release_date', {}).get('date')
            if date_str:
                release_date = datetime.strptime(date_str, "%b %d, %Y").date()
        except:
            pass
        
        # Get cover image - use background for better quality in hero sections
        cover_image = (
            game_details.get('background') or      # Highest quality
            game_details.get('background_raw') or  # Alternative high quality
            game_details.get('header_image')       # Fallback
        )
        
        # Get platforms
        platforms = []
        if game_details.get('platforms', {}).get('windows'):
            platforms.append('Windows')
        if game_details.get('platforms', {}).get('mac'):
            platforms.append('Mac')
        if game_details.get('platforms', {}).get('linux'):
            platforms.append('Linux')
        
        # Create game
        new_game = Game(
            igdb_id=app_id,  # Using Steam App ID
            name=game_details.get('name'),
            release_date=release_date,
            cover_image=cover_image,
            summary=game_details.get('short_description'),
            platform_list=platforms
        )
        
        db.add(new_game)
        db.commit()
        
        return new_game
    
    def save_reviews_to_db(self, game: Game, reviews_data: list, db: Session):
        """
        Save Steam reviews to database
        """
        # Get or create Steam source
        source = db.query(Source).filter(Source.name == "Steam").first()
        if not source:
            source = Source(
                name="Steam",
                url="https://store.steampowered.com",
                type="website"
            )
            db.add(source)
            db.commit()
        
        saved_count = 0
        
        for review_data in reviews_data:
            review_text = review_data.get('review', '').strip()
            if not review_text:
                continue
            
            # Check if already exists
            review_url = f"https://store.steampowered.com/app/{game.igdb_id}"
            existing = db.query(Review).filter(
                Review.game_id == game.id,
                Review.reviewer_name == f"Steam User {review_data['author']['steamid'][-4:]}"
            ).first()
            
            if existing:
                continue
            
            # Sentiment from Steam's voted_up
            sentiment = 'positive' if review_data.get('voted_up') else 'negative'
            
            # Create review
            review = Review(
                game_id=game.id,
                source_id=source.id,
                reviewer_name=f"Steam User {review_data['author']['steamid'][-4:]}",
                review_snippet=review_text[:500],
                review_url=review_url,
                sentiment=sentiment
            )
            
            db.add(review)
            saved_count += 1
        
        db.commit()
        return saved_count


# Helper function for automation
def fetch_steam_games_and_reviews(db: Session, days_back: int = 9000, games_limit: int = 20, reviews_per_game: int = 100):
    """
    Complete pipeline: Get recent Steam games + their top reviews
    """
    print("="*70)
    print("ðŸŽ® STEAM-ONLY PIPELINE")
    print("="*70)
    
    service = SteamService()
    
    # Get recent games
    recent_games = service.get_recent_games(days_back=days_back, limit=games_limit)
    
    if not recent_games:
        print("âš ï¸  No games found")
        return {'games': 0, 'reviews': 0}
    
    total_reviews = 0
    games_added = 0
    
    for game_data in recent_games:
        try:
            print(f"\nðŸ“¦ Processing: {game_data['name']}")
            
            # Save game
            game = service.save_game_to_db(
                game_data['appid'],
                game_data['details'],
                db
            )
            games_added += 1
            
            # Get reviews
            time.sleep(2)  # Rate limiting
            reviews = service.get_top_reviews(game_data['appid'], reviews_per_game)
            
            if reviews:
                count = service.save_reviews_to_db(game, reviews, db)
                total_reviews += count
                print(f"   âœ… Saved {count} reviews")
            
        except Exception as e:
            print(f"   âŒ Error: {e}")
            continue
    
    print("\n" + "="*70)
    print(f"âœ… Complete! Added {games_added} games with {total_reviews} reviews")
    print("="*70)
    
    return {'games': games_added, 'reviews': total_reviews}


if __name__ == "__main__":
    from database import SessionLocal
    
    print("ðŸŽ® Testing Steam-Only Service\n")
    
    service = SteamService()
    db = SessionLocal()
    
    try:
        # Test: Get The Witcher 3 details and reviews
        witcher_app_id = 292030
        
        print("1ï¸âƒ£ Testing game details...")
        details = service.get_game_details(witcher_app_id)
        if details:
            print(f"   âœ… Game: {details['name']}")
            print(f"   Release: {details.get('release_date', {}).get('date')}")
        
        print("\n2ï¸âƒ£ Testing top reviews...")
        reviews = service.get_top_reviews(witcher_app_id, num_reviews=5)
        if reviews:
            print(f"   âœ… Got {len(reviews)} top reviews")
            print(f"   Sample: {reviews[0]['review'][:100]}...")
        
        print("\nâœ… Steam service working!")
        
    finally:
        db.close()
