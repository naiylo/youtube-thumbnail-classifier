async function classifyThumbnail(thumbnailData) {
    const response = await chrome.runtime.sendMessage({
      type: "classify-thumbnail",
      thumbnailData,
    });

    if (!response) {
      throw new Error("Classifier did not return a response");
    }

    if (response.error) {
      throw new Error(response.error);
    }

    return response.score;
  }