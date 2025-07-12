import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Recycle, Users, Heart, TrendingUp } from 'lucide-react';
import { useAuth } from '../hooks/useAuth.tsx';
import api from '../utils/api';
import { Item } from '../types';

const Landing = () => {
  const { user } = useAuth();
  const [featuredItems, setFeaturedItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedItems();
  }, []);

  const fetchFeaturedItems = async () => {
    try {
      const response = await api.get('/items?limit=6');
      setFeaturedItems(response.data);
    } catch (error) {
      console.error('Failed to fetch featured items:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-emerald-400 via-green-500 to-teal-600 text-white py-20 overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white to-green-100 bg-clip-text text-transparent">
              Your closet's second chance at slay ✨
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-green-100 max-w-3xl mx-auto">
              Give your clothes a glow-up! Join thousands swapping styles, earning points, 
              and saving the planet one outfit at a time 🌱
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to={user ? "/browse" : "/signup"}
                className="inline-flex items-center px-8 py-4 bg-orange-500 text-white font-bold rounded-xl hover:bg-orange-600 transform hover:scale-105 transition-all duration-200 shadow-lg"
              >
                Start Swapping <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/browse"
                className="inline-flex items-center px-8 py-4 bg-white/20 backdrop-blur-sm text-white font-bold rounded-xl hover:bg-white/30 transition-colors border border-white/30"
              >
                Browse Items <Sparkles className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>

        {/* Floating elements */}
        <div className="absolute top-20 left-10 animate-bounce">
          <div className="w-12 h-12 bg-orange-400/30 rounded-full"></div>
        </div>
        <div className="absolute bottom-20 right-10 animate-pulse">
          <div className="w-8 h-8 bg-pink-400/30 rounded-full"></div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Recycle className="h-8 w-8 text-emerald-600" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">10K+</h3>
              <p className="text-gray-600">Items swapped and loved again</p>
            </div>
            <div className="text-center">
              <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-orange-600" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">5K+</h3>
              <p className="text-gray-600">Happy swappers worldwide</p>
            </div>
            <div className="text-center">
              <div className="bg-pink-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="h-8 w-8 text-pink-600" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">500T</h3>
              <p className="text-gray-600">CO₂ saved from fashion waste</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Items */}
      <section className="py-16 bg-gradient-to-br from-green-50 to-emerald-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Trending swaps that are absolutely iconic ✨
            </h2>
            <p className="text-xl text-gray-600">
              Fresh drops from our amazing community
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-2xl shadow-lg overflow-hidden animate-pulse">
                  <div className="h-64 bg-gray-200"></div>
                  <div className="p-6">
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : featuredItems.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredItems.map((item) => (
                <Link
                  key={item.id}
                  to={`/items/${item.id}`}
                  className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 group"
                >
                  <div className="relative h-64 bg-gradient-to-br from-gray-100 to-gray-200">
                    {item.primary_image_url ? (
                      <img
                        src={item.primary_image_url}
                        alt={item.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    ) : (
                      <div className="flex items-center justify-center h-full text-gray-400">
                        <Sparkles className="h-12 w-12" />
                      </div>
                    )}
                    <div className="absolute top-3 right-3 bg-emerald-500 text-white px-2 py-1 rounded-full text-xs font-medium">
                      {item.points_value} pts
                    </div>
                  </div>
                  <div className="p-6">
                    <h3 className="font-bold text-gray-900 mb-2 group-hover:text-emerald-600 transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-gray-600 text-sm mb-3">
                      {item.description || "No description available"}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-emerald-600 bg-emerald-100 px-2 py-1 rounded-full">
                        {item.condition}
                      </span>
                      <span className="text-xs text-gray-500 flex items-center">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        {item.view_count} views
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="bg-white rounded-2xl shadow-lg p-12 max-w-md mx-auto">
                <Sparkles className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Items will load here
                </h3>
                <p className="text-gray-600">
                  Waiting for amazing swaps to appear! ✨
                </p>
              </div>
            </div>
          )}

          <div className="text-center mt-12">
            <Link
              to="/browse"
              className="inline-flex items-center px-8 py-4 bg-emerald-600 text-white font-bold rounded-xl hover:bg-emerald-700 transition-colors"
            >
              See All Items <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How the magic happens ✨
            </h2>
            <p className="text-xl text-gray-600">
              Three simple steps to swap success
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-gradient-to-br from-emerald-400 to-green-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                1
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">List Your Fits</h3>
              <p className="text-gray-600">
                Upload pics of clothes you're ready to let go. Add deets and watch the magic happen! 📸
              </p>
            </div>
            <div className="text-center">
              <div className="bg-gradient-to-br from-orange-400 to-pink-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                2
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Find Your Vibe</h3>
              <p className="text-gray-600">
                Browse through thousands of unique pieces. When you see something that speaks to your soul, go for it! 💫
              </p>
            </div>
            <div className="text-center">
              <div className="bg-gradient-to-br from-purple-400 to-indigo-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                3
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Swap & Slay</h3>
              <p className="text-gray-600">
                Complete the swap, earn points, and rock your new look. Mother Earth says thank you! 🌍
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-emerald-600 to-green-700 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold mb-6">
            Ready to transform your wardrobe? 🦋
          </h2>
          <p className="text-xl mb-8 text-green-100">
            Join the sustainable fashion revolution. Your closet (and the planet) will thank you!
          </p>
          <Link
            to={user ? "/browse" : "/signup"}
            className="inline-flex items-center px-8 py-4 bg-orange-500 text-white font-bold rounded-xl hover:bg-orange-600 transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            {user ? "Start Browsing" : "Join ReWear"} <Sparkles className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Landing;