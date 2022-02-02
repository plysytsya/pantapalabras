from typing import Dict, List

import uvicorn
from fastapi import FastAPI

from pantapalabras.config import settings
from pantapalabras.spreadsheet import SPREADSHEET_CLIENT

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"/{settings.PROJECT_NAME}/docs",
    openapi_url=f"/{settings.PROJECT_NAME}/openapi.json",
)


@app.get("/", response_model=Dict)
def health_check() -> Dict:
    return {"success": True, "status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/spreadsheet")
def get_spreadsheet() -> List[dict]:
    sheet = SPREADSHEET_CLIENT.open(settings.SPREADSHEET).sheet1
    return sheet.get_all_records()


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=9173, reload=True)
