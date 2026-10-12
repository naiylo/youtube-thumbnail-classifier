# YouTube Thumbnail AI Classifier

A learning project for building a browser extension that estimates the likelihood of YouTube thumbnails being AI-generated.

The project uses a Brave/Chrome browser extension connected to a locally hosted FastAPI backend, which handles thumbnail classification and returns prediction scores.

## Features

- **Browser Extension:** Detects YouTube thumbnails and displays an AI-generated likelihood score as a badge.
- **Dynamic Detection:** Automatically processes new thumbnails loaded while scrolling.
- **FastAPI Backend:** Runs a local Python server that receives thumbnail classification requests.
- **Local AI Inference:** Designed to host and run an AI classification model locally without relying on external APIs.
- **Privacy-Focused:** Thumbnail processing is intended to happen locally.

## Architecture

```text
YouTube
   |
   v
Browser Extension
   |  Detects thumbnails
   |  Sends classification requests
   v
Local FastAPI Server
   |  Receives thumbnail data
   |  Runs classification logic
   v
AI Classification Model
   |
   v
Prediction Score
   |
   v
Extension Badge on Thumbnail
```

## Current Status

**The browser extension and local FastAPI classification backend are implemented.**

The extension communicates with the local server, which handles classification requests and returns scores.

However, the actual machine learning model is **not connected yet**. The backend currently uses placeholder classification logic rather than predictions from a trained model.