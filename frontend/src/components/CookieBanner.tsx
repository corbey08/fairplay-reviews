"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function CookieBanner() {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    // Check if user has already made a choice
    const consent = localStorage.getItem("cookie-consent");
    if (!consent) {
      setShowBanner(true);
    } else if (consent === "accepted") {
      // Initialize Google Analytics here if consent was given
      initializeAnalytics();
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem("cookie-consent", "accepted");
    setShowBanner(false);
    initializeAnalytics();
  };

  const declineCookies = () => {
    localStorage.setItem("cookie-consent", "declined");
    setShowBanner(false);
  };

  const initializeAnalytics = () => {
    // Add Google Analytics initialization here
    // Example:
    // window.gtag('consent', 'update', {
    //   analytics_storage: 'granted'
    // });
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-dark-card border-t border-neon-blue/30 shadow-lg backdrop-blur-sm" style={{ backgroundColor: '#12121A' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex-1 text-sm text-gray-300">
            <p>
              We use cookies to analyze site traffic and improve your experience. 
              By clicking "Accept", you consent to our use of cookies.{" "}
              <Link href="/privacy" className="text-neon-blue hover:text-neon-pink underline">
                Learn more
              </Link>
            </p>
          </div>
          <div className="flex gap-3 shrink-0">
            <button
              onClick={declineCookies}
              className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-dark-hover transition-colors"
            >
              Decline
            </button>
            <button
              onClick={acceptCookies}
              className="px-4 py-2 bg-gradient-to-r from-neon-blue to-neon-pink rounded-lg font-semibold hover:shadow-neon transition-all duration-300"
            >
              Accept
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
