export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-neon-blue to-neon-pink bg-clip-text text-transparent">
          Privacy Policy
        </h1>

        <div className="space-y-6 text-gray-300 leading-relaxed">
          <section>
            <h2 className="text-2xl font-bold text-white mb-4">1. Information We Collect</h2>
            <p>
              Fairplay Reviews does not collect personal information. We do not require user accounts, 
              and we do not track individual users.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">2. Anonymous Analytics</h2>
            <p>
              We may use anonymous analytics to understand how our service is used (page views, popular 
              searches). This data cannot be used to identify individual users.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">3. Cookies</h2>
            <p>
              We use essential cookies only to maintain site functionality. We do not use tracking 
              cookies or third-party advertising cookies.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">4. Third-Party Services</h2>
            <p>
              Our service displays game data and images from Steam. When you click external links 
              to Steam, you are subject to their privacy policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">5. Data Security</h2>
            <p>
              We implement reasonable security measures to protect our service. All data transmitted 
              between your browser and our servers is encrypted via HTTPS.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">6. Children's Privacy</h2>
            <p>
              Our service does not knowingly collect information from children under 13. The service 
              is intended for general audiences.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">7. Your Rights</h2>
            <p>
              Since we don't collect personal information, there is no personal data to access, 
              modify, or delete.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">8. Changes to Privacy Policy</h2>
            <p>
              We may update this privacy policy from time to time. We will notify users of significant 
              changes by posting a notice on our website.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">9. Contact Us</h2>
            <p>
              If you have questions about this privacy policy, please contact us at{" "}
              <a href="mailto:privacy@fairplayreviews.com" className="text-neon-blue hover:text-neon-pink">
                privacy@fairplayreviews.com
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