import GameGrid from "@/components/GameGrid";
import HowItWorks from "@/components/HowItWorks";
import Hero from "@/components/Hero";

export default function Home() {
  return (
    <div>
      <Hero />
      
      {/* Latest Games Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
            Latest Games
          </h2>
          <a href="/games" className="text-neon-blue hover:text-neon-pink transition-colors">
            View All &rarr;
          </a>
        </div>
        <GameGrid limit={12} />
      </section>

      <HowItWorks />
    </div>
  );
}