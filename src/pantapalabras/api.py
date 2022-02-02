import io
from pathlib import Path
from typing import Dict, List

import uvicorn
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
from starlette.responses import StreamingResponse

from pantapalabras.config import settings
from pantapalabras.constants import PROJECT_PARENT_DIR
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


@app.get("/image", response_class=StreamingResponse)
def get_image():
    img = Image.new("RGB", (960, 540), color=(255, 255, 255))

    d = ImageDraw.Draw(img)
    font_path = str(Path(PROJECT_PARENT_DIR / "fonts/times.ttf"))
    font = ImageFont.truetype(font_path, 150)
    d.text((10, 10), "Hello World", font=font, fill=(0, 0, 0))
    d.text((10, 250), "Hola Mundo", font=font, fill=(0, 0, 0))
    img = img.transpose(Image.ROTATE_90)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")

    img_byte_arr = img_byte_arr.getvalue()
    return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=9173, reload=True)
