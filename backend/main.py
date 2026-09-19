from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class ThumbnailRequest(BaseModel):
    videoId: str | None = None
    imageUrl: HttpUrl
    title: str | None = None


@app.post("/classify")
async def classify_thumbnail(thumbnail: ThumbnailRequest):
    print(f"Received thumbnail: {thumbnail.videoId}")

    # Temporary result until we add a model.
    return {"score": 41}