from __future__ import annotations
from typing import List

MAX_DATA_CODEWORDS_V1_L = 19      # 19 data codewords
MAX_DATA_BITS_V1_L = MAX_DATA_CODEWORDS_V1_L * 8  # 152 bits


def _to_bits(value: int, bit_count: int) -> str:
    """Return bit_count-bit binary string for non-negative integer."""
    if value < 0:
        raise ValueError("value must be non-negative")
    return format(value, f"0{bit_count}b")


def encode_byte_mode_v1_l(text: str) -> List[int]:
    """
    Encode text into QR Version 1, ECC Level L, Byte mode *data codewords*.

    Steps:
      1. Encode text to ISO-8859-1 bytes.
      2. Build bitstring: 4-bit mode + 8-bit length + 8 bits per byte.
      3. Add terminator bits (up to 4 zeros) without exceeding 152 bits.
      4. Pad with zeros to make length a multiple of 8.
      5. Split into 8-bit bytes -> initial data codewords.
      6. If fewer than 19 CW, pad with 0xEC, 0x11 alternating.
    """
    # 1) bytes
    data_bytes = text.encode("iso-8859-1", errors="replace")
    if len(data_bytes) > 17:
        raise ValueError("Version 1-L Byte mode can hold at most 17 bytes")

    # 2) build bitstring
    bits = ""
    bits += "0100"                       # Byte mode indicator
    bits += _to_bits(len(data_bytes), 8) # length in 8 bits

    for b in data_bytes:
        bits += _to_bits(b, 8)

    # 3) terminator (up to 4 zeros)
    remaining = MAX_DATA_BITS_V1_L - len(bits)
    if remaining >= 4:
        bits += "0000"
    elif remaining > 0:
        bits += "0" * remaining

    # 4) pad to multiple of 8
    if len(bits) % 8 != 0:
        bits += "0" * (8 - len(bits) % 8)

    # 5) split into 8-bit bytes
    codewords = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]

    # 6) pad with 0xEC, 0x11 alternating
    pad_bytes = [0xEC, 0x11]
    idx = 0
    while len(codewords) < MAX_DATA_CODEWORDS_V1_L:
        codewords.append(pad_bytes[idx % 2])
        idx += 1

    return codewords