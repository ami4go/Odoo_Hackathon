import React from 'react';
import { Link } from 'react-router-dom';
import { Item } from '../../types';
import { Badge } from '../ui/Badge';
import { Heart, Eye } from 'lucide-react';

interface ItemCardProps {
  item: Item;
  className?: string;
}

export const ItemCard: React.FC<ItemCardProps> = ({ item, className = '' }) => {
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

  return (
    <Link
      to={`/items/${item.id}`}
      className={`group block bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden ${className}`}
    >
      <div className="relative">
        <div className="aspect-square bg-gray-200 overflow-hidden">
          {item.primaryImageUrl ? (
            <img
              src={`http://localhost:8000${item.primaryImageUrl}`}
              alt={item.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              <div className="text-center">
                <div className="text-4xl mb-2">👕</div>
                <p className="text-sm">No image</p>
              </div>
            </div>
          )}
        </div>
        
        <div className="absolute top-3 left-3">
          <Badge className={getConditionColor(item.condition)}>
            {item.condition.replace('_', ' ')}
          </Badge>
        </div>
        
        <div className="absolute top-3 right-3 flex items-center space-x-2">
          {item.isFeatured && (
            <Badge className="bg-orange-100 text-orange-800">⭐ Featured</Badge>
          )}
          <div className="bg-black bg-opacity-50 text-white px-2 py-1 rounded-lg flex items-center space-x-1">
            <Eye className="h-3 w-3" />
            <span className="text-xs">{item.viewCount}</span>
          </div>
        </div>
      </div>

      <div className="p-4">
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-green-600 transition-colors">
          {item.title}
        </h3>
        
        {item.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {item.description}
          </p>
        )}

        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            {item.size && (
              <Badge variant="outline">Size {item.size}</Badge>
            )}
            {item.brand && (
              <Badge variant="outline">{item.brand}</Badge>
            )}
          </div>
          
          <div className="flex items-center space-x-1 text-green-600 font-semibold">
            <span>{item.pointsValue}</span>
            <span className="text-xs">pts</span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className={`h-2 w-2 rounded-full ${item.isAvailable ? 'bg-green-500' : 'bg-red-500'}`} />
            <span className="text-xs text-gray-600">
              {item.isAvailable ? 'Available' : 'Swapped'}
            </span>
          </div>
          
          <button className="text-gray-400 hover:text-red-500 transition-colors">
            <Heart className="h-4 w-4" />
          </button>
        </div>
      </div>
    </Link>
  );
};