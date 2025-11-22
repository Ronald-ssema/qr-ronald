from __future__ import annotations

from qr_ronald.encoding import encode_byte_mode_v1_l
from qr_ronald.ecc import generate_ecc_v1_l, codewords_to_bitstring
from qr_ronald.matrix import empty_matrix, add_finder_patterns, add_timing_patterns
from qr_ronald.placement import place_data_bits, apply_mask_0
from qr_ronald.format_info import add_format_info
from qr_ronald.render_png import save_qr_png


def print_matrix_ascii(matrix, title="Matrix"):
    print(f"\n{title}:\n")
    for row in matrix:
        print("".join("██" if x else "  " for x in row))
    print()


def main() -> None:

    # ======================================
    # 1) TEXT TO ENCODE
    # ======================================
    text = "https://YOURUSERNAME.github.io/guvnorace-links/"

    # ======================================
    # 2) ENCODING + ECC
    # ======================================
    print("=== ENCODING + ECC ===")
    data_cw = encode_byte_mode_v1_l(text)
    ecc_cw = generate_ecc_v1_l(data_cw)
    all_cw = data_cw + ecc_cw
    bits = codewords_to_bitstring(all_cw)

    print(f"Input text: {text!r}")
    print(f"Data codewords  ({len(data_cw)}): {data_cw}")
    print(f"ECC codewords   ({len(ecc_cw)}): {ecc_cw}")
    print(f"Total bits: {len(bits)}")

    # ======================================
    # 3) QR MATRIX BASE
    # ======================================
    print("\n=== BUILDING MATRIX ===")
    m = empty_matrix()
    add_finder_patterns(m)
    add_timing_patterns(m)

    # ======================================
    # 4) PLACE DATA BITS
    # ======================================
    print("\n=== PLACING DATA BITS ===")
    reserved = place_data_bits(m, bits)

    # ======================================
    # 5) APPLY MASK 0
    # ======================================
    print("\n=== APPLY MASK 0 ===")
    apply_mask_0(m, reserved)

    # ======================================
    # 6) ADD FORMAT INFO
    # ======================================
    print("\n=== ADD FORMAT INFO ===")
    add_format_info(m, ecc_level="L", mask_id=0)

    # ======================================
    # 7) EXPORT PNG (PROFESSIONAL OUTPUT)
    # ======================================
    print("\n=== EXPORTING PNG ===")
    save_qr_png(m, "guvnorace_links_qr.png", scale=30, quiet=4)

    # ======================================
    # 8) ASCII PREVIEW
    # ======================================
    print_matrix_ascii(m, "ASCII preview (FINAL, scannable)")


if __name__ == "__main__":
    main()
