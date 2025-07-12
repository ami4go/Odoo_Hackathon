import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  User, 
  Package, 
  ArrowRightLeft, 
  TrendingUp, 
  Plus, 
  Eye,
  Calendar,
  Star,
  Gift
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth.tsx';
import api from '../utils/api';
import { Item, Swap, PointTransaction } from '../types';

const Dashboard = () => {
  const { user } = useAuth();
  const [userItems, setUserItems] = useState<Item[]>([]);
  const [userSwaps, setUserSwaps] = useState<Swap[]>([]);
  const [pointsHistory, setPointsHistory] = useState<PointTransaction[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [itemsRes, swapsRes, pointsRes, analyticsRes] = await Promise.all([
        api.get('/items?user_id=' + user?.id),
        api.get('/swaps'),
        api.get('/points/history?limit=5'),
        api.get('/analytics/swaps')
      ]);

      setUserItems(itemsRes.data);
      setUserSwaps(swapsRes.data);
      setPointsHistory(pointsRes.data);
      setAnalytics(analyticsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-green-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your amazing stats...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-green-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Hey {user?.first_name}! 👋
          </h1>
          <p className="text-xl text-gray-600">
            Your sustainable fashion journey is looking absolutely iconic ✨
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Points</p>
                <p className="text-3xl font-bold text-emerald-600">
                  {user?.points_balance || 0}
                </p>
              </div>
              <div className="bg-emerald-100 p-3 rounded-full">
                <Gift className="h-6 w-6 text-emerald-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Items Listed</p>
                <p className="text-3xl font-bold text-blue-600">
                  {userItems.length}
                </p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <Package className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Swaps</p>
                <p className="text-3xl font-bold text-purple-600">
                  {analytics?.total_swaps || 0}
                </p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <ArrowRightLeft className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Points Earned</p>
                <p className="text-3xl font-bold text-orange-600">
                  {analytics?.total_points_earned || 0}
                </p>
              </div>
              <div className="bg-orange-100 p-3 rounded-full">
                <TrendingUp className="h-6 w-6 text-orange-600" />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* My Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">My Items 📦</h2>
                <Link
                  to="/add-item"
                  className="inline-flex items-center px-4 py-2 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Item
                </Link>
              </div>

              {userItems.length > 0 ? (
                <div className="space-y-4">
                  {userItems.slice(0, 5).map((item) => (
                    <div key={item.id} className="flex items-center p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
                      <div className="w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex items-center justify-center mr-4">
                        {item.primary_image_url ? (
                          <img
                            src={item.primary_image_url}
                            alt={item.title}
                            className="w-full h-full object-cover rounded-lg"
                          />
                        ) : (
                          <Package className="h-6 w-6 text-gray-400" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{item.title}</h3>
                        <p className="text-sm text-gray-600">{item.condition} • {item.points_value} points</p>
                        <div className="flex items-center mt-1">
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            item.is_available 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {item.is_available ? 'Available' : 'Unavailable'}
                          </span>
                          <span className="text-xs text-gray-500 ml-2 flex items-center">
                            <Eye className="h-3 w-3 mr-1" />
                            {item.view_count} views
                          </span>
                        </div>
                      </div>
                      <Link
                        to={`/items/${item.id}`}
                        className="text-emerald-600 hover:text-emerald-800 font-medium text-sm"
                      >
                        View
                      </Link>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Package className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No items yet</h3>
                  <p className="text-gray-600 mb-4">
                    Ready to start your swapping journey? List your first item!
                  </p>
                  <Link
                    to="/add-item"
                    className="inline-flex items-center px-6 py-3 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Your First Item
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Points History */}
          <div className="space-y-8">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Points 💎</h2>
              {pointsHistory.length > 0 ? (
                <div className="space-y-3">
                  {pointsHistory.map((transaction) => (
                    <div key={transaction.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {transaction.description || transaction.transaction_type}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(transaction.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <span className={`font-bold ${
                        transaction.transaction_type === 'EARNED' 
                          ? 'text-green-600' 
                          : 'text-red-600'
                      }`}>
                        {transaction.transaction_type === 'EARNED' ? '+' : '-'}{transaction.amount}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Gift className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-600">No points activity yet</p>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions ⚡</h2>
              <div className="space-y-3">
                <Link
                  to="/browse"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <Package className="h-5 w-5 mr-3 text-emerald-600" />
                  Browse Items
                </Link>
                <Link
                  to="/add-item"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <Plus className="h-5 w-5 mr-3 text-blue-600" />
                  List New Item
                </Link>
                <Link
                  to="/swaps"
                  className="flex items-center p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <ArrowRightLeft className="h-5 w-5 mr-3 text-purple-600" />
                  My Swaps
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;