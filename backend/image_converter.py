import httpx
from urllib.parse import urlsplit
from fastapi import HTTPException

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MiB

def validate_thumbnail_url(url: str) -> bool:

    parsed = urlsplit(url)

    if parsed.scheme != "https":
        return False

    if parsed.hostname != "i.ytimg.com":
        return False

    return True

async def download_thumbnail(url: str) -> bytes:
    if not validate_thumbnail_url(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid thumbnail URL"
            )

    image_bytes = bytearray()

    async with httpx.AsyncClient(
               timeout=10.0,
               follow_redirects=False,
               trust_env=False
               ) as client:

        async with client.stream("GET", url) as response:
            response.raise_for_status()

            async for chunk in response.aiter_bytes():
                        image_bytes.extend(chunk)

                        if len(image_bytes) > MAX_IMAGE_SIZE:
                            raise HTTPException(
                                status_code=413,
                                detail="Thumbnail too large"
                            )

    return bytes(image_bytes)
