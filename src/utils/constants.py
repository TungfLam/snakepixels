"""
Các hằng số và cấu hình cho ứng dụng
"""

# Tỷ lệ khung hình có sẵn
ASPECT_RATIOS = {
    "Instagram Post (1:1)": (1, 1),
    "Instagram Story (9:16)": (9, 16),
    "Facebook Post (16:9)": (16, 9),
    "YouTube Thumbnail (16:9)": (16, 9),
    "Twitter Post (16:9)": (16, 9),
    "Pinterest Pin (2:3)": (2, 3),
    "A4 Portrait (210:297)": (210, 297),
    "A4 Landscape (297:210)": (297, 210),
    "Custom": (0, 0)
}

# Độ phân giải mặc định cho mỗi tỷ lệ
DEFAULT_RESOLUTIONS = {
    "Instagram Post (1:1)": (1080, 1080),
    "Instagram Story (9:16)": (1080, 1920),
    "Facebook Post (16:9)": (1200, 630),
    "YouTube Thumbnail (16:9)": (1280, 720),
    "Twitter Post (16:9)": (1200, 675),
    "Pinterest Pin (2:3)": (1000, 1500),
    "A4 Portrait (210:297)": (2480, 3508),
    "A4 Landscape (297:210)": (3508, 2480),
    "Custom": (1920, 1080)
}

# Định dạng file được hỗ trợ
SUPPORTED_IMAGE_FORMATS = {
    "Import": "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*.*)",
    "Export": "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp);;WEBP (*.webp);;All Files (*.*)"
}

# Font chữ mặc định
DEFAULT_FONTS = [
    "Arial",
    "Arial Black",
    "Comic Sans MS",
    "Courier New",
    "Georgia",
    "Impact",
    "Times New Roman",
    "Trebuchet MS",
    "Verdana",
    "Helvetica",
    "Tahoma",
    "Palatino",
    "Garamond",
    "Bookman",
    "Century Gothic"
]

# Kích thước font
FONT_SIZES = list(range(10, 201, 2))

# Màu sắc có sẵn
PRESET_COLORS = [
    "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
    "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500", "#800080",
    "#FFC0CB", "#A52A2A", "#808080", "#FFD700", "#4B0082"
]

# Layer types
LAYER_TYPE_IMAGE = "image"
LAYER_TYPE_TEXT = "text"

# Canvas settings
MIN_ZOOM = 0.1
MAX_ZOOM = 5.0
ZOOM_STEP = 0.1

# Grid settings
GRID_SIZE = 50
GRID_COLOR = "#E0E0E0"

# History settings
MAX_HISTORY = 50

# Default values
DEFAULT_TEXT = "Double click to edit"
DEFAULT_FONT_SIZE = 48
DEFAULT_TEXT_COLOR = "#000000"  # Black text by default
DEFAULT_BG_COLOR = "#FFFFFF"

# Filter ranges
BRIGHTNESS_RANGE = (-100, 100)
CONTRAST_RANGE = (-100, 100)
SATURATION_RANGE = (-100, 100)
BLUR_RANGE = (0, 10)
