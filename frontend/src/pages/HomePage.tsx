import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { itemsApi } from '../services/api';
import { Item } from '../types';
import { Button } from '../components/ui/Button';
import { ItemCard } from '../components/items/ItemCard';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { ChevronRight, Sparkles, Recycle, Users } from 'lucide-react';

export const HomePage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [featuredItems, setFeaturedItems] = useState<Item[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedItems();
  }, []);

  const fetchFeaturedItems = async () => {
    try {
      const items = await itemsApi.browse({ limit: 8, sort_by: 'popular' });
      setFeaturedItems(items);
    } catch (error) {
      console.error('Failed to fetch featured items:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-400 via-emerald-500 to-green-600 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 py-20 lg:py-32">
          <div className="text-center">
            <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
              Closet full of regrets?
              <br />
              <span className="bg-gradient-to-r from-yellow-300 to-orange-400 bg-clip-text text-transparent">
                Let's swap it out! 
              </span>
            </h1>
            <p className="text-xl lg:text-2xl mb-8 text-green-50 max-w-3xl mx-auto">
              Join the coolest sustainable fashion community. List it. Swap it. Slay sustainably. ✨
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
              {user ? (
                <>
                  <Button
                    size="lg"
                    variant="accent"
                    onClick={() => navigate('/browse')}
                    className="text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
                  >
                    Browse Drip 💫
                  </Button>
                  <Button
                    size="lg"
                    variant="secondary"
                    onClick={() => navigate('/add-item')}
                    className="text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
                  >
                    List My Fit 👗
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    size="lg"
                    variant="accent"
                    onClick={() => navigate('/signup')}
                    className="text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
                  >
                    Start Swapping 🔥
                  </Button>
                  <Button
                    size="lg"
                    variant="ghost"
                    onClick={() => navigate('/browse')}
                    className="text-lg px-8 py-4 text-white border-white hover:bg-white hover:text-green-600 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
                  >
                    Explore First 👀
                  </Button>
                </>
              )}
            </div>

            <div className="flex items-center justify-center space-x-8 text-green-100">
              <div className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5" />
                <span>Zero waste fashion</span>
              </div>
              <div className="flex items-center space-x-2">
                <Recycle className="h-5 w-5" />
                <span>Circular economy</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5" />
                <span>Gen Z vibes only</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Items Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              This week's hottest fits 🔥
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Discover the most-loved pieces from our sustainable fashion community
            </p>
          </div>

          {isLoading ? (
            <div className="flex justify-center">
              <LoadingSpinner size="lg" />
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {featuredItems.map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>

              <div className="text-center">
                <Link
                  to="/browse"
                  className="inline-flex items-center space-x-2 text-green-600 hover:text-green-700 font-semibold text-lg transition-colors"
                >
                  <span>See all the drip</span>
                  <ChevronRight className="h-5 w-5" />
                </Link>
              </div>
            </>
          )}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              How ReWear works ✨
            </h2>
            <p className="text-lg text-gray-600">
              Three simple steps to sustainable fashion
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold group-hover:scale-110 transition-transform">
                1
              </div>
              <h3 className="text-xl font-semibold mb-4">List your fits</h3>
              <p className="text-gray-600">
                Upload photos of clothes you're ready to part with. Set your points and watch the magic happen!
              </p>
            </div>

            <div className="text-center group">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold group-hover:scale-110 transition-transform">
                2
              </div>
              <h3 className="text-xl font-semibold mb-4">Find your vibe</h3>
              <p className="text-gray-600">
                Browse through thousands of unique pieces. When you find something you love, request a swap!
              </p>
            </div>

            <div className="text-center group">
              <div className="w-20 h-20 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold group-hover:scale-110 transition-transform">
                3
              </div>
              <h3 className="text-xl font-semibold mb-4">Make it happen</h3>
              <p className="text-gray-600">
                Connect with other swappers, exchange items, and build your dream sustainable wardrobe!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-orange-400 to-pink-500 text-white">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">
            Ready to join the revolution? 🌍
          </h2>
          <p className="text-xl mb-8 text-orange-50">
            Be part of the coolest sustainable fashion community. Your closet (and the planet) will thank you!
          </p>
          
          {!user && (
            <Button
              size="lg"
              variant="secondary"
              onClick={() => navigate('/signup')}
              className="text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all"
            >
              Join ReWear Today 🚀
            </Button>
          )}
        </div>
      </section>
    </div>
  );
};