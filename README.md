# Mausam — Personalized Weather Experience

Mausam is a modern, mobile-first weather application delivering hyper-local meteorological forecasts, real-time Air Quality (US EPA), official disaster/weather alerts (NDMA/IMD Sachet CAP), and personalized lifestyle insights tailored to individual daily routines.

Built for the **Smart India Hackathon (SIH 2026)**.

---

## 🌟 Architecture Overview

```
Frontend (React + Vite)
      ↓  (HTTPS REST calls to /api)
Backend Proxy (FastAPI on Render)
      ├── Open-Meteo Weather API (Temperature, Humidity, Wind, UV, Hourly & 7-Day Forecast)
      ├── Open-Meteo Marine API (Wave Height, Period, Direction for Coastal Locations)
      ├── Open-Meteo Air Quality (US EPA AQI Index & Pollutants)
      └── NDMA Sachet CAP Feed (Official IMD / SDMA Disaster & Severe Weather Warnings)
```

---

## 🚀 Local Development

### Prerequisites
- **Node.js**: v18+ (tested with v20/v26)
- **Python**: 3.10+ (tested with 3.11/3.14)

### 1. Backend Setup
```bash
# Navigate to project root
cd /path/to/SIH

# Install Python dependencies
pip install -r backend/requirements.txt

# Start FastAPI server on port 8000
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive API documentation: `http://localhost:8000/docs`  
Health check: `http://localhost:8000/api/health`

### 2. Frontend Setup
```bash
# In another terminal window:
npm install

# Start Vite dev server on port 3000
npm run dev
```
Open `http://localhost:3000` in your browser. The Vite dev server automatically proxies all `/api` requests to `http://127.0.0.1:8000`.

---

## 🌐 Production Deployment (Render)

The repository includes a ready-to-use [`render.yaml`](./render.yaml) blueprint for automated zero-configuration deployment on Render.

### Services:
1. **Backend Web Service (`mausam-backend`)**:
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `FRONTEND_URL`: `https://mausam-frontend.onrender.com` (configured in CORS)
2. **Frontend Static Site (`mausam-frontend`)**:
   - **Runtime**: Static
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_BASE_URL`: `https://mausam-backend.onrender.com`

---

## 🛡️ Security & Privacy
- **Zero Exposed API Keys**: All external API integrations (Open-Meteo, NDMA Sachet) are open public meteorological feeds or proxied securely backend-side. No API keys exist in the client bundle.
- **Strict CORS**: CORS is locked to local development origins (`http://localhost:3000`) and the deployed frontend HTTPS origin. Wildcards (`*`) are disallowed.
- **Client Storage**: All personalization preferences and canonical location selections are persisted exclusively in client-side `localStorage`. No user tracking, cookies, or databases required.
