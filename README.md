# ReWear – Community Clothing Exchange 👕♻️

A web-based platform that enables users to exchange unused clothing through direct swaps or a point-based redemption system. Built for Odoo Hackathon '25.

## 🧩 Problem Statement

This project is based on **Problem Statement 3: ReWear – Community Clothing Exchange**, from the official Odoo Hackathon '25 problem statements.

The goal is to promote sustainable fashion and reduce textile waste by encouraging users to reuse wearable garments instead of discarding them.


# ✅ ReWear Backend Completion Checklist

## 🔵 High Priority (Core UX/Engagement)

- [ ] **WebSocket Notification Integration**
  - [ ] Create `/ws/notifications` WebSocket endpoint
  - [ ] Emit notification updates on swap status changes
  - [ ] Update frontend to listen for real-time updates

- [ ] **Expose Chatbot API (Gemini-based)**
  - [ ] Create route `/chatbot/query`
  - [ ] Accept user question input
  - [ ] Send to Gemini and return response
  - [ ] Optionally store chat history per user

## 🟡 Medium Priority (Enhance Personalization & Insights)

- [ ] **Enhanced AI Recommendations**
  - [x] Use tag/category history for item recs (basic done)
  - [ ] Extend `/search/recommendations` to use Gemini to rank items
  - [ ] Track user click/view data for future personalization

- [ ] **Swap Activity Web View (Public History)**
  - [ ] Create `/users/{id}/swaps` for public profile viewing
  - [ ] Optional: Add feedback history with swap context

## 🟠 Low Priority (Optional but Nice)

- [ ] **Preview/Draft Item Listing**
  - [ ] Route: `POST /items/drafts` – Save a draft listing
  - [ ] Route: `GET /items/drafts` – Fetch user’s draft items
  - [ ] Route: `PUT /items/drafts/{id}` – Update draft

- [ ] **Rate-Limiting & Abuse Protection**
  - [ ] Add per-user rate limits (e.g., 10 items per hour)
  - [ ] Consider IP-based limits for anonymous endpoints

## ✅ Already Completed

- [x] User auth (signup/login)
- [x] Swap flow with status management
- [x] Points system (earn/spend/history)
- [x] Notifications (create/read/read-all)
- [x] AI spam detection (Gemini)
- [x] Ratings system
- [x] Admin controls (approve/reject/ban)
- [x] Analytics dashboard
- [x] Tag-based recommendations (basic)
- [x] Smart search filters
- [x] Featured items, availability, image upload
