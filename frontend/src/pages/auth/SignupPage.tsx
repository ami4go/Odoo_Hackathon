import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import toast from 'react-hot-toast';

export const SignupPage: React.FC = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match!');
      return;
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters long!');
      return;
    }

    setIsLoading(true);

    try {
      await signup(formData.email, formData.password, formData.firstName, formData.lastName);
      toast.success('Welcome to ReWear! Your sustainable journey starts now! 🌱');
      navigate('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create account. Try again!');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-green-50 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-green-100">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Join the revolution! 🌍
            </h1>
            <p className="text-gray-600">
              Swap don't shop 💁 Let's make fashion circular 🔄
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input
                type="text"
                name="firstName"
                label="First Name"
                placeholder="Your first name"
                value={formData.firstName}
                onChange={handleChange}
                required
              />

              <Input
                type="text"
                name="lastName"
                label="Last Name"
                placeholder="Your last name"
                value={formData.lastName}
                onChange={handleChange}
                required
              />
            </div>

            <Input
              type="email"
              name="email"
              label="Email"
              placeholder="your.email@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />

            <Input
              type="password"
              name="password"
              label="Password"
              placeholder="Create a strong password"
              value={formData.password}
              onChange={handleChange}
              required
            />

            <Input
              type="password"
              name="confirmPassword"
              label="Confirm Password"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />

            <Button
              type="submit"
              variant="primary"
              isLoading={isLoading}
              className="w-full text-lg py-3 mt-6"
            >
              {isLoading ? 'Creating your account...' : 'Start Swapping 🚀'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already part of the revolution?{' '}
              <Link
                to="/login"
                className="text-green-600 hover:text-green-700 font-semibold transition-colors"
              >
                Log in here
              </Link>
            </p>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="text-center">
              <p className="text-sm text-gray-500 mb-2">🎯 By joining, you're helping to:</p>
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                <div>♻️ Reduce textile waste</div>
                <div>🌱 Lower carbon footprint</div>
                <div>💝 Build community</div>
                <div>✨ Look amazing</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};