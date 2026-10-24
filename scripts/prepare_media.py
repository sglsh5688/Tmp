#!/usr/bin/env python3
"""Create lightweight, browser-compatible copies of the source reference videos."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "dual_arm_color_sorting_english.mp4",
    "demo1.mp4",
    "cup_ID.mp4",
    "cup_ID2.mp4",
    "cup_OOD.mp4",
    "tape_ID.mp4",
    "tape_OOD1.mp4",
    "tape_OOD2.mp4",
    "tape_OOD3.mp4",
)


def prepare(name, source_dir):
    source = source_dir / name
    video = ROOT / "assets/videos" / name
    poster = ROOT / "assets/posters" / (source.stem + ".jpg")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", "scale=-2:720:force_original_aspect_ratio=decrease,fps=24",
        "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-threads", "2",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-ac", "1",
        "-movflags", "+faststart", "-map_metadata", "-1", str(video),
    ], check=True)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "1.5",
        "-i", str(video), "-frames:v", "1", "-vf", "scale=960:-2",
        "-q:v", "3", str(poster),
    ], check=True)
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
        "-of", "json", str(video),
    ], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    visual = next(s for s in info["streams"] if s["codec_type"] == "video")
    entry = {
        "file": name,
        "source_bytes": source.stat().st_size,
        "bytes": video.stat().st_size,
        "duration": round(float(info["format"]["duration"]), 3),
        "width": visual["width"],
        "height": visual["height"],
    }
    print(f'{name}: {entry["source_bytes"] / 1048576:.2f} -> {entry["bytes"] / 1048576:.2f} MiB', flush=True)
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Directory containing the original reference MP4 files")
    args = parser.parse_args()
    missing = [name for name in FILES if not (args.source / name).is_file()]
    if missing:
        parser.error("Missing files: " + ", ".join(missing))
    for folder in ("assets/videos", "assets/posters"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        entries = list(pool.map(lambda name: prepare(name, args.source), FILES))
    (ROOT / "assets/media-manifest.json").write_text(json.dumps(entries, indent=2) + "\n")
    before = sum(item["source_bytes"] for item in entries)
    after = sum(item["bytes"] for item in entries)
    print(f'Total: {before / 1048576:.2f} -> {after / 1048576:.2f} MiB ({100 * (1 - after / before):.1f}% smaller)')


if __name__ == "__main__":
    main()
