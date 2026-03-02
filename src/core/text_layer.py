"""
Layer cho text
"""
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics, QPainterPath
from .layer import Layer
from ..utils.constants import LAYER_TYPE_TEXT, DEFAULT_TEXT, DEFAULT_FONT_SIZE, DEFAULT_TEXT_COLOR


class TextLayer(Layer):
    """Layer chứa text"""
    
    def __init__(self, name, text=DEFAULT_TEXT):
        super().__init__(name, LAYER_TYPE_TEXT)
        
        self.text = text
        self.font_family = "Arial"
        self.font_size = DEFAULT_FONT_SIZE
        self.font_bold = False
        self.font_italic = False
        self.font_underline = False
        
        self.text_color = QColor(DEFAULT_TEXT_COLOR)
        self.text_align = Qt.AlignLeft
        
        # Outline properties
        self.outline_enabled = False
        self.outline_width = 2
        self.outline_color = QColor("#FFFFFF")
        
        # Background properties
        self.background_enabled = False
        self.background_color = QColor("#FFFFFF")
        self.background_padding = 10
        
        # Text box dimensions (user can resize this)
        self.text_box_width = 300  # Default text box width
        self.text_box_height = 100  # Will be auto-calculated based on text
        
        self.update_size()
    
    def get_font(self):
        """Lấy QFont object"""
        font = QFont(self.font_family, self.font_size)
        font.setBold(self.font_bold)
        font.setItalic(self.font_italic)
        font.setUnderline(self.font_underline)
        return font
    
    def update_size(self):
        """Cập nhật kích thước dựa trên text - tính toán word wrap"""
        font = self.get_font()
        metrics = QFontMetrics(font)
        
        # Sử dụng QTextDocument để tính toán word wrap chính xác
        from PyQt5.QtGui import QTextDocument
        doc = QTextDocument()
        doc.setDefaultFont(font)
        doc.setPlainText(self.text)
        doc.setTextWidth(self.text_box_width)
        
        # Kích thước thực tế của text box
        self.width = self.text_box_width
        self.height = doc.size().height()
        
        if self.background_enabled:
            self.width += self.background_padding * 2
            self.height += self.background_padding * 2
    
    def set_text(self, text):
        """Đặt text mới"""
        self.text = text
        self.update_size()
    
    def set_font_family(self, family):
        """Đặt font family"""
        self.font_family = family
        self.update_size()
    
    def set_font_size(self, size):
        """Đặt font size"""
        self.font_size = max(1, size)
        self.update_size()
    
    def set_text_box_width(self, width):
        """Đặt độ rộng text box (cho word wrap)"""
        self.text_box_width = max(50, width)  # Minimum 50px
        self.update_size()
    
    def set_text_box_height(self, height):
        """Đặt độ cao text box (không ảnh hưởng nhiều, chỉ là min height)"""
        # Height sẽ tự động điều chỉnh theo nội dung
        # Nhưng ta vẫn lưu để user có thể set minimum height
        self.text_box_height = max(20, height)
        self.update_size()
    
    def set_text_color(self, color):
        """Đặt màu text"""
        if isinstance(color, str):
            self.text_color = QColor(color)
        else:
            self.text_color = color
    
    def render(self, painter, selected=False):
        """Render layer"""
        if not self.visible or not self.text:
            return
        
        painter.save()
        
        # Apply opacity
        painter.setOpacity(self.opacity)
        
        # Apply transform
        painter.setTransform(self.get_transform(), True)
        
        font = self.get_font()
        painter.setFont(font)
        
        rect = QRectF(0, 0, self.width, self.height)
        
        # Draw background if enabled
        if self.background_enabled:
            painter.fillRect(rect, self.background_color)
            text_rect = rect.adjusted(
                self.background_padding,
                self.background_padding,
                -self.background_padding,
                -self.background_padding
            )
        else:
            text_rect = rect
        
        # Draw text with word wrap using QTextDocument
        from PyQt5.QtGui import QTextDocument, QTextOption
        from PyQt5.QtCore import QPointF as QPointF_
        
        doc = QTextDocument()
        doc.setDefaultFont(font)
        doc.setPlainText(self.text)
        doc.setTextWidth(text_rect.width())
        
        # Set text alignment
        if self.text_align == Qt.AlignLeft:
            doc.setDefaultTextOption(doc.defaultTextOption())
        elif self.text_align == Qt.AlignCenter:
            option = QTextOption()
            option.setAlignment(Qt.AlignHCenter)
            doc.setDefaultTextOption(option)
        elif self.text_align == Qt.AlignRight:
            option = QTextOption()
            option.setAlignment(Qt.AlignRight)
            doc.setDefaultTextOption(option)
        
        # Draw outline if enabled
        if self.outline_enabled:
            # Vẽ outline bằng cách vẽ text nhiều lần với offset
            painter.setPen(QPen(self.outline_color, self.outline_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            for dx in range(-self.outline_width, self.outline_width + 1):
                for dy in range(-self.outline_width, self.outline_width + 1):
                    if dx == 0 and dy == 0:
                        continue
                    painter.save()
                    painter.translate(text_rect.topLeft() + QPointF_(dx, dy))
                    doc.drawContents(painter)
                    painter.restore()
        
        # Draw text - set default text format with color
        from PyQt5.QtGui import QTextCharFormat, QTextCursor
        
        # Set text color for the entire document
        cursor = QTextCursor(doc)
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setForeground(self.text_color)
        cursor.mergeCharFormat(fmt)
        
        painter.setPen(self.text_color)
        painter.translate(text_rect.topLeft())
        doc.drawContents(painter)
        
        # Draw selection border if selected
        if selected:
            pen = QPen(QColor("#00A8FF"), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
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
        new_layer = TextLayer(f"{self.name} Copy", self.text)
        new_layer.position = self.position
        new_layer.scale = self.scale
        new_layer.scale_x = self.scale_x
        new_layer.scale_y = self.scale_y
        new_layer.rotation = self.rotation
        new_layer.opacity = self.opacity
        new_layer.visible = self.visible
        
        new_layer.font_family = self.font_family
        new_layer.font_size = self.font_size
        new_layer.font_bold = self.font_bold
        new_layer.font_italic = self.font_italic
        new_layer.font_underline = self.font_underline
        new_layer.text_color = QColor(self.text_color)
        new_layer.text_align = self.text_align
        
        new_layer.outline_enabled = self.outline_enabled
        new_layer.outline_width = self.outline_width
        new_layer.outline_color = QColor(self.outline_color)
        
        new_layer.background_enabled = self.background_enabled
        new_layer.background_color = QColor(self.background_color)
        new_layer.background_padding = self.background_padding
        
        new_layer.text_box_width = self.text_box_width
        new_layer.text_box_height = self.text_box_height
        
        new_layer.update_size()
        
        return new_layer
    
    def to_dict(self):
        """Chuyển sang dictionary"""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'font_bold': self.font_bold,
            'font_italic': self.font_italic,
            'font_underline': self.font_underline,
            'text_color': self.text_color.name(),
            'text_align': int(self.text_align),
            'outline_enabled': self.outline_enabled,
            'outline_width': self.outline_width,
            'outline_color': self.outline_color.name(),
            'background_enabled': self.background_enabled,
            'background_color': self.background_color.name(),
            'background_padding': self.background_padding,
            'text_box_width': self.text_box_width,
            'text_box_height': self.text_box_height
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Tạo layer từ dictionary"""
        layer = cls(data['name'], data['text'])
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
        
        layer.font_family = data.get('font_family', 'Arial')
        layer.font_size = data.get('font_size', DEFAULT_FONT_SIZE)
        layer.font_bold = data.get('font_bold', False)
        layer.font_italic = data.get('font_italic', False)
        layer.font_underline = data.get('font_underline', False)
        layer.text_color = QColor(data.get('text_color', DEFAULT_TEXT_COLOR))
        layer.text_align = Qt.AlignmentFlag(data.get('text_align', Qt.AlignLeft))
        
        layer.outline_enabled = data.get('outline_enabled', False)
        layer.outline_width = data.get('outline_width', 2)
        layer.outline_color = QColor(data.get('outline_color', '#FFFFFF'))
        
        layer.background_enabled = data.get('background_enabled', False)
        layer.background_color = QColor(data.get('background_color', '#FFFFFF'))
        layer.background_padding = data.get('background_padding', 10)
        
        layer.text_box_width = data.get('text_box_width', 300)
        layer.text_box_height = data.get('text_box_height', 100)
        
        layer.update_size()
        
        return layer
