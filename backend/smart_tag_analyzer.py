import re
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Game, Review, Tag, game_tags
from typing import List, Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SmartTagAnalyzer:
    """
    Uses predefined clean tags but matches them to varied review language
    """
    
    def __init__(self):
        # Define clean tag names and their related phrases
        self.tag_categories = {
            'Great Graphics': [
                'graphics', 'visuals', 'looks', 'beautiful', 'gorgeous', 'stunning',
                'art style', 'art', 'realistic', 'pretty', 'amazing visuals',
                'eye candy', 'visual quality', 'textures', 'lighting', 'details'
            ],
            'Great Story': [
                'story', 'narrative', 'plot', 'characters', 'writing', 'dialogue',
                'storyline', 'campaign', 'lore', 'character development', 'emotional',
                'storytelling', 'script', 'voice acting'
            ],
            'Fun Gameplay': [
                'gameplay', 'fun', 'enjoyable', 'entertaining', 'addictive', 'engaging',
                'mechanics', 'controls', 'playable', 'satisfying', 'great game',
                'well designed', 'polished', 'smooth'
            ],
            'Great Combat': [
                'combat', 'fighting', 'action', 'battles', 'gunplay', 'weapons',
                'enemies', 'boss fights', 'fluid combat', 'satisfying combat'
            ],
            'Immersive World': [
                'world', 'immersive', 'atmosphere', 'environment', 'map', 'exploration',
                'open world', 'detailed world', 'living world', 'setting', 'ambient'
            ],
            'Lots of Content': [
                'content', 'hours', 'playtime', 'replayability', 'replay value',
                'things to do', 'activities', 'quests', 'missions', 'side content'
            ],
            'Great Multiplayer': [
                'multiplayer', 'co-op', 'online', 'pvp', 'friends', 'competitive',
                'coop', 'community', 'with friends'
            ],
            'Well Optimized': [
                'optimized', 'performance', 'runs well', 'smooth', 'fps',
                'no lag', 'stable', 'well optimized'
            ],
            'Buggy': [
                'bugs', 'glitches', 'crashes', 'broken', 'buggy', 'issues',
                'problems', 'freezes', 'errors', 'unstable', 'glitchy'
            ],
            'Poor Graphics': [
                'ugly', 'dated', 'bad graphics', 'poor visuals', 'outdated',
                'looks old', 'bad art'
            ],
            'Boring': [
                'boring', 'dull', 'tedious', 'repetitive', 'monotonous',
                'uninteresting', 'bland', 'stale'
            ],
            'Bad Story': [
                'bad story', 'weak story', 'poor writing', 'boring story',
                'confusing', 'doesn\'t make sense', 'weak narrative'
            ],
            'Poor Performance': [
                'poor performance', 'low fps', 'frame drops', 'stuttering',
                'optimization issues', 'runs badly', 'lag'
            ],
            'Too Short': [
                'short', 'not enough content', 'lack of content', 'empty',
                'shallow', 'limited content'
            ],
            'Overpriced': [
                'overpriced', 'expensive', 'not worth', 'too much money',
                'rip off', 'cash grab', 'greedy'
            ]
        }
        
        # Map tags to colors
        self.tag_colors = {
            'Great Graphics': 'green',
            'Great Story': 'green',
            'Fun Gameplay': 'green',
            'Great Combat': 'green',
            'Immersive World': 'green',
            'Lots of Content': 'green',
            'Great Multiplayer': 'green',
            'Well Optimized': 'green',
            'Buggy': 'red',
            'Poor Graphics': 'red',
            'Boring': 'red',
            'Bad Story': 'red',
            'Poor Performance': 'red',
            'Too Short': 'red',
            'Overpriced': 'red'
        }
    
    def find_matching_tags(self, review_text: str) -> List[Tuple[str, str, float]]:
        """
        Find which predefined tags match this review text
        Returns list of (tag_name, color, relevance_score)
        """
        text_lower = review_text.lower()
        matches = []
        
        for tag_name, keywords in self.tag_categories.items():
            # Count how many related keywords appear
            match_count = 0
            for keyword in keywords:
                if keyword in text_lower:
                    match_count += 1
            
            if match_count > 0:
                # Calculate relevance (more keyword matches = higher relevance)
                relevance = match_count / len(keywords)
                color = self.tag_colors.get(tag_name, 'gray')
                matches.append((tag_name, color, relevance))
        
        return matches
    
    def generate_consensus_tags(self, game: Game, db: Session, top_n: int = 5):
        """
        Generate consensus tags for a game based on its reviews
        """
        print(f"\n{'='*60}")
        print(f"🏷️  Generating consensus tags for: {game.name}")
        print(f"{'='*60}")
        
        # Get all reviews
        reviews = db.query(Review).filter(Review.game_id == game.id).all()
        
        if not reviews:
            print(f"   ⚠️  No reviews found")
            return []
        
        print(f"   📊 Analyzing {len(reviews)} reviews...")
        
        # Accumulate tag scores across all reviews
        tag_scores = defaultdict(lambda: {'color': '', 'score': 0.0, 'count': 0})
        
        for review in reviews:
            text = review.review_snippet or ''
            if len(text.strip()) < 10:
                continue
            
            matches = self.find_matching_tags(text)
            for tag_name, color, relevance in matches:
                tag_scores[tag_name]['color'] = color
                tag_scores[tag_name]['score'] += relevance
                tag_scores[tag_name]['count'] += 1
        
        if not tag_scores:
            print(f"   ⚠️  No matching tags found")
            return []
        
        # Sort by frequency (how many reviews mentioned it)
        sorted_tags = sorted(
            tag_scores.items(),
            key=lambda x: (x[1]['count'], x[1]['score']),
            reverse=True
        )[:top_n]
        
        print(f"\n   📋 Top {len(sorted_tags)} consensus tags:")
        
        result_tags = []
        for tag_name, data in sorted_tags:
            count = data['count']
            color = data['color']
            percentage = (count / len(reviews)) * 100
            
            print(f"      • {tag_name} ({color}) - {count} reviews ({percentage:.1f}%)")
            
            # Get or create tag
            tag = db.query(Tag).filter(
                func.lower(Tag.name) == tag_name.lower()
            ).first()
            
            if not tag:
                tag = Tag(name=tag_name, color=color)
                db.add(tag)
                db.flush()
            
            # Link to game
            existing_link = db.query(game_tags).filter(
                game_tags.c.game_id == game.id,
                game_tags.c.tag_id == tag.id
            ).first()
            
            if not existing_link:
                relevance = count / len(reviews)
                stmt = game_tags.insert().values(
                    game_id=game.id,
                    tag_id=tag.id,
                    relevance_score=relevance
                )
                db.execute(stmt)
            
            result_tags.append(tag)
        
        db.commit()
        print(f"\n   ✅ Successfully tagged {game.name}")
        
        return result_tags
    
    def analyze_all_games(self, db: Session, limit: int = None):
        """
        Generate tags for all games with reviews
        """
        query = db.query(Game).join(Review).distinct()
        
        if limit:
            query = query.limit(limit)
        
        games = query.all()
        
        print(f"\n🎮 Found {len(games)} games to analyze")
        
        for i, game in enumerate(games, 1):
            try:
                print(f"\n[{i}/{len(games)}]")
                self.generate_consensus_tags(game, db)
            except Exception as e:
                print(f"❌ Error analyzing {game.name}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\n{'='*60}")
        print(f"✅ Tag analysis complete!")
        print(f"{'='*60}")