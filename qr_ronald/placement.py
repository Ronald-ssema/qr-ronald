# placement.py
from typing import List

QR_SIZE = 21  # Version 1 QR


def build_reserved_mask() -> List[List[bool]]:
    """
    Build a mask marking which cells are reserved (finder patterns,
    timing patterns, format info areas, and dark module).
    True = reserved (do NOT place data bits here).
    """
    res = [[False] * QR_SIZE for _ in range(QR_SIZE)]

    def reserve_block(r0: int, c0: int, h: int, w: int):
        for r in range(r0, min(r0 + h, QR_SIZE)):
            for c in range(c0, min(c0 + w, QR_SIZE)):
                res[r][c] = True

    # Finder patterns + separators (treated as 9×9 blocks)
    reserve_block(0, 0, 9, 9)                     # top-left
    reserve_block(0, QR_SIZE - 8, 9, 9)           # top-right
    reserve_block(QR_SIZE - 8, 0, 9, 9)           # bottom-left

    # Timing patterns (row 6, col 6)
    for i in range(QR_SIZE):
        res[6][i] = True
        res[i][6] = True

    # Format info – top-left row/col
    for c in range(0, 9):
        res[8][c] = True
    for r in range(0, 9):
        res[r][8] = True

    # Format info – top-right
    for c in range(QR_SIZE - 8, QR_SIZE):
        res[8][c] = True

    # Format info – bottom-left
    for r in range(QR_SIZE - 8, QR_SIZE):
        res[r][8] = True

    # Dark module (row=13, col=8 for Version 1)
    res[13][8] = True

    return res


def place_data_bits(matrix: List[List[int]], bits: str, reserved: List[List[bool]]) -> None:
    """
    Place data bits into matrix using the standard QR zig-zag pattern.
    This version is for QR Version 1 (21×21), with mask 0.
    """
    bit_idx = 0
    direction = -1  # moving upward initially
    r = QR_SIZE - 1
    c = QR_SIZE - 1

    while c > 0:
        # Skip the timing column (column 6)
        if c == 6:
            c -= 1

        # Move vertically through this 2-column block
        while True:
            for cc in (c, c - 1):
                if not reserved[r][cc]:
                    if bit_idx < len(bits):
                        matrix[r][cc] = int(bits[bit_idx])
                        bit_idx += 1
                    else:
                        matrix[r][cc] = 0  # Should not happen for v1-L

            # Move up/down
            r += direction
            if r < 0 or r >= QR_SIZE:
                r -= direction
                direction *= -1  # Reverse direction
                break

        c -= 2  # Move to next block


def apply_mask_0(matrix: List[List[int]], reserved: List[List[bool]]) -> None:
    """
    Apply QR mask pattern 0:
       (row + col) % 2 == 0  → flip bit
    Only apply mask to non-reserved cells.
    """
    for r in range(QR_SIZE):
        for c in range(QR_SIZE):
            if not reserved[r][c]:
                if (r + c) % 2 == 0:
                    matrix[r][c] ^= 1

