# 👕 ReWear – Community Clothing Exchange

**ReWear** is a full-stack web application designed to promote sustainable fashion by enabling users to **swap unused clothing** or **redeem them using a point system**. The platform encourages reuse and reduces textile waste through a community-driven exchange model.

---

## 🌍 Project Overview

ReWear empowers users to:

- List unused clothes and swap with others.
- Earn and spend points for clothes.
- Explore items with smart filters.
- Admins moderate item listings with AI-assistance.
- Get intelligent recommendations powered by AI.

The project uses:
- **FastAPI** backend (Python)
- **React + Tailwind CSS** frontend
- **PostgreSQL** database via **SQLAlchemy ORM**
- **Gemini AI** for spam detection
- **JWT + OAuth2** for secure auth

---

## ✨ Features

### 🧑 User Features
- Email/Password Sign-up and Login
- Dashboard: Profile, Points, Items, Swaps
- Upload Items: Add details, tags, images
- Browse Items: Filter by tag, category, condition
- Detailed Item View: Images, status, uploader info
- Request Swaps or Redeem Items with Points
- Notifications (Swap Updates, Item Approval)
- Rating System (rate other users post-swap)

### 🛠️ Admin Features
- Same login page (shared auth)
- Approve/Reject/Remove item listings
- View AI-flagged content
- Ban/Unban users
- View admin stats (basic dashboard)
- Real-time updates (WebSocket ready)

---

## 💡 Extra Features (Implemented but Frontend Pending)
- 🧠 Smart search filters
- 🏷️ Tag-based recommendations
- 🌈 Dark mode toggle
- 🧾 Points history + swap analytics
- 👀 Preview card before listing item
- 🧠 AI spam detection (Gemini)
- 🔔 Notification system
- 🚀 One-click swap request
- 📦 Item availability indicators
- 🤖 Chatbot integration
- 🧪 Admin analytics dashboard

---

## 🔧 Tech Stack

| Layer        | Tech                     |
|--------------|---------------------------|
| Backend      | FastAPI, SQLAlchemy       |
| Frontend     | React.js, Tailwind CSS    |
| Database     | PostgreSQL                |
| Auth         | JWT + OAuth2              |
| AI/ML        | Google Gemini (via API)   |
| Dev Tools    | Vite, dotenv, WebSocket-ready |
| Media Upload | Local static folder (`/static/uploads`) |

---

## 🚀 Getting Started

### 1️⃣ Backend Setup (FastAPI)

```bash
# Clone the repo
git clone https://github.com/your-org/rewear.git
cd rewear/backend
