# 🚀 Advanced AI Demand Forecasting System

An AI-powered full-stack SaaS application built using FastAPI, React, and MySQL for intelligent demand forecasting, analytics, forecasting reports, notifications, and admin management.

---

# 🛠️ Tech Stack

## 🔹 Backend

* ⚡ FastAPI
* 🗄️ MySQL
* 🧠 Scikit-learn
* 📊 Pandas
* 📈 Statsmodels
* 🔐 JWT Authentication
* 🧩 SQLAlchemy

## 🔹 Frontend

* ⚛️ React.js
* 🌐 React Router DOM
* 📉 Recharts
* 🎨 Lucide React Icons
* 🔗 Axios

## 🔹 Reports & Export

* 📄 ReportLab (PDF)
* 📊 OpenPyXL (Excel)

---

# ✨ Features

## 🔐 Authentication Module

✅ User Registration
✅ User Login
✅ JWT Authentication
✅ Protected APIs
✅ Admin Role Management

---

## 📂 Dataset Module

✅ Upload CSV/XLSX datasets
✅ Dataset metadata storage
✅ Dataset filtering
✅ Pagination support
✅ Product category support
✅ Region support

---

## 🤖 Forecasting Module

✅ Multiple Forecasting Models

* 📈 Linear Regression
* 🌲 Random Forest
* 📉 ARIMA
* 📊 Moving Average

✅ Forecast generation
✅ Model comparison
✅ Forecast history tracking
✅ Accuracy metrics storage

* 📏 MAE
* 📏 RMSE
* 📏 MAPE

---

## 📊 Dashboard Module

✅ Dashboard summary cards
✅ Forecast activity analytics
✅ Model usage charts
✅ Model performance charts
✅ Dataset analytics
✅ Recent forecasting activity

---

## 👨‍💼 Admin Panel

✅ User management
✅ Dataset monitoring
✅ Forecast monitoring
✅ Reports monitoring
✅ System analytics

---

## 🔔 Notifications Module

✅ In-app notifications
✅ Forecast completed notifications
✅ Dataset upload failure alerts
✅ Report generation notifications

---

## 📄 Reports Module

✅ Forecast summary reports
✅ PDF report export
✅ Excel report export
✅ Downloadable reports

---

## 🎨 Frontend Enhancements

✅ Modern colorful SaaS UI
✅ Responsive design
✅ Sidebar navigation
✅ Dashboard analytics charts
✅ Beautiful cards & widgets
✅ Authentication pages
✅ Mobile responsive layout

---

# 📁 Project Structure

```bash
advanced-ai-demand-forecasting/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── ml/
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── reports/
│   ├── requirements.txt
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── context/
│   │  ├── layouts/
│   │  ├── pages/
│   │  ├── components/
│   │  └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
```

---

# ⚙️ Backend Setup

## 1️⃣ Navigate to backend

```bash
cd backend
```

## 2️⃣ Create virtual environment

```bash
python -m venv venv
```

## 3️⃣ Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

## 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 5️⃣ Configure MySQL database

Create database:

```sql
CREATE DATABASE demand_forecasting_db;
```

Update database credentials in:

```bash
app/database.py
```

## 6️⃣ Run backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Docs:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Frontend Setup

## 1️⃣ Navigate to frontend

```bash
cd frontend
```

## 2️⃣ Install dependencies

```bash
npm install
```

## 3️⃣ Run frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# 📌 Main Workflow

## 👤 User Flow

1️⃣ Register account
2️⃣ Login
3️⃣ Upload dataset
4️⃣ Generate forecast
5️⃣ Compare models
6️⃣ View analytics dashboard
7️⃣ Generate PDF/Excel reports
8️⃣ Download reports
9️⃣ View notifications

---

# 👨‍💼 Admin Workflow

✅ Monitor users
✅ Monitor datasets
✅ Monitor forecasts
✅ View reports
✅ System analytics

---

# 📊 Sample Forecast Models

| Model                | Purpose                 |
| -------------------- | ----------------------- |
| 📈 Linear Regression | Trend prediction        |
| 🌲 Random Forest     | Non-linear forecasting  |
| 📉 ARIMA             | Time series forecasting |
| 📊 Moving Average    | Simple demand smoothing |

---

# 🔑 API Modules

| Module            | APIs                     |
| ----------------- | ------------------------ |
| 🔐 Authentication | Register/Login/Profile   |
| 📂 Dataset        | Upload/List/Delete       |
| 🤖 Forecasting    | Generate/Compare/History |
| 📊 Dashboard      | Summary/Analytics        |
| 🔔 Notifications  | Read/Unread/Mark Read    |
| 📄 Reports        | Generate/Download        |
| 👨‍💼 Admin       | Users/Datasets/Forecasts |

---

# 🚀 Future Enhancements

🔹 Docker Deployment
🔹 Redis Caching
🔹 Email Notifications
🔹 WebSocket Live Updates
🔹 Advanced AI Forecasting
🔹 Cloud Storage Integration
🔹 Dark Mode
🔹 CI/CD Pipeline
🔹 Unit Testing
🔹 Kubernetes Deployment

---

# 👨‍💻 Developed Using

* FastAPI
* React
* MySQL
* Recharts

---

# 📬 Conclusion

The Advanced AI Demand Forecasting System provides a scalable and modern AI-powered forecasting platform with forecasting intelligence, analytics dashboards, reporting, notifications, and administrative monitoring capabilities using a clean full-stack architecture.



👨‍💻 Author

Prabu Ram
