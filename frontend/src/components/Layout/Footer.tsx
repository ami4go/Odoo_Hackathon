import React from 'react';
import { Heart, Recycle, Globe } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
              ReWear
            </h3>
            <p className="text-gray-300 mb-4">
              The coolest way to refresh your closet sustainably. Swap, don't shop, and make fashion circular! ♻️
            </p>
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <Heart className="h-5 w-5 text-red-400" />
                <span className="text-sm">Made with love for the planet</span>
              </div>
              <div className="flex items-center space-x-2">
                <Recycle className="h-5 w-5 text-green-400" />
                <span className="text-sm">Circular fashion</span>
              </div>
              <div className="flex items-center space-x-2">
                <Globe className="h-5 w-5 text-blue-400" />
                <span className="text-sm">Global community</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-gray-300">
              <li>
                <a href="/browse" className="hover:text-green-400 transition-colors">
                  Browse Items
                </a>
              </li>
              <li>
                <a href="/how-it-works" className="hover:text-green-400 transition-colors">
                  How It Works
                </a>
              </li>
              <li>
                <a href="/sustainability" className="hover:text-green-400 transition-colors">
                  Sustainability
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-gray-300">
              <li>
                <a href="/faq" className="hover:text-green-400 transition-colors">
                  FAQ
                </a>
              </li>
              <li>
                <a href="/contact" className="hover:text-green-400 transition-colors">
                  Contact Us
                </a>
              </li>
              <li>
                <a href="/community" className="hover:text-green-400 transition-colors">
                  Community Guidelines
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 ReWear. Making fashion sustainable, one swap at a time. 🌱</p>
        </div>
      </div>
    </footer>
  );
};