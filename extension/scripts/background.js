const CLASSIFIER_URL = "http://127.0.0.1:8000/classify";

async function requestClassification(thumbnailData) {
  const response = await fetch(CLASSIFIER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(thumbnailData),
  });

  if (!response.ok) {
    throw new Error(`Classifier returned HTTP ${response.status}`);
  }

  const result = await response.json();
  if (typeof result.score !== "number") {
    throw new Error("Classifier returned an invalid score");
  }

  return result.score;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== "classify-thumbnail") {
    return;
  }

  requestClassification(message.thumbnailData)
    .then((score) => {
      sendResponse({ score });
    })
    .catch((error) => {
      console.error("Classification request failed:", error);
      sendResponse({ error: error.message });
    });

  // Keep the message channel open until the HTTP request finishes.
  return true;
});