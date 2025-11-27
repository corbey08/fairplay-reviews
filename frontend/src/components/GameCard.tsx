"use client";

import Link from "next/link";
import Image from "next/image";
import { Calendar } from "lucide-react";

interface GameCardProps {
  game: {
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
  };
}

export default function GameCard({ game }: GameCardProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return null;
    try {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
      });
    } catch {
      return null;
    }
  };

  return (
    <Link href={`/games/${game.id}`}>
      <div className="bg-dark-card rounded-lg overflow-hidden neon-border card-hover group">
        {/* Game Image */}
        <div className="relative aspect-[16/9] bg-dark-hover overflow-hidden">
          {game.cover_image ? (
            <Image
              src={game.cover_image}
              alt={game.name}
              fill
              className="object-cover group-hover:scale-110 transition-transform duration-300"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-600">
              <span className="text-4xl">🎮</span>
            </div>
          )}
          
          {/* Gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-dark-card via-transparent to-transparent opacity-60" />
        </div>

        {/* Game Info */}
        <div className="p-4 space-y-3">
          <h3 className="font-bold text-lg line-clamp-2 group-hover:text-neon-blue transition-colors">
            {game.name}
          </h3>

          {game.release_date && (
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <Calendar size={14} />
              <span>{formatDate(game.release_date)}</span>
            </div>
          )}

          {/* Tags */}
          {game.tags && game.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {game.tags.slice(0, 3).map((tag) => (
                <Link 
                  key={tag.id}
                  href={`/tags?tags=${encodeURIComponent(tag.name)}`}
                  onClick={(e) => e.stopPropagation()}  // Prevents card click
                >
                  <span className={`tag-${tag.color} cursor-pointer hover:opacity-80 transition-opacity`}>
                    {tag.name}
                  </span>
                </Link>
              ))}
              {game.tags.length > 3 && (
                <span className="text-xs text-gray-500 self-center">
                  +{game.tags.length - 3} more
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </Link>
  );

}

