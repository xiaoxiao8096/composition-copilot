---
name: composition-copilot
description: Composition-only photo copilot. Use when a user provides an existing photo and wants a stronger crop, aspect ratio, horizon straightening, or perspective correction without changing color, light, skin, texture, or content. Analyze the frame, protect meaningful edge context, propose or safely apply a deterministic crop/geometry plan, and export a new image plus a JSON composition record.
---

# Composition Copilot

Use this Skill to improve **framing and geometry only**. Treat the original photo as immutable. Create a new output through crop, rotation, or justified perspective correction; do not alter pixels semantically or photographically.

Accept requests in the user's language. Keep crop coordinates, script commands, and JSON records in English-compatible machine format. Explain the composition choice in the user's language.

## Absolute Boundary

| Allowed | Forbidden |
|---|---|
| Crop, aspect-ratio change, horizon straightening, and perspective correction | Exposure, white balance, contrast, color, HSL, filters, skin retouching, sharpening, blur, denoise, body/face edits, object removal, content replacement, sky changes, generative fill, or adding pixels |

Do not use an AI image editor or generative process for ordinary composition. Use deterministic geometry only. Never stretch an image to fit a ratio. Never overwrite the source.

## Resources

| Resource | Read when | Purpose |
|---|---|---|
| [Composition decision framework](references/composition-decision-framework.md) | Before every crop proposal | Decide whether to keep the full frame, select one ratio, protect edges, and apply geometry safely |
| [Composition brief](templates/composition-brief.md) | For every photo or homogeneous batch | Record subject hierarchy, crop rectangle, approval, rotation, output, and checks |
| [apply_composition.py](scripts/apply_composition.py) | After a crop contract is approved or auto-safe | Apply deterministic crop/rotation and write a JSON composition record |

## Required Workflow

1. **Inspect the full frame.** Identify primary subject, supporting context, visual direction, horizon/verticals, negative space, and every meaningful edge element.
2. **Decide whether to crop.** “Keep full frame” is a valid result. Crop only when it creates a clearer hierarchy, removes non-meaningful dead space, corrects a framing error, or matches an explicitly requested delivery ratio.
3. **Create a composition contract.** State one target ratio or the original ratio; define the crop rectangle in original EXIF-oriented pixels; name the subject placement; list retained and removed edge content; and state any rotation/perspective correction.
4. **Apply the safety gate.** Auto-execute only a low-risk crop where lost edges are clearly non-meaningful. Ask first if the crop may remove a face, person, hand, animal close-up, text, label, collectible, product edge, group-memory context, or documentary fact.
5. **Apply deterministic geometry.** Use `apply_composition.py` with the approved pixel rectangle and only a justified rotation. Do not alter color, light, texture, or content.
6. **Check the output.** Confirm subject integrity, retained context, correct ratio, no unapproved edge loss, no unintended rotation border, and no non-geometry change.
7. **Deliver reproducibly.** Provide the cropped image and its JSON record. State the exact ratio, crop rationale, and how feedback can change the frame.

## Composition Contract

Use this form before exporting:

> **Frame:** [keep full frame / crop to ratio]. Primary subject: **[subject]** at **[placement]**. Keep **[supporting context]**; remove only **[non-meaningful edge area]**. Geometry: **[none / rotate clockwise X° / perspective correction]**.
>
> **Pixels:** crop `[left, top, right, bottom]` from the EXIF-oriented original. **Approval:** [auto-safe / pending / approved].

Do not state a crop in vague language. Always include the pixel rectangle and the reason.

## Apply the Crop

Run the script only after the safety gate passes:

```bash
python3 scripts/apply_composition.py INPUT OUTPUT \
  --crop LEFT,TOP,RIGHT,BOTTOM \
  --rotate DEGREES \
  --reason "subject placement and retained context"
```

Use `--rotate 0` when no straightening is needed. The script writes a sidecar JSON record beside the output unless `--record` is provided.

## Composition Rules

Read the decision framework for ratio selection and safety boundaries. Do not mechanically force thirds, symmetry, centered framing, or a social-media ratio. Use a rule only when it improves this photo’s subject hierarchy.

Keep group memories and documentary frames wide unless the user explicitly approves context loss. For portraits, protect face, headroom, hands, shoulders, gaze direction, and any relationship context. For food and objects, protect the plate/object shape, readable labels, and the context required to understand the scene. For landscapes, protect weather, horizon, directional flow, and essential foreground/sky balance.

## Quality Gate

Do not deliver if any check fails.

| Check | Pass condition |
|---|---|
| Rationale | The crop has one concrete visual purpose, or full frame is intentionally retained |
| Subject | The primary subject is intact and clearly prioritized |
| Context | Important edge context is retained or explicitly approved for removal |
| Geometry | Rotation/perspective correction is justified and does not distort the scene |
| Fidelity | Only crop/rotation/perspective operations were applied; no visual retouching or generated content exists |
| Traceability | The JSON record matches the source dimensions, crop rectangle, rotation, and output |

If a crop is uncertain, do not guess. Present one recommended contract and ask a single focused question such as “keep more sky or more foreground?”

## Feedback

Interpret feedback only as framing instruction: wider, tighter, move subject left/right/up/down, retain more sky/foreground, change ratio, keep more context, or undo straightening. Apply feedback to the current photo only unless the user explicitly names a batch or a lasting preference.

After delivery, stop. Do not expand into color or content editing unless the user asks for a separate workflow.
