"""
Bộ lọc và hiệu ứng cho ảnh
"""
from PIL import Image, ImageEnhance, ImageFilter


def apply_brightness(image, value):
    """
    Áp dụng brightness
    value: -100 đến 100
    """
    if value == 0:
        return image
    
    factor = 1 + (value / 100)
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def apply_contrast(image, value):
    """
    Áp dụng contrast
    value: -100 đến 100
    """
    if value == 0:
        return image
    
    factor = 1 + (value / 100)
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def apply_saturation(image, value):
    """
    Áp dụng saturation
    value: -100 đến 100
    """
    if value == 0:
        return image
    
    factor = 1 + (value / 100)
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def apply_blur(image, value):
    """
    Áp dụng blur
    value: 0 đến 10
    """
    if value == 0:
        return image
    
    return image.filter(ImageFilter.GaussianBlur(radius=value))


def apply_sharpen(image):
    """Áp dụng sharpen"""
    return image.filter(ImageFilter.SHARPEN)


def apply_grayscale(image):
    """Chuyển sang grayscale"""
    return image.convert('L').convert('RGB')


def apply_sepia(image):
    """Áp dụng sepia tone"""
    grayscale = image.convert('L')
    sepia = Image.new('RGB', image.size)
    
    pixels = grayscale.load()
    sepia_pixels = sepia.load()
    
    for y in range(image.height):
        for x in range(image.width):
            gray = pixels[x, y]
            
            # Sepia formula
            r = min(255, int(gray * 1.0))
            g = min(255, int(gray * 0.95))
            b = min(255, int(gray * 0.82))
            
            sepia_pixels[x, y] = (r, g, b)
    
    return sepia


def apply_invert(image):
    """Đảo ngược màu"""
    from PIL import ImageOps
    return ImageOps.invert(image.convert('RGB'))


def apply_edge_enhance(image):
    """Tăng cường cạnh"""
    return image.filter(ImageFilter.EDGE_ENHANCE)


def apply_emboss(image):
    """Áp dụng emboss"""
    return image.filter(ImageFilter.EMBOSS)


def apply_contour(image):
    """Áp dụng contour"""
    return image.filter(ImageFilter.CONTOUR)


def apply_posterize(image, bits=4):
    """Áp dụng posterize"""
    from PIL import ImageOps
    return ImageOps.posterize(image, bits)


def apply_solarize(image, threshold=128):
    """Áp dụng solarize"""
    from PIL import ImageOps
    return ImageOps.solarize(image, threshold)


def add_border(image, border_width, border_color):
    """Thêm viền cho ảnh"""
    from PIL import ImageOps
    return ImageOps.expand(image, border=border_width, fill=border_color)


def rotate_image(image, angle):
    """Xoay ảnh"""
    return image.rotate(angle, expand=True, fillcolor=(255, 255, 255, 0))


def flip_horizontal(image):
    """Lật ngang"""
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def flip_vertical(image):
    """Lật dọc"""
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def crop_image(image, box):
    """Crop ảnh"""
    return image.crop(box)


def resize_image(image, size, keep_aspect=True):
    """Resize ảnh"""
    if keep_aspect:
        image.thumbnail(size, Image.Resampling.LANCZOS)
        return image
    else:
        return image.resize(size, Image.Resampling.LANCZOS)
