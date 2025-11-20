"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import GameCard from "@/components/GameCard";
import { Search } from "lucide-react";

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

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      if (!query) {
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/search?q=${encodeURIComponent(query)}`
        );
        
        if (response.ok) {
          const data = await response.json();
          setGames(data.results || []);
        }
      } catch (error) {
        console.error("Search error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [query]);

  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <Search className="text-neon-blue" size={32} />
            <h1 className="text-3xl font-bold">Search Results</h1>
          </div>
          <p className="text-gray-400">
            {query ? `Showing results for "${query}"` : "Enter a search query"}
          </p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
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
        )}

        {/* Results */}
        {!loading && games.length > 0 && (
          <>
            <p className="text-sm text-gray-400 mb-6">
              Found {games.length} {games.length === 1 ? "game" : "games"}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {games.map((game) => (
                <GameCard key={game.id} game={game} />
              ))}
            </div>
          </>
        )}

        {/* No Results */}
        {!loading && query && games.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🎮</div>
            <h2 className="text-2xl font-bold mb-2">No games found</h2>
            <p className="text-gray-400 mb-6">
              Try adjusting your search or browse all games
            </p>
            <a
              href="/games"
              className="inline-block px-6 py-3 bg-neon-blue rounded-lg hover:bg-neon-blue/80 transition-colors"
            >
              Browse All Games
            </a>
          </div>
        )}

        {/* Empty State */}
        {!loading && !query && (
          <div className="text-center py-16">
            <Search className="mx-auto text-gray-600 mb-4" size={64} />
            <h2 className="text-2xl font-bold mb-2">Start Searching</h2>
            <p className="text-gray-400">
              Use the search bar above to find games
            </p>
          </div>
        )}
      </div>
    </div>
  );
}