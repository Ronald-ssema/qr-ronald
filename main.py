from __future__ import annotations

from qr_ronald.encoding import encode_byte_mode_v1_l
from qr_ronald.ecc import generate_ecc_v1_l, codewords_to_bitstring


def main() -> None:
    text = "known"
    data_cw = encode_byte_mode_v1_l(text)
    ecc_cw = generate_ecc_v1_l(data_cw)
    all_cw = data_cw + ecc_cw
    bits = codewords_to_bitstring(all_cw)

    print(f"Input text: {text!r}")
    print(f"Data codewords ({len(data_cw)}): {data_cw}")
    print(f"ECC codewords ({len(ecc_cw)}): {ecc_cw}")
    print(f"Total bits: {len(bits)} (should be 26 * 8 = 208)")


if __name__ == "__main__":
    main()
