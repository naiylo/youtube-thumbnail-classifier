const THUMBNAIL_SELECTOR = "ytd-thumbnail, yt-thumbnail-view-model";

function getVideoIdFromUrl(thumbnailUrl) {
    const match = thumbnailUrl.match(/\/vi\/([^/]+)\//);
    return match?.[1] ?? null;
  }

async function addScoreBadge(thumbnail) {
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
  badge.dataset.state = "loading";
  badge.setAttribute("role", "status");
  badge.setAttribute("aria-live", "polite");
  badge.setAttribute("aria-label", "Analyzing thumbnail");
  badge.innerHTML = `
    <span class="ai-score-badge__indicator" aria-hidden="true"></span>
    <span class="ai-score-badge__value">Analyzing</span>
  `;

  thumbnail.appendChild(badge);

  try {
    const score = await classifyThumbnail(thumbnailData);
    const displayScore = Math.round(Math.max(0, Math.min(100, score)));
    const confidenceLevel = displayScore >= 70
      ? "high"
      : displayScore >= 40
        ? "medium"
        : "low";

    badge.dataset.state = "complete";
    badge.dataset.level = confidenceLevel;
    badge.setAttribute("aria-label", `${displayScore}% AI likelihood`);
    badge.innerHTML = `
      <span class="ai-score-badge__indicator" aria-hidden="true"></span>
      <span class="ai-score-badge__value">${displayScore}%</span>
      <span class="ai-score-badge__label">AI</span>
    `;
  } catch (error) {
    badge.dataset.state = "error";
    badge.setAttribute("aria-label", "Thumbnail analysis failed");
    badge.innerHTML = `
      <span class="ai-score-badge__indicator" aria-hidden="true"></span>
      <span class="ai-score-badge__value">Unavailable</span>
    `;
    console.error("Could not classify thumbnail:", error);
  }
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
