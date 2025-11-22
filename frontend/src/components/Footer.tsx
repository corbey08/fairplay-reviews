"use client";

import Link from "next/link";
import Image from "next/image";
import { Github, Twitter, Mail, Instagram } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-dark-card border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="inline-block mb-4">
              <img 
                src="/images/logo-full.png" 
                alt="Fairplay Reviews" 
                className="h-10 w-auto"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.nextElementSibling.style.display = 'block';
                }}
              />
              <span 
                className="text-xl font-bold hidden"
                style={{ color: '#00F0FF', display: 'none' }}
              >
                Fairplay Reviews
              </span>
            </Link>
            <p className="text-gray-400 mb-4 max-w-md">
              Independent, community-driven game reviews. We analyze thousands of real player reviews 
              to give you unbiased consensus on what games are really like. Our reviews are never 
              influenced by advertising or affiliate relationships.
            </p>
            <div className="flex gap-4">
              <a
                href="https://github.com/corbey08"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-neon-blue transition-colors"
                aria-label="GitHub"
              >
                <Github size={24} />
              </a>
              <a
                href="https://x.com/FairplayReview4"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-neon-blue transition-colors"
                aria-label="X (Twitter)"
              >
                <Twitter size={24} />
              </a>
              <a
                href="https://www.instagram.com/fairplayreviews/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-neon-blue transition-colors"
                aria-label="Instagram"
              >
                <Instagram size={24} />
              </a>
              <a
                href="mailto:contact@fairplayreviews.net"
                className="text-gray-400 hover:text-neon-blue transition-colors"
                aria-label="Email"
              >
                <Mail size={24} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold mb-4" style={{ color: '#00F0FF' }}>Explore</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-400 hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/games" className="text-gray-400 hover:text-white transition-colors">
                  All Games
                </Link>
              </li>
              <li>
                <Link href="/search" className="text-gray-400 hover:text-white transition-colors">
                  Search
                </Link>
              </li>
            </ul>
          </div>

          {/* About Links */}
          <div>
            <h3 className="font-bold mb-4" style={{ color: '#00F0FF' }}>About</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-gray-400 hover:text-white transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-gray-400 hover:text-white transition-colors">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Fairplay Reviews. All rights reserved.
          </p>
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 text-gray-500 text-sm text-center">
            <span>Powered by Steam Reviews</span>
            <span className="hidden sm:inline">•</span>
            <span>
              Website designed by{" "}
              <a 
                href="https://github.com/corbey08" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-neon-blue hover:text-neon-pink transition-colors"
              >
                Greg Corbett
              </a>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}