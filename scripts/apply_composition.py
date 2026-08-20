#!/usr/bin/env python3
"""Apply a deterministic crop and optional rotation without changing photo content."""

import argparse
import json
import sys
from pathlib import Path
from PIL import Image, ImageOps


def parse_crop(value: str) -> tuple[int, int, int, int]:
    try:
        values = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("crop must be left,top,right,bottom integers") from error
    if len(values) != 4:
        raise argparse.ArgumentTypeError("crop must contain four comma-separated integers")
    left, top, right, bottom = values
    if right <= left or bottom <= top:
        raise argparse.ArgumentTypeError("crop right/bottom must be greater than left/top")
    return values


def output_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "JPEG"
    if suffix == ".png":
        return "PNG"
    raise ValueError("output must end with .jpg, .jpeg, or .png")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a content-preserving crop and optional rotation, then write a JSON composition record."
    )
    parser.add_argument("input", type=Path, help="source image")
    parser.add_argument("output", type=Path, help="new .jpg/.jpeg/.png output")
    parser.add_argument(
        "--crop",
        type=parse_crop,
        required=True,
        metavar="LEFT,TOP,RIGHT,BOTTOM",
        help="crop rectangle in pixels after EXIF orientation is applied",
    )
    parser.add_argument(
        "--rotate",
        type=float,
        default=0.0,
        help="clockwise rotation in degrees after crop; use only for a justified horizon/vertical correction",
    )
    parser.add_argument(
        "--record",
        type=Path,
        help="optional JSON record path; defaults beside output",
    )
    parser.add_argument(
        "--reason",
        default="",
        help="short composition rationale to preserve in the JSON record",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"input not found: {args.input}")

    image = ImageOps.exif_transpose(Image.open(args.input))
    source_width, source_height = image.size
    left, top, right, bottom = args.crop
    if left < 0 or top < 0 or right > source_width or bottom > source_height:
        parser.error(
            f"crop {args.crop} lies outside oriented source dimensions {source_width}x{source_height}"
        )

    result = image.crop(args.crop)
    if args.rotate:
        # Pillow positive angles are counter-clockwise, so invert the user-facing clockwise value.
        result = result.rotate(-args.rotate, resample=Image.Resampling.BICUBIC, expand=False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fmt = output_format(args.output)
    if fmt == "JPEG" and result.mode not in {"RGB", "L"}:
        result = result.convert("RGB")
    save_args = {"quality": 95, "subsampling": 0} if fmt == "JPEG" else {}
    result.save(args.output, format=fmt, **save_args)

    record_path = args.record or args.output.with_suffix(args.output.suffix + ".composition.json")
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "source": str(args.input),
        "source_dimensions_after_exif_orientation": [source_width, source_height],
        "crop": {"left": left, "top": top, "right": right, "bottom": bottom},
        "rotation_clockwise_degrees": args.rotate,
        "output": str(args.output),
        "output_dimensions": list(result.size),
        "output_aspect_ratio": round(result.size[0] / result.size[1], 6),
        "rationale": args.reason,
        "operations": ["EXIF orientation", "crop"] + (["rotation"] if args.rotate else []),
        "content_changes": "none",
    }
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
