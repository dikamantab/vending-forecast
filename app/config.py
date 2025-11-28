from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # MQTT
    MQTT_BROKER_HOST: str 
    MQTT_BROKER_PORT: int 
    MQTT_USERNAME: str = ""
    MQTT_PASSWORD: str = ""
    MQTT_TOPIC: str 

    # ML
    ML_MODEL_PATH: str

    # Playwright
    VENDOR_URL: str 
    USERNAME: str 
    PASSWORD: str 
    DOWNLOAD_FOLDER: str 

    class Config:
        env_file = ".env"

settings = Settings()