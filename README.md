# YouTube Thumbnail AI Classifier

A local browser extension that adds an estimated **AI likelihood score** to YouTube thumbnails.
It sends each image to a local FastAPI server, where CLIP and a trained
logistic-regression model classify it. No API key or GPU is required.

> The score is only an estimate. The model was trained on Tiny-GenImage, not YouTube thumbnails.

## Requirements

- Python 3.10+ (Python 3.12 is known to work)
- Chrome, Brave, Edge, or another Chromium browser
- Git and an internet connection for the initial downloads

## Setup and run

Clone the repository and enter its folder:

```bash
git clone https://github.com/naiylo/youtube-thumbnail-classifier.git
cd youtube-thumbnail-classifier
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies and start the backend:

```bash
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" httpx pillow torch transformers scikit-learn joblib
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Keep this terminal open. The first start downloads CLIP from Hugging Face. Once
ready, check the API at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Load the extension

1. Open `chrome://extensions`, `brave://extensions`, or `edge://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select this repository's `extension` folder.
4. Open or refresh [YouTube](https://www.youtube.com/).

Thumbnails should show `Analyzing...`, then a score such as `73% AI`.

## Troubleshooting

- **Analysis failed:** Confirm the backend and `/docs` are running, then refresh YouTube.
- **Missing Python module:** Activate `.venv` and repeat the install command.
- **Port 8000 is busy:** Stop the other process or also change `CLASSIFIER_URL`.
- **Extension is missing:** Select the `extension` folder, then reload the page.

## Optional: retrain the model

The included model is ready to use. To rebuild it, run from the repository root (For that you will need some own training data):

```bash
python -m pip install datasets pandas numpy
mkdir -p data/splits data/embeddings models  # macOS/Linux
python training/prepare_dataset.py
python training/split_dataset.py
python training/extract_embeddings.py
python training/training_baseline.py
```

On Windows, replace `mkdir` with `New-Item -ItemType Directory -Force data/splits, data/embeddings, models`.
Training downloads 2,000 images and overwrites `models/LR_model.joblib`.
