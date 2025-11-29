import { notFound } from "next/navigation";
import Image from "next/image";
import { Calendar, ExternalLink } from "lucide-react";
import ReviewsList from "@/components/ReviewsList";
import Link from "next/link";

interface Game {
  id: number;
  igdb_id: number;
  name: string;
  cover_image: string | null;
  release_date: string | null;
  summary: string | null;
  platform_list: string[] | null;
  tags: Array<{
    id: number;
    name: string;
    color: string;
    description: string | null;
  }>;
}

async function getGame(id: string): Promise<Game | null> {
  try {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/games/${id}`,
      { cache: "no-store" }
    );
    
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default async function GamePage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = await params;
  const game = await getGame(resolvedParams.id);

  if (!game) {
    notFound();
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "TBA";
    try {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    } catch {
      return "TBA";
    }
  };

  // Desktop: library_hero (3840x1240, 3.1:1) - wide cinematic format
  const desktopImageUrl = game.cover_image;
  
  // Mobile: library_600x900_2x (1200x1800, 2:3) - high-DPI portrait format
  // This is the retina/2x version for better quality on high-DPI mobile screens
  const mobileImageUrl = game.cover_image ? `https://cdn.akamai.steamstatic.com/steam/apps/${game.igdb_id}/library_600x900_2x.jpg` : null;

  return (
    <div className="min-h-screen">
      {/* Hero Section with Responsive Images */}
      
      {/* Mobile Hero - Portrait format (600x900) */}
      {mobileImageUrl && (
        <div className="relative w-full md:hidden" style={{ aspectRatio: "600/900" }}>
          <Image
            src={mobileImageUrl}
            alt={game.name}
            fill
            className="object-cover"
            priority
            quality={95}
            unoptimized={true}
            sizes="100vw"
          />
          {/* Gradient overlays for mobile */}
          <div className="absolute inset-0 bg-gradient-to-t from-dark-bg via-dark-bg/30 to-transparent" />

          {/* Game Title Overlay - Mobile */}
          <div className="absolute bottom-0 left-0 right-0 p-6">
            <div className="max-w-7xl mx-auto">
              <h1 className="text-3xl font-bold mb-3" style={{
                textShadow: '2px 2px 4px rgba(0,0,0,0.9), -1px -1px 2px rgba(0,0,0,0.9), 1px -1px 2px rgba(0,0,0,0.9), -1px 1px 2px rgba(0,0,0,0.9)'
              }}>
                {game.name}
              </h1>
              <div className="flex flex-wrap items-center gap-3 text-sm text-gray-300" style={{
                textShadow: '2px 2px 4px rgba(0,0,0,0.9), -1px -1px 2px rgba(0,0,0,0.9), 1px -1px 2px rgba(0,0,0,0.9), -1px 1px 2px rgba(0,0,0,0.9)'
              }}>
                {game.release_date && (
                  <div className="flex items-center gap-2">
                    <Calendar size={16} style={{ filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.9))' }} />
                    <span>{formatDate(game.release_date)}</span>
                  </div>
                )}
                {game.platform_list && game.platform_list.length > 0 && (
                  <div className="flex items-center gap-2">
                    <span>•</span>
                    <span>{game.platform_list.join(", ")}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Desktop Hero - Wide format (3840x1240) */}
      {desktopImageUrl && (
        <div className="relative w-full hidden md:block" style={{ aspectRatio: "3840/1240" }}>
          <Image
            src={desktopImageUrl}
            alt={game.name}
            fill
            className="object-cover"
            priority
            quality={95}
            unoptimized={true}
            sizes="100vw"
          />
          {/* Gradient overlays for desktop */}
          <div className="absolute inset-0 bg-gradient-to-t from-dark-bg via-dark-bg/50 to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-r from-dark-bg/80 via-transparent to-dark-bg/80" />

          {/* Game Title Overlay - Desktop */}
          <div className="absolute bottom-0 left-0 right-0 p-8">
            <div className="max-w-7xl mx-auto">
              <h1 className="text-5xl md:text-6xl font-bold mb-4" style={{
                textShadow: '2px 2px 4px rgba(0,0,0,0.8), -1px -1px 2px rgba(0,0,0,0.8), 1px -1px 2px rgba(0,0,0,0.8), -1px 1px 2px rgba(0,0,0,0.8)'
              }}>
                {game.name}
              </h1>
              <div className="flex flex-wrap items-center gap-4 text-gray-300" style={{
                textShadow: '2px 2px 4px rgba(0,0,0,0.8), -1px -1px 2px rgba(0,0,0,0.8), 1px -1px 2px rgba(0,0,0,0.8), -1px 1px 2px rgba(0,0,0,0.8)'
              }}>
                {game.release_date && (
                  <div className="flex items-center gap-2">
                    <Calendar size={20} style={{ filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.8))' }} />
                    <span>{formatDate(game.release_date)}</span>
                  </div>
                )}
                {game.platform_list && game.platform_list.length > 0 && (
                  <div className="flex items-center gap-2">
                    <span>•</span>
                    <span>{game.platform_list.join(", ")}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* If no image on mobile, show title here */}
      {!mobileImageUrl && (
        <div className="md:hidden p-6 bg-dark-card">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold mb-3">
              {game.name}
            </h1>
            <div className="flex flex-wrap items-center gap-3 text-sm text-gray-300">
              {game.release_date && (
                <div className="flex items-center gap-2">
                  <Calendar size={16} />
                  <span>{formatDate(game.release_date)}</span>
                </div>
              )}
              {game.platform_list && game.platform_list.length > 0 && (
                <div className="flex items-center gap-2">
                  <span>•</span>
                  <span>{game.platform_list.join(", ")}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* If no image on desktop, show title here */}
      {!desktopImageUrl && (
        <div className="hidden md:block p-8 bg-dark-card">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-5xl md:text-6xl font-bold mb-4">
              {game.name}
            </h1>
            <div className="flex flex-wrap items-center gap-4 text-gray-300">
              {game.release_date && (
                <div className="flex items-center gap-2">
                  <Calendar size={20} />
                  <span>{formatDate(game.release_date)}</span>
                </div>
              )}
              {game.platform_list && game.platform_list.length > 0 && (
                <div className="flex items-center gap-2">
                  <span>•</span>
                  <span>{game.platform_list.join(", ")}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Content Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Summary */}
            {game.summary && (
              <section>
                <h2 className="text-2xl font-bold mb-4 text-neon-blue">About</h2>
                <p className="text-gray-300 leading-relaxed">{game.summary}</p>
              </section>
            )}

            {/* Consensus Tags */}
            {game.tags && game.tags.length > 0 && (
              <section>
                <h2 className="text-2xl font-bold mb-4 text-neon-blue">
                  Community Consensus
                </h2>
                <div className="bg-dark-card rounded-lg p-6 border border-neon-blue/20">
                  <p className="text-sm text-gray-400 mb-4">
                    Based on analysis of player reviews
                  </p>
                  <div className="flex flex-wrap gap-3">
                    {game.tags.map((tag) => (
                      <Link 
                        key={tag.id}
                        href={`/tags?tags=${encodeURIComponent(tag.name)}`}
                      >
                        <span
                          className={`tag-${tag.color} text-base px-4 py-2 cursor-pointer hover:opacity-80 transition-opacity`}
                          title={tag.description || undefined}
                        >
                          {tag.name}
                        </span>
                      </Link>
                    ))}
                  </div>
                </div>
              </section>
            )}

            {/* Reviews Section */}
            <section>
              <h2 className="text-2xl font-bold mb-4 text-neon-blue">
                Player Reviews
              </h2>
              <ReviewsList gameId={game.id} />
            </section>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Steam Link */}
            <div className="bg-dark-card rounded-lg p-6 border border-neon-blue/20">
              <h3 className="font-bold mb-4">Get the Game</h3>
              <a
                href={`https://store.steampowered.com/app/${game.igdb_id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-gradient-to-r from-neon-blue to-neon-pink rounded-lg font-semibold hover:shadow-neon transition-all duration-300"
              >
                View on Steam
                <ExternalLink size={18} />
              </a>
            </div>

            {/* Info Box */}
            <div className="bg-dark-card rounded-lg p-6 border border-gray-800">
              <h3 className="font-bold mb-4">Game Info</h3>
              <div className="space-y-3 text-sm">
                {game.release_date && (
                  <div>
                    <span className="text-gray-400">Release Date:</span>
                    <div className="font-medium mt-1">{formatDate(game.release_date)}</div>
                  </div>
                )}
                {game.platform_list && game.platform_list.length > 0 && (
                  <div>
                    <span className="text-gray-400">Platforms:</span>
                    <div className="font-medium mt-1">
                      {game.platform_list.join(", ")}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
