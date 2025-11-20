"use client";

import { useState } from "react";
import Link from "next/link";
import { Search, Menu, X } from "lucide-react";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <nav className="sticky top-0 z-50 bg-dark-card/95 backdrop-blur-sm border-b border-neon-blue/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 bg-gradient-to-br from-neon-blue to-neon-pink rounded-lg flex items-center justify-center group-hover:shadow-neon transition-all duration-300">
              <span className="text-2xl font-bold">FP</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
              Fairplay Reviews
            </span>
          </Link>

          {/* Desktop Search */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search games or tags..."
                className="w-full bg-dark-bg border border-neon-blue/30 rounded-lg px-4 py-2 pl-10 focus:outline-none focus:border-neon-blue transition-colors"
              />
              <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
            </div>
          </form>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <Link href="/" className="hover:text-neon-blue transition-colors">
              Home
            </Link>
            <Link href="/games" className="hover:text-neon-blue transition-colors">
              All Games
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
          <div className="md:hidden py-4 space-y-4">
            <form onSubmit={handleSearch} className="w-full">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search games or tags..."
                  className="w-full bg-dark-bg border border-neon-blue/30 rounded-lg px-4 py-2 pl-10 focus:outline-none focus:border-neon-blue transition-colors"
                />
                <Search className="absolute left-3 top-2.5 text-gray-400" size={20} />
              </div>
            </form>
            <div className="flex flex-col space-y-2">
              <Link href="/" className="py-2 hover:text-neon-blue transition-colors">
                Home
              </Link>
              <Link href="/games" className="py-2 hover:text-neon-blue transition-colors">
                All Games
              </Link>
              <Link href="/about" className="py-2 hover:text-neon-blue transition-colors">
                About
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}