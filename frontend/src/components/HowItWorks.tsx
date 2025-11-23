"use client";

import { Shield, Target, BarChart3, Users, Zap, Eye } from "lucide-react";

export default function HowItWorks() {
  const features = [
    {
      icon: Shield,
      title: "100% Independent",
      description: "No sponsors, no influence from advertisers. We're not paid by publishers.",
      color: "text-neon-green",
    },
    {
      icon: Users,
      title: "Community-Driven",
      description: "We aggregate thousands of real player reviews from Steam to find true consensus.",
      color: "text-neon-blue",
    },
    {
      icon: Target,
      title: "Consensus Tags",
      description: "Our AI analyzes reviews to extract the most mentioned themes - positive and negative.",
      color: "text-neon-pink",
    },
    {
      icon: BarChart3,
      title: "Data-Backed",
      description: "Every tag is based on actual review data, not editorial opinion or marketing speak.",
      color: "text-neon-purple",
    },
    {
      icon: Eye,
      title: "Fully Transparent",
      description: "See the actual reviews behind each tag. No hidden algorithms or secret scores.",
      color: "text-neon-orange",
    },
    {
      icon: Zap,
      title: "Always Updated",
      description: "New reviews are analyzed daily to keep our consensus tags current and accurate.",
      color: "text-neon-blue",
    },
  ];

  return (
    <section className="bg-gradient-to-b from-dark-bg to-dark-card py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Why Trust <span style={{ color: '#00F0FF' }}>Fairplay Reviews</span>?
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            In a world of sponsored content and paid reviews, we're different.
            Here's how we ensure complete independence and accuracy.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-dark-card rounded-lg p-6 border border-gray-800 hover:border-neon-blue/30 transition-all duration-300 card-hover"
            >
              <div className="mb-4" style={{ 
                color: feature.color === 'text-neon-purple' ? '#9D00FF' : 
                      feature.color === 'text-neon-orange' ? '#FF6600' : 
                      feature.color === 'text-neon-green' ? '#39FF14' :
                      feature.color === 'text-neon-pink' ? '#FF00F5' :
                      '#00F0FF'
              }}>
                <feature.icon size={40} />
              </div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* How It Works Process */}
        <div className="mt-20">
          <h3 className="text-3xl font-bold text-center mb-12">Our Process</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              {
                step: "01",
                title: "Collect Reviews",
                description: "We gather top-rated reviews from Steam for each game",
              },
              {
                step: "02",
                title: "Analyze Content",
                description: "Our AI reads every review to identify common themes",
              },
              {
                step: "03",
                title: "Generate Tags",
                description: "We create consensus tags based on what players actually say",
              },
              {
                step: "04",
                title: "Stay Current",
                description: "Daily updates ensure tags reflect the latest player sentiment",
              },
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-neon-blue to-neon-pink mb-4 text-2xl font-bold">
                  {item.step}
                </div>
                <h4 className="text-lg font-semibold mb-2">{item.title}</h4>
                <p className="text-sm text-gray-400">{item.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <a
            href="/about"
            className="inline-block px-8 py-3 border-2 border-neon-blue text-neon-blue rounded-lg font-semibold hover:bg-neon-blue/10 transition-all duration-300"
          >
            Learn More About Our Methodology
          </a>
        </div>
      </div>
    </section>
  );

}
