export default function TermsPage() {
  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
          Terms of Service
        </h1>

        <div className="space-y-6 text-gray-300 leading-relaxed">
          <section>
            <h2 className="text-2xl font-bold text-white mb-4">1. Acceptance of Terms</h2>
            <p>
              By accessing and using Fairplay Reviews, you accept and agree to be bound by the terms 
              and provision of this agreement.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">2. Use of Service</h2>
            <p>
              Fairplay Reviews provides aggregated game review data sourced from publicly available 
              Steam reviews. Our service is provided "as is" without any warranties, expressed or implied.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">3. Data Sources</h2>
            <p>
              We aggregate and analyze publicly available reviews from Steam. We do not create or modify 
              review content. All reviews remain the property of their original authors.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">4. Intellectual Property</h2>
            <p>
              Game titles, images, and descriptions are trademarks of their respective owners. 
              Steam® is a registered trademark of Valve Corporation.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">5. Independence</h2>
            <p>
              Fairplay Reviews is an independent service. We are not affiliated with, endorsed by, 
              or sponsored by any game publishers, developers, or platforms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">6. Limitation of Liability</h2>
            <p>
              Fairplay Reviews shall not be liable for any indirect, incidental, special, consequential 
              or punitive damages resulting from your use of the service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">7. Changes to Terms</h2>
            <p>
              We reserve the right to modify these terms at any time. Continued use of the service 
              constitutes acceptance of modified terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">8. Contact</h2>
            <p>
              For questions about these terms, please contact us at{" "}
              <a href="mailto:legal@fairplayreviews.com" className="text-neon-blue hover:text-neon-pink">
                legal@fairplayreviews.com
              </a>
            </p>
          </section>

          <p className="text-sm text-gray-500 pt-8">
            Last updated: November 22, 2024
          </p>
        </div>
      </div>
    </div>
  );
}