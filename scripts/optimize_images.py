from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "Resources" / "Images"
OUTPUT_DIR = SOURCE_DIR / "optimized"

JOBS = [
    {
        "source": SOURCE_DIR / "pfp.jpg",
        "output": OUTPUT_DIR / "pfp-420.webp",
        "width": 420,
        "quality": 80,
        "lossless": False,
    },
    {
        "source": SOURCE_DIR / "pfp.jpg",
        "output": OUTPUT_DIR / "pfp-840.webp",
        "width": 840,
        "quality": 82,
        "lossless": False,
    },
    {
        "source": SOURCE_DIR / "UoMLogo.png",
        "output": OUTPUT_DIR / "uomlogo-160.webp",
        "width": 160,
        "quality": 100,
        "lossless": True,
    },
    {
        "source": SOURCE_DIR / "kings.png",
        "output": OUTPUT_DIR / "kings-160.webp",
        "width": 160,
        "quality": 82,
        "lossless": False,
    },
    {
        "source": SOURCE_DIR / "aiupscale.png",
        "output": OUTPUT_DIR / "aiupscale-512.webp",
        "width": 512,
        "quality": 84,
        "lossless": False,
    },
    {
        "source": SOURCE_DIR / "Ico192.png",
        "output": OUTPUT_DIR / "website-192.webp",
        "width": 192,
        "quality": 84,
        "lossless": False,
    },
]


def prepare_image(image: Image.Image) -> Image.Image:
    if image.mode in {"RGB", "RGBA"}:
        return image
    has_alpha = "A" in image.getbands()
    return image.convert("RGBA" if has_alpha else "RGB")


def resize_image(
    image: Image.Image, width: int
) -> Image.Image:
    if image.width <= width:
        return image

    ratio = width / image.width
    height = round(image.height * ratio)
    return image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )


def build_asset(job: dict) -> None:
    source = job["source"]
    output = job["output"]
    output.parent.mkdir(
        parents=True, exist_ok=True
    )

    image = Image.open(source)
    image = prepare_image(image)
    image = resize_image(image, job["width"])
    image.save(
        output,
        format="WEBP",
        quality=job["quality"],
        lossless=job["lossless"],
        method=6,
    )

    print(
        f"{source.relative_to(ROOT)} -> "
        f"{output.relative_to(ROOT)} | "
        f"{source.stat().st_size} -> "
        f"{output.stat().st_size}"
    )


def main() -> None:
    for job in JOBS:
        build_asset(job)


if __name__ == "__main__":
    main()
