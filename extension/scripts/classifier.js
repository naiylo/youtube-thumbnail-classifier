async function classifyThumbnail(thumbnailData) {
    const response = await chrome.runtime.sendMessage({
      type: "classify-thumbnail",
      thumbnailData,
    });

    return response.score;
  }