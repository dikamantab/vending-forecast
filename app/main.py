from fastapi import FastAPI
from app.api import ml, temperature
from app.database import engine
from app import models
from app.services.mqtt_worker import start_in_thread
from app.services import excel_service
from app.config import settings
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = FastAPI(title="Vending Forecast API")
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