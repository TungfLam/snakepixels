"""
Panel quản lý layers
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QListWidgetItem, QPushButton, QLabel, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter


class LayerItem(QWidget):
    """Widget cho mỗi layer item"""
    
    visibility_changed = pyqtSignal(str, bool)  # layer_id, visible
    
    def __init__(self, layer):
        super().__init__()
        self.layer = layer
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Visibility checkbox
        self.visible_check = QCheckBox()
        self.visible_check.setChecked(layer.visible)
        self.visible_check.stateChanged.connect(self.on_visibility_changed)
        layout.addWidget(self.visible_check)
        
        # Thumbnail (if image layer)
        if hasattr(layer, 'pixmap'):
            thumb = layer.pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            thumb_label = QLabel()
            thumb_label.setPixmap(thumb)
            thumb_label.setFixedSize(40, 40)
            layout.addWidget(thumb_label)
        
        # Layer name
        name_label = QLabel(layer.name)
        name_label.setStyleSheet("color: white;")
        layout.addWidget(name_label, 1)
        
        # Type icon
        type_label = QLabel(f"[{layer.layer_type}]")
        type_label.setStyleSheet("color: #888;")
        layout.addWidget(type_label)
        
        self.setLayout(layout)
    
    def on_visibility_changed(self, state):
        """Xử lý thay đổi visibility"""
        self.layer.visible = (state == Qt.Checked)
        self.visibility_changed.emit(self.layer.id, self.layer.visible)


class LayerPanel(QWidget):
    """Panel quản lý layers"""
    
    layer_selected = pyqtSignal(str)  # layer_id
    layers_changed = pyqtSignal()
    
    def __init__(self, project):
        super().__init__()
        self.project = project
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("Layers")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Layer list
        self.layer_list = QListWidget()
        self.layer_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                border: 1px solid #555;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #007acc;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
        """)
        self.layer_list.currentRowChanged.connect(self.on_layer_selected)
        layout.addWidget(self.layer_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_move_up = QPushButton("▲")
        self.btn_move_up.setToolTip("Move layer up")
        self.btn_move_up.clicked.connect(self.move_layer_up)
        button_layout.addWidget(self.btn_move_up)
        
        self.btn_move_down = QPushButton("▼")
        self.btn_move_down.setToolTip("Move layer down")
        self.btn_move_down.clicked.connect(self.move_layer_down)
        button_layout.addWidget(self.btn_move_down)
        
        self.btn_duplicate = QPushButton("Duplicate")
        self.btn_duplicate.clicked.connect(self.duplicate_layer)
        button_layout.addWidget(self.btn_duplicate)
        
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_layer)
        button_layout.addWidget(self.btn_delete)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.update_layer_list()
    
    def update_layer_list(self):
        """Cập nhật danh sách layers"""
        self.layer_list.clear()
        
        # Add layers in reverse order (top layer first)
        for layer in reversed(self.project.layers):
            item = QListWidgetItem()
            self.layer_list.addItem(item)
            
            layer_widget = LayerItem(layer)
            layer_widget.visibility_changed.connect(self.on_visibility_changed)
            item.setSizeHint(layer_widget.sizeHint())
            self.layer_list.setItemWidget(item, layer_widget)
            
            # Select if this is the selected layer
            if self.project.selected_layer_id == layer.id:
                self.layer_list.setCurrentItem(item)
    
    def on_layer_selected(self, row):
        """Xử lý chọn layer"""
        if row >= 0 and row < len(self.project.layers):
            # Convert from display order to actual order
            actual_index = len(self.project.layers) - 1 - row
            layer = self.project.layers[actual_index]
            self.project.selected_layer_id = layer.id
            self.layer_selected.emit(layer.id)
    
    def on_visibility_changed(self, layer_id, visible):
        """Xử lý thay đổi visibility"""
        self.layers_changed.emit()
    
    def move_layer_up(self):
        """Di chuyển layer lên trên"""
        layer = self.project.get_selected_layer()
        if not layer:
            return
        
        index = self.project.layers.index(layer)
        if index < len(self.project.layers) - 1:
            self.project.move_layer(layer.id, index + 1)
            self.update_layer_list()
            self.layers_changed.emit()
    
    def move_layer_down(self):
        """Di chuyển layer xuống dưới"""
        layer = self.project.get_selected_layer()
        if not layer:
            return
        
        index = self.project.layers.index(layer)
        if index > 0:
            self.project.move_layer(layer.id, index - 1)
            self.update_layer_list()
            self.layers_changed.emit()
    
    def duplicate_layer(self):
        """Nhân đôi layer"""
        layer = self.project.get_selected_layer()
        if layer:
            self.project.duplicate_layer(layer.id)
            self.update_layer_list()
            self.layers_changed.emit()
    
    def delete_layer(self):
        """Xóa layer"""
        layer = self.project.get_selected_layer()
        if layer:
            self.project.remove_layer(layer.id)
            self.update_layer_list()
            self.layers_changed.emit()
