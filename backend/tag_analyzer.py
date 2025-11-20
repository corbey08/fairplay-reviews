import re
from collections import Counter
from sqlalchemy.orm import Session
from models import Game, Review, Tag, game_tags
from typing import List, Dict, Tuple

class TagAnalyzer:
    """
    Analyze reviews to extract consensus tags with sentiment
    """
    
    def __init__(self):
        # Common positive gaming terms
        self.positive_keywords = {
            'gameplay': ['engaging gameplay', 'fun gameplay', 'addictive gameplay', 'great gameplay', 
                        'solid gameplay', 'satisfying gameplay', 'excellent gameplay'],
            'graphics': ['stunning visuals', 'beautiful graphics', 'gorgeous visuals', 'great graphics',
                        'amazing graphics', 'impressive visuals', 'stunning graphics'],
            'story': ['compelling story', 'great story', 'engaging narrative', 'amazing story',
                     'captivating story', 'well-written', 'emotional story'],
            'combat': ['satisfying combat', 'great combat', 'fun combat', 'excellent combat',
                      'smooth combat', 'fluid combat'],
            'world': ['massive open world', 'beautiful world', 'immersive world', 'huge world',
                     'detailed world', 'rich world'],
            'content': ['tons of content', 'lots of content', 'plenty of content', 'hours of content'],
            'difficulty': ['challenging', 'rewarding difficulty', 'tough but fair'],
            'multiplayer': ['great multiplayer', 'fun multiplayer', 'excellent co-op'],
            'innovation': ['innovative', 'unique', 'fresh', 'original'],
            'polish': ['polished', 'well-made', 'refined', 'quality']
        }
        
        # Common negative gaming terms
        self.negative_keywords = {
            'bugs': ['buggy', 'glitchy', 'broken', 'crashes', 'unstable', 'technical issues'],
            'gameplay': ['boring gameplay', 'repetitive gameplay', 'tedious', 'dull gameplay'],
            'graphics': ['poor graphics', 'dated visuals', 'ugly graphics', 'bad graphics'],
            'story': ['weak story', 'poor writing', 'confusing story', 'boring story', 
                     'bad narrative', 'forced themes', 'poorly written'],
            'combat': ['clunky combat', 'poor combat', 'frustrating combat', 'bad controls'],
            'performance': ['poor performance', 'frame drops', 'low fps', 'optimization issues'],
            'content': ['lack of content', 'too short', 'not enough content', 'empty world'],
            'price': ['overpriced', 'not worth the price', 'too expensive'],
            'design': ['poor design', 'bad design choices', 'frustrating design'],
            'monetization': ['pay to win', 'microtransactions', 'greedy', 'cash grab']
        }
        
        # Mixed/neutral terms
        self.mixed_keywords = {
            'difficulty': ['very difficult', 'extremely hard', 'brutal difficulty', 'punishing'],
            'length': ['short', 'lengthy', 'long campaign'],
            'learning': ['steep learning curve', 'complex systems'],
            'niche': ['niche appeal', 'not for everyone', 'acquired taste']
        }
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Determine if text is positive, negative, or mixed
        """
        text_lower = text.lower()
        
        positive_count = 0
        negative_count = 0
        
        # Count positive matches
        for category, keywords in self.positive_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    positive_count += 1
        
        # Count negative matches
        for category, keywords in self.negative_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    negative_count += 1
        
        # Simple sentiment determination
        if positive_count > negative_count * 1.5:
            return 'positive'
        elif negative_count > positive_count * 1.5:
            return 'negative'
        else:
            return 'mixed'
    
    def extract_tags_from_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract tag phrases from review text
        Returns list of (tag_text, sentiment) tuples
        """
        text_lower = text.lower()
        found_tags = []
        
        # Check positive keywords
        for category, keywords in self.positive_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Clean up the keyword into a tag
                    tag_name = keyword.title()
                    found_tags.append((tag_name, 'green'))
        
        # Check negative keywords
        for category, keywords in self.negative_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    tag_name = keyword.title()
                    found_tags.append((tag_name, 'red'))
        
        # Check mixed keywords
        for category, keywords in self.mixed_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    tag_name = keyword.title()
                    found_tags.append((tag_name, 'orange'))
        
        return found_tags
    
    def generate_consensus_tags(self, game: Game, db: Session, top_n: int = 4):
        """
        Generate top consensus tags for a game based on its reviews
        """
        print(f"\n{'='*60}")
        print(f"ðŸ·ï¸  Generating consensus tags for: {game.name}")
        print(f"{'='*60}")
        
        # Get all reviews for this game
        reviews = db.query(Review).filter(Review.game_id == game.id).all()
        
        if not reviews:
            print(f"   âš ï¸  No reviews found for {game.name}")
            return []
        
        print(f"   ðŸ“Š Analyzing {len(reviews)} reviews...")
        
        # Update sentiment for each review
        for review in reviews:
            if not review.sentiment:
                review.sentiment = self.analyze_sentiment(review.review_snippet or '')
        
        db.commit()
        
        # Extract all tags from all reviews
        all_tags = []
        for review in reviews:
            review_text = review.review_snippet or ''
            tags = self.extract_tags_from_text(review_text)
            all_tags.extend(tags)
        
        if not all_tags:
            print(f"   âš ï¸  No tags could be extracted from reviews")
            return []
        
        # Count tag occurrences
        tag_counter = Counter(all_tags)
        
        # Get top N most common tags
        top_tags = tag_counter.most_common(top_n)
        
        print(f"\n   ðŸ“‹ Top {top_n} consensus tags:")
        
        result_tags = []
        for (tag_name, color), count in top_tags:
            print(f"      â€¢ {tag_name} ({color}) - mentioned {count} times")
            
            # Get or create tag in database
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, color=color)
                db.add(tag)
                db.commit()
            
            # Link tag to game (if not already linked)
            existing_link = db.query(game_tags).filter(
                game_tags.c.game_id == game.id,
                game_tags.c.tag_id == tag.id
            ).first()
            
            if not existing_link:
                # Calculate relevance score based on frequency
                relevance = count / len(reviews)
                
                stmt = game_tags.insert().values(
                    game_id=game.id,
                    tag_id=tag.id,
                    relevance_score=relevance
                )
                db.execute(stmt)
            
            result_tags.append(tag)
        
        db.commit()
        print(f"\n   âœ… Successfully tagged {game.name}")
        
        return result_tags
    
    def analyze_all_games(self, db: Session, limit: int = None):
        """
        Generate consensus tags for all games that have reviews
        """
        # Get games that have reviews but no tags
        query = db.query(Game).join(Review).outerjoin(game_tags).filter(
            game_tags.c.tag_id == None
        ).distinct()
        
        if limit:
            query = query.limit(limit)
        
        games = query.all()
        
        print(f"\nðŸŽ® Found {len(games)} games to analyze")
        
        for game in games:
            try:
                self.generate_consensus_tags(game, db)
            except Exception as e:
                print(f"âŒ Error analyzing {game.name}: {e}")
                continue
        
        print(f"\n{'='*60}")
        print(f"âœ… Tag analysis complete!")
        print(f"{'='*60}")


def generate_tags_for_game(game_id: int, db: Session):
    """Helper function to generate tags for a specific game"""
    analyzer = TagAnalyzer()
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        print(f"âŒ Game with ID {game_id} not found")
        return None
    
    return analyzer.generate_consensus_tags(game, db)


if __name__ == "__main__":
    # Test the tag analyzer
    from database import SessionLocal
    
    db = SessionLocal()
    
    print("ðŸ·ï¸  Testing Tag Analyzer...")
    print("\nThis will analyze reviews and generate consensus tags")
    print("Make sure you've run the review scraper first!\n")
    
    # Get a game that has reviews
    game = db.query(Game).join(Review).first()
    
    if game:
        analyzer = TagAnalyzer()
        tags = analyzer.generate_consensus_tags(game, db)
        
        if tags:
            print(f"\nðŸ“Š Final tags for {game.name}:")
            for tag in tags:
                color_emoji = {'green': 'ðŸŸ¢', 'orange': 'ðŸŸ ', 'red': 'ðŸ”´'}
                print(f"   {color_emoji.get(tag.color, 'âšª')} {tag.name} ({tag.color})")
    else:
        print("âŒ No games with reviews found!")
        print("Run these commands in order:")
        print("  1. python igdb_service.py    # Fetch games")
        print("  2. python review_scraper.py  # Scrape reviews")
        print("  3. python tag_analyzer.py    # Generate tags")
    
    db.close()