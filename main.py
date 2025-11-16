from __future__ import annotations

from qr_ronald.encoding import encode_byte_mode_v1_l
from qr_ronald.ecc import generate_ecc_v1_l, codewords_to_bitstring
from qr_ronald.matrix import (
    empty_matrix,
    add_finder_patterns,
    add_timing_patterns,
)


def main() -> None:
    # ===== ENCODING + ECC =====
    text = "known"
    data_cw = encode_byte_mode_v1_l(text)
    ecc_cw = generate_ecc_v1_l(data_cw)
    all_cw = data_cw + ecc_cw
    bits = codewords_to_bitstring(all_cw)

    print(f"Input text: {text!r}")
    print(f"Data codewords ({len(data_cw)}): {data_cw}")
    print(f"ECC codewords ({len(ecc_cw)}): {ecc_cw}")
    print(f"Total bits: {len(bits)} (should be 26 * 8 = 208)")

    # ===== QR MATRIX CONSTRUCTION =====
    m = empty_matrix()
    add_finder_patterns(m)
    add_timing_patterns(m)

    print("\nMatrix with finder + timing patterns:\n")
    for row in m:
        print("".join(str(x) for x in row))


if __name__ == "__main__":
    main()
