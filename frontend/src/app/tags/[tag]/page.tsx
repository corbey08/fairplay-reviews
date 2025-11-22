import GameGrid from "@/components/GameGrid";
import { notFound } from "next/navigation";

interface PageProps {
  params: Promise<{ tag: string }>;
}

export default async function TagFilterPage({ params }: PageProps) {
  const resolvedParams = await params;
  const tagName = decodeURIComponent(resolvedParams.tag);

  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
            Games Tagged: {tagName}
          </h1>
          <p className="text-gray-400">
            Showing games with consensus tag "{tagName}" based on player reviews
          </p>
        </div>

        {/* Games Grid filtered by tag */}
        <GameGrid tagFilter={tagName} limit={100} />
      </div>
    </div>
  );
}