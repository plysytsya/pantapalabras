import io
from typing import Dict, List

import uvicorn
from fastapi import FastAPI
from starlette.responses import StreamingResponse

from pantapalabras.config import settings
from pantapalabras.controller.image_controller import _create_image_from_texts
from pantapalabras.controller.spreadsheet_controller import SpreadsheetController
from pantapalabras.schemas.vocabulary import User, Vocabulary

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"/{settings.PROJECT_NAME}/docs",
    openapi_url=f"/{settings.PROJECT_NAME}/openapi.json",
)

SPREADSHEET_CONTROLLER = SpreadsheetController()


@app.get("/", response_model=Dict)
def health_check() -> Dict:
    return {"success": True, "status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/spreadsheet")
def get_spreadsheet() -> List[dict]:
    return SPREADSHEET_CONTROLLER.get_whole_spreadsheet()


@app.put("/vocabulary")
def put_vocabulary(vocabulary: Vocabulary):
    SPREADSHEET_CONTROLLER.add_vocabulary_pair(vocabulary.text_a, vocabulary.text_b)


@app.post("/image", response_class=StreamingResponse)
def create_image_from_texts(vocabulary: Vocabulary, user: User):
    image_with_texts = _create_image_from_texts(vocabulary, user)
    img_byte_arr = io.BytesIO()
    image_with_texts.save(img_byte_arr, format="PNG")

    img_byte_arr = img_byte_arr.getvalue()
    return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=9173, reload=True)
