"""
Các hàm hỗ trợ tiện ích
"""
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtCore import QRect, QBuffer, QIODevice
from PIL import Image, ImageQt
import io


def qimage_to_pil(qimage):
    """Chuyển QImage sang PIL Image"""
    # Sử dụng QBuffer thay vì BytesIO
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, "PNG")
    buffer.close()
    
    # Chuyển data sang PIL
    data = buffer.data()
    return Image.open(io.BytesIO(data))


def pil_to_qimage(pil_image):
    """Chuyển PIL Image sang QImage"""
    # Convert sang RGB/RGBA nếu cần để tránh lỗi với một số format
    if pil_image.mode not in ('RGB', 'RGBA'):
        if pil_image.mode == 'P' and 'transparency' in pil_image.info:
            pil_image = pil_image.convert('RGBA')
        else:
            pil_image = pil_image.convert('RGB')
    
    # Sử dụng toqimage thay vì ImageQt constructor
    data = pil_image.tobytes("raw", pil_image.mode)
    qimage = QImage(data, pil_image.width, pil_image.height, 
                    QImage.Format_RGB888 if pil_image.mode == 'RGB' else QImage.Format_RGBA8888)
    # Copy data để tránh bị xóa khi PIL image bị garbage collected
    return qimage.copy()


def pil_to_qpixmap(pil_image):
    """Chuyển PIL Image sang QPixmap"""
    qimage = pil_to_qimage(pil_image)
    return QPixmap.fromImage(qimage)


def qpixmap_to_pil(qpixmap):
    """Chuyển QPixmap sang PIL Image"""
    qimage = qpixmap.toImage()
    return qimage_to_pil(qimage)


def hex_to_qcolor(hex_color):
    """Chuyển mã hex sang QColor"""
    return QColor(hex_color)


def qcolor_to_hex(qcolor):
    """Chuyển QColor sang mã hex"""
    return qcolor.name()


def calculate_aspect_ratio(width, height):
    """Tính tỷ lệ khung hình"""
    from math import gcd
    divisor = gcd(width, height)
    return (width // divisor, height // divisor)


def fit_rect_in_rect(source_rect, target_rect, keep_aspect=True):
    """Fit một rectangle vào rectangle khác"""
    if not keep_aspect:
        return target_rect
    
    source_aspect = source_rect.width() / source_rect.height()
    target_aspect = target_rect.width() / target_rect.height()
    
    if source_aspect > target_aspect:
        # Source rộng hơn
        new_width = target_rect.width()
        new_height = int(new_width / source_aspect)
    else:
        # Source cao hơn
        new_height = target_rect.height()
        new_width = int(new_height * source_aspect)
    
    x = target_rect.x() + (target_rect.width() - new_width) // 2
    y = target_rect.y() + (target_rect.height() - new_height) // 2
    
    return QRect(x, y, new_width, new_height)


def clamp(value, min_value, max_value):
    """Giới hạn giá trị trong khoảng"""
    return max(min_value, min(value, max_value))


def generate_unique_name(base_name, existing_names):
    """Tạo tên duy nhất"""
    if base_name not in existing_names:
        return base_name
    
    counter = 1
    while f"{base_name} {counter}" in existing_names:
        counter += 1
    
    return f"{base_name} {counter}"
