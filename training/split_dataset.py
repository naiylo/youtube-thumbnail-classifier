import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

# Read data
INPUT_FILE = Path("data/metadata.csv")
metadata = pd.read_csv(INPUT_FILE)
print(metadata.head())

# Verify files labels are correct, all files exist, and there are no duplicates
if metadata["label"].isin([0,1]).all():
    print(f"\n\n\nAll labels are valid")
else:
    print("Some labels are not valid")

if metadata["path"].apply(lambda x: Path(x).is_file()).all():
    print("All files exist")
else:
    print("Some files are missing")

duplicate_count = metadata["path"].duplicated().sum()
print(f"Number of duplicated files: {duplicate_count}\n\n\n")

# Verify split of data (same number of ai and real pictures) + nuber of pictures per generator

print("Images per class:")
class_counts = metadata["label"].value_counts()

print(f"Real: {class_counts[0]}")
print(f"AI:   {class_counts[1]}\n\n\n")

print("Images per generator:")
print(metadata["generator"].value_counts())

# Split the dataset
train_df, temp_df = train_test_split(
    metadata,
    test_size=0.3,
    random_state=42,
    stratify=metadata["label"]
)

test_df, val_df = train_test_split(
    temp_df,
    test_size=0.5,
    random_state=42,
    stratify=temp_df["label"]
)

# Check that the distribution worked out
assert len(train_df) == 0.7*len(metadata), "Training set does not meet size requirements"
assert len(test_df) == 0.15*len(metadata), "Testing set does not meet size requirements"
assert len(val_df) == 0.15*len(metadata), "Validation set does not meet size requirements"

# Check that each set is also balanced (stratify worked out correctly)
assert train_df["label"].value_counts()[0] == train_df["label"].value_counts()[1], "Stratify did not work out for Training set"
assert test_df["label"].value_counts()[0] == test_df["label"].value_counts()[1], "Stratify did not work out for Test set"
assert val_df["label"].value_counts()[0] == val_df["label"].value_counts()[1], "Stratify did not work out for Val set"

# Check for data leakage

train_paths = set(train_df["path"])
test_paths = set(test_df["path"])
val_paths = set(val_df["path"])

assert train_paths.isdisjoint(test_paths) and test_paths.isdisjoint(val_paths) and val_paths.isdisjoint(train_paths), "Overlapping happened"

# Safe the splits
SAVE_PATH = Path("data/splits")
train_df.to_csv(SAVE_PATH / "train.csv", index = False)
test_df.to_csv(SAVE_PATH / "test.csv", index = False)
val_df.to_csv(SAVE_PATH / "val.csv", index = False)


