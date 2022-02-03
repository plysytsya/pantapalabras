import io
from typing import Dict, List

import uvicorn
from fastapi import FastAPI
from starlette.responses import StreamingResponse

from pantapalabras.config import settings
from pantapalabras.schemas.vocabulary import Vocabulary
from pantapalabras.spreadsheet import SPREADSHEET_CLIENT
from pantapalabras.text_to_image import _create_image_from_texts

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


@app.post("/image", response_class=StreamingResponse)
def create_image_from_texts(vocabulary: Vocabulary):
    image_with_texts = _create_image_from_texts(vocabulary.text_a, vocabulary.text_b)
    img_byte_arr = io.BytesIO()
    image_with_texts.save(img_byte_arr, format="PNG")

    img_byte_arr = img_byte_arr.getvalue()
    return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=9173, reload=True)
