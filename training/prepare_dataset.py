
from collections import Counter
from pathlib import Path
import csv

from datasets import load_dataset

DATASET_NAME = "TheKernel01/Tiny-GenImage"
OUTPUT_DIR = Path("data")
SAMPLES_PER_CLASS = 1000

# Load the existing training split.
dataset = load_dataset(DATASET_NAME, split="train")

# Shuffle to avoid selecting samples only from
# the beginning of the dataset.
dataset = dataset.shuffle(seed=42)

# Look up the actual label names.
label_names = dataset.features["label"].names
generator_names = dataset.features["generator"].names

print("Available labels:", label_names)
print("Available generators:", generator_names)

counts = Counter()
metadata = []

for sample in dataset:
    original_label = label_names[sample["label"]].lower()

    # Our project convention: 1 = AI, 0 = real
    label = 1 if original_label == "fake" else 0

    if counts[label] >= SAMPLES_PER_CLASS:
        continue

    category = "ai" if label == 1 else "real"
    generator = generator_names[sample["generator"]]

    folder = OUTPUT_DIR / "raw" / category
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"{category}_{counts[label]:05d}.jpg"
    path = folder / filename

    sample["image"].convert("RGB").save(
        path, format="JPEG", quality=90
    )

    metadata.append({
        "path": path.as_posix(),
        "label": label,
        "source": DATASET_NAME,
        "generator": generator,
        "channel_id": "",
        "video_id": "",
    })

    counts[label] += 1

    if all(
        counts[k] == SAMPLES_PER_CLASS
        for k in (0, 1)
    ):
        break

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(
    OUTPUT_DIR / "metadata.csv",
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "path", "label", "source",
            "generator", "channel_id", "video_id"
        ],
    )
    writer.writeheader()
    writer.writerows(metadata)

print("Dataset created!")
print("Real images:", counts[0])
print("AI images:", counts[1])
print("Metadata:", OUTPUT_DIR / "metadata.csv")
