from __future__ import annotations
from typing import List
import reedsolo

NUM_ECC_CODEWORDS_V1_L = 7  # for Version 1, Level L


def generate_ecc_v1_l(data_codewords: List[int]) -> List[int]:
    """
    Given 19 data codewords, return 7 ECC codewords for Version 1, Level L.
    """
    if len(data_codewords) != 19:
        raise ValueError("Version 1-L must have exactly 19 data codewords")

    rs = reedsolo.RSCodec(nsym=NUM_ECC_CODEWORDS_V1_L)
    encoded = rs.encode(bytes(data_codewords))
    ecc_bytes = encoded[-NUM_ECC_CODEWORDS_V1_L:]
    return list(ecc_bytes)


def codewords_to_bitstring(codewords: List[int]) -> str:
    """Convert a list of codewords to a single MSB-first bitstring."""
    return "".join(format(cw, "08b") for cw in codewords)


def finalize_codewords_v1_l(data_codewords: List[int]) -> List[int]:
    """
    For Version 1-L, return the full sequence of codewords (data then ECC).
    Expects exactly 19 data codewords.
    """
    ecc = generate_ecc_v1_l(data_codewords)
    return data_codewords + ecc


def final_bitstream_v1_l(data_codewords: List[int]) -> str:
    """
    Return the final MSB-first bitstring for Version 1-L after appending ECC.
    """
    final_cw = finalize_codewords_v1_l(data_codewords)
    return codewords_to_bitstring(final_cw)


__all__ = [
    "NUM_ECC_CODEWORDS_V1_L",
    "generate_ecc_v1_l",
    "codewords_to_bitstring",
    "finalize_codewords_v1_l",
    "final_bitstream_v1_l",
]