import axios from 'axios';
import { User, Item, Swap, PointTransaction, SwapAnalytics } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    const response = await api.post('/login', formData);
    return response.data;
  },

  signup: async (email: string, password: string, firstName: string, lastName: string) => {
    const response = await api.post('/signup', {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    });
    return response.data;
  },

  getProfile: async (): Promise<User> => {
    const response = await api.get('/me');
    return response.data;
  },
};

export const itemsApi = {
  browse: async (filters: {
    category_id?: string;
    tags?: string;
    condition?: string;
    item_type?: string;
    search?: string;
    sort_by?: string;
    skip?: number;
    limit?: number;
  } = {}): Promise<Item[]> => {
    const response = await api.get('/items', { params: filters });
    return response.data;
  },

  getDetail: async (itemId: string): Promise<Item> => {
    const response = await api.get(`/items/${itemId}`);
    return response.data;
  },

  create: async (itemData: FormData): Promise<{ message: string; item_id: string }> => {
    const response = await api.post('/items', itemData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const swapsApi = {
  request: async (initiatorItemId: string, recipientItemId: string): Promise<Swap> => {
    const response = await api.post('/swaps/request', {
      initiator_item_id: initiatorItemId,
      recipient_item_id: recipientItemId,
    });
    return response.data;
  },

  updateStatus: async (swapId: string, status: string) => {
    const response = await api.put(`/swaps/${swapId}/status`, { status });
    return response.data;
  },

  getUserSwaps: async (): Promise<Swap[]> => {
    // Mock implementation - you'll need to implement /swaps/me endpoint in backend
    console.warn("Mocking getUserSwaps. Implement backend endpoint /swaps/me");
    return [
      {
        id: 'swap1',
        initiatorId: 'user1',
        recipientId: 'user2',
        initiatorItemId: 'item1',
        recipientItemId: 'item2',
        status: 'PENDING',
        pointsExchanged: 0,
        createdAt: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        updatedAt: new Date(Date.now() - 86400000).toISOString(),
      },
      {
        id: 'swap2',
        initiatorId: 'user3',
        recipientId: 'user1',
        initiatorItemId: 'item3',
        recipientItemId: 'item4',
        status: 'COMPLETED',
        pointsExchanged: 50,
        createdAt: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
        updatedAt: new Date(Date.now() - 86400000).toISOString(),
      },
      {
        id: 'swap3',
        initiatorId: 'user1',
        recipientId: 'user4',
        initiatorItemId: 'item5',
        recipientItemId: 'item6',
        status: 'ACCEPTED',
        pointsExchanged: 25,
        createdAt: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
        updatedAt: new Date(Date.now() - 172800000).toISOString(),
      },
    ];
  },
  getAnalytics: async (): Promise<SwapAnalytics> => {
    const response = await api.get('/analytics/swaps');
    return response.data;
  },
};

export const pointsApi = {
  getHistory: async (transactionType?: string): Promise<PointTransaction[]> => {
    const response = await api.get('/points/history', {
      params: transactionType ? { transaction_type: transactionType } : {},
    });
    return response.data;
  },
};

export const adminApi = {
  getPendingItems: async (): Promise<Item[]> => {
    const response = await api.get('/admin/items/pending');
    return response.data;
  },

  getFlaggedItems: async (): Promise<Item[]> => {
    const response = await api.get('/admin/items/flagged');
    return response.data;
  },

  approveItem: async (itemId: string) => {
    const response = await api.post(`/admin/items/${itemId}/approve`);
    return response.data;
  },

  rejectItem: async (itemId: string, reason?: string) => {
    const response = await api.post(`/admin/items/${itemId}/reject`, { reason });
    return response.data;
  },

  removeItem: async (itemId: string, reason?: string) => {
    const response = await api.delete(`/admin/items/${itemId}/remove`, { 
      data: { reason } 
    });
    return response.data;
  },
};