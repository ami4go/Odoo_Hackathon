import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { itemsApi, swapsApi } from '../services/api';
import { Item } from '../types';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { ArrowLeft, Heart, Share2, Eye, User, Calendar, ArrowRightLeft, Coins } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

export const ItemDetailPage: React.FC = () => {
  const { itemId } = useParams<{ itemId: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [item, setItem] = useState<Item | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSwapping, setIsSwapping] = useState(false);
  const [selectedImage, setSelectedImage] = useState(0);

  useEffect(() => {
    if (itemId) {
      fetchItemDetail();
    }
  }, [itemId]);

  const fetchItemDetail = async () => {
    try {
      const itemData = await itemsApi.getDetail(itemId!);
      setItem(itemData);
    } catch (error) {
      console.error('Failed to fetch item:', error);
      toast.error('Item not found or unavailable');
      navigate('/browse');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSwapRequest = async () => {
    if (!user) {
      toast.error('Please log in to request a swap');
      navigate('/login');
      return;
    }

    if (!item) return;

    // For now, we'll show a mock swap request
    // In a real implementation, you'd show a modal to select which of the user's items to swap
    setIsSwapping(true);
    
    try {
      // Mock swap request - in reality, user would select their item first
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      toast.success('Swap request sent! 🔄');
    } catch (error) {
      toast.error('Failed to send swap request');
    } finally {
      setIsSwapping(false);
    }
  };

  const getConditionColor = (condition: string) => {
    switch (condition.toUpperCase()) {
      case 'NEW':
        return 'bg-green-100 text-green-800';
      case 'LIKE_NEW':
        return 'bg-blue-100 text-blue-800';
      case 'GOOD':
        return 'bg-yellow-100 text-yellow-800';
      case 'FAIR':
        return 'bg-orange-100 text-orange-800';
      case 'POOR':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!item) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">😕</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Item not found</h1>
          <p className="text-gray-600 mb-4">This item might have been removed or doesn't exist</p>
          <Button onClick={() => navigate('/browse')}>Browse Other Items</Button>
        </div>
      </div>
    );
  }

  const images = item.images && item.images.length > 0 ? item.images : [item.primaryImageUrl].filter(Boolean);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Back Button */}
        <Button
          variant="ghost"
          onClick={() => navigate(-1)}
          className="mb-6 flex items-center space-x-2"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back</span>
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Image Gallery */}
          <div className="space-y-4">
            <div className="aspect-square bg-gray-200 rounded-2xl overflow-hidden">
              {images.length > 0 ? (
                <img
                  src={`http://localhost:8000${images[selectedImage]}`}
                  alt={item.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  <div className="text-center">
                    <div className="text-6xl mb-4">👕</div>
                    <p className="text-lg">No image available</p>
                  </div>
                </div>
              )}
            </div>

            {images.length > 1 && (
              <div className="grid grid-cols-4 gap-2">
                {images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`aspect-square rounded-lg overflow-hidden border-2 transition-colors ${
                      selectedImage === index ? 'border-green-500' : 'border-gray-200'
                    }`}
                  >
                    <img
                      src={`http://localhost:8000${image}`}
                      alt={`${item.title} ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Item Details */}
          <div className="space-y-6">
            <div>
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{item.title}</h1>
                  <div className="flex items-center space-x-2 mb-3">
                    <Badge className={getConditionColor(item.condition)}>
                      {item.condition.replace('_', ' ')}
                    </Badge>
                    <Badge variant="outline">{item.itemType}</Badge>
                    {item.size && <Badge variant="outline">Size {item.size}</Badge>}
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-2 text-green-600 mb-2">
                    <Coins className="h-5 w-5" />
                    <span className="text-2xl font-bold">{item.pointsValue}</span>
                    <span className="text-sm">points</span>
                  </div>
                  <div className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs ${
                    item.isAvailable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    <div className={`h-2 w-2 rounded-full ${item.isAvailable ? 'bg-green-500' : 'bg-red-500'}`} />
                    <span>{item.isAvailable ? 'Available' : 'Swapped'}</span>
                  </div>
                </div>
              </div>

              {item.description && (
                <p className="text-gray-700 text-lg leading-relaxed">{item.description}</p>
              )}
            </div>

            {/* Item Details Grid */}
            <div className="grid grid-cols-2 gap-4 p-4 bg-white rounded-xl border border-gray-200">
              {item.brand && (
                <div>
                  <p className="text-sm text-gray-600">Brand</p>
                  <p className="font-semibold text-gray-900">{item.brand}</p>
                </div>
              )}
              {item.color && (
                <div>
                  <p className="text-sm text-gray-600">Color</p>
                  <p className="font-semibold text-gray-900">{item.color}</p>
                </div>
              )}
              {item.material && (
                <div>
                  <p className="text-sm text-gray-600">Material</p>
                  <p className="font-semibold text-gray-900">{item.material}</p>
                </div>
              )}
              <div>
                <p className="text-sm text-gray-600">Category</p>
                <p className="font-semibold text-gray-900">{item.category?.name || 'Uncategorized'}</p>
              </div>
            </div>

            {/* Tags */}
            {item.tags && item.tags.length > 0 && (
              <div>
                <p className="text-sm text-gray-600 mb-2">Tags</p>
                <div className="flex flex-wrap gap-2">
                  {item.tags.map((tag, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      #{tag}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Uploader Info */}
            <div className="flex items-center justify-between p-4 bg-white rounded-xl border border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center text-white font-bold">
                  {item.uploader?.name?.charAt(0) || 'U'}
                </div>
                <div>
                  <p className="font-semibold text-gray-900">{item.uploader?.name || 'Unknown User'}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <Calendar className="h-4 w-4" />
                      <span>Listed {formatDistanceToNow(new Date(item.createdAt), { addSuffix: true })}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Eye className="h-4 w-4" />
                      <span>{item.viewCount || 0} views</span>
                    </div>
                  </div>
                </div>
              </div>
              <Button variant="ghost" size="sm">
                <User className="h-4 w-4 mr-2" />
                View Profile
              </Button>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              {user && item.uploader?.id !== user.id && item.isAvailable ? (
                <Button
                  variant="primary"
                  size="lg"
                  onClick={handleSwapRequest}
                  isLoading={isSwapping}
                  className="w-full text-lg py-4"
                >
                  <ArrowRightLeft className="h-5 w-5 mr-2" />
                  {isSwapping ? 'Sending Request...' : 'Request Swap 🔥'}
                </Button>
              ) : !user ? (
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => navigate('/login')}
                  className="w-full text-lg py-4"
                >
                  Log In to Swap
                </Button>
              ) : item.uploader?.id === user.id ? (
                <div className="text-center py-4">
                  <p className="text-gray-600">This is your item ✨</p>
                </div>
              ) : (
                <div className="text-center py-4">
                  <p className="text-gray-600">This item is no longer available</p>
                </div>
              )}

              <div className="flex space-x-3">
                <Button variant="ghost" className="flex-1">
                  <Heart className="h-4 w-4 mr-2" />
                  Save
                </Button>
                <Button variant="ghost" className="flex-1">
                  <Share2 className="h-4 w-4 mr-2" />
                  Share
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* You Might Also Like */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            You might also love... 💕
          </h2>
          <div className="text-center py-8 bg-white rounded-xl border border-gray-200">
            <div className="text-4xl mb-4">🔍</div>
            <p className="text-gray-600">
              Recommendations coming soon! For now, check out our{' '}
              <button
                onClick={() => navigate('/browse')}
                className="text-green-600 hover:text-green-700 font-semibold"
              >
                browse page
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};