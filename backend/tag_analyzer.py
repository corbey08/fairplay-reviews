import re
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Game, Review, Tag, game_tags
from typing import List, Dict, Tuple, Set
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from textblob import TextBlob

class ImprovedTagAnalyzer:
    """
    Enhanced analyzer using RAKE and sklearn for better tag extraction
    """
    
    def __init__(self, similarity_threshold: float = 0.75):
        self.similarity_threshold = similarity_threshold
        
        # Initialize RAKE for keyword extraction
        self.rake = Rake(
            min_length=1,
            max_length=3,  # Extract phrases up to 3 words
            include_repeated_phrases=False
        )
        
        # Positive and negative indicator words for sentiment
        self.positive_indicators = {
            'great', 'amazing', 'excellent', 'fantastic', 'wonderful', 'superb',
            'outstanding', 'brilliant', 'incredible', 'awesome', 'perfect',
            'love', 'loved', 'enjoy', 'enjoyed', 'fun', 'engaging', 'addictive',
            'satisfying', 'compelling', 'immersive', 'beautiful', 'stunning',
            'gorgeous', 'solid', 'polished', 'smooth', 'fluid', 'innovative',
            'unique', 'fresh', 'rewarding', 'impressive', 'captivating'
        }
        
        self.negative_indicators = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'weak', 'lacking',
            'disappointing', 'boring', 'dull', 'tedious', 'repetitive', 'broken',
            'buggy', 'glitchy', 'clunky', 'frustrating', 'annoying', 'confusing',
            'mess', 'waste', 'avoid', 'hate', 'hated', 'worst', 'ugly',
            'dated', 'empty', 'shallow', 'overpriced', 'crash', 'unstable'
        }
        
        # Negation words that flip sentiment
        self.negations = {
            "not", "no", "never", "neither", "nobody", "nothing", 
            "nowhere", "isn't", "aren't", "wasn't", "weren't", "won't",
            "wouldn't", "don't", "doesn't", "didn't", "can't", "couldn't",
            "shouldn't", "barely", "hardly", "scarcely"
        }
        
        # Gaming aspects to focus on
        self.aspect_keywords = {
            'gameplay': ['gameplay', 'mechanics', 'controls', 'combat', 'fighting', 'action'],
            'story': ['story', 'narrative', 'plot', 'writing', 'characters', 'dialogue'],
            'graphics': ['graphics', 'visuals', 'art', 'design', 'aesthetic'],
            'performance': ['performance', 'fps', 'optimization', 'runs', 'frame'],
            'content': ['content', 'length', 'hours', 'replayability', 'endgame'],
            'difficulty': ['difficulty', 'challenging', 'hard', 'easy', 'difficult'],
            'multiplayer': ['multiplayer', 'co-op', 'pvp', 'online', 'competitive'],
            'world': ['world', 'map', 'exploration', 'open world', 'environment'],
            'sound': ['music', 'sound', 'audio', 'soundtrack', 'voice'],
            'bugs': ['bugs', 'glitches', 'crashes', 'issues', 'problems']
        }
    
    def detect_negation_context(self, text: str, keyword_pos: int, window: int = 3) -> bool:
        """
        Check if a keyword appears in a negation context
        """
        words = text.lower().split()
        keyword_idx = None
        
        # Find the keyword index
        for i, word in enumerate(words):
            if keyword_pos <= len(' '.join(words[:i+1])):
                keyword_idx = i
                break
        
        if keyword_idx is None:
            return False
        
        # Check words before the keyword within the window
        start_idx = max(0, keyword_idx - window)
        for i in range(start_idx, keyword_idx):
            if words[i] in self.negations:
                return True
        
        return False
    
    def analyze_sentiment_with_context(self, text: str, phrase: str) -> str:
        """
        Analyze sentiment of a phrase considering negation context
        Uses TextBlob for additional sentiment analysis
        """
        text_lower = text.lower()
        phrase_lower = phrase.lower()
        
        # Find phrase position in text
        phrase_pos = text_lower.find(phrase_lower)
        if phrase_pos == -1:
            return 'neutral'
        
        # Check for negation
        is_negated = self.detect_negation_context(text, phrase_pos)
        
        # Analyze the phrase and surrounding context
        context_start = max(0, phrase_pos - 50)
        context_end = min(len(text), phrase_pos + len(phrase) + 50)
        context = text[context_start:context_end]
        
        # Use TextBlob for sentiment
        blob = TextBlob(context)
        polarity = blob.sentiment.polarity
        
        # Count positive and negative indicators in phrase
        phrase_words = set(phrase_lower.split())
        positive_count = len(phrase_words & self.positive_indicators)
        negative_count = len(phrase_words & self.negative_indicators)
        
        # Determine sentiment
        if is_negated:
            # Flip the sentiment if negated
            if positive_count > negative_count or polarity > 0.1:
                return 'negative'
            elif negative_count > positive_count or polarity < -0.1:
                return 'positive'
        else:
            if positive_count > negative_count or polarity > 0.1:
                return 'positive'
            elif negative_count > positive_count or polarity < -0.1:
                return 'negative'
        
        return 'mixed'
    
    def extract_keyphrases(self, reviews: List[Review]) -> List[Tuple[str, float, str]]:
        """
        Extract key phrases from reviews using RAKE
        Returns list of (phrase, score, sentiment) tuples
        """
        all_phrases = []
        
        for review in reviews:
            text = review.review_snippet or ''
            if len(text.strip()) < 10:
                continue
            
            # Extract keywords with RAKE
            self.rake.extract_keywords_from_text(text)
            ranked_phrases = self.rake.get_ranked_phrases_with_scores()
            
            # Process top phrases from this review
            for score, phrase in ranked_phrases[:10]:  # Top 10 from each review
                # Filter out very short or very long phrases
                if len(phrase.split()) > 4 or len(phrase) < 3:
                    continue
                
                # Skip if phrase is just numbers or special characters
                if not any(c.isalpha() for c in phrase):
                    continue
                
                # Analyze sentiment with context
                sentiment = self.analyze_sentiment_with_context(text, phrase)
                
                # Only keep phrases with clear sentiment or gaming relevance
                if sentiment != 'neutral' or self.is_gaming_relevant(phrase):
                    all_phrases.append((phrase, score, sentiment))
        
        return all_phrases
    
    def is_gaming_relevant(self, phrase: str) -> bool:
        """
        Check if phrase is relevant to gaming aspects
        """
        phrase_lower = phrase.lower()
        for aspect, keywords in self.aspect_keywords.items():
            if any(keyword in phrase_lower for keyword in keywords):
                return True
        return False
    
    def normalize_and_cluster_tags(self, phrases: List[Tuple[str, float, str]], 
                                   db: Session) -> List[Tuple[str, str, float]]:
        """
        Cluster similar phrases together and normalize them
        Returns list of (normalized_tag, color, relevance_score) tuples
        """
        if not phrases:
            return []
        
        # Get existing tags from database
        existing_tags = db.query(Tag).all()
        existing_tag_names = [tag.name.lower() for tag in existing_tags]
        
        # Separate by sentiment
        phrase_by_sentiment = defaultdict(list)
        for phrase, score, sentiment in phrases:
            phrase_by_sentiment[sentiment].append((phrase, score))
        
        result_tags = []
        
        for sentiment, phrase_list in phrase_by_sentiment.items():
            if not phrase_list:
                continue
            
            phrases_only = [p[0] for p in phrase_list]
            scores = [p[1] for p in phrase_list]
            
            # Create TF-IDF vectors
            try:
                vectorizer = TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 3),
                    min_df=1
                )
                tfidf_matrix = vectorizer.fit_transform(phrases_only)
                
                # Calculate similarity matrix
                similarity_matrix = cosine_similarity(tfidf_matrix)
                
                # Cluster similar phrases
                used = set()
                clusters = []
                
                for i in range(len(phrases_only)):
                    if i in used:
                        continue
                    
                    cluster = [i]
                    used.add(i)
                    
                    for j in range(i + 1, len(phrases_only)):
                        if j not in used and similarity_matrix[i][j] > self.similarity_threshold:
                            cluster.append(j)
                            used.add(j)
                    
                    clusters.append(cluster)
                
                # For each cluster, choose the best representative phrase
                for cluster in clusters:
                    cluster_phrases = [(phrases_only[i], scores[i]) for i in cluster]
                    
                    # Sort by score and length (prefer shorter, higher scored phrases)
                    cluster_phrases.sort(key=lambda x: (-x[1], len(x[0])))
                    
                    best_phrase = cluster_phrases[0][0]
                    avg_score = sum(s for _, s in cluster_phrases) / len(cluster_phrases)
                    
                    # Normalize the phrase
                    normalized = self.normalize_phrase(best_phrase, existing_tag_names)
                    
                    # Determine color based on sentiment
                    color = self.sentiment_to_color(sentiment)
                    
                    result_tags.append((normalized, color, avg_score))
            
            except Exception as e:
                print(f"   ⚠️  Error clustering tags: {e}")
                # Fallback: just take unique phrases
                for phrase, score in phrase_list:
                    normalized = self.normalize_phrase(phrase, existing_tag_names)
                    color = self.sentiment_to_color(sentiment)
                    result_tags.append((normalized, color, score))
        
        return result_tags
    
    def normalize_phrase(self, phrase: str, existing_tags: List[str]) -> str:
        """
        Normalize phrase to match existing tags or create clean tag name
        """
        phrase = phrase.strip().title()
        
        # Check against existing tags with high similarity
        phrase_lower = phrase.lower()
        for existing in existing_tags:
            # Calculate simple word overlap
            phrase_words = set(phrase_lower.split())
            existing_words = set(existing.split())
            
            if phrase_words == existing_words:
                # Exact match, use existing
                return existing.title()
            
            # Check if one is subset of other
            if phrase_words.issubset(existing_words) or existing_words.issubset(phrase_words):
                # Use the shorter one
                return existing.title() if len(existing) < len(phrase) else phrase
        
        # Clean up the phrase
        phrase = re.sub(r'\s+', ' ', phrase)
        phrase = phrase.strip()
        
        return phrase
    
    def sentiment_to_color(self, sentiment: str) -> str:
        """Convert sentiment to tag color"""
        color_map = {
            'positive': 'green',
            'negative': 'red',
            'mixed': 'orange',
            'neutral': 'gray'
        }
        return color_map.get(sentiment, 'gray')
    
    def generate_consensus_tags(self, game: Game, db: Session, top_n: int = 6):
        """
        Generate consensus tags for a game using improved NLP methods
        """
        print(f"\n{'='*60}")
        print(f"🎮  Generating consensus tags for: {game.name}")
        print(f"{'='*60}")
        
        # Get all reviews
        reviews = db.query(Review).filter(Review.game_id == game.id).all()
        
        if not reviews:
            print(f"   ⚠️  No reviews found for {game.name}")
            return []
        
        print(f"   📊 Analyzing {len(reviews)} reviews...")
        
        # Extract key phrases
        print(f"   🔍 Extracting key phrases...")
        phrases = self.extract_keyphrases(reviews)
        
        if not phrases:
            print(f"   ⚠️  No meaningful phrases extracted")
            return []
        
        print(f"   📝 Found {len(phrases)} potential tags")
        
        # Normalize and cluster
        print(f"   🔄 Clustering similar tags...")
        normalized_tags = self.normalize_and_cluster_tags(phrases, db)
        
        # Sort by relevance score and take top N
        normalized_tags.sort(key=lambda x: x[2], reverse=True)
        top_tags = normalized_tags[:top_n]
        
        print(f"\n   📋 Top {len(top_tags)} consensus tags:")
        
        result_tags = []
        for tag_name, color, score in top_tags:
            print(f"      • {tag_name} ({color}) - score: {score:.2f}")
            
            # Get or create tag in database
            tag = db.query(Tag).filter(
                func.lower(Tag.name) == tag_name.lower()
            ).first()
            
            if not tag:
                tag = Tag(name=tag_name, color=color)
                db.add(tag)
                db.flush()  # Get the ID without committing
            
            # Link tag to game (if not already linked)
            existing_link = db.query(game_tags).filter(
                game_tags.c.game_id == game.id,
                game_tags.c.tag_id == tag.id
            ).first()
            
            if not existing_link:
                # Normalize relevance score to 0-1 range
                relevance = min(1.0, score / 10.0)
                
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
        Generate consensus tags for all games that have reviews
        """
        # Get games with reviews
        query = db.query(Game).join(Review).distinct()
        
        if limit:
            query = query.limit(limit)
        
        games = query.all()
        
        print(f"\n🎯 Found {len(games)} games to analyze")
        
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


def generate_tags_for_game(game_id: int, db: Session):
    """Helper function to generate tags for a specific game"""
    analyzer = ImprovedTagAnalyzer()
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        print(f"❌ Game with ID {game_id} not found")
        return None
    
    return analyzer.generate_consensus_tags(game, db)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from database import SessionLocal
    
    # Load environment variables from .env file
    load_dotenv()
    
    db = SessionLocal()
    
    print("🎮  Testing Improved Tag Analyzer...")
    print("\nThis will analyze reviews using RAKE and sklearn")
    print("Make sure you've run the review scraper first!\n")
    
    # Get a game that has reviews
    game = db.query(Game).join(Review).first()
    
    if game:
        analyzer = ImprovedTagAnalyzer(similarity_threshold=0.75)
        tags = analyzer.generate_consensus_tags(game, db, top_n=6)
        
        if tags:
            print(f"\n📊 Final tags for {game.name}:")
            for tag in tags:
                color_emoji = {'green': '🟢', 'orange': '🟠', 'red': '🔴', 'gray': '⚪'}
                print(f"   {color_emoji.get(tag.color, '⚪')} {tag.name} ({tag.color})")
    else:
        print("❌ No games with reviews found!")
        print("Run these commands in order:")
        print("  1. python igdb_service.py    # Fetch games")
        print("  2. python review_scraper.py  # Scrape reviews")
        print("  3. python tag_analyzer.py    # Generate tags")
    
    db.close()