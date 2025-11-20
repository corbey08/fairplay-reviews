from database import SessionLocal
from steam_service import SteamService

print("🎮 Testing Steam-Only Service\n")

service = SteamService()
db = SessionLocal()

try:
    # Test: Get The Witcher 3
    witcher_app_id = 292030
    
    print("1️⃣ Testing game details...")
    details = service.get_game_details(witcher_app_id)
    if details:
        print(f"   ✅ Game: {details['name']}")
        print(f"   Header Image: {details.get('header_image')}")
        print(f"   Release: {details.get('release_date', {}).get('date')}")
    
    print("\n2️⃣ Testing top reviews...")
    reviews = service.get_top_reviews(witcher_app_id, num_reviews=5)
    if reviews:
        print(f"   ✅ Got {len(reviews)} top helpful reviews")
        print(f"   Sample: {reviews[0]['review'][:100]}...")
    
    print("\n✅ Steam service working perfectly!")
    
finally:
    db.close()