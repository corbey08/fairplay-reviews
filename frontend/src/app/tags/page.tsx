"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import GameCard from "@/components/GameCard";
import { ChevronDown, ChevronUp, X } from "lucide-react";

interface Tag {
  id: number;
  name: string;
  color: string;
}

interface Game {
  id: number;
  name: string;
  cover_image: string | null;
  release_date: string | null;
  summary: string | null;
  tags: Tag[];
  matching_tags?: number;
  missing_tags?: number;
}

type TagSelectionState = "none" | "include" | "exclude";

interface SelectedTag {
  tag: Tag;
  state: TagSelectionState;
}

function BrowseTagsContent() {
  const searchParams = useSearchParams();
  const [allTags, setAllTags] = useState<Tag[]>([]);
  const [selectedTags, setSelectedTags] = useState<Map<number, TagSelectionState>>(new Map());
  const [searchResults, setSearchResults] = useState<{ [key: number]: Game[] }>({});
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set([0]));
  const [totalRequiredTags, setTotalRequiredTags] = useState(0);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/tags`
        );
        if (response.ok) {
          const data = await response.json();
          setAllTags(data);
          
          // Pre-select tag from URL if present
          const preSelectedTagName = searchParams.get('tags');
          if (preSelectedTagName) {
            const preSelectedTag = data.find((tag: Tag) => tag.name === preSelectedTagName);
            if (preSelectedTag) {
              const newMap = new Map<number, TagSelectionState>();
              newMap.set(preSelectedTag.id, "include");
              setSelectedTags(newMap);
              
              // Auto-search with the pre-selected tag
              setTimeout(() => {
                performSearch([preSelectedTagName], []);
              }, 100);
            }
          }
        }
      } catch (error) {
        console.error("Error fetching tags:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTags();
  }, [searchParams]);

  const handleTagClick = (tagId: number) => {
    setSelectedTags((prev) => {
      const newMap = new Map(prev);
      const currentState = newMap.get(tagId) || "none";
      
      // Cycle through: none -> include -> exclude -> none
      if (currentState === "none") {
        newMap.set(tagId, "include");
      } else if (currentState === "include") {
        newMap.set(tagId, "exclude");
      } else {
        newMap.delete(tagId);
      }
      
      return newMap;
    });
  };

  const clearSelection = () => {
    setSelectedTags(new Map());
    setSearchResults({});
    setExpandedSections(new Set([0]));
  };

  const performSearch = async (includedTags: string[], excludedTags: string[]) => {
    setSearching(true);
    try {
      const params = new URLSearchParams();
      params.append("include", includedTags.join(","));
      if (excludedTags.length > 0) {
        params.append("exclude", excludedTags.join(","));
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/games/search/multi-tag?${params}`
      );

      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.results || {});
        setTotalRequiredTags(data.total_required_tags || includedTags.length);
        // Auto-expand the "All tags match" section
        setExpandedSections(new Set([0]));
      }
    } catch (error) {
      console.error("Error searching games:", error);
    } finally {
      setSearching(false);
    }
  };

  const searchGames = async () => {
    const includedTags: string[] = [];
    const excludedTags: string[] = [];

    selectedTags.forEach((state, tagId) => {
      const tag = allTags.find((t) => t.id === tagId);
      if (tag) {
        if (state === "include") includedTags.push(tag.name);
        if (state === "exclude") excludedTags.push(tag.name);
      }
    });

    if (includedTags.length === 0) {
      alert("Please select at least one tag to include (single click)");
      return;
    }

    await performSearch(includedTags, excludedTags);
  };

  const toggleSection = (missingCount: number) => {
    setExpandedSections((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(missingCount)) {
        newSet.delete(missingCount);
      } else {
        newSet.add(missingCount);
      }
      return newSet;
    });
  };

  const getTagStateClass = (tagId: number): string => {
    const state = selectedTags.get(tagId);
    if (state === "include") return "ring-2 ring-green-400 opacity-100";
    if (state === "exclude") return "ring-2 ring-red-400 opacity-60";
    return "opacity-100 hover:opacity-80";
  };

  const getTagStateIndicator = (tagId: number): string => {
    const state = selectedTags.get(tagId);
    if (state === "include") return " ✓";
    if (state === "exclude") return " ✗";
    return "";
  };

  const hasResults = Object.keys(searchResults).length > 0;
  const includedCount = Array.from(selectedTags.values()).filter((s) => s === "include").length;
  const excludedCount = Array.from(selectedTags.values()).filter((s) => s === "exclude").length;

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
        <h1 className="text-4xl font-bold mb-4" style={{ color: "#00F0FF" }}>
          Browse by Multiple Tags
        </h1>
        <p className="text-gray-400 mb-2">
          Click once to <span className="text-green-400 font-semibold">include</span> a tag, 
          twice to <span className="text-red-400 font-semibold">exclude</span> it, 
          three times to deselect
        </p>
        <p className="text-gray-500 text-sm mb-8">
          Results will show games grouped by how many of your selected tags they match
        </p>

        {/* Tag Selection Area */}
        <div className="bg-dark-card rounded-lg p-6 mb-8">
          <div className="flex flex-wrap gap-3 mb-4">
            {allTags.map((tag) => (
              <button
                key={tag.id}
                onClick={() => handleTagClick(tag.id)}
                className={`tag-${tag.color} text-base px-6 py-3 cursor-pointer transition-all ${getTagStateClass(
                  tag.id
                )}`}
              >
                {tag.name}
                {getTagStateIndicator(tag.id)}
              </button>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-4 pt-4 border-t border-gray-700">
            <button
              onClick={searchGames}
              disabled={includedCount === 0 || searching}
              className="px-8 py-3 border-2 border-neon-blue text-neon-blue rounded-lg font-semibold hover:bg-neon-blue/10 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {searching ? "Searching..." : "Search Games"}
            </button>

            {selectedTags.size > 0 && (
              <button
                onClick={clearSelection}
                className="px-6 py-3 bg-gray-700 text-white rounded-lg font-semibold hover:bg-gray-600 transition-colors flex items-center gap-2"
              >
                <X size={16} />
                Clear Selection
              </button>
            )}

            {selectedTags.size > 0 && (
              <div className="text-sm text-gray-400">
                {includedCount > 0 && (
                  <span className="text-green-400">
                    {includedCount} included
                  </span>
                )}
                {includedCount > 0 && excludedCount > 0 && (
                  <span className="mx-2">•</span>
                )}
                {excludedCount > 0 && (
                  <span className="text-red-400">
                    {excludedCount} excluded
                  </span>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Search Results */}
        {hasResults && (
          <div className="space-y-6">
            {Object.keys(searchResults)
              .map(Number)
              .sort((a, b) => a - b)
              .map((missingCount) => {
                const games = searchResults[missingCount];
                const matchCount = totalRequiredTags - missingCount;
                const isExpanded = expandedSections.has(missingCount);

                let sectionTitle = "";
                let sectionColor = "";

                if (missingCount === 0) {
                  sectionTitle = `Perfect Match - All ${totalRequiredTags} tags`;
                  sectionColor = "text-green-400";
                } else if (missingCount === 1) {
                  sectionTitle = `Missing 1 tag (${matchCount}/${totalRequiredTags} tags match)`;
                  sectionColor = "text-yellow-400";
                } else {
                  sectionTitle = `Missing ${missingCount} tags (${matchCount}/${totalRequiredTags} tags match)`;
                  sectionColor = "text-orange-400";
                }

                return (
                  <div key={missingCount} className="bg-dark-card rounded-lg overflow-hidden">
                    {/* Section Header */}
                    <button
                      onClick={() => toggleSection(missingCount)}
                      className="w-full px-6 py-4 flex items-center justify-between hover:bg-dark-hover transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <h2 className={`text-2xl font-bold ${sectionColor}`}>
                          {sectionTitle}
                        </h2>
                        <span className="text-gray-400 text-lg">
                          ({games.length} {games.length === 1 ? "game" : "games"})
                        </span>
                      </div>
                      {isExpanded ? (
                        <ChevronUp className="text-gray-400" size={24} />
                      ) : (
                        <ChevronDown className="text-gray-400" size={24} />
                      )}
                    </button>

                    {/* Games Grid */}
                    {isExpanded && (
                      <div className="p-6 pt-2">
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                          {games.map((game) => (
                            <GameCard key={game.id} game={game} />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
          </div>
        )}

        {/* No Results Message */}
        {!hasResults && selectedTags.size === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400">
              Select tags above and click "Search Games" to find matching games
            </p>
          </div>
        )}

        {!hasResults && selectedTags.size > 0 && !searching && (
          <div className="text-center py-12">
            <p className="text-gray-400">
              Click "Search Games" to find games matching your selected tags
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// Wrapper component with Suspense
export default function BrowseTagsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <p className="text-gray-400">Loading tags...</p>
      </div>
    }>
      <BrowseTagsContent />
    </Suspense>
  );
}
