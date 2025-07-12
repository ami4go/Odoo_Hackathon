import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminApi } from '../services/api';
import { Item } from '../types';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Shield, CheckCircle, XCircle, Trash2, AlertTriangle, Eye, User } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

export const AdminPage: React.FC = () => {
  const { user } = useAuth();
  const [pendingItems, setPendingItems] = useState<Item[]>([]);
  const [flaggedItems, setFlaggedItems] = useState<Item[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [rejectReason, setRejectReason] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    if (!user?.isAdmin) {
      toast.error('Access denied! Admin privileges required 🚫');
      return;
    }
    fetchAdminData();
  }, [user]);

  const fetchAdminData = async () => {
    try {
      const [pending, flagged] = await Promise.all([
        adminApi.getPendingItems(),
        adminApi.getFlaggedItems(),
      ]);
      setPendingItems(pending);
      setFlaggedItems(flagged);
    } catch (error) {
      console.error('Failed to fetch admin data:', error);
      toast.error('Failed to load admin data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = async (itemId: string) => {
    setActionLoading(itemId);
    try {
      await adminApi.approveItem(itemId);
      toast.success('Item approved! ✅');
      fetchAdminData();
    } catch (error) {
      toast.error('Failed to approve item');
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async (itemId: string) => {
    const reason = rejectReason[itemId];
    if (!reason?.trim()) {
      toast.error('Please provide a reason for rejection');
      return;
    }

    setActionLoading(itemId);
    try {
      await adminApi.rejectItem(itemId, reason);
      toast.success('Item rejected and removed 🗑️');
      fetchAdminData();
      setRejectReason(prev => ({ ...prev, [itemId]: '' }));
    } catch (error) {
      toast.error('Failed to reject item');
    } finally {
      setActionLoading(null);
    }
  };

  const handleRemove = async (itemId: string) => {
    const reason = rejectReason[itemId];
    if (!reason?.trim()) {
      toast.error('Please provide a reason for removal');
      return;
    }

    setActionLoading(itemId);
    try {
      await adminApi.removeItem(itemId, reason);
      toast.success('Item removed successfully 🗑️');
      fetchAdminData();
      setRejectReason(prev => ({ ...prev, [itemId]: '' }));
    } catch (error) {
      toast.error('Failed to remove item');
    } finally {
      setActionLoading(null);
    }
  };

  const updateRejectReason = (itemId: string, reason: string) => {
    setRejectReason(prev => ({ ...prev, [itemId]: reason }));
  };

  if (!user?.isAdmin) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Shield className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h1>
          <p className="text-gray-600">You need admin privileges to access this page</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return <LoadingSpinner />;
  }

  const ItemCard: React.FC<{ item: Item; type: 'pending' | 'flagged' }> = ({ item, type }) => (
    <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
      <div className="flex">
        {/* Image */}
        <div className="w-32 h-32 bg-gray-200 flex-shrink-0">
          {item.primaryImageUrl ? (
            <img
              src={`http://localhost:8000${item.primaryImageUrl}`}
              alt={item.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              <div className="text-center">
                <div className="text-2xl mb-1">👕</div>
                <p className="text-xs">No image</p>
              </div>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="flex-1 p-4">
          <div className="flex items-start justify-between mb-2">
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">{item.title}</h3>
              <div className="flex items-center space-x-2 mb-2">
                <Badge className="bg-blue-100 text-blue-800">
                  {item.condition?.replace('_', ' ')}
                </Badge>
                <Badge className="bg-green-100 text-green-800">
                  {item.pointsValue} pts
                </Badge>
                {type === 'flagged' && (
                  <Badge className="bg-red-100 text-red-800">
                    <AlertTriangle className="h-3 w-3 mr-1" />
                    AI Flagged
                  </Badge>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-1 text-gray-500 text-sm">
              <Eye className="h-4 w-4" />
              <span>{item.viewCount || 0}</span>
            </div>
          </div>

          {item.description && (
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">{item.description}</p>
          )}

          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <User className="h-4 w-4" />
              <span>{item.uploader?.name || 'Unknown User'}</span>
            </div>
            <span className="text-xs text-gray-500">
              {formatDistanceToNow(new Date(item.createdAt), { addSuffix: true })}
            </span>
          </div>

          {/* Reason Input */}
          <div className="mb-3">
            <input
              type="text"
              placeholder="Reason for rejection/removal..."
              value={rejectReason[item.id] || ''}
              onChange={(e) => updateRejectReason(item.id, e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-2">
            <Button
              variant="primary"
              size="sm"
              onClick={() => handleApprove(item.id)}
              isLoading={actionLoading === item.id}
              className="flex items-center space-x-1"
            >
              <CheckCircle className="h-4 w-4" />
              <span>Approve</span>
            </Button>

            <Button
              variant="danger"
              size="sm"
              onClick={() => handleReject(item.id)}
              isLoading={actionLoading === item.id}
              className="flex items-center space-x-1"
            >
              <XCircle className="h-4 w-4" />
              <span>Reject</span>
            </Button>

            {type === 'flagged' && (
              <Button
                variant="danger"
                size="sm"
                onClick={() => handleRemove(item.id)}
                isLoading={actionLoading === item.id}
                className="flex items-center space-x-1"
              >
                <Trash2 className="h-4 w-4" />
                <span>Remove</span>
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-8 mb-8 text-white">
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="h-8 w-8" />
            <h1 className="text-3xl font-bold">Admin Control Center</h1>
          </div>
          <p className="text-purple-100 text-lg">
            Keep the community clean & sustainable! 🌱✨
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-yellow-100 p-3 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Pending Approval</p>
                <p className="text-2xl font-bold text-gray-900">{pendingItems.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-red-100 p-3 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-red-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">AI Flagged Items</p>
                <p className="text-2xl font-bold text-gray-900">{flaggedItems.length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Pending Items */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-6">
            <AlertTriangle className="h-6 w-6 text-yellow-600" />
            <h2 className="text-2xl font-bold text-gray-900">
              Pending Items ({pendingItems.length})
            </h2>
          </div>

          {pendingItems.length === 0 ? (
            <div className="bg-white rounded-xl p-8 text-center shadow-sm border border-gray-100">
              <div className="text-4xl mb-4">🎉</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                All caught up!
              </h3>
              <p className="text-gray-600">No items pending approval right now.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {pendingItems.map((item) => (
                <ItemCard key={item.id} item={item} type="pending" />
              ))}
            </div>
          )}
        </div>

        {/* Flagged Items */}
        <div>
          <div className="flex items-center space-x-3 mb-6">
            <AlertTriangle className="h-6 w-6 text-red-600" />
            <h2 className="text-2xl font-bold text-gray-900">
              AI Flagged Items ({flaggedItems.length})
            </h2>
          </div>

          {flaggedItems.length === 0 ? (
            <div className="bg-white rounded-xl p-8 text-center shadow-sm border border-gray-100">
              <div className="text-4xl mb-4">🤖✅</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                AI is happy!
              </h3>
              <p className="text-gray-600">No flagged items to review.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {flaggedItems.map((item) => (
                <ItemCard key={item.id} item={item} type="flagged" />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};