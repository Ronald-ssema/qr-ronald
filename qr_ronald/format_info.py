# format_info.py
from typing import List, Tuple

QR_SIZE = 21  # Version 1

# ECC level bits (2-bit)
ECC_BITS = {
    "L": 0b01,
    "M": 0b00,
    "Q": 0b11,
    "H": 0b10,
}

# BCH generator for format info
FORMAT_POLY = 0b10100110111  # 0x537
FORMAT_MASK = 0b101010000010010  # 0x5412


def _bch_remainder(bits: int) -> int:
    """
    Compute BCH remainder for 5-bit format data shifted left by 10.
    """
    # bits is already (data << 10)
    for i in range(14, 9, -1):  # from bit 14 down to 10
        if (bits >> i) & 1:
            bits ^= FORMAT_POLY << (i - 10)
    return bits & 0b1111111111  # 10 bits remainder


def get_format_bits(ecc_level: str, mask_id: int) -> str:
    """
    Return final 15-bit format string (MSB-first) after BCH + XOR mask.
    """
    if ecc_level not in ECC_BITS:
        raise ValueError("ecc_level must be one of L, M, Q, H")
    if not (0 <= mask_id <= 7):
        raise ValueError("mask_id must be 0..7")

    data5 = (ECC_BITS[ecc_level] << 3) | mask_id  # 5 bits
    bits = data5 << 10
    rem = _bch_remainder(bits)
    fmt15 = (data5 << 10) | rem
    fmt15 ^= FORMAT_MASK

    return format(fmt15, "015b")


def add_format_info(matrix: List[List[int]], ecc_level: str = "L", mask_id: int = 0) -> None:
    """
    Write the 15 format bits into the two required locations.
    Coordinates follow QR spec for Version 1 (21x21).
    """
    fmt = get_format_bits(ecc_level, mask_id)

    # First copy (around top-left finder)
    coords1: List[Tuple[int, int]] = [
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
        (8, 7), (8, 8),
        (7, 8),
        (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)
    ]

    # Second copy (top-right row + bottom-left col)
    coords2: List[Tuple[int, int]] = [
        (QR_SIZE - 1, 8), (QR_SIZE - 2, 8), (QR_SIZE - 3, 8),
        (QR_SIZE - 4, 8), (QR_SIZE - 5, 8), (QR_SIZE - 6, 8),
        (QR_SIZE - 7, 8),
        (8, QR_SIZE - 1), (8, QR_SIZE - 2), (8, QR_SIZE - 3),
        (8, QR_SIZE - 4), (8, QR_SIZE - 5), (8, QR_SIZE - 6),
        (8, QR_SIZE - 7), (8, QR_SIZE - 8)
    ]

    for i, (r, c) in enumerate(coords1):
        matrix[r][c] = int(fmt[i])

    for i, (r, c) in enumerate(coords2):
        matrix[r][c] = int(fmt[i])
