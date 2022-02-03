import os
from typing import List

from pydantic import AnyHttpUrl, BaseSettings

from pantapalabras.constants import ENV_DEV, ENV_LOCAL, ENV_PROD


class Settings(BaseSettings):
    PROJECT_NAME: str = "pantapalabras"
    HOST = "0.0.0.0"
    PORT = 9173
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SPREADSHEET: str = "Pantapalabras"
    FONT: str = "Roboto-Black.ttf"

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", ENV_LOCAL)
    if ENVIRONMENT == ENV_LOCAL:
        BACKEND_CORS_ORIGINS.append("http://localhost")

    if ENVIRONMENT in [ENV_DEV, ENV_PROD]:
        SENTRY_DSN = os.environ["SENTRY_DSN"]

    class Config:
        case_sensitive = True


settings = Settings()
