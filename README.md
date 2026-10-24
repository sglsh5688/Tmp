# Real-world experiment plan

A dark, responsive page with ten reference videos and a concise experiment plan. All page content is in English. Plain HTML, CSS, and JavaScript; no build step or external runtime dependencies.

## Preview

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000>.

## Content

| Section | Reference files | Planned use |
| --- | --- | --- |
| Project-page video | `dual_arm_color_sorting_english.mp4`, `dual_arm_color_sorting.mp4`, `demo1.mp4` | Film one successful run for a showcase; no evaluation |
| Pick & place — Cup, ID | `cup_ID.mp4`, `cup_ID2.mp4` | Training + ID evaluation |
| Pick & place — Cup, OOD | `cup_OOD.mp4` | Evaluation only |
| Stack — Tape, ID | `tape_ID.mp4` | Training + ID evaluation |
| Stack — Tape, OOD | `tape_OOD1.mp4`, `tape_OOD2.mp4`, `tape_OOD3.mp4` | Evaluation only |
| Deformable objects | TBD | Task and object to be decided |

These are planning references, not reported model evaluation results.

## Media

`assets/videos/` contains compressed sharing copies. Source files are kept outside this repository and left unchanged. Videos use H.264, up to 720p, 24 fps, AAC audio where present, and MP4 fast start. Playback is user initiated, muted by default, with native controls and poster images; only one video plays at a time.

To regenerate the videos and posters with FFmpeg installed:

```sh
python3 scripts/prepare_media.py /path/to/original/videos
```

Compression sizes and durations are recorded in `assets/media-manifest.json`.
The ten videos total 5.08 MiB, down from 74.40 MiB (93.2% smaller).

## Editing

- `index.html`: English copy, section structure, and clip selections.
- `styles.css`: dark theme and responsive layout.
- `app.js`: clip selection, playback, and section navigation.

The repository root is ready for static hosting, including GitHub Pages. Relative asset paths also work when served from a project subdirectory.
