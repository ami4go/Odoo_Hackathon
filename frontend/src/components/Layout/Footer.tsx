import React from 'react';
import { Link } from 'react-router-dom';
import { Recycle, Heart, Instagram, Twitter, BookText as TikTok } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="bg-emerald-500 p-2 rounded-full">
                <Recycle className="h-6 w-6" />
              </div>
              <span className="text-2xl font-bold">ReWear</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              Your closet's second chance at slay ✨ Join the sustainable fashion revolution 
              where every swap saves the planet, one outfit at a time! 🌱
            </p>
            <div className="flex space-x-4">
              <button className="text-gray-400 hover:text-pink-400 transition-colors">
                <Instagram className="h-5 w-5" />
              </button>
              <button className="text-gray-400 hover:text-blue-400 transition-colors">
                <Twitter className="h-5 w-5" />
              </button>
              <button className="text-gray-400 hover:text-purple-400 transition-colors">
                <TikTok className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/browse" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  Browse Items
                </Link>
              </li>
              <li>
                <Link to="/add-item" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  List an Item
                </Link>
              </li>
              <li>
                <Link to="/how-it-works" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link to="/sustainability" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  Sustainability
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/help" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  Help Center
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-gray-300 hover:text-emerald-400 transition-colors">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © 2024 ReWear. Made with <Heart className="h-4 w-4 inline text-red-500" /> for the planet.
          </p>
          <p className="text-gray-400 text-sm mt-2 md:mt-0">
            Sustainable fashion, one swap at a time 🌍
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;