"""
Improved Smart Tag Analyzer using Sentence Transformers
Analyzes Steam reviews to extract consensus tags using semantic similarity
"""

import re
import os
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Game, Review, Tag, game_tags
from typing import List, Tuple, Dict, Optional
import numpy as np
from dataclasses import dataclass

# Sentence transformers for semantic similarity (lightweight, works on CPU)
try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Run: pip install sentence-transformers")

# Optional: Claude API for LLM enhancement
try:
    import anthropic
    ANTHROPIC_AVAILABLE = bool(os.getenv('ANTHROPIC_API_KEY'))
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class TagDefinition:
    """Structured tag definition with semantic examples"""
    name: str
    color: str
    category: str  # 'positive', 'negative', 'neutral'
    keywords: List[str]
    semantic_examples: List[str]  # Full sentence examples for better matching


class ImprovedTagAnalyzer:
    """
    Advanced tag analyzer using semantic similarity and optional LLM enhancement
    """
    
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm and ANTHROPIC_AVAILABLE
        self.model = None
        self.tag_embeddings = None
        
        # Initialize sentence transformer model (small, CPU-friendly)
        if TRANSFORMERS_AVAILABLE:
            print("🔄 Loading sentence transformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')  # 80MB, fast
            print("✅ Model loaded")
        
        # Define comprehensive tag taxonomy
        self.tags = self._define_tags()
        
        # Pre-compute embeddings for tag definitions
        if self.model:
            self._precompute_tag_embeddings()
    
    def _define_tags(self) -> List[TagDefinition]:
        """Define all possible tags with semantic examples"""
        return [
            # POSITIVE TAGS (10)
            TagDefinition(
                name="Amazing Graphics",
                color="green",
                category="positive",
                keywords=['graphics', 'visuals', 'beautiful', 'stunning', 'gorgeous'],
                semantic_examples=[
                    "The graphics are absolutely breathtaking",
                    "Visual quality is top-notch",
                    "One of the most beautiful games I've ever seen"
                ]
            ),
            TagDefinition(
                name="Compelling Story",
                color="green",
                category="positive",
                keywords=['story', 'narrative', 'plot', 'characters', 'writing'],
                semantic_examples=[
                    "The storyline kept me hooked from start to finish",
                    "Character development is excellent",
                    "Narrative is engaging and well-written"
                ]
            ),
            TagDefinition(
                name="Addictive Gameplay",
                color="green",
                category="positive",
                keywords=['gameplay', 'fun', 'addictive', 'engaging', 'mechanics'],
                semantic_examples=[
                    "Can't stop playing this game",
                    "Gameplay loop is incredibly satisfying",
                    "Core mechanics are polished and fun"
                ]
            ),
            TagDefinition(
                name="Excellent Combat",
                color="green",
                category="positive",
                keywords=['combat', 'fighting', 'action', 'battles'],
                semantic_examples=[
                    "Combat system feels great",
                    "Fighting mechanics are fluid and responsive",
                    "Boss battles are challenging and rewarding"
                ]
            ),
            TagDefinition(
                name="Immersive World",
                color="green",
                category="positive",
                keywords=['world', 'immersive', 'atmosphere', 'environment'],
                semantic_examples=[
                    "The world feels alive and detailed",
                    "Atmosphere is incredible",
                    "Love exploring every corner of this world"
                ]
            ),
            TagDefinition(
                name="Great Value",
                color="green",
                category="positive",
                keywords=['content', 'hours', 'value', 'worth', 'playtime'],
                semantic_examples=[
                    "Tons of content for the price",
                    "Already have 100 hours and still finding new things",
                    "Great value for money"
                ]
            ),
            TagDefinition(
                name="Fun Multiplayer",
                color="green",
                category="positive",
                keywords=['multiplayer', 'coop', 'online', 'friends'],
                semantic_examples=[
                    "Playing with friends is a blast",
                    "Multiplayer is where this game really shines",
                    "Co-op mode is incredibly fun"
                ]
            ),
            TagDefinition(
                name="Runs Smoothly",
                color="green",
                category="positive",
                keywords=['optimized', 'performance', 'smooth', 'stable'],
                semantic_examples=[
                    "Runs perfectly on my system",
                    "No performance issues whatsoever",
                    "Great optimization, solid 60fps"
                ]
            ),
            TagDefinition(
                name="Great Soundtrack",
                color="green",
                category="positive",
                keywords=['music', 'soundtrack', 'audio', 'sound'],
                semantic_examples=[
                    "The music is absolutely phenomenal",
                    "Soundtrack perfectly matches the atmosphere",
                    "Audio design is top tier"
                ]
            ),
            TagDefinition(
                name="High Replayability",
                color="green",
                category="positive",
                keywords=['replay', 'replayability', 'multiple', 'variety'],
                semantic_examples=[
                    "Each playthrough feels different",
                    "So much replay value",
                    "Keep coming back for more"
                ]
            ),
            
            # NEGATIVE TAGS (12)
            TagDefinition(
                name="Buggy/Broken",
                color="red",
                category="negative",
                keywords=['bugs', 'glitches', 'crashes', 'broken', 'issues'],
                semantic_examples=[
                    "Game crashes constantly",
                    "Encountered so many bugs",
                    "Broken mechanics ruin the experience"
                ]
            ),
            TagDefinition(
                name="Poor Graphics",
                color="red",
                category="negative",
                keywords=['ugly', 'dated', 'bad graphics', 'outdated'],
                semantic_examples=[
                    "Graphics look like they're from 2005",
                    "Visually very disappointing",
                    "Art style is unappealing"
                ]
            ),
            TagDefinition(
                name="Repetitive/Boring",
                color="red",
                category="negative",
                keywords=['boring', 'repetitive', 'tedious', 'dull'],
                semantic_examples=[
                    "Gets boring after a few hours",
                    "Same thing over and over",
                    "Extremely repetitive gameplay"
                ]
            ),
            TagDefinition(
                name="Weak Story",
                color="red",
                category="negative",
                keywords=['bad story', 'weak story', 'boring story'],
                semantic_examples=[
                    "Story is forgettable",
                    "Narrative makes no sense",
                    "Characters are poorly written"
                ]
            ),
            TagDefinition(
                name="Performance Issues",
                color="red",
                category="negative",
                keywords=['fps', 'lag', 'stuttering', 'optimization'],
                semantic_examples=[
                    "Terrible frame rate issues",
                    "Constant stuttering",
                    "Poorly optimized"
                ]
            ),
            TagDefinition(
                name="Too Short",
                color="red",
                category="negative",
                keywords=['short', 'not enough content', 'lack of content'],
                semantic_examples=[
                    "Finished in 3 hours",
                    "Way too short for the price",
                    "Barely any content"
                ]
            ),
            TagDefinition(
                name="Overpriced",
                color="red",
                category="negative",
                keywords=['overpriced', 'expensive', 'not worth'],
                semantic_examples=[
                    "Not worth the asking price",
                    "Way too expensive for what you get",
                    "Wait for a sale"
                ]
            ),
            TagDefinition(
                name="Pay-to-Win",
                color="red",
                category="negative",
                keywords=['pay to win', 'p2w', 'microtransactions', 'cash grab'],
                semantic_examples=[
                    "Aggressive microtransactions everywhere",
                    "Pay to win mechanics ruin it",
                    "Feels like a cash grab"
                ]
            ),
            TagDefinition(
                name="Bad Controls",
                color="red",
                category="negative",
                keywords=['controls', 'clunky', 'unresponsive'],
                semantic_examples=[
                    "Controls feel terrible",
                    "Clunky and unresponsive",
                    "Controller support is awful"
                ]
            ),
            TagDefinition(
                name="Grindy",
                color="red",
                category="negative",
                keywords=['grind', 'grinding', 'grindy'],
                semantic_examples=[
                    "Way too much grinding",
                    "Progress feels like a chore",
                    "Extremely grindy"
                ]
            ),
            TagDefinition(
                name="Dead Multiplayer",
                color="red",
                category="negative",
                keywords=['dead', 'no players', 'empty servers'],
                semantic_examples=[
                    "Can't find any matches",
                    "Multiplayer is completely dead",
                    "No one plays this anymore"
                ]
            ),
            TagDefinition(
                name="Unfair Difficulty",
                color="red",
                category="negative",
                keywords=['unfair', 'too hard', 'frustrating'],
                semantic_examples=[
                    "Difficulty feels cheap and unfair",
                    "Frustratingly hard for the wrong reasons",
                    "Artificial difficulty ruins it"
                ]
            ),
            
            # NEUTRAL/MIXED TAGS (5)
            TagDefinition(
                name="Challenging",
                color="orange",
                category="neutral",
                keywords=['difficult', 'hard', 'challenging'],
                semantic_examples=[
                    "Very challenging but fair",
                    "Difficult game that rewards skill",
                    "Hard but satisfying"
                ]
            ),
            TagDefinition(
                name="Unique Concept",
                color="orange",
                category="neutral",
                keywords=['unique', 'innovative', 'original', 'different'],
                semantic_examples=[
                    "Really unique gameplay idea",
                    "Haven't seen anything like this before",
                    "Innovative mechanics"
                ]
            ),
            TagDefinition(
                name="Great for Kids",
                color="orange",
                category="neutral",
                keywords=['kids', 'family', 'children', 'casual'],
                semantic_examples=[
                    "Perfect for playing with kids",
                    "Family-friendly content",
                    "Great for younger players"
                ]
            ),
            TagDefinition(
                name="Niche Appeal",
                color="orange",
                category="neutral",
                keywords=['niche', 'specific', 'fans'],
                semantic_examples=[
                    "Only for hardcore fans of the genre",
                    "Very niche appeal",
                    "You'll know if this is for you"
                ]
            ),
            TagDefinition(
                name="Mixed Experience",
                color="orange",
                category="neutral",
                keywords=['mixed', 'some good', 'some bad'],
                semantic_examples=[
                    "Has potential but also issues",
                    "Some great parts, some not so great",
                    "Your mileage may vary"
                ]
            ),
        ]
    
    def _precompute_tag_embeddings(self):
        """Pre-compute embeddings for all tag definitions"""
        print("🔄 Computing tag embeddings...")
        
        # Create comprehensive text for each tag
        tag_texts = []
        for tag in self.tags:
            # Combine name, keywords, and examples for better matching
            text = f"{tag.name}. {' '.join(tag.keywords)}. {' '.join(tag.semantic_examples)}"
            tag_texts.append(text)
        
        self.tag_embeddings = self.model.encode(tag_texts, show_progress_bar=False)
        print(f"✅ Computed embeddings for {len(self.tags)} tags")
    
    def analyze_review_semantic(self, review_text: str, threshold: float = 0.35) -> List[Tuple[str, str, float]]:
        """
        Analyze review using semantic similarity
        Returns: [(tag_name, color, similarity_score), ...]
        """
        if not self.model or not review_text or len(review_text.strip()) < 10:
            return []
        
        # Encode the review
        review_embedding = self.model.encode([review_text])[0]
        
        # Calculate similarity with all tags
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity([review_embedding], self.tag_embeddings)[0]
        
        # Get matches above threshold
        matches = []
        for i, score in enumerate(similarities):
            if score >= threshold:
                tag = self.tags[i]
                matches.append((tag.name, tag.color, float(score)))
        
        # Sort by similarity score
        matches.sort(key=lambda x: x[2], reverse=True)
        
        return matches
    
    def analyze_batch_with_llm(self, reviews: List[str], game_name: str) -> Dict[str, List[str]]:
        """
        Use Claude API to analyze a batch of reviews (optional enhancement)
        Returns: {tag_name: [supporting_quotes], ...}
        """
        if not self.use_llm or not ANTHROPIC_AVAILABLE:
            return {}
        
        try:
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
            # Sample reviews if too many
            sample_reviews = reviews[:30] if len(reviews) > 30 else reviews
            reviews_text = "\n\n".join([f"Review {i+1}: {r}" for i, r in enumerate(sample_reviews)])
            
            # Available tags for the LLM
            available_tags = [tag.name for tag in self.tags]
            
            prompt = f"""Analyze these Steam reviews for "{game_name}" and identify the strongest consensus themes.

Available tags: {', '.join(available_tags)}

Reviews:
{reviews_text}

Return a JSON object with tags as keys and lists of brief supporting quotes as values. Only include tags mentioned by multiple reviews. Example:
{{"Amazing Graphics": ["breathtaking visuals", "looks stunning"], "Buggy/Broken": ["crashes often", "game-breaking bugs"]}}"""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            import json
            response_text = message.content[0].text
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            
            return json.loads(response_text)
            
        except Exception as e:
            print(f"⚠️  LLM analysis failed: {e}")
            return {}
    
    def _resolve_tag_conflicts(self, tag_scores: dict) -> dict:
        """
        Remove conflicting tags, keeping the one with higher score
        """
        # Define conflicting tag pairs
        conflicts = [
            ('Amazing Graphics', 'Poor Graphics'),
            ('Compelling Story', 'Weak Story'),
            ('Runs Smoothly', 'Performance Issues'),
            ('Great Value', 'Overpriced'),
            ('Fun Multiplayer', 'Dead Multiplayer'),
            ('Addictive Gameplay', 'Repetitive/Boring'),
        ]
        
        resolved_scores = dict(tag_scores)
        
        for tag1, tag2 in conflicts:
            if tag1 in resolved_scores and tag2 in resolved_scores:
                score1 = resolved_scores[tag1]['final_score']
                score2 = resolved_scores[tag2]['final_score']
                
                # Remove the weaker one
                if score1 > score2:
                    print(f"   ⚖️  Conflict: Keeping '{tag1}' over '{tag2}' ({score1:.3f} vs {score2:.3f})")
                    del resolved_scores[tag2]
                else:
                    print(f"   ⚖️  Conflict: Keeping '{tag2}' over '{tag1}' ({score2:.3f} vs {score1:.3f})")
                    del resolved_scores[tag1]
        
        return resolved_scores
    
    def generate_consensus_tags(self, game: Game, db: Session, top_n: int = 5):
        """
        Generate consensus tags for a game using semantic similarity
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
        
        if not TRANSFORMERS_AVAILABLE:
            print(f"   ⚠️  sentence-transformers not available, skipping")
            return []
        
        # Accumulate tag scores across all reviews
        tag_scores = defaultdict(lambda: {
            'color': '',
            'total_score': 0.0,
            'count': 0,
            'max_score': 0.0
        })
        
        review_texts = []
        for review in reviews:
            text = review.review_snippet or ''
            if len(text.strip()) < 10:
                continue
            
            review_texts.append(text)
            matches = self.analyze_review_semantic(text)
            
            for tag_name, color, score in matches:
                tag_scores[tag_name]['color'] = color
                tag_scores[tag_name]['total_score'] += score
                tag_scores[tag_name]['count'] += 1
                tag_scores[tag_name]['max_score'] = max(
                    tag_scores[tag_name]['max_score'], 
                    score
                )
        
        # Optional: Enhance with LLM analysis
        if self.use_llm and len(review_texts) > 0:
            print(f"   🤖 Running LLM analysis...")
            llm_tags = self.analyze_batch_with_llm(review_texts, game.name)
            
            # Boost scores for LLM-confirmed tags
            for tag_name in llm_tags.keys():
                if tag_name in tag_scores:
                    tag_scores[tag_name]['count'] += 5  # Boost
                    print(f"      🎯 LLM confirmed: {tag_name}")
        
        if not tag_scores:
            print(f"   ⚠️  No matching tags found")
            return []
        
        # Calculate final relevance score
        for tag_name, data in tag_scores.items():
            # Weighted score: frequency × average similarity
            frequency = data['count'] / len(reviews)
            avg_similarity = data['total_score'] / data['count']
            data['final_score'] = frequency * avg_similarity
        
        # Resolve conflicts BEFORE selecting top tags
        tag_scores = self._resolve_tag_conflicts(tag_scores)
        
        # Sort by final score
        sorted_tags = sorted(
            tag_scores.items(),
            key=lambda x: x[1]['final_score'],
            reverse=True
        )[:top_n]
        
        print(f"\n   📋 Top {len(sorted_tags)} consensus tags:")
        
        result_tags = []
        for tag_name, data in sorted_tags:
            count = data['count']
            color = data['color']
            percentage = (count / len(reviews)) * 100
            relevance = data['final_score']
            
            print(f"      • {tag_name} ({color}) - {count} reviews ({percentage:.1f}%) - score: {relevance:.3f}")
            
            # Get or create tag
            tag = db.query(Tag).filter(
                func.lower(Tag.name) == tag_name.lower()
            ).first()
            
            if not tag:
                tag = Tag(name=tag_name, color=color)
                db.add(tag)
                db.flush()
            
            # Link to game if not already linked
            existing_link = db.query(game_tags).filter(
                game_tags.c.game_id == game.id,
                game_tags.c.tag_id == tag.id
            ).first()
            
            if not existing_link:
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
    
    def analyze_all_games(self, db: Session, limit: Optional[int] = None):
        """
        Generate tags for all games with reviews
        """
        query = db.query(Game).join(Review).distinct()
        
        if limit:
            query = query.limit(limit)
        
        games = query.all()
        
        print(f"\n🎮 Found {len(games)} games to analyze")
        print(f"🔧 Using semantic similarity: {TRANSFORMERS_AVAILABLE}")
        print(f"🤖 Using LLM enhancement: {self.use_llm}")
        
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


# Example usage
if __name__ == "__main__":
    from database import SessionLocal
    
    # Initialize analyzer
    # Set use_llm=True if you have ANTHROPIC_API_KEY set
    analyzer = ImprovedTagAnalyzer(use_llm=False)
    
    # Analyze all games
    db = SessionLocal()
    try:
        analyzer.analyze_all_games(db, limit=None)
    finally:
        db.close()

