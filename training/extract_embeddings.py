import pandas as pd
import numpy as np
import torch
from pathlib import Path
from PIL import Image
from transformers import AutoImageProcessor, CLIPModel

MODEL_NAME = "openai/clip-vit-base-patch32"
PATH_TO_FILES = Path("data/splits")
BATCH_SIZE = 8

train_df = pd.read_csv(PATH_TO_FILES / "train.csv")
test_df = pd.read_csv(PATH_TO_FILES / "test.csv")
val_df = pd.read_csv(PATH_TO_FILES / "val.csv")
clip_image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
clip_model = CLIPModel.from_pretrained(MODEL_NAME)
clip_model.eval()

def extract_embeddings(df, batch_size=8):
    all_embeddings = []

    for start in range(0, len(df), batch_size):
        images = []
        for path in df["path"].iloc[start:start+batch_size]:
            with Image.open(path) as image:
                images.append(image.convert("RGB"))

        inputs = clip_image_processor(images, return_tensors="pt")
        with torch.inference_mode():
            embedding_output = clip_model.get_image_features(
                pixel_values=inputs["pixel_values"]
            )

        # Depending on Transformers version, the output
        # may be a tensor or a model-output object.
        embedding = (
            embedding_output
            if isinstance(embedding_output, torch.Tensor)
            else embedding_output.pooler_output
        )

        all_embeddings.append(embedding.cpu())

    return torch.cat(all_embeddings, dim=0)

train_embedding = extract_embeddings(train_df, batch_size=8)
test_embedding = extract_embeddings(test_df, batch_size=8)
val_embedding = extract_embeddings(val_df, batch_size=8)

print("Training:", train_embedding.shape)
print("Testing:", test_embedding.shape)
print("Validation:", val_embedding.shape)

np.save("data/embeddings/train.npy", train_embedding.numpy())
np.save("data/embeddings/test.npy", test_embedding.numpy())
np.save("data/embeddings/val.npy", val_embedding.numpy())