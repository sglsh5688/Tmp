"use strict";

const videos = Array.from(document.querySelectorAll("video"));
const status = document.getElementById("playback-status");
let statusTimer;

function showPlaybackStatus(message) {
  window.clearTimeout(statusTimer);
  status.textContent = message;
  status.hidden = false;
  statusTimer = window.setTimeout(() => { status.hidden = true; }, 6000);
}

async function playVideo(video) {
  try {
    for (const other of videos) {
      if (other !== video) other.pause();
    }
    video.controls = true;
    await video.play();
    status.hidden = true;
  } catch (error) {
    if (error.name !== "AbortError") {
      showPlaybackStatus("Unable to play this clip. Please try the video controls.");
    }
  }
}

for (const video of videos) {
  // Show the poster and a single play button until playback is requested.
  // Native controls remain available when JavaScript is disabled.
  video.controls = false;
  video.addEventListener("play", () => {
    if (video.paused) return;
    for (const other of videos) {
      if (other !== video) other.pause();
    }
    video.closest(".video-frame").classList.add("is-playing");
  });
  for (const event of ["pause", "ended", "emptied"]) {
    video.addEventListener(event, () => {
      video.closest(".video-frame").classList.remove("is-playing");
    });
  }
  video.addEventListener("error", () => {
    showPlaybackStatus("This video could not be loaded. Please refresh and try again.");
  });
}

for (const button of document.querySelectorAll("[data-play]")) {
  button.addEventListener("click", () => {
    playVideo(document.getElementById(button.dataset.play));
  });
}

for (const button of document.querySelectorAll("[data-player]")) {
  button.addEventListener("click", () => {
    const video = document.getElementById(button.dataset.player);
    if (button.getAttribute("aria-pressed") !== "true") {
      video.pause();
      video.poster = button.dataset.poster;
      video.src = button.dataset.src;
      video.setAttribute("aria-label", button.dataset.title);
      video.load();
      for (const sibling of document.querySelectorAll(`[data-player="${video.id}"]`)) {
        const selected = sibling === button;
        sibling.classList.toggle("is-active", selected);
        sibling.setAttribute("aria-pressed", String(selected));
      }
      document.querySelector(`[data-current-for="${video.id}"]`).textContent = button.dataset.title;
    }
    playVideo(video);
  });
}

if ("IntersectionObserver" in window) {
  const navLinks = Array.from(document.querySelectorAll("nav a"));
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting);
    if (!visible.length) return;
    const section = visible[visible.length - 1].target.id;
    for (const link of navLinks) {
      const current = link.hash === `#${section}`;
      link.classList.toggle("is-current", current);
      if (current) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }, { rootMargin: "-18% 0px -52% 0px", threshold: 0 });
  for (const section of document.querySelectorAll("main section")) observer.observe(section);
}

document.addEventListener("visibilitychange", () => {
  if (document.hidden) videos.forEach((video) => video.pause());
});
