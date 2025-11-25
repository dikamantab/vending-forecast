from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
    MQTT_BROKER_HOST: str = "your-cloudamqp-host"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: str = ""
    MQTT_PASSWORD: str = ""
    MQTT_TOPIC: str = "sensors/#"
    ML_MODEL_PATH: str = "app/ml/model.pkl"
    DOWNLOAD_FOLDER: str = "/shared/downloads"


    class Config:
        env_file = ".env"


settings = Settings()