"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Tag {
  id: number;
  name: string;
  color: string;
  game_count?: number;
}

export default function BrowseTagsPage() {
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/tags`
        );
        if (response.ok) {
          const data = await response.json();
          setTags(data);
        }
      } catch (error) {
        console.error("Error fetching tags:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTags();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <p className="text-gray-400">Loading tags...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold mb-4" style={{ color: '#00F0FF' }}>
          Browse by Tag
        </h1>
        <p className="text-gray-400 mb-8">
          Click any tag to see all games with that consensus from player reviews
        </p>

        <div className="flex flex-wrap gap-3">
          {tags.map((tag) => (
            <Link key={tag.id} href={`/tags/${encodeURIComponent(tag.name)}`}>
              <span className={`tag-${tag.color} text-base px-6 py-3 cursor-pointer hover:opacity-80 transition-opacity inline-block`}>
                {tag.name}
              </span>
            </Link>
          ))}
        </div>

        {tags.length === 0 && (
          <p className="text-gray-400 text-center py-12">No tags available yet</p>
        )}
      </div>
    </div>
  );
}