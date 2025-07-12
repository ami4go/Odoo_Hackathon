
# 👕♻️ ReWear – Community Clothing Exchange

ReWear is a sustainable fashion platform that enables users to **swap unused clothing** through direct exchanges or a **point-based redemption system**. Our goal is to **reduce textile waste**, promote **eco-conscious fashion**, and create a fun, Gen-Z-friendly community for circular clothing reuse.

---

## 🚀 Features

### Core
- 🔐 User Authentication (Email/Password)
- 🏠 Landing Page with Calls-to-Action
- 👤 User Dashboard with Profile, Points, Swap History
- 🛍️ Item Detail Page with “Swap” & “Redeem” options
- ➕ Add New Item Page with Live Preview
- 🧾 Points History & Analytics
- ⚙️ Admin Panel with Moderation Tools

### Extras
- 🔍 Smart Search + Filters
- 🏷️ Tag-Based Recommendations
- 🌙 Theme & Dark Mode Toggle
- 📦 Item Availability Indicator
- 🔔 Notification System
- ⭐ Rating System
- 📊 Admin Dashboard Stats
- 🤖 Chatbot Integration
- 🧠 Spam Detection (via Gemini)
- 🔄 Real-time Updates (WebSocket ready)

---

## 🧱 Tech Stack

### 🔧 Backend
- Python (FastAPI / Flask)
- PostgreSQL (or any SQL DB)
- SQLAlchemy
- JWT-based Authentication
- REST APIs

### 💅 Frontend
- React (via **Vite**)
- Tailwind CSS
- Axios for API requests
- React Router
- Zustand or Context API for global state (optional)
- Fully responsive and Gen-Z inspired UI

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rewear.git
cd rewear
```

---

### 2. ⚙️ Backend Setup

> Make sure you have Python 3.10+ and pip installed.

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

#### Run the backend server:

```bash
uvicorn main:app --reload
```

The backend will run at `http://localhost:8000`

---

### 3. 💻 Frontend Setup

> Make sure you have **Node.js v16+** and **npm** installed.

```bash
cd frontend
npm install
```

#### Run the frontend (Vite Dev Server):

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## ✅ Final Checklist Before Running

- ✅ Backend is running on port `8000`
- ✅ Frontend is connected to backend via `.env` or Axios base URL
- ✅ No mock data or hardcoding — all data fetched from APIs
- ✅ Database is seeded (if needed) with sample data (optional)
- ✅ Admin credentials are created (if admin functionality exists)

---

## 📁 Project Structure

```
rewear/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── assets/
│   │   └── ...
│   └── index.html
└── README.md
```

---

## ✨ Contributing

We love contributors! Please follow our coding standards (linting, folder structure, reusable components) and raise a pull request 🚀

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

---

> Built with 💚 to swap fast fashion for smart fashion.
