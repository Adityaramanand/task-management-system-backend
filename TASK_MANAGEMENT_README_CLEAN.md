# 🚀 Task Management System

A full-stack Task Management System built with **React (Frontend)** and **FastAPI + PostgreSQL (Backend)**.

---

## 📌 Features

- ✅ Task creation, update, delete
- 📊 Dashboard with analytics & charts
- 🔍 Search, filter, pagination
- 👤 Role-based access (Admin & User)
- 📈 Real-time statistics and insights

---

## 👥 User Roles

### 👤 Regular User
- Manage only their own tasks
- Add, edit, delete tasks
- Track progress via dashboard

### 🛠️ Admin
- View all users' tasks
- Filter by user
- Manage tasks per user
- Access full analytics

---

## 🛠️ Tech Stack

### Frontend
- React
- Redux Toolkit
- Axios
- Bootstrap 5
- Chart.js
- Formik + Yup

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd project-folder
```

---

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create DB:
```sql
CREATE DATABASE taskdb;
```

Run server:
```bash
uvicorn main:app --reload
```

---

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 🔐 Admin Setup

```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
```

---

## 📊 Pages Overview

- 🏠 Home
- 🔐 Login / Register
- 📋 Tasks
- 📊 Dashboard
- 📈 Analytics

---

## 🔒 Security

- Protected routes
- Role-based access control
- JWT/Auth-based validation

---

## 📸 Highlights

- Clean UI with Bootstrap
- Interactive charts
- Scalable architecture

---

## 📁 Project Structure

```
frontend/
backend/
```

---

## 💡 Future Improvements

- Notifications system
- Real-time updates (WebSockets)
- Mobile responsiveness improvements

---

## 🧑‍💻 Author

Built by you 🚀

---

## ⭐ If you like this project

Give it a star on GitHub ⭐
