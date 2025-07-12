export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  pointsBalance: number;
  isAdmin: boolean;
  isVerified: boolean;
  profilePictureUrl?: string;
  createdAt: string;
}

export interface Item {
  id: string;
  title: string;
  description?: string;
  categoryId: string;
  size?: string;
  condition: 'NEW' | 'LIKE_NEW' | 'GOOD' | 'FAIR' | 'POOR';
  itemType: 'CLOTHING' | 'SHOES' | 'ACCESSORIES';
  brand?: string;
  color?: string;
  material?: string;
  pointsValue: number;
  isAvailable: boolean;
  isApproved: boolean;
  isFeatured: boolean;
  viewCount: number;
  primaryImageUrl?: string;
  images?: string[];
  tags?: string[];
  category?: { id: string; name: string };
  uploader?: { id: string; name: string };
  createdAt: string;
}

export interface Swap {
  id: string;
  initiatorId: string;
  recipientId: string;
  initiatorItemId: string;
  recipientItemId: string;
  status: 'PENDING' | 'ACCEPTED' | 'REJECTED' | 'CANCELLED' | 'COMPLETED';
  pointsExchanged: number;
  createdAt: string;
  updatedAt: string;
}

export interface PointTransaction {
  id: string;
  userId: string;
  transactionType: 'EARNED' | 'SPENT';
  amount: number;
  description: string;
  relatedSwapId?: string;
  createdAt: string;
}

export interface SwapAnalytics {
  totalSwaps: number;
  completedSwaps: number;
  totalPointsEarned: number;
  totalPointsSpent: number;
  mostSwappedCategory?: string;
}