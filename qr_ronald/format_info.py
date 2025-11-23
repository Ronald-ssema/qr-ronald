from typing import List

QR_SIZE = 21

# Format info positions for Version 1
FORMAT_POS_1 = [
    (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,7),(8,8),
    (7,8),(5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
]
FORMAT_POS_2 = [
    (20,8),(19,8),(18,8),(17,8),(16,8),(15,8),(14,8),
    (13,8),(8,20),(8,19),(8,18),(8,17),(8,16),(8,15),(8,14),
]

FORMAT_MASK = 0b101010000010010

ECC_BITS = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}

def bch_encode_15_5(value: int) -> int:
    # generator polynomial: x^10 + x^8 + x^5 + x^4 + x^2 + x + 1  (0b10100110111)
    g = 0b10100110111
    v = value << 10
    for i in range(14, 9, -1):
        if (v >> i) & 1:
            v ^= g << (i - 10)
    return (value << 10) | v

def get_format_bits(ecc_level: str, mask_id: int) -> str:
    data = (ECC_BITS[ecc_level] << 3) | mask_id
    bits15 = bch_encode_15_5(data) ^ FORMAT_MASK
    return format(bits15, "015b")

def add_format_info(matrix: List[List[int]], ecc_level="L", mask_id=0) -> None:
    bits = get_format_bits(ecc_level, mask_id)

    for (r,c), b in zip(FORMAT_POS_1, bits):
        matrix[r][c] = int(b)

    for (r,c), b in zip(FORMAT_POS_2, bits):
        matrix[r][c] = int(b)
