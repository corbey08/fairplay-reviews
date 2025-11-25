from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

app = FastAPI(title="Game Review Aggregator API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is working!", "status": "ok"}

@app.get("/test")
async def test():
    return {"test": "endpoint working"}

# Only try database if this endpoint is called
@app.get("/test-db")
async def test_db():
    try:
        from database import get_db
        from models import Tag
        
        db = next(get_db())
        tags = db.query(Tag).limit(5).all()
        db.close()
        
        return {
            "status": "database connected",
            "tag_count": len(tags),
            "tags": [{"id": t.id, "name": t.name} for t in tags]
        }
    except Exception as e:
        return {
            "status": "database error",
            "error": str(e),
            "error_type": type(e).__name__
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
