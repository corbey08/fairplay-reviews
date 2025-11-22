from database import SessionLocal, engine
from models import Base, Game, Review, Tag, Source

print("🗑️  Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("✅ All tables dropped")

print("🔨 Recreating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables recreated")

db = SessionLocal()
game_count = db.query(Game).count()
print(f"📊 Games in database: {game_count}")
db.close()

if game_count == 0:
    print("✅ Database is clean! Ready to populate with Steam data.")
else:
    print(f"⚠️  Warning: Still {game_count} games in database")