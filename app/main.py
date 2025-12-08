from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ml, temperature
from app.database import engine
from app import models
from app.services.mqtt_worker import start_in_thread
from app.services import excel_service
from app.config import settings
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = FastAPI(title="Vending Forecast API")
origins = [
    "http://localhost:5173",   # ✅ Izinkan Vite (default port)
    "http://localhost:3000",   # Jika kamu juga pakai React/Next.js
    "http://127.0.0.1:5173",   # Kadang browser pakai ini
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Izinkan semua origin (untuk development)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, dll
    allow_headers=["*"],  # Semua header
)
app.include_router(temperature.router)
app.include_router(ml.router)

# create tables at startup
models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    # start mqtt worker thread which posts to API
    start_in_thread()
    # scheduler to monitor shared folder for new Excel files
    scheduler = BackgroundScheduler()
    download_folder = settings.DOWNLOAD_FOLDER
    os.makedirs(download_folder, exist_ok=True)
    # scheduler.add_job(lambda: excel_service.process_pending_folder(download_folder), "interval", seconds=60)
    # scheduler.start()