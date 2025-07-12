# Clothing Swap Platform - Backend

A FastAPI-based backend for a clothing swapping platform with AI-powered spam detection and user recommendations.

## Features Implemented

### ✅ Core Features
- **User Authentication**: Email/password signup and login with JWT tokens
- **Item Management**: Upload, browse, and manage clothing items
- **Swap System**: Request, accept, reject, and complete item swaps
- **Points System**: Earn and spend points for item redemption
- **Rating System**: Rate other users after swaps
- **Admin Panel**: Moderate items, ban users, view analytics
- **AI Spam Detection**: Gemini AI integration for automatic content moderation
- **Notifications**: Real-time notifications for swap events
- **Search & Filters**: Advanced search with category, condition, and tag filters

### ✅ Extra Features
- **Smart Search**: Multi-criteria search with filters
- **Tag-based Recommendations**: Popular tags and personalized recommendations
- **Points History**: Complete transaction history and analytics
- **One-Click Swap**: Streamlined swap request process
- **Item Availability**: Real-time availability status
- **Notification System**: Comprehensive notification management
- **Rating System**: User rating and feedback system
- **Admin Dashboard**: Statistics and analytics for admins

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
# Database Configuration
DATABASE_URL=sqlite:///./swap_app.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Gemini AI API Key
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. Create Static Directory
```bash
mkdir static
mkdir static/uploads
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /login` - User login
- `GET /me` - Get current user profile

### Items
- `POST /items` - Create new item
- `GET /items` - Browse items with filters
- `GET /items/{item_id}` - Get item details
- `GET /items/featured` - Get featured items
- `POST /items/{item_id}/redeem` - Redeem item with points

### User Dashboard
- `GET /users/me/dashboard` - Get user dashboard data
- `GET /users/me/items` - Get user's items
- `GET /users/me/swaps` - Get user's swap history
- `GET /users/me/points` - Get points history

### Swaps
- `POST /swaps/request` - Request a swap
- `PUT /swaps/{swap_id}/status` - Update swap status

### Notifications
- `GET /notifications` - Get user notifications
- `POST /notifications/{notification_id}/read` - Mark notification as read
- `POST /notifications/read-all` - Mark all notifications as read

### Ratings
- `POST /ratings` - Rate a user
- `GET /ratings/user/{user_id}` - Get user ratings

### Admin
- `GET /admin/dashboard` - Admin dashboard statistics
- `GET /admin/items/pending` - Get pending items
- `POST /admin/items/{item_id}/approve` - Approve item
- `POST /admin/items/{item_id}/reject` - Reject item
- `GET /admin/items/flagged` - Get AI-flagged items
- `POST /admin/users/{user_id}/ban` - Ban user
- `POST /admin/users/{user_id}/unban` - Unban user

### Search & Recommendations
- `GET /search/recommendations` - Get personalized recommendations
- `GET /categories` - Get all categories
- `GET /tags/popular` - Get popular tags

### Analytics
- `GET /analytics/swaps` - Get swap analytics
- `GET /points/history` - Get points transaction history

## Database Models

The application includes comprehensive database models for:
- Users with authentication and points
- Items with images, tags, and categories
- Swaps with status tracking
- Notifications for real-time updates
- Ratings and reviews
- Point transactions
- Admin actions for moderation
- View logs for analytics

## AI Integration

### Spam Detection
- Uses Google Gemini AI to automatically flag inappropriate content
- Checks item titles and descriptions for spam indicators
- Integrates with admin moderation workflow

### Recommendations
- Personalized item recommendations based on user swap history
- Category-based filtering and prioritization
- Popular items and trending tags

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (admin/user)
- Input validation and sanitization
- CORS configuration for frontend integration

## File Structure

```
app/
├── main.py          # Main FastAPI application
├── database.py      # Database configuration
├── requirements.txt # Python dependencies
└── README.md       # This file

static/
└── uploads/        # Uploaded item images
```

## Development

### Adding New Features
1. Define database models in `main.py`
2. Create Pydantic schemas for request/response validation
3. Implement API endpoints with proper error handling
4. Add authentication and authorization as needed
5. Update documentation

### Testing
The API includes comprehensive error handling and validation. Test endpoints using:
- FastAPI's automatic interactive docs at `/docs`
- Postman or similar API testing tools
- Frontend integration testing

## Production Deployment

1. Use a production database (PostgreSQL recommended)
2. Set secure environment variables
3. Configure proper CORS origins
4. Set up static file serving
5. Use a production ASGI server (Gunicorn + Uvicorn)
6. Implement proper logging and monitoring 