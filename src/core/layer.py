"""
Class cơ bản cho Layer
"""
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QPainter, QTransform
import uuid


class Layer:
    """Base class cho tất cả các layer"""
    
    def __init__(self, name, layer_type):
        self.id = str(uuid.uuid4())
        self.name = name
        self.layer_type = layer_type
        self.visible = True
        self.locked = False
        self.opacity = 1.0
        
        # Transform properties
        self.position = QPointF(0, 0)
        self.scale = 1.0
        self.scale_x = 1.0  # Scale riêng cho chiều ngang
        self.scale_y = 1.0  # Scale riêng cho chiều dọc
        self.rotation = 0.0
        
        # Bounding box
        self.width = 0
        self.height = 0
        
    def get_bounding_rect(self):
        """Lấy bounding rectangle"""
        return QRectF(
            self.position.x(),
            self.position.y(),
            self.width * self.scale_x,
            self.height * self.scale_y
        )
    
    def set_position(self, x, y):
        """Đặt vị trí layer"""
        self.position = QPointF(x, y)
    
    def move(self, dx, dy):
        """Di chuyển layer"""
        self.position += QPointF(dx, dy)
    
    def set_scale(self, scale):
        """Đặt tỷ lệ scale đồng đều cả 2 chiều"""
        self.scale = max(0.01, scale)
        self.scale_x = self.scale
        self.scale_y = self.scale
    
    def set_scale_x(self, scale_x):
        """Đặt tỷ lệ scale theo chiều ngang"""
        self.scale_x = max(0.01, scale_x)
    
    def set_scale_y(self, scale_y):
        """Đặt tỷ lệ scale theo chiều dọc"""
        self.scale_y = max(0.01, scale_y)
    
    def set_rotation(self, angle):
        """Đặt góc xoay"""
        self.rotation = angle % 360
    
    def contains_point(self, point):
        """Kiểm tra điểm có nằm trong layer không"""
        return self.get_bounding_rect().contains(point)
    
    def get_transform(self):
        """Lấy transform matrix"""
        transform = QTransform()
        
        # Translate to position
        transform.translate(self.position.x(), self.position.y())
        
        # Rotate around center
        if self.rotation != 0:
            center_x = (self.width * self.scale_x) / 2
            center_y = (self.height * self.scale_y) / 2
            transform.translate(center_x, center_y)
            transform.rotate(self.rotation)
            transform.translate(-center_x, -center_y)
        
        # Scale (có thể khác nhau cho X và Y)
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            transform.scale(self.scale_x, self.scale_y)
        
        return transform
    
    def render(self, painter, selected=False):
        """Render layer - phải override trong subclass"""
        raise NotImplementedError
    
    def clone(self):
        """Clone layer - phải override trong subclass"""
        raise NotImplementedError
    
    def to_dict(self):
        """Chuyển sang dictionary để lưu"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.layer_type,
            'visible': self.visible,
            'locked': self.locked,
            'opacity': self.opacity,
            'position': [self.position.x(), self.position.y()],
            'scale': self.scale,
            'scale_x': self.scale_x,
            'scale_y': self.scale_y,
            'rotation': self.rotation,
            'width': self.width,
            'height': self.height
        }
    
    @classmethod
    def from_dict(cls, data):
        """Tạo layer từ dictionary - phải override trong subclass"""
        raise NotImplementedError
