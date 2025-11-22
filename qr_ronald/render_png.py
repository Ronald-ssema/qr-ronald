# qr_ronald/render_png.py
from typing import List
from PIL import Image


def save_qr_png(
    matrix: List[List[int]],
    path: str = "guvnorace_links_qr.png",
    scale: int = 25,
    quiet: int = 4
) -> None:
    """
    Save QR matrix as a crisp PNG.

    matrix: 2D list of 0/1
    path: output filename
    scale: pixels per module (bigger = higher resolution)
    quiet: quiet-zone size in modules
    """
    size = len(matrix)
    img_size = (size + quiet * 2) * scale

    img = Image.new("RGB", (img_size, img_size), "white")
    px = img.load()

    for r in range(size):
        for c in range(size):
            val = matrix[r][c]
            color = (0, 0, 0) if val == 1 else (255, 255, 255)

            rr0 = (r + quiet) * scale
            cc0 = (c + quiet) * scale

            for rr in range(rr0, rr0 + scale):
                for cc in range(cc0, cc0 + scale):
                    px[cc, rr] = color

    img.save(path)
    print(f"Saved PNG → {path}")
