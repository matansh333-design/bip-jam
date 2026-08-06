# BIP Jam — handoff notes for Claude Code

## What's in here
- `bip_jam_studio.html` — the current working build (single-file, Three.js, embedded geometry/audio as base64).
- `build.py` — the Python script that assembles the HTML from `cube_data_final.json`. Run `python3 build.py` after editing to regenerate the HTML.
- `cube_data_final.json` — all exported geometry/materials/textures/audio, base64-encoded. Keys: `materials`, `primitives` (base cube), `purpleColor`, `divider`, `drum`, `snareAudio`, `tree`, `kickAudio`, `triangle`, `triangleAudio`.

## Architecture so far
- 3D scene built with vanilla Three.js (r0.185, loaded from cdnjs as an ES module) — no React, no GLTFLoader/OrbitControls at runtime (both hand-rolled since they weren't reliably available via CDN in the artifact sandbox). If you're now in a normal npm project, you likely have access to the full three.js ecosystem (OrbitControls, GLTFLoader, drei, etc.) and could swap these back in for cleaner code.
- Custom camera orbit/zoom/pan via pointer events + spherical coordinates (see `spherical`, `updateCamera()`).
- Grid: `GRID_COLS` (4/8/12 bars × 4 cols each) × `GRID_ROWS` (4 lanes). Each column = one quarter-note beat. Every 4 columns = a divider (purple bar), matching the source game's bar dividers.
- `ELEMENT_TYPES` registry (drum/tree/triangle) — the pattern to follow when adding new draggable game elements: geometry + materials + one audio sample per type.
- Metronome/playhead: `advancePlayhead()` steps one column per quarter note, triggers `playElementSound()` for any placed element in that column.
- All 3D assets were exported from Blender via Blender-MCP: duplicated the source object (never modified originals), applied rotation/scale, decimated AI-generated (Tripo) meshes that came in at 500k–1M triangles down to ~5–30k, fixed origins to bottom-center of the base, and exported as .glb with baked transforms.

## Known rough edges to clean up in a "real" build
- Everything is base64-embedded in one HTML file (~3MB total) — a real project should serve .glb/.mp3 as separate static assets instead.
- No React/component structure yet — it's one big script. Worth restructuring into components once the UI chrome (Studio panel, Beat Block grid, etc.) gets built from Figma.
- Textures on AI-generated props are shrunk to 160–256px; revisit if higher fidelity is needed.
