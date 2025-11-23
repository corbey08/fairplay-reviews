"use client";

import { useState, useEffect } from "react";
import GameCard from "@/components/GameCard";

interface Game {
  id: number;
  name: string;
  cover_image: string | null;
  release_date: string | null;
  summary: string | null;
  tags: Array<{
    id: number;
    name: string;
    color: string;
  }>;
}

export default function AllGamesPage() {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [skip, setSkip] = useState(0);
  const limit = 20; // Load 20 games at a time

  const fetchGames = async (currentSkip: number) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/games?skip=${currentSkip}&limit=${limit}`
      );
      
      if (response.ok) {
        const newGames = await response.json();
        
        if (newGames.length < limit) {
          setHasMore(false); // No more games to load
        }
        
        setGames(prev => [...prev, ...newGames]);
      }
    } catch (error) {
      console.error("Error fetching games:", error);
    }
  };

  // Initial load
  useEffect(() => {
    fetchGames(0).then(() => setLoading(false));
  }, []);

  const loadMore = async () => {
    setLoadingMore(true);
    const newSkip = skip + limit;
    await fetchGames(newSkip);
    setSkip(newSkip);
    setLoadingMore(false);
  };

  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
          All Games
        </h1>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(20)].map((_, i) => (
              <div
                key={i}
                className="bg-dark-card rounded-lg overflow-hidden animate-pulse"
              >
                <div className="aspect-[16/9] bg-dark-hover" />
                <div className="p-4 space-y-3">
                  <div className="h-6 bg-dark-hover rounded" />
                  <div className="h-4 bg-dark-hover rounded w-2/3" />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {games.map((game) => (
                <GameCard key={game.id} game={game} />
              ))}
            </div>

            {/* Load More Button */}
            {hasMore && (
              <div className="text-center mt-12">
                <button
                  onClick={loadMore}
                  disabled={loadingMore}
                  className="px-8 py-3 bg-gradient-to-r from-neon-blue to-neon-pink rounded-lg font-semibold hover:shadow-neon transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loadingMore ? "Loading..." : "Load More Games"}
                </button>
                <p className="text-gray-400 text-sm mt-4">
                  Showing {games.length} games
                </p>
              </div>
            )}

            {!hasMore && games.length > 0 && (
              <p className="text-center text-gray-400 mt-12">
                That's all the games! 🎮
              </p>
            )}
          </>
        )}
      </div>
    </div>
  );
}
