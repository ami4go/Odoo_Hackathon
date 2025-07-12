import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/Button';
import { ShoppingBag, User, LogOut, Plus, Shield } from 'lucide-react';

export const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-white shadow-lg border-b-4 border-green-500">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <ShoppingBag className="h-8 w-8 text-green-600" />
            <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-500 bg-clip-text text-transparent">
              ReWear
            </span>
          </Link>

          <nav className="hidden md:flex items-center space-x-6">
            <Link
              to="/browse"
              className="text-gray-700 hover:text-green-600 font-medium transition-colors"
            >
              Browse Drip
            </Link>
            {user && (
              <>
                <Link
                  to="/add-item"
                  className="text-gray-700 hover:text-green-600 font-medium transition-colors"
                >
                  List My Fit
                </Link>
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-green-600 font-medium transition-colors"
                >
                  Dashboard
                </Link>
              </>
            )}
          </nav>

          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <div className="hidden md:flex items-center space-x-3">
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-700">
                      {user.firstName} {user.lastName}
                    </p>
                    <p className="text-xs text-green-600 font-semibold">
                      {user.pointsBalance} points
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Button
                    variant="accent"
                    size="sm"
                    onClick={() => navigate('/add-item')}
                    className="flex items-center space-x-1"
                  >
                    <Plus className="h-4 w-4" />
                    <span className="hidden sm:inline">Add Item</span>
                  </Button>
                  
                  {user.isAdmin && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => navigate('/admin')}
                      className="flex items-center space-x-1"
                    >
                      <Shield className="h-4 w-4" />
                    </Button>
                  )}
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => navigate('/dashboard')}
                    className="flex items-center space-x-1"
                  >
                    <User className="h-4 w-4" />
                  </Button>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleLogout}
                    className="flex items-center space-x-1"
                  >
                    <LogOut className="h-4 w-4" />
                  </Button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-3">
                <Button
                  variant="ghost"
                  onClick={() => navigate('/login')}
                >
                  Log In
                </Button>
                <Button
                  variant="primary"
                  onClick={() => navigate('/signup')}
                >
                  Start Swapping
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};