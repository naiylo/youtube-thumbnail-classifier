from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, HttpUrl
from io import BytesIO
from PIL import Image

from backend.model import predict_image
from backend.image_converter import download_thumbnail


app = FastAPI()


class ThumbnailRequest(BaseModel):
    videoId: str | None = None
    imageUrl: HttpUrl
    title: str | None = None

@app.post("/classify")
async def classify(request: ThumbnailRequest):

    # Get imageUrl
    imageUrl = str(request.imageUrl)
    image_bytes = await download_thumbnail(imageUrl)
    with Image.open(BytesIO(image_bytes)) as img:
        image = img.convert("RGB")

    # Predict using your trained classifier
    probability = await run_in_threadpool(predict_image, image)
    
    # Convert to percentage
    score = round(probability * 100)
    
    return {
        "score": score,
        "modelVersion": "clip-logreg-v1"
    }