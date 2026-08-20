# Composition Brief

> Create one brief per photo. Preserve the original. This brief may authorize only crop, rotation, and perspective correction; never color, texture, beauty, or semantic changes.

## 1. Read the Frame

| Field | Record |
|---|---|
| Source | Filename and EXIF-oriented width × height |
| Primary subject | The person, object, scene, or visual event that must lead the frame |
| Secondary context | Context that supports the story and should remain visible |
| Visual direction | Horizontal flow / vertical flow / depth / symmetry / intimacy / negative space |
| Edge scan | Important people, hands, text, labels, objects, horizon, or distractions near every edge |
| Geometry | Horizon / verticals / perspective: none or specific issue |
| Full-frame verdict | Keep full frame / crop justified; state why |

## 2. Composition Contract

| Field | Record |
|---|---|
| Target ratio | Original / 3:2 / 4:3 / 4:5 / 1:1 / 16:9 / 9:16; state the purpose |
| Pixel crop | `left, top, right, bottom` in EXIF-oriented source pixels |
| Subject placement | Center / upper third / lower third / side lead room / symmetry; describe rather than force a rule |
| Retained edges | Meaningful edge content that remains visible |
| Lost edges | Exact content removed; state why it is non-meaningful or approved |
| Rotation / perspective | Clockwise degrees or correction plan; state why |
| Approval route | Auto-safe / user approval required / approved |
| One-sentence rationale | Why this crop makes the image stronger without changing the story |

## 3. Export Record

| Field | Record |
|---|---|
| Output | New filename, format, dimensions, and ratio |
| Script command | Exact `apply_composition.py` command |
| JSON record | Path to the generated composition record |
| Checks | Subject intact / protected context intact / no unapproved content loss / no color or semantic changes |

## User Feedback

Ask for feedback in framing terms: wider / tighter / keep more sky / keep more foreground / move subject left/right/up/down / retain more context / choose a different ratio / undo rotation. Default scope is the current photo only.
