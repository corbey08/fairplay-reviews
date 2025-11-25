from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime
import os

from models import Game, Tag, Review, Source, game_tags
from database import get_db
from steam_service import fetch_steam_games_and_reviews

app = FastAPI(title="Game Review Aggregator API")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://fairplayreviews.net",
        "https://www.fairplayreviews.net",
        "https://fairplay-reviews-m5galzts6-chris-beardwoods-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas for request/response validation
class TagBase(BaseModel):
    name: str
    color: str
    description: Optional[str] = None

class TagResponse(TagBase):
    id: int
    
    class Config:
        from_attributes = True

class GameBase(BaseModel):
    name: str
    release_date: Optional[date] = None
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    platform_list: Optional[List[str]] = None

class GameResponse(GameBase):
    id: int
    igdb_id: int
    tags: List[TagResponse] = []
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    reviewer_name: Optional[str] = None
    review_snippet: Optional[str] = None
    review_url: Optional[str] = None
    sentiment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    game_id: int
    published_at: Optional[date] = None
    
    class Config:
        from_attributes = True


# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Game Review Aggregator API",
        "version": "1.0.0",
        "endpoints": {
            "games": "/games",
            "game_detail": "/games/{game_id}",
            "tags": "/tags",
            "reviews": "/games/{game_id}/reviews",
            "multi_tag_search": "/games/search/multi-tag"
        }
    }

@app.get("/games", response_model=List[GameResponse])
async def get_games(
    skip: int = 0,
    limit: int = 20,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of games with optional filtering by tag
    """
    if tag:
        games = db.query(Game).join(Game.tags).filter(Tag.name == tag).offset(skip).limit(limit).all()
    else:
        games = db.query(Game).offset(skip).limit(limit).all()
    return games

@app.get("/games/search/multi-tag")
async def search_games_by_multiple_tags(
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Search games by multiple tags with include/exclude logic.
    Returns games grouped by match level.
    
    Parameters:
    - include: Comma-separated list of tag names that should be included
    - exclude: Comma-separated list of tag names that should be excluded
    
    Returns games organized by how many of the included tags they match.
    """
    if not include:
        return {"error": "At least one tag to include is required", "results": {}}
    
    # Parse tag lists
    included_tags = [t.strip() for t in include.split(',') if t.strip()]
    excluded_tags = [t.strip() for t in exclude.split(',') if t.strip()] if exclude else []
    
    if not included_tags:
        return {"error": "At least one tag to include is required", "results": {}}
    
    # Get tag IDs for included and excluded tags
    included_tag_objects = db.query(Tag).filter(Tag.name.in_(included_tags)).all()
    excluded_tag_objects = db.query(Tag).filter(Tag.name.in_(excluded_tags)).all() if excluded_tags else []
    
    included_tag_ids = [t.id for t in included_tag_objects]
    excluded_tag_ids = [t.id for t in excluded_tag_objects]
    
    if not included_tag_ids:
        return {"error": "No valid tags found", "results": {}}
    
    # First, get all games that have at least one of the included tags
    # and don't have any of the excluded tags
    query = db.query(
        Game.id,
        Game.igdb_id,
        Game.name,
        Game.release_date,
        Game.cover_image,
        Game.summary,
        Game.platform_list,
        Game.created_at,
        func.count(game_tags.c.tag_id).label('matching_tags_count')
    ).join(
        game_tags, Game.id == game_tags.c.game_id
    ).filter(
        game_tags.c.tag_id.in_(included_tag_ids)
    ).group_by(
        Game.id,
        Game.igdb_id,
        Game.name,
        Game.release_date,
        Game.cover_image,
        Game.summary,
        Game.platform_list,
        Game.created_at
    )
    
    games_with_counts = query.all()
    
    # Filter out games that have excluded tags
    if excluded_tag_ids:
        games_with_excluded = db.query(game_tags.c.game_id).filter(
            game_tags.c.tag_id.in_(excluded_tag_ids)
        ).distinct().all()
        excluded_game_ids = {g[0] for g in games_with_excluded}
        games_with_counts = [g for g in games_with_counts if g.id not in excluded_game_ids]
    
    # Organize games by match level
    total_required = len(included_tag_ids)
    results_by_match_level = {}
    
    for game_data in games_with_counts:
        matches = int(game_data.matching_tags_count)
        missing = total_required - matches
        
        if missing not in results_by_match_level:
            results_by_match_level[missing] = []
        
        # Get full game object with tags
        game = db.query(Game).filter(Game.id == game_data.id).first()
        
        results_by_match_level[missing].append({
            "id": game.id,
            "igdb_id": game.igdb_id,
            "name": game.name,
            "release_date": game.release_date,
            "cover_image": game.cover_image,
            "summary": game.summary,
            "platform_list": game.platform_list,
            "tags": [{"id": t.id, "name": t.name, "color": t.color} for t in game.tags],
            "matching_tags": matches,
            "missing_tags": missing
        })
    
    # Sort each group by name
    for key in results_by_match_level:
        results_by_match_level[key].sort(key=lambda x: x['name'])
    
    return {
        "included_tags": included_tags,
        "excluded_tags": excluded_tags,
        "total_required_tags": total_required,
        "results": results_by_match_level
    }

@app.get("/games/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific game
    """
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.get("/games/{game_id}/reviews", response_model=List[ReviewResponse])
async def get_game_reviews(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a specific game
    """
    reviews = db.query(Review).filter(Review.game_id == game_id).all()
    return reviews

@app.get("/tags", response_model=List[TagResponse])
async def get_tags(db: Session = Depends(get_db)):
    """
    Get all available tags
    """
    tags = db.query(Tag).all()
    return tags

@app.get("/search")
async def search_games(q: str, db: Session = Depends(get_db)):
    """
    Search games by name with smart matching (handles abbreviations)
    """
    if not q or len(q.strip()) < 2:
        return {"query": q, "results": []}
    
    query_lower = q.lower().strip()
    
    # Common game abbreviations
    abbreviations = {
        'gta': 'grand theft auto',
        'rdr': 'red dead redemption',
        'cod': 'call of duty',
        'csgo': 'counter strike',
        'cs': 'counter strike',
        'gow': 'god of war',
        'tlou': 'the last of us',
        'botw': 'breath of the wild',
        'totk': 'tears of the kingdom',
        'bg3': 'baldur\'s gate 3',
        'tw3': 'the witcher 3',
        'rdr2': 'red dead redemption 2',
        'gta5': 'grand theft auto v',
        'gtav': 'grand theft auto v',
    }
    
    # Check if query is an abbreviation
    search_term = abbreviations.get(query_lower, query_lower)
    
    # Search for games
    games = db.query(Game).filter(
        Game.name.ilike(f"%{search_term}%")
    ).limit(20).all()
    
    return {
        "query": q,
        "results": [
            {
                "id": g.id,
                "name": g.name,
                "cover_image": g.cover_image,
                "release_date": g.release_date,
                "summary": g.summary,
                "tags": [{"id": t.id, "name": t.name, "color": t.color} for t in g.tags] if g.tags else []
            }
            for g in games
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
