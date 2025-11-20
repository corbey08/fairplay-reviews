"use client";

import { useEffect, useState } from "react";
import { ThumbsUp, ThumbsDown, Minus, ExternalLink } from "lucide-react";

interface Review {
  id: number;
  reviewer_name: string | null;
  review_snippet: string | null;
  review_url: string | null;
  sentiment: "positive" | "mixed" | "negative" | null;
  published_at: string | null;
}

interface ReviewsListProps {
  gameId: number;
}

export default function ReviewsList({ gameId }: ReviewsListProps) {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "positive" | "mixed" | "negative">("all");

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/games/${gameId}/reviews`
        );
        if (response.ok) {
          const data = await response.json();
          setReviews(data);
        }
      } catch (error) {
        console.error("Error fetching reviews:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [gameId]);

  const filteredReviews = reviews.filter(
    (review) => filter === "all" || review.sentiment === filter
  );

  const getSentimentIcon = (sentiment: string | null) => {
    switch (sentiment) {
      case "positive":
        return <ThumbsUp size={20} className="text-neon-green" />;
      case "negative":
        return <ThumbsDown size={20} className="text-red-400" />;
      case "mixed":
        return <Minus size={20} className="text-neon-orange" />;
      default:
        return null;
    }
  };

  const getSentimentColor = (sentiment: string | null) => {
    switch (sentiment) {
      case "positive":
        return "border-neon-green/30 bg-neon-green/5";
      case "negative":
        return "border-red-500/30 bg-red-500/5";
      case "mixed":
        return "border-neon-orange/30 bg-neon-orange/5";
      default:
        return "border-gray-700 bg-dark-card";
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            className="bg-dark-card rounded-lg p-6 border border-gray-800 animate-pulse"
          >
            <div className="h-4 bg-dark-hover rounded w-1/4 mb-3" />
            <div className="space-y-2">
              <div className="h-3 bg-dark-hover rounded" />
              <div className="h-3 bg-dark-hover rounded w-5/6" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="bg-dark-card rounded-lg p-8 border border-gray-800 text-center">
        <p className="text-gray-400">No reviews available yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filter Buttons */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => setFilter("all")}
          className={`px-4 py-2 rounded-lg transition-all ${
            filter === "all"
              ? "bg-neon-blue text-white"
              : "bg-dark-card text-gray-400 hover:bg-dark-hover"
          }`}
        >
          All ({reviews.length})
        </button>
        <button
          onClick={() => setFilter("positive")}
          className={`px-4 py-2 rounded-lg transition-all ${
            filter === "positive"
              ? "bg-neon-green text-white"
              : "bg-dark-card text-gray-400 hover:bg-dark-hover"
          }`}
        >
          Positive ({reviews.filter((r) => r.sentiment === "positive").length})
        </button>
        <button
          onClick={() => setFilter("mixed")}
          className={`px-4 py-2 rounded-lg transition-all ${
            filter === "mixed"
              ? "bg-neon-orange text-white"
              : "bg-dark-card text-gray-400 hover:bg-dark-hover"
          }`}
        >
          Mixed ({reviews.filter((r) => r.sentiment === "mixed").length})
        </button>
        <button
          onClick={() => setFilter("negative")}
          className={`px-4 py-2 rounded-lg transition-all ${
            filter === "negative"
              ? "bg-red-500 text-white"
              : "bg-dark-card text-gray-400 hover:bg-dark-hover"
          }`}
        >
          Negative ({reviews.filter((r) => r.sentiment === "negative").length})
        </button>
      </div>

      {/* Reviews List */}
      <div className="space-y-4">
        {filteredReviews.map((review) => (
          <div
            key={review.id}
            className={`rounded-lg p-6 border ${getSentimentColor(review.sentiment)}`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                {getSentimentIcon(review.sentiment)}
                <span className="font-medium text-gray-300">
                  {review.reviewer_name || "Anonymous"}
                </span>
              </div>
              {review.review_url && (
                <a
                  href={review.review_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-neon-blue hover:text-neon-pink transition-colors"
                >
                  <ExternalLink size={18} />
                </a>
              )}
            </div>
            <p className="text-gray-300 leading-relaxed">
              {review.review_snippet}
            </p>
            {review.published_at && (
              <p className="text-xs text-gray-500 mt-3">
                {new Date(review.published_at).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </p>
            )}
          </div>
        ))}
      </div>

      {filteredReviews.length === 0 && (
        <div className="bg-dark-card rounded-lg p-8 border border-gray-800 text-center">
          <p className="text-gray-400">No {filter} reviews found.</p>
        </div>
      )}
    </div>
  );
}