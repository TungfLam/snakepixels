"""
Layer cho ảnh
"""
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PIL import Image
import base64
import io

from .layer import Layer
from ..utils.constants import LAYER_TYPE_IMAGE
from ..utils.helpers import pil_to_qpixmap, qpixmap_to_pil


class ImageLayer(Layer):
    """Layer chứa ảnh"""
    
    def __init__(self, name, image_path=None, pixmap=None):
        super().__init__(name, LAYER_TYPE_IMAGE)
        
        if image_path:
            self.pixmap = QPixmap(image_path)
        elif pixmap:
            self.pixmap = pixmap
        else:
            self.pixmap = QPixmap(100, 100)
            self.pixmap.fill(Qt.white)
        
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        
        # Filter properties
        self.brightness = 0
        self.contrast = 0
        self.saturation = 0
        self.blur = 0
        
        # Border properties
        self.border_width = 0
        self.border_color = QColor("#000000")
        
    def set_pixmap(self, pixmap):
        """Đặt pixmap mới"""
        self.pixmap = pixmap
        self.width = pixmap.width()
        self.height = pixmap.height()
    
    def apply_filters(self):
        """Áp dụng các filter lên ảnh"""
        if (self.brightness == 0 and self.contrast == 0 and 
            self.saturation == 0 and self.blur == 0):
            return
        
        # Chuyển sang PIL để xử lý
        pil_image = qpixmap_to_pil(self.pixmap)
        
        # Import filters
        from .filters import apply_brightness, apply_contrast, apply_saturation, apply_blur
        
        if self.brightness != 0:
            pil_image = apply_brightness(pil_image, self.brightness)
        
        if self.contrast != 0:
            pil_image = apply_contrast(pil_image, self.contrast)
        
        if self.saturation != 0:
            pil_image = apply_saturation(pil_image, self.saturation)
        
        if self.blur > 0:
            pil_image = apply_blur(pil_image, self.blur)
        
        # Chuyển lại QPixmap
        self.pixmap = pil_to_qpixmap(pil_image)
    
    def render(self, painter, selected=False):
        """Render layer"""
        if not self.visible:
            return
        
        painter.save()
        
        # Apply opacity
        painter.setOpacity(self.opacity)
        
        # Apply transform
        painter.setTransform(self.get_transform(), True)
        
        # Draw image
        rect = QRectF(0, 0, self.width, self.height)
        painter.drawPixmap(rect.toRect(), self.pixmap)
        
        # Draw border if set
        if self.border_width > 0:
            pen = QPen(self.border_color, self.border_width)
            painter.setPen(pen)
            painter.drawRect(rect)
        
        # Draw selection border if selected
        if selected:
            pen = QPen(QColor("#00A8FF"), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(rect)
            
            # Draw 8 resize handles (4 góc + 4 cạnh)
            handle_size = 10
            
            # 4 góc
            corners = [
                rect.topLeft(),
                rect.topRight(),
                rect.bottomLeft(),
                rect.bottomRight()
            ]
            
            # 4 cạnh
            from PyQt5.QtCore import QPointF
            edges = [
                QPointF(rect.center().x(), rect.top()),      # top
                QPointF(rect.center().x(), rect.bottom()),   # bottom
                QPointF(rect.left(), rect.center().y()),     # left
                QPointF(rect.right(), rect.center().y())     # right
            ]
            
            # Vẽ handles góc (màu xanh đậm)
            painter.setBrush(QColor("#00A8FF"))
            painter.setPen(QPen(QColor("#FFFFFF"), 1))
            for handle in corners:
                handle_rect = QRectF(
                    handle.x() - handle_size/2,
                    handle.y() - handle_size/2,
                    handle_size,
                    handle_size
                )
                painter.drawRect(handle_rect)
            
            # Vẽ handles cạnh (màu xanh nhạt)
            painter.setBrush(QColor("#4FC3F7"))
            for handle in edges:
                handle_rect = QRectF(
                    handle.x() - handle_size/2,
                    handle.y() - handle_size/2,
                    handle_size,
                    handle_size
                )
                painter.drawRect(handle_rect)
        
        painter.restore()
    
    def clone(self):
        """Clone layer"""
        new_layer = ImageLayer(f"{self.name} Copy", pixmap=self.pixmap.copy())
        new_layer.position = self.position
        new_layer.scale = self.scale
        new_layer.scale_x = self.scale_x
        new_layer.scale_y = self.scale_y
        new_layer.rotation = self.rotation
        new_layer.opacity = self.opacity
        new_layer.visible = self.visible
        new_layer.brightness = self.brightness
        new_layer.contrast = self.contrast
        new_layer.saturation = self.saturation
        new_layer.blur = self.blur
        new_layer.border_width = self.border_width
        new_layer.border_color = self.border_color
        return new_layer
    
    def to_dict(self):
        """Chuyển sang dictionary"""
        data = super().to_dict()
        
        # Convert pixmap to base64
        byte_array = io.BytesIO()
        pil_image = qpixmap_to_pil(self.pixmap)
        pil_image.save(byte_array, format='PNG')
        image_base64 = base64.b64encode(byte_array.getvalue()).decode()
        
        data.update({
            'image_data': image_base64,
            'brightness': self.brightness,
            'contrast': self.contrast,
            'saturation': self.saturation,
            'blur': self.blur,
            'border_width': self.border_width,
            'border_color': self.border_color.name()
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Tạo layer từ dictionary"""
        # Decode image
        image_data = base64.b64decode(data['image_data'])
        pil_image = Image.open(io.BytesIO(image_data))
        pixmap = pil_to_qpixmap(pil_image)
        
        layer = cls(data['name'], pixmap=pixmap)
        layer.id = data['id']
        layer.visible = data['visible']
        layer.locked = data['locked']
        layer.opacity = data['opacity']
        layer.position.setX(data['position'][0])
        layer.position.setY(data['position'][1])
        layer.scale = data['scale']
        layer.scale_x = data.get('scale_x', data['scale'])
        layer.scale_y = data.get('scale_y', data['scale'])
        layer.rotation = data['rotation']
        layer.brightness = data.get('brightness', 0)
        layer.contrast = data.get('contrast', 0)
        layer.saturation = data.get('saturation', 0)
        layer.blur = data.get('blur', 0)
        layer.border_width = data.get('border_width', 0)
        layer.border_color = QColor(data.get('border_color', '#000000'))
        
        return layer
