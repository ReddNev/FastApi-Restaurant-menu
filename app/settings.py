import os
from functools import lru_cache

from pydantic import BaseSettings


APP_MODELS = ['app.db.models', 'aerich.models']
DB_PATH = os.getenv('db_path')


class Settings(BaseSettings):
    app_name: str = "CRUD Menu"
    db_path: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
