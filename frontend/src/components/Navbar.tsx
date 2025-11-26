"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { Search, Menu, X } from "lucide-react";
import { usePathname } from "next/navigation";

interface SearchResult {
  id: number;
  name: string;
  cover_image: string | null;
}

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  const pathname = usePathname();

  useEffect(() => {
    setIsMenuOpen(false); // auto-close menu on route change
  }, [pathname]);

  // Debounced search
  useEffect(() => {
    if (searchQuery.trim().length < 2) {
      setSearchResults([]);
      setShowDropdown(false);
      return;
    }

    const timer = setTimeout(async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/search?q=${encodeURIComponent(searchQuery)}`
        );
        if (response.ok) {
          const data = await response.json();
          setSearchResults(data.results.slice(0, 5));
          setShowDropdown(true);
        }
      } catch (error) {
        console.error("Search error:", error);
      }
    }, 300); // Wait 300ms after user stops typing

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setShowDropdown(false);
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  const handleResultClick = () => {
    setShowDropdown(false);
    setSearchQuery("");
  };

  return (
    <nav className="sticky top-0 z-50 bg-dark-card/95 backdrop-blur-sm border-b border-neon-blue/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3 group">
            <img 
              src="/images/logo.png" 
              alt="Fairplay Reviews" 
              className="h-10 w-10 sm:hidden group-hover:shadow-neon transition-all duration-300"
            />
            <img 
              src="/images/logo-full.png" 
              alt="Fairplay Reviews" 
              className="h-8 hidden sm:block"
            />
          </Link>

          {/* Search - always visible with dropdown */}
          <div className="relative flex-1 max-w-md mx-4 sm:mx-8" ref={searchRef}>
            <form onSubmit={handleSearch}>
              <div className="relative w-full">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search games..."
                  className="w-full bg-dark-bg border border-neon-blue/30 rounded-lg px-4 py-2 pl-10 focus:outline-none focus:border-neon-blue transition-colors"
                />
                <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
              </div>
            </form>

            {/* Search Dropdown */}
            {showDropdown && searchResults.length > 0 && (
              <div className="absolute top-full mt-2 w-full border border-neon-blue/30 rounded-lg shadow-lg overflow-hidden z-50" style={{ backgroundColor: '#12121A' }}>
                {searchResults.map((game) => (
                  <Link
                    key={game.id}
                    href={`/games/${game.id}`}
                    onClick={handleResultClick}
                    className="flex items-center gap-3 p-3 hover:bg-dark-hover transition-colors"
                  >
                    {game.cover_image ? (
                      <img
                        src={game.cover_image}
                        alt={game.name}
                        className="w-12 h-12 object-cover rounded"
                      />
                    ) : (
                      <div className="w-12 h-12 bg-dark-hover rounded flex items-center justify-center text-2xl">
                        🎮
                      </div>
                    )}
                    <span className="text-sm text-gray-300 hover:text-white">
                      {game.name}
                    </span>
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <Link href="/" className="hover:text-neon-blue transition-colors">
              Home
            </Link>
            <Link href="/games" className="hover:text-neon-blue transition-colors">
              All Games
            </Link>
            <Link href="/tags" className="hover:text-neon-blue transition-colors">
              Browse Tags
            </Link>
            <Link href="/about" className="hover:text-neon-blue transition-colors">
              About
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-dark-hover transition-colors"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 space-y-2">
            <Link href="/" className="block py-2 hover:text-neon-blue transition-colors">
              Home
            </Link>
            <Link href="/games" className="block py-2 hover:text-neon-blue transition-colors">
              All Games
            </Link>
            <Link href="/tags" className="block py-2 hover:text-neon-blue transition-colors">
              Browse Tags
            </Link>
            <Link href="/about" className="block py-2 hover:text-neon-blue transition-colors">
              About
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}

