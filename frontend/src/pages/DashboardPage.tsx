import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { itemsApi, swapsApi, pointsApi } from '../services/api';
import { Item, SwapAnalytics, PointTransaction, Swap } from '../types';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Button } from '../components/ui/Button';
import { ItemCard } from '../components/items/ItemCard';
import { User, TrendingUp, Coins, Package, Plus, BarChart3, ArrowRightLeft, Clock, CheckCircle, XCircle } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const [userItems, setUserItems] = useState<Item[]>([]);
  const [userSwaps, setUserSwaps] = useState<Swap[]>([]);
  const [analytics, setAnalytics] = useState<SwapAnalytics | null>(null);
  const [pointsHistory, setPointsHistory] = useState<PointTransaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // For now, we'll fetch recent items as user items (since we don't have user-specific endpoint)
      const [items, swaps, swapAnalytics, points] = await Promise.all([
        itemsApi.browse({ limit: 6, sort_by: 'newest' }),
        swapsApi.getUserSwaps(),
        swapsApi.getAnalytics(),
        pointsApi.getHistory().catch(() => []), // Fallback to empty array if fails
      ]);

      setUserItems(items);
      setUserSwaps(swaps);
      setAnalytics(swapAnalytics);
      setPointsHistory(points.slice(0, 5)); // Show only recent 5 transactions
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getSwapStatusIcon = (status: string) => {
    switch (status) {
      case 'PENDING':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case 'ACCEPTED':
        return <ArrowRightLeft className="h-4 w-4 text-blue-500" />;
      case 'COMPLETED':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'REJECTED':
      case 'CANCELLED':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  const getSwapStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'ACCEPTED':
        return 'bg-blue-100 text-blue-800';
      case 'COMPLETED':
        return 'bg-green-100 text-green-800';
      case 'REJECTED':
      case 'CANCELLED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-8 mb-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">
                Hey {user?.firstName}! 👋
              </h1>
              <p className="text-green-100 text-lg">
                Ready to make some sustainable swaps today?
              </p>
            </div>
            <div className="text-right">
              <div className="bg-white bg-opacity-20 rounded-xl p-4">
                <div className="flex items-center space-x-2 mb-1">
                  <Coins className="h-5 w-5" />
                  <span className="text-sm font-medium">Your Balance</span>
                </div>
                <p className="text-2xl font-bold">{user?.pointsBalance || 0} points</p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-100 p-3 rounded-lg">
                <Package className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Swaps</p>
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.totalSwaps || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-green-100 p-3 rounded-lg">
                <TrendingUp className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Completed</p>
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.completedSwaps || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-orange-100 p-3 rounded-lg">
                <Coins className="h-6 w-6 text-orange-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Points Earned</p>
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.totalPointsEarned || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-purple-100 p-3 rounded-lg">
                <BarChart3 className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Points Spent</p>
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.totalPointsSpent || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* My Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900">
                  My Listed Items 👗
                </h2>
                <Link to="/add-item">
                  <Button variant="primary" size="sm" className="flex items-center space-x-2">
                    <Plus className="h-4 w-4" />
                    <span>Add Item</span>
                  </Button>
                </Link>
              </div>

              {userItems.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">📦</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    No items listed yet
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Start by listing some items from your closet!
                  </p>
                  <Link to="/add-item">
                    <Button variant="primary">List Your First Item</Button>
                  </Link>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {userItems.map((item) => (
                    <ItemCard key={item.id} item={item} />
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Points History */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                Recent Points Activity 💰
              </h3>

              {pointsHistory.length === 0 ? (
                <div className="text-center py-4">
                  <div className="text-2xl mb-2">🤷‍♀️</div>
                  <p className="text-gray-600 text-sm">
                    No point transactions yet
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {pointsHistory.map((transaction) => (
                    <div
                      key={transaction.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {transaction.description}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatDistanceToNow(new Date(transaction.createdAt), { addSuffix: true })}
                        </p>
                      </div>
                      <span
                        className={`font-semibold ${
                          transaction.transactionType === 'EARNED'
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {transaction.transactionType === 'EARNED' ? '+' : '-'}
                        {transaction.amount}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* My Swaps */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900">
                  My Swaps 🔄
                </h2>
                <Link to="/browse">
                  <Button variant="ghost" size="sm" className="flex items-center space-x-2">
                    <ArrowRightLeft className="h-4 w-4" />
                    <span>Find Items</span>
                  </Button>
                </Link>
              </div>

              {userSwaps.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">🔄</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    No swaps yet
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Start browsing to find items you'd love to swap for!
                  </p>
                  <Link to="/browse">
                    <Button variant="primary">Browse Items</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {userSwaps.slice(0, 5).map((swap) => (
                    <div
                      key={swap.id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        {getSwapStatusIcon(swap.status)}
                        <div>
                          <p className="font-medium text-gray-900">
                            Swap #{swap.id.slice(0, 8)}
                          </p>
                          <p className="text-sm text-gray-600">
                            {formatDistanceToNow(new Date(swap.createdAt), { addSuffix: true })}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        {swap.pointsExchanged > 0 && (
                          <span className="text-sm font-medium text-green-600">
                            +{swap.pointsExchanged} pts
                          </span>
                        )}
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSwapStatusColor(swap.status)}`}>
                          {swap.status}
                        </span>
                      </div>
                    </div>
                  ))}
                  
                  {userSwaps.length > 5 && (
                    <div className="text-center pt-4">
                      <Button variant="ghost" size="sm">
                        View All Swaps ({userSwaps.length})
                      </Button>
                    </div>
                  )}
                </div>
              )}
            </div>
            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                Quick Actions ⚡
              </h3>
              <div className="space-y-3">
                <Link to="/browse" className="block">
                  <Button variant="ghost" className="w-full justify-start">
                    🔍 Browse Items
                  </Button>
                </Link>
                <Link to="/add-item" className="block">
                  <Button variant="ghost" className="w-full justify-start">
                    📸 List New Item
                  </Button>
                </Link>
                <Link to="/swaps" className="block">
                  <Button variant="ghost" className="w-full justify-start">
                    🔄 My Swaps
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};