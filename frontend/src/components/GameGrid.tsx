"use client";

import { useEffect, useState } from "react";
import GameCard from "./GameCard";

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

interface GameGridProps {
  limit?: number;
  tagFilter?: string;
}

export default function GameGrid({ limit, tagFilter }: GameGridProps) {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (limit) params.append("limit", limit.toString());
        if (tagFilter) params.append("tag", tagFilter);

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/games?${params}`
        );
        
        if (!response.ok) throw new Error("Failed to fetch games");
        
        const data = await response.json();
        setGames(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchGames();
  }, [limit, tagFilter]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {[...Array(limit || 12)].map((_, i) => (
          <div
            key={i}
            className="bg-dark-card rounded-lg overflow-hidden animate-pulse"
          >
            <div className="aspect-[16/9] bg-dark-hover" />
            <div className="p-4 space-y-3">
              <div className="h-6 bg-dark-hover rounded" />
              <div className="h-4 bg-dark-hover rounded w-2/3" />
              <div className="flex gap-2">
                <div className="h-6 bg-dark-hover rounded w-20" />
                <div className="h-6 bg-dark-hover rounded w-20" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400">Error loading games: {error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-6 py-2 bg-neon-blue rounded-lg hover:bg-neon-blue/80 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  if (games.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">No games found</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {games.map((game) => (
        <GameCard key={game.id} game={game} />
      ))}
    </div>
  );
}