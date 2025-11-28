from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, ForeignKey, Table, ARRAY, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Many-to-many relationship table for games and tags
game_tags = Table(
    'game_tags',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('relevance_score', Float, default=1.0)
)


class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True, index=True)
    igdb_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    release_date = Column(Date, nullable=True)
    cover_image = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    platform_list = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tags = relationship('Tag', secondary=game_tags, back_populates='games')
    reviews = relationship('Review', back_populates='game', cascade='all, delete-orphan')


class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    
    __table_args__ = (
        CheckConstraint(color.in_(['green', 'orange', 'red', 'gray']), name='check_color'),
    )
    
    # Relationships
    games = relationship('Game', secondary=game_tags, back_populates='tags')


class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)
    logo = Column(Text, nullable=True)
    
    __table_args__ = (
        CheckConstraint(type.in_(['website', 'youtube']), name='check_source_type'),
    )
    
    # Relationships
    reviews = relationship('Review', back_populates='source')


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    reviewer_name = Column(String(255), nullable=True)
    review_snippet = Column(Text, nullable=True)
    review_url = Column(Text, nullable=True)
    sentiment = Column(String(10), nullable=True)
    published_at = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint(sentiment.in_(['positive', 'mixed', 'negative']), name='check_sentiment'),
    )
    
    # Relationships
    game = relationship('Game', back_populates='reviews')

    source = relationship('Source', back_populates='reviews')
