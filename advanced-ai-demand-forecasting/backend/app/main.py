from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import ForecastHistory
from app.models.notification import Notification
from app.models.report import Report

from app.routers import auth_router
from app.routers import dataset_router
from app.routers import forecast_router
from app.routers import dashboard_router
from app.routers import admin_router
from app.routers import notification_router
from app.routers import report_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Advanced AI Demand Forecasting API",
    description="FastAPI backend for AI demand forecasting SaaS system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(dataset_router.router)
app.include_router(forecast_router.router)
app.include_router(dashboard_router.router)
app.include_router(admin_router.router)
app.include_router(notification_router.router)
app.include_router(report_router.router)


@app.get("/")
def root():
    return {
        "message": "Advanced AI Demand Forecasting API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }