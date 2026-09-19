const THUMBNAIL_SELECTOR = "ytd-thumbnail, yt-thumbnail-view-model";

function getVideoIdFromUrl(thumbnailUrl) {
    const match = thumbnailUrl.match(/\/vi\/([^/]+)\//);
    return match?.[1] ?? null;
  }

function classifyThumbnail(thumbnailData) {
    console.log("Classifying thumbnail:", thumbnailData);

    // Temporary result until a real classifier is connected.
    return 42;
  }

function addScoreBadge(thumbnail) {
  // Do not add the badge twice.
  if (thumbnail.querySelector(".ai-score-badge")) {
    return;
  }

  const image = thumbnail.querySelector("img");

  if (!image) {
    return;
  }

  const thumbnailUrl = image?.currentSrc || image?.src;

  if (!thumbnailUrl) {
    image.addEventListener(
      "load",
      () => addScoreBadge(thumbnail),
      { once: true }
    );

    return;
  }

  const thumbnailData = {
    videoId: getVideoIdFromUrl(thumbnailUrl),
    imageUrl: thumbnailUrl,
    title: image.alt || null,
  };

  console.log("Thumbnail data:", thumbnailData);

  thumbnail.classList.add("ai-score-container");

  const badge = document.createElement("div");
  badge.className = "ai-score-badge";

  // Temporary fake score.
  const score = classifyThumbnail(thumbnailData);
  badge.textContent = `${score}% AI`;

  thumbnail.appendChild(badge);
}

function processThumbnails(root = document) {
  // Handle root itself if it is a thumbnail.
  if (root.matches?.(THUMBNAIL_SELECTOR)) {
    addScoreBadge(root);
  }

  // Handle thumbnails contained inside root.
  root.querySelectorAll?.(THUMBNAIL_SELECTOR).forEach(addScoreBadge);
}

// Process thumbnails already on the page.
processThumbnails();

// Process thumbnails YouTube adds later.
const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    for (const node of mutation.addedNodes) {
      if (node.nodeType === Node.ELEMENT_NODE) {
        processThumbnails(node);
      }
    }
  }
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});

console.log("AI Thumbnail Detector is running");
