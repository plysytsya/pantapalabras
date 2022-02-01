from typing import Dict, List

import gspread
import sentry_sdk
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.requests import Request
from oauth2client.service_account import ServiceAccountCredentials
from starlette.middleware.cors import CORSMiddleware

from pantapalabras.config import settings
from pantapalabras.constants import ENV_DEV, ENV_PROD, PROJECT_DIR

if settings.ENVIRONMENT in [ENV_DEV, ENV_PROD]:
    sentry_sdk.init(settings.SENTRY_DSN, environment=settings.ENVIRONMENT)
    logger.info("Initialized sentry.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"/{settings.PROJECT_NAME}/docs",
    openapi_url=f"/{settings.PROJECT_NAME}/openapi.json",
)

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_credentials = ServiceAccountCredentials.from_json_keyfile_name(
    f"{PROJECT_DIR}/client_secret.json", scopes
)
SPREADSHEET_CLIENT = gspread.authorize(service_account_credentials)


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request)
            user_id = "database_user_id"  # when available
            scope.user = {"ip_address": request.client.host, "id": user_id}
            sentry_sdk.capture_exception(e)
        raise e


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", response_model=Dict)
def health_check() -> Dict:
    return {"success": True, "status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/spreadsheet")
def get_spreadsheet() -> List[dict]:
    sheet = SPREADSHEET_CLIENT.open(settings.SPREADSHEET).sheet1
    return sheet.get_all_records()
