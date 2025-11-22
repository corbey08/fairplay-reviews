from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
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
        "https://fairplay-reviews-m5galzts6-chris-beardwoods-projects.vercel.app",
        "https://*.vercel.app"  # Allow all Vercel preview deployments
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
            "reviews": "/games/{game_id}/reviews"
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
    Search games by name
    """
    games = db.query(Game).filter(Game.name.ilike(f"%{q}%")).limit(20).all()
    return {"query": q, "results": [{"id": g.id, "name": g.name, "cover_image": g.cover_image} for g in games]}


@app.post("/admin/fetch-games")
async def fetch_games(days_back: int = 30, db: Session = Depends(get_db)):
    """
    Admin endpoint to manually trigger fetching games from IGDB
    """
    try:
        result = fetch_and_save_recent_games(db, days_back=days_back, limit=50)
        return {
            "success": True,
            "message": f"Fetched and processed {result['total']} games",
            "details": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
