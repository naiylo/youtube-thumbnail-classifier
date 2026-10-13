import torch
import joblib
from pathlib import Path
from PIL import Image
from transformers import CLIPModel, AutoImageProcessor
from sklearn.preprocessing import normalize

# Place for the inference pipeline to first convert and embedd the picture and then classify it
MODEL_NAME = "openai/clip-vit-base-patch32"
clip_image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
clip_model = CLIPModel.from_pretrained(MODEL_NAME)
clip_model.eval()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "LR_model.joblib"
LR_classifier = joblib.load(MODEL_PATH)

def predict_image(image: Image.Image) -> float:
    # First we convert the image to RGB (like we did in the embedding)
    image = image.convert("RGB")
    inputs = clip_image_processor(image, return_tensors="pt")

    # Then we use Clip to embedd it into 512 features
    with torch.inference_mode():
        embedding_output = clip_model.get_image_features(
            pixel_values=inputs["pixel_values"]
            )
        
    embedding = (
                embedding_output
                if isinstance(embedding_output, torch.Tensor)
                else embedding_output.pooler_output
            )

    # Then we convert it to numpy and prepare it for inference prediction
    image_embedding = embedding.cpu().numpy()
    image_normalized = normalize(image_embedding,norm="l2")

    # Predict probability
    prediction = LR_classifier.predict_proba(image_normalized)[0, 1]

    return float(prediction)

    