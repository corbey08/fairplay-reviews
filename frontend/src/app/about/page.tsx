import { Shield, Target, TrendingUp, Users, Zap, Database } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Hero */}
      <div className="bg-gradient-to-b from-dark-card to-dark-bg py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">
            About <span className="bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">Fairplay Reviews</span>
          </h1>
          <p className="text-xl text-gray-300 leading-relaxed">
            We're building a better way to discover games through unbiased, community-driven reviews. 
            No sponsors, no paid promotions, just real player consensus.
          </p>
        </div>
      </div>

      {/* Our Mission */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold mb-6 text-neon-blue">Our Mission</h2>
        <div className="space-y-4 text-gray-300 leading-relaxed">
          <p>
            The gaming industry has a trust problem. Traditional review sites often have conflicts of interest through 
            advertising, sponsorships, or early access agreements. Individual influencers may be sponsored or have 
            their own biases. Players deserve better.
          </p>
          <p>
            Fairplay Reviews was created to solve this problem. We aggregate thousands of real player reviews from 
            Steam and use AI to identify true consensus. What do most players actually think about a game's graphics, 
            story, gameplay, or performance? Our tags tell you at a glance.
          </p>
          <p>
            We're 100% independent. We don't take money from publishers, we don't run ads, and we don't use affiliate 
            links. Our only goal is to help you make informed decisions about which games are worth your time and money.
          </p>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-dark-card py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-12 text-center text-neon-blue">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Database,
                title: "1. Data Collection",
                description: "We automatically fetch the most helpful reviews from Steam for each game, ensuring we capture a representative sample of player opinions.",
                color: "text-neon-blue"
              },
              {
                icon: Target,
                title: "2. AI Analysis",
                description: "Our natural language processing analyzes each review to identify specific themes, issues, and praise mentioned by players.",
                color: "text-neon-pink"
              },
              {
                icon: TrendingUp,
                title: "3. Consensus Building",
                description: "We identify which themes appear most frequently across reviews and calculate consensus scores for each tag.",
                color: "text-neon-purple"
              },
              {
                icon: Shield,
                title: "4. Quality Control",
                description: "Tags are color-coded: green for positives, orange for mixed opinions, red for negatives - all based on actual review sentiment.",
                color: "text-neon-green"
              },
              {
                icon: Zap,
                title: "5. Daily Updates",
                description: "Our system runs daily to incorporate new reviews, ensuring tags stay current with the latest player sentiment.",
                color: "text-neon-orange"
              },
              {
                icon: Users,
                title: "6. Full Transparency",
                description: "Every game page shows the actual reviews our tags are based on. No hidden algorithms or secret scores.",
                color: "text-neon-blue"
              }
            ].map((step, index) => (
              <div key={index} className="bg-dark-bg rounded-lg p-6 border border-gray-800">
                <div className={`${step.color} mb-4`}>
                  <step.icon size={40} />
                </div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-gray-400">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Trust Us */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold mb-8 text-neon-blue">Why Trust Fairplay Reviews?</h2>
        
        <div className="space-y-6">
          <div className="bg-dark-card rounded-lg p-6 border border-neon-green/30">
            <h3 className="text-xl font-bold mb-3 text-neon-green">🛡️ 100% Independent</h3>
            <p className="text-gray-300">
              We don't accept money from game publishers, run advertisements, or use affiliate links. 
              Zero conflicts of interest.
            </p>
          </div>

          <div className="bg-dark-card rounded-lg p-6 border border-neon-blue/30">
            <h3 className="text-xl font-bold mb-3 text-neon-blue">📊 Data-Driven</h3>
            <p className="text-gray-300">
              Our tags aren't opinions - they're statistical consensus from hundreds or thousands of real player reviews.
            </p>
          </div>

          <div className="bg-dark-card rounded-lg p-6 border border-neon-pink/30">
            <h3 className="text-xl font-bold mb-3 text-neon-pink">👁️ Fully Transparent</h3>
            <p className="text-gray-300">
              You can read the actual reviews behind every tag. Our methodology is open and we show our sources.
            </p>
          </div>

          <div className="bg-dark-card rounded-lg p-6 border border-neon-orange/30">
            <h3 className="text-xl font-bold mb-3 text-neon-orange">🔄 Always Current</h3>
            <p className="text-gray-300">
              Daily updates ensure our data reflects the latest patches, DLC, and community sentiment.
            </p>
          </div>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="bg-gradient-to-b from-dark-bg to-dark-card py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Questions or Feedback?</h2>
          <p className="text-gray-300 mb-8">
            We're always looking to improve. Get in touch with suggestions or questions.
          </p>
          <a
            href="mailto:contact@fairplayreviews.com"
            className="inline-block px-8 py-3 bg-gradient-to-r from-neon-blue to-neon-pink rounded-lg font-semibold hover:shadow-neon transition-all duration-300"
          >
            Contact Us
          </a>
        </div>
      </section>
    </div>
  );
}