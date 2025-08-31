"""
QR code utility using the 'qrcode' package.
Reference: https://pypi.org/project/qrcode/
"""
import io
import qrcode 
from PIL import Image


def generate_qr_png(data: str, scale: int = 4, border: int = 2) -> bytes:
    """
    Generate a QR code PNG as bytes from the given data using qrcode.

    Parameters:
        data: The string to encode (e.g., a shareable link).
        scale: Pixel scaling factor (larger = bigger image).
        border: Border size in QR modules.

    Returns:
        PNG bytes suitable for st.image.
    """
    if not data:
        raise ValueError("QR data must be a non-empty string.")
    buf = io.BytesIO()

    # qrcode: box_size approximates scale; border is in boxes
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=max(1, scale),
        border=max(0, border),
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Ensure PNG and consistent mode
    img = img.convert("RGB")
    img.save(buf, format="PNG")
    return buf.getvalue()