"""
Canvas để vẽ và tương tác với layers
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QCursor
from ..utils.constants import MIN_ZOOM, MAX_ZOOM, ZOOM_STEP, GRID_SIZE, GRID_COLOR


class Canvas(QWidget):
    """Canvas widget"""
    
    layer_selected = pyqtSignal(str)  # layer_id
    layer_moved = pyqtSignal()
    layer_transformed = pyqtSignal()
    
    def __init__(self, project):
        super().__init__()
        self.project = project
        
        self.zoom = 1.0
        self.offset = QPointF(0, 0)
        
        self.show_grid = False
        self.snap_to_grid = False
        
        # Interaction state
        self.dragging = False
        self.drag_start = QPointF()
        self.drag_layer_start = QPointF()
        self.panning = False
        self.pan_start = QPointF()
        
        # Resize state
        self.resizing = False
        self.resize_handle = None
        self.resize_start_scale_x = 1.0
        self.resize_start_scale_y = 1.0
        self.resize_start_pos = QPointF()
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Background
        self.setStyleSheet("background-color: #2b2b2b;")
    
    def paintEvent(self, event):
        """Vẽ canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Fill background
        painter.fillRect(self.rect(), QColor("#2b2b2b"))
        
        # Calculate canvas position (centered)
        canvas_width = self.project.width * self.zoom
        canvas_height = self.project.height * self.zoom
        canvas_x = (self.width() - canvas_width) / 2 + self.offset.x()
        canvas_y = (self.height() - canvas_height) / 2 + self.offset.y()
        
        # Save canvas rect for later use
        self.canvas_rect = QRectF(canvas_x, canvas_y, canvas_width, canvas_height)
        
        # Draw canvas background
        painter.fillRect(self.canvas_rect, self.project.background_color)
        
        # Draw grid if enabled
        if self.show_grid:
            self.draw_grid(painter)
        
        # Set up transform for layers
        painter.save()
        painter.translate(canvas_x, canvas_y)
        painter.scale(self.zoom, self.zoom)
        
        # Draw layers (from bottom to top)
        selected_layer = self.project.get_selected_layer()
        for layer in self.project.layers:
            is_selected = (selected_layer and layer.id == selected_layer.id)
            layer.render(painter, is_selected)
        
        painter.restore()
        
        # Draw canvas border
        pen = QPen(QColor("#555555"), 1)
        painter.setPen(pen)
        painter.drawRect(self.canvas_rect)
    
    def draw_grid(self, painter):
        """Vẽ lưới"""
        painter.save()
        
        pen = QPen(QColor(GRID_COLOR), 1)
        painter.setPen(pen)
        
        grid_size = GRID_SIZE * self.zoom
        
        # Vertical lines
        x = self.canvas_rect.left()
        while x < self.canvas_rect.right():
            painter.drawLine(int(x), int(self.canvas_rect.top()), 
                           int(x), int(self.canvas_rect.bottom()))
            x += grid_size
        
        # Horizontal lines
        y = self.canvas_rect.top()
        while y < self.canvas_rect.bottom():
            painter.drawLine(int(self.canvas_rect.left()), int(y),
                           int(self.canvas_rect.right()), int(y))
            y += grid_size
        
        painter.restore()
    
    def mousePressEvent(self, event):
        """Xử lý click chuột"""
        if event.button() == Qt.MiddleButton:
            # Pan with middle mouse
            self.panning = True
            self.pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            return
        
        if event.button() == Qt.LeftButton:
            # Convert to canvas coordinates
            canvas_pos = self.screen_to_canvas(event.pos())
            
            # Check if clicked on selected layer's resize handle
            selected_layer = self.project.get_selected_layer()
            if selected_layer and selected_layer.visible:
                handle = self.get_resize_handle_at_pos(canvas_pos, selected_layer)
                if handle:
                    # Start resizing
                    self.resizing = True
                    self.resize_handle = handle
                    self.drag_start = canvas_pos
                    self.resize_start_scale_x = selected_layer.scale_x
                    self.resize_start_scale_y = selected_layer.scale_y
                    self.resize_start_pos = QPointF(selected_layer.position)
                    
                    # Lưu text_box_width ban đầu cho text layer
                    if selected_layer.layer_type == "text":
                        self.resize_start_text_width = selected_layer.text_box_width
                    
                    return
            
            # Check if clicked on a layer
            clicked_layer = None
            for layer in reversed(self.project.layers):
                if layer.visible and layer.contains_point(canvas_pos):
                    clicked_layer = layer
                    break
            
            if clicked_layer:
                self.project.selected_layer_id = clicked_layer.id
                self.layer_selected.emit(clicked_layer.id)
                
                # Start dragging
                self.dragging = True
                self.drag_start = event.pos()
                self.drag_layer_start = QPointF(clicked_layer.position)
                
                self.update()
            else:
                # Deselect
                self.project.selected_layer_id = None
                self.layer_selected.emit("")
                self.update()
    
    def mouseMoveEvent(self, event):
        """Xử lý di chuyển chuột"""
        if self.panning:
            delta = event.pos() - self.pan_start
            self.offset += delta
            self.pan_start = event.pos()
            self.update()
            return
        
        if self.resizing:
            layer = self.project.get_selected_layer()
            if layer and not layer.locked:
                canvas_pos = self.screen_to_canvas(event.pos())
                
                # Tính khoảng cách di chuyển
                delta_x = canvas_pos.x() - self.drag_start.x()
                delta_y = canvas_pos.y() - self.drag_start.y()
                
                # Kích thước ban đầu
                orig_width = layer.width * self.resize_start_scale_x
                orig_height = layer.height * self.resize_start_scale_y
                
                # TEXT LAYER: Chỉ thay đổi text box dimensions, không scale
                if layer.layer_type == "text":
                    # Lưu text_box_width ban đầu
                    if not hasattr(self, 'resize_start_text_width'):
                        self.resize_start_text_width = layer.text_box_width
                    
                    if self.resize_handle in ['left', 'right', 'tl', 'tr', 'bl', 'br']:
                        # Thay đổi chiều rộng text box
                        if self.resize_handle == 'right' or self.resize_handle in ['tr', 'br']:
                            new_width = self.resize_start_text_width + delta_x
                        else:  # left, tl, bl
                            new_width = self.resize_start_text_width - delta_x
                        
                        new_width = max(50, new_width)  # Minimum width
                        layer.set_text_box_width(new_width)
                        
                        # Điều chỉnh vị trí nếu kéo từ bên trái
                        if self.resize_handle in ['left', 'tl', 'bl']:
                            diff_x = self.resize_start_text_width - layer.text_box_width
                            layer.set_position(self.resize_start_pos.x() + diff_x, self.resize_start_pos.y())
                    
                    # Note: Height tự động điều chỉnh dựa trên word wrap
                    # Không cần xử lý resize height cho text layer
                
                # IMAGE LAYER: Scale như cũ
                else:
                    if self.resize_handle in ['tl', 'tr', 'bl', 'br']:
                        # Resize từ góc - giữ tỷ lệ
                        center_x = self.resize_start_pos.x() + orig_width / 2
                        center_y = self.resize_start_pos.y() + orig_height / 2
                        
                        start_dist = ((self.drag_start.x() - center_x) ** 2 + 
                                     (self.drag_start.y() - center_y) ** 2) ** 0.5
                        current_dist = ((canvas_pos.x() - center_x) ** 2 + 
                                       (canvas_pos.y() - center_y) ** 2) ** 0.5
                        
                        if start_dist > 0:
                            scale_factor = current_dist / start_dist
                            new_scale_x = self.resize_start_scale_x * scale_factor
                            new_scale_y = self.resize_start_scale_y * scale_factor
                            new_scale_x = max(0.1, min(5.0, new_scale_x))
                            new_scale_y = max(0.1, min(5.0, new_scale_y))
                            
                            layer.set_scale_x(new_scale_x)
                            layer.set_scale_y(new_scale_y)
                            layer.scale = (new_scale_x + new_scale_y) / 2
                    
                    elif self.resize_handle == 'top':
                        # Resize từ cạnh trên - chỉ thay đổi chiều cao
                        new_height = orig_height - delta_y
                        if layer.height > 0:
                            new_scale_y = new_height / layer.height
                            new_scale_y = max(0.1, min(5.0, new_scale_y))
                            layer.set_scale_y(new_scale_y)
                            # Điều chỉnh vị trí Y
                            diff_y = orig_height - (layer.height * new_scale_y)
                            layer.set_position(layer.position.x(), self.resize_start_pos.y() + diff_y)
                    
                    elif self.resize_handle == 'bottom':
                        # Resize từ cạnh dưới - chỉ thay đổi chiều cao
                        new_height = orig_height + delta_y
                        if layer.height > 0:
                            new_scale_y = new_height / layer.height
                            new_scale_y = max(0.1, min(5.0, new_scale_y))
                            layer.set_scale_y(new_scale_y)
                    
                    elif self.resize_handle == 'left':
                        # Resize từ cạnh trái - chỉ thay đổi chiều rộng
                        new_width = orig_width - delta_x
                        if layer.width > 0:
                            new_scale_x = new_width / layer.width
                            new_scale_x = max(0.1, min(5.0, new_scale_x))
                            layer.set_scale_x(new_scale_x)
                            # Điều chỉnh vị trí X
                            diff_x = orig_width - (layer.width * new_scale_x)
                            layer.set_position(self.resize_start_pos.x() + diff_x, layer.position.y())
                    
                    elif self.resize_handle == 'right':
                        # Resize từ cạnh phải - chỉ thay đổi chiều rộng
                        new_width = orig_width + delta_x
                        if layer.width > 0:
                            new_scale_x = new_width / layer.width
                            new_scale_x = max(0.1, min(5.0, new_scale_x))
                            layer.set_scale_x(new_scale_x)
                
                self.update()
            return
        
        if self.dragging:
            layer = self.project.get_selected_layer()
            if layer and not layer.locked:
                delta = event.pos() - self.drag_start
                new_pos = self.drag_layer_start + delta / self.zoom
                
                if self.snap_to_grid:
                    new_pos.setX(round(new_pos.x() / GRID_SIZE) * GRID_SIZE)
                    new_pos.setY(round(new_pos.y() / GRID_SIZE) * GRID_SIZE)
                
                layer.set_position(new_pos.x(), new_pos.y())
                self.layer_moved.emit()
                self.update()
        else:
            # Update cursor based on hover
            canvas_pos = self.screen_to_canvas(event.pos())
            
            # Check if hovering over resize handle
            selected_layer = self.project.get_selected_layer()
            if selected_layer and selected_layer.visible:
                handle = self.get_resize_handle_at_pos(canvas_pos, selected_layer)
                if handle:
                    # Đặt cursor phù hợp với loại handle
                    if handle in ['tl', 'br']:
                        self.setCursor(Qt.SizeFDiagCursor)  # ↘
                    elif handle in ['tr', 'bl']:
                        self.setCursor(Qt.SizeBDiagCursor)  # ↙
                    elif handle in ['top', 'bottom']:
                        self.setCursor(Qt.SizeVerCursor)    # ↕
                    elif handle in ['left', 'right']:
                        self.setCursor(Qt.SizeHorCursor)    # ↔
                    return
            
            # Check if hovering over layer
            hover_layer = None
            for layer in reversed(self.project.layers):
                if layer.visible and layer.contains_point(canvas_pos):
                    hover_layer = layer
                    break
            
            if hover_layer:
                self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def mouseReleaseEvent(self, event):
        """Xử lý thả chuột"""
        if event.button() == Qt.MiddleButton:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)
        
        if event.button() == Qt.LeftButton:
            if self.resizing:
                self.resizing = False
                self.resize_handle = None
                # Clear resize state
                if hasattr(self, 'resize_start_text_width'):
                    del self.resize_start_text_width
                self.project.save_state()
            elif self.dragging:
                self.dragging = False
                self.project.save_state()
    
    def wheelEvent(self, event):
        """Xử lý zoom bằng scroll wheel"""
        delta = event.angleDelta().y()
        
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def keyPressEvent(self, event):
        """Xử lý phím bấm"""
        if event.key() == Qt.Key_Delete:
            layer = self.project.get_selected_layer()
            if layer:
                self.project.remove_layer(layer.id)
                self.update()
        
        elif event.key() == Qt.Key_Escape:
            self.project.selected_layer_id = None
            self.layer_selected.emit("")
            self.update()
    
    def screen_to_canvas(self, screen_pos):
        """Chuyển tọa độ màn hình sang tọa độ canvas"""
        canvas_x = (screen_pos.x() - self.canvas_rect.x()) / self.zoom
        canvas_y = (screen_pos.y() - self.canvas_rect.y()) / self.zoom
        return QPointF(canvas_x, canvas_y)
    
    def zoom_in(self):
        """Zoom in"""
        self.set_zoom(self.zoom + ZOOM_STEP)
    
    def zoom_out(self):
        """Zoom out"""
        self.set_zoom(self.zoom - ZOOM_STEP)
    
    def set_zoom(self, zoom):
        """Đặt mức zoom"""
        self.zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))
        self.update()
    
    def reset_zoom(self):
        """Reset zoom về 100%"""
        self.zoom = 1.0
        self.offset = QPointF(0, 0)
        self.update()
    
    def fit_to_window(self):
        """Fit canvas vào window"""
        margin = 50
        available_width = self.width() - margin * 2
        available_height = self.height() - margin * 2
        
        zoom_x = available_width / self.project.width
        zoom_y = available_height / self.project.height
        
        self.zoom = min(zoom_x, zoom_y)
        self.offset = QPointF(0, 0)
        self.update()
    
    def get_resize_handle_at_pos(self, pos, layer):
        """Kiểm tra xem vị trí có ở trên resize handle không"""
        rect = layer.get_bounding_rect()
        handle_size = 12  # Kích thước handle
        
        # Các góc (4 corners)
        corners = [
            ('tl', rect.topLeft()),
            ('tr', rect.topRight()),
            ('bl', rect.bottomLeft()),
            ('br', rect.bottomRight())
        ]
        
        # Các cạnh (4 edges)
        edges = [
            ('top', QPointF(rect.center().x(), rect.top())),
            ('bottom', QPointF(rect.center().x(), rect.bottom())),
            ('left', QPointF(rect.left(), rect.center().y())),
            ('right', QPointF(rect.right(), rect.center().y()))
        ]
        
        # Kiểm tra góc trước (ưu tiên)
        for handle_name, corner in corners:
            handle_rect = QRectF(
                corner.x() - handle_size / 2,
                corner.y() - handle_size / 2,
                handle_size,
                handle_size
            )
            if handle_rect.contains(pos):
                return handle_name
        
        # Kiểm tra cạnh
        for handle_name, edge in edges:
            handle_rect = QRectF(
                edge.x() - handle_size / 2,
                edge.y() - handle_size / 2,
                handle_size,
                handle_size
            )
            if handle_rect.contains(pos):
                return handle_name
        
        return None
    
    def render_to_pixmap(self):
        """Render canvas ra QPixmap"""
        pixmap = QPixmap(self.project.width, self.project.height)
        pixmap.fill(self.project.background_color)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Draw all visible layers
        for layer in self.project.layers:
            if layer.visible:
                layer.render(painter, False)
        
        painter.end()
        return pixmap
