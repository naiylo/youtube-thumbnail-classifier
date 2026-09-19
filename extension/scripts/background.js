chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type !== "classify-thumbnail") {
      return;
    }

    console.log("Background received:", message.thumbnailData);

    // Temporary response until we connect the real classifier.
    sendResponse({ score: 42 });
  });