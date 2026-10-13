from pathlib import Path
from PIL import Image
from backend.model import predict_image

PROJECT_ROOT = Path(__file__).resolve().parent.parent

image_path = PROJECT_ROOT / "data/raw/ai/ai_00998.jpg"

with Image.open(image_path) as image:
    probability = predict_image(image)

print(f"AI probability: {probability:.2%}")