export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_admin?: boolean;
  points_balance?: number;
}

export interface Item {
  id: string;
  title: string;
  description?: string;
  category_id: string;
  condition: string;
  item_type: string;
  brand?: string;
  color?: string;
  material?: string;
  points_value: number;
  is_available: boolean;
  is_approved: boolean;
  is_featured: boolean;
  view_count: number;
  primary_image_url?: string;
  created_at: string;
}

export interface ItemDetail extends Item {
  category: {
    id: string;
    name: string;
  };
  tags: string[];
  images: string[];
  uploader: {
    id: string;
    name: string;
  };
}

export interface Swap {
  id: string;
  status: string;
  initiator_id: string;
  recipient_id: string;
  initiator_item_id: string;
  recipient_item_id: string;
  points_exchanged: number;
  created_at: string;
}

export interface Notification {
  id: string;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface PointTransaction {
  id: string;
  transaction_type: string;
  amount: number;
  description?: string;
  created_at: string;
}

export interface Rating {
  id: string;
  rating: number;
  comment?: string;
  created_at: string;
}