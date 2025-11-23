from __future__ import annotations
import qrcode

def main() -> None:
    # put your REAL landing page here (full https)
    URL = "https://ronald-ssema.github.io/qr-ronald/"

    qr = qrcode.QRCode(
        version=3,  # Version 3
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # H = high recovery
        box_size=20,
        border=4,
    )

    qr.add_data(URL)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = "guvnorace_links_qr.png"
    img.save(filename)

    print(f"Saved QR -> {filename}")
    print(f"QR opens -> {URL}")

if __name__ == "__main__":
    main()
