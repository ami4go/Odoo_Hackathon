import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { itemsApi } from '../services/api';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Upload, X, Eye } from 'lucide-react';
import toast from 'react-hot-toast';

export const AddItemPage: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [images, setImages] = useState<File[]>([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category_id: 'clothing',
    size: '',
    condition: 'GOOD',
    item_type: 'CLOTHING',
    brand: '',
    color: '',
    material: '',
    points_value: 10,
    tags: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (images.length === 0) {
      toast.error('Please add at least one image!');
      return;
    }

    setIsLoading(true);

    try {
      const submitData = new FormData();
      
      // Add form fields
      Object.entries(formData).forEach(([key, value]) => {
        submitData.append(key, value.toString());
      });

      // Add images
      images.forEach((image) => {
        submitData.append('images', image);
      });

      const result = await itemsApi.create(submitData);
      toast.success('Item listed successfully! ✨');
      navigate(`/items/${result.item_id}`);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create item');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'points_value' ? parseInt(value) || 0 : value,
    }));
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    
    if (images.length + files.length > 5) {
      toast.error('Maximum 5 images allowed!');
      return;
    }

    setImages(prev => [...prev, ...files]);
  };

  const removeImage = (index: number) => {
    setImages(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Drop the drip 📸
          </h1>
          <p className="text-lg text-gray-600">
            Upload that cute top you're ghosting 👻👚
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Image Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Photos (up to 5) *
              </label>
              
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4">
                {images.map((image, index) => (
                  <div key={index} className="relative aspect-square">
                    <img
                      src={URL.createObjectURL(image)}
                      alt={`Upload ${index + 1}`}
                      className="w-full h-full object-cover rounded-lg"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
                
                {images.length < 5 && (
                  <label className="aspect-square border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-green-500 transition-colors">
                    <Upload className="h-8 w-8 text-gray-400 mb-2" />
                    <span className="text-sm text-gray-500">Add photo</span>
                    <input
                      type="file"
                      accept="image/*"
                      multiple
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </label>
                )}
              </div>
            </div>

            {/* Basic Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="Title *"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g., Vintage band tee"
                required
              />

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Condition *
                </label>
                <select
                  name="condition"
                  value={formData.condition}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                >
                  <option value="NEW">New (with tags)</option>
                  <option value="LIKE_NEW">Like New</option>
                  <option value="GOOD">Good</option>
                  <option value="FAIR">Fair</option>
                  <option value="POOR">Poor</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={4}
                placeholder="Tell us about this piece... What makes it special? 💫"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>

            {/* Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Type *
                </label>
                <select
                  name="item_type"
                  value={formData.item_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                >
                  <option value="CLOTHING">Clothing</option>
                  <option value="SHOES">Shoes</option>
                  <option value="ACCESSORIES">Accessories</option>
                </select>
              </div>

              <Input
                label="Size"
                name="size"
                value={formData.size}
                onChange={handleChange}
                placeholder="XS, S, M, L, XL..."
              />

              <Input
                label="Points Value"
                name="points_value"
                type="number"
                value={formData.points_value}
                onChange={handleChange}
                min="0"
                max="100"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Input
                label="Brand"
                name="brand"
                value={formData.brand}
                onChange={handleChange}
                placeholder="Nike, Zara, Vintage..."
              />

              <Input
                label="Color"
                name="color"
                value={formData.color}
                onChange={handleChange}
                placeholder="Black, white, rainbow..."
              />

              <Input
                label="Material"
                name="material"
                value={formData.material}
                onChange={handleChange}
                placeholder="Cotton, denim, silk..."
              />
            </div>

            <Input
              label="Tags (comma separated)"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="vintage, streetwear, summer, boho..."
            />

            {/* Preview Card */}
            {formData.title && (
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Eye className="h-5 w-5 mr-2" />
                  Preview
                </h3>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <h4 className="font-semibold text-gray-900">{formData.title}</h4>
                  {formData.description && (
                    <p className="text-gray-600 text-sm mt-1">{formData.description}</p>
                  )}
                  <div className="flex items-center justify-between mt-3">
                    <div className="flex items-center space-x-2">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                        {formData.condition.replace('_', ' ')}
                      </span>
                      {formData.size && (
                        <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs">
                          Size {formData.size}
                        </span>
                      )}
                    </div>
                    <span className="text-green-600 font-semibold">
                      {formData.points_value} pts
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Submit */}
            <div className="flex items-center justify-between pt-6 border-t border-gray-200">
              <Button
                type="button"
                variant="ghost"
                onClick={() => navigate(-1)}
              >
                Cancel
              </Button>

              <Button
                type="submit"
                variant="primary"
                isLoading={isLoading}
                className="px-8"
              >
                {isLoading ? 'Creating listing...' : 'List Item ✨'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};