from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str 
    MQTT_BROKER_HOST: str 
    MQTT_BROKER_PORT: int 
    MQTT_USERNAME: str 
    MQTT_PASSWORD: str 
    MQTT_TOPIC: str 
    ML_MODEL_PATH: str 
    DOWNLOAD_FOLDER: str 

    VENDOR_URL: str 
    USERNAME: str 
    PASSWORD: str 
    DOWNLOAD_FOLDER: str 

    class Config:
        env_file = ".env"


settings = Settings()