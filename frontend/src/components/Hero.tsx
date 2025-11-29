"use client";
import { Shield, Users, TrendingUp, Bookmark } from "lucide-react";
import { useState } from "react";

export default function Hero() {
  const [bookmarked, setBookmarked] = useState(false);

  const handleBookmark = () => {
    // Check if the browser supports bookmarking
    if (window.sidebar && window.sidebar.addPanel) {
      // Firefox
      window.sidebar.addPanel(document.title, window.location.href, '');
    } else if (window.external && ('AddFavorite' in window.external)) {
      // IE
      window.external.AddFavorite(window.location.href, document.title);
    } else if (window.opera && window.print) {
      // Opera
      const elem = document.createElement('a');
      elem.setAttribute('href', window.location.href);
      elem.setAttribute('title', document.title);
      elem.setAttribute('rel', 'sidebar');
      elem.click();
    } else {
      // For browsers that don't support programmatic bookmarking (Chrome, Safari, modern browsers)
      setBookmarked(true);
      // Show instructions for manual bookmarking
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const shortcut = isMac ? 'Cmd+D' : 'Ctrl+D';
      alert(`Press ${shortcut} to bookmark this page!`);
    }
  };

  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-dark-card to-dark-bg">
      {/* Animated background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#00F0FF10_1px,transparent_1px),linear-gradient(to_bottom,#00F0FF10_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center space-y-8">
          {/* Main Heading */}
          <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold">
            <span className="block mb-2 text-white">Unbiased Game Reviews</span>
            <span className="block" style={{ color: '#00F0FF' }}>
              Powered by Community
            </span>
          </h1>
          {/* Subtitle */}
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            No sponsors. No bias. Just honest consensus from thousands of real players.
            We analyze reviews across platforms to give you the truth.
          </p>
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <a
              href="/games"
              className="px-8 py-3 border-2 border-neon-blue text-neon-blue rounded-lg font-semibold hover:bg-neon-blue/10 transition-all duration-300"
            >
              Explore Games
            </a>
            <a
              href="/about"
              className="px-8 py-3 bg-gradient-to-r from-neon-blue to-neon-pink rounded-lg font-semibold hover:shadow-neon transition-all duration-300 hover:scale-105"
            >
              How It Works
            </a>
          </div>
          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 pt-16 max-w-3xl mx-auto">
            <div className="space-y-2">
              <div className="flex justify-center">
                <Shield className="text-neon-green" size={32} />
              </div>
              <div className="text-2xl font-bold text-neon-green">100%</div>
              <div className="text-sm text-gray-400">Independent</div>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-center">
                <Users className="text-neon-blue" size={32} />
              </div>
              <div className="text-2xl font-bold text-neon-blue">1000s</div>
              <div className="text-sm text-gray-400">Real Reviews</div>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-center">
                <TrendingUp className="text-neon-pink" size={32} />
              </div>
              <div className="text-2xl font-bold text-neon-pink">Daily</div>
              <div className="text-sm text-gray-400">Updates</div>
            </div>
          </div>

          {/* Bookmark Section */}
          <div className="pt-12 max-w-2xl mx-auto">
            <div className="bg-dark-card/50 backdrop-blur-sm rounded-lg p-6 border border-orange-500/30">
              <div className="space-y-4">
                <p className="text-gray-300 text-lg">
                  Find this useful? Bookmark us for quick access to unbiased reviews!
                </p>
                <button
                  onClick={handleBookmark}
                  className="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg font-semibold hover:from-orange-600 hover:to-orange-700 transition-all duration-300 hover:scale-105 hover:shadow-[0_0_20px_rgba(249,115,22,0.5)] flex items-center gap-2 mx-auto"
                >
                  <Bookmark size={20} className={bookmarked ? "fill-current" : ""} />
                  {bookmarked ? "Bookmarked!" : "Bookmark This Page"}
                </button>
                {bookmarked && (
                  <p className="text-sm text-orange-400 animate-fade-in">
                    Thanks for bookmarking! Come back anytime for honest game reviews.
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
