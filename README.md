
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

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your DATABASE_URL and GEMINI_API_KEY inside .env

# Run backend
uvicorn main:app --reload
```

---

### 2️⃣ PostgreSQL Database Setup

Ensure PostgreSQL is installed and a database named `rewear` is created.

```bash
# Example commands
psql -U postgres
CREATE DATABASE rewear;
\q
```

---

### 3️⃣ Frontend Setup (React + Tailwind)

```bash
cd ../frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

This will launch the frontend at `http://localhost:5173`.

---

## ✅ Usage Flow

1. **User signs up** → Login
2. **Adds item** → Backend uses Gemini AI to flag potential spam
3. **Admin logs in** → Views flagged or pending items → Approves or rejects
4. **Only approved items** appear in public browse page
5. **User can swap or redeem** → Backend updates ownership and logs transactions
6. **Points tracked** → User can view full history
7. **Ratings posted** after swap → Builds trust across platform

---

## 📁 Folder Structure (Simplified)

```
rewear/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── static/uploads/
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── tailwind.config.js
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👥 Team

- Backend: FastAPI Team
- Frontend: React Team
- AI/ML: Gemini Integration
- DB: PostgreSQL Gurus

---

## 🔐 Admin Credentials

Use the following admin credentials to log in from the same login page:

- **Email:** `admin@swapapp.com`
- **Password:** `admin123`

> Once logged in, admins will automatically see the `/admin` panel in the header if `isAdmin` is true.

---
