# qr_ronald/matrix.py
from __future__ import annotations
from typing import List

QR_SIZE = 21  # Version 1 QR is always 21x21


def empty_matrix(size: int = QR_SIZE) -> List[List[int]]:
    """
    Create an empty QR matrix filled with zeros.
    Allow size to be passed OR default to 21.
    """
    return [[0 for _ in range(size)] for _ in range(size)]


def _place_finder(m: List[List[int]], r0: int, c0: int) -> None:
    """
    Place a standard 7x7 finder pattern at top-left corner (r0, c0).
    """
    for r in range(7):
        for c in range(7):
            rr, cc = r0 + r, c0 + c

            outer = (r == 0 or r == 6 or c == 0 or c == 6)
            inner = (2 <= r <= 4 and 2 <= c <= 4)

            m[rr][cc] = 1 if (outer or inner) else 0


def add_finder_patterns(m: List[List[int]]) -> None:
    """
    Add finder patterns to the three corners.
    """
    size = len(m)
    _place_finder(m, 0, 0)                # top-left
    _place_finder(m, 0, size - 7)         # top-right
    _place_finder(m, size - 7, 0)         # bottom-left

    # Optional separators (white border) around finders (still ok if left 0)
    # These help scanning but not required for coursework correctness.
    # Top-left separator
    for i in range(8):
        if i < size:
            m[7][i] = 0
            m[i][7] = 0

    # Top-right separator
    for i in range(8):
        m[7][size - 1 - i] = 0
        m[i][size - 8] = 0

    # Bottom-left separator
    for i in range(8):
        m[size - 8][i] = 0
        m[size - 1 - i][7] = 0


def add_timing_patterns(m: List[List[int]]) -> None:
    """
    Add timing patterns on row 6 and col 6.
    Alternate black/white modules.
    """
    size = len(m)

    # Row 6 timing (skip finder areas)
    for c in range(size):
        if 8 <= c <= size - 9:
            m[6][c] = 1 if c % 2 == 0 else 0

    # Col 6 timing (skip finder areas)
    for r in range(size):
        if 8 <= r <= size - 9:
            m[r][6] = 1 if r % 2 == 0 else 0

    # Dark module for Version 1 at (13, 8)
    m[size - 8][8] = 1
