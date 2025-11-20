"use client";

import Link from "next/link";
import { Github, Twitter, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-dark-card border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="inline-flex items-center space-x-3 group mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-neon-blue to-neon-pink rounded-lg flex items-center justify-center">
                <span className="text-2xl font-bold">FP</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
                Fairplay Reviews
              </span>
            </Link>
            <p className="text-gray-400 mb-4 max-w-md">
              Independent, community-driven game reviews. No sponsors, no bias, just honest consensus from real players.
            </p>
            <div className="flex gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-neon-blue transition-colors"
              >
                <Github size={24} />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-neon-blue transition-colors"
              >
                <Twitter size={24} />
              </a>
              <a
                href="mailto:contact@fairplayreviews.com"
                className="text-gray-400 hover:text-neon-blue transition-colors"
              >
                <Mail size={24} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold mb-4 text-neon-blue">Explore</h3>
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
            <h3 className="font-bold mb-4 text-neon-blue">About</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-gray-400 hover:text-white transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link href="/methodology" className="text-gray-400 hover:text-white transition-colors">
                  Our Methodology
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">
                  Privacy Policy
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
          <p className="text-gray-500 text-sm">
            Built with Next.js • Powered by Steam Reviews
          </p>
        </div>
      </div>
    </footer>
  );
}