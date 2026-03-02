"""
Quản lý project
"""
import json
from PyQt5.QtGui import QColor
from ..utils.constants import DEFAULT_BG_COLOR


class Project:
    """Class quản lý project"""
    
    def __init__(self, width=1920, height=1080, name="Untitled"):
        self.name = name
        self.width = width
        self.height = height
        self.background_color = QColor(DEFAULT_BG_COLOR)
        
        self.layers = []
        self.selected_layer_id = None
        
        # History for undo/redo
        self.history = []
        self.history_index = -1
        
    def add_layer(self, layer, index=None):
        """Thêm layer"""
        if index is None:
            self.layers.append(layer)
        else:
            self.layers.insert(index, layer)
        
        self.selected_layer_id = layer.id
        self.save_state()
    
    def remove_layer(self, layer_id):
        """Xóa layer"""
        self.layers = [l for l in self.layers if l.id != layer_id]
        
        if self.selected_layer_id == layer_id:
            self.selected_layer_id = None
            if self.layers:
                self.selected_layer_id = self.layers[-1].id
        
        self.save_state()
    
    def get_layer_by_id(self, layer_id):
        """Lấy layer theo ID"""
        for layer in self.layers:
            if layer.id == layer_id:
                return layer
        return None
    
    def get_selected_layer(self):
        """Lấy layer đang được chọn"""
        return self.get_layer_by_id(self.selected_layer_id)
    
    def move_layer(self, layer_id, new_index):
        """Di chuyển layer đến vị trí mới"""
        layer = self.get_layer_by_id(layer_id)
        if not layer:
            return
        
        self.layers.remove(layer)
        self.layers.insert(new_index, layer)
        self.save_state()
    
    def duplicate_layer(self, layer_id):
        """Nhân đôi layer"""
        layer = self.get_layer_by_id(layer_id)
        if not layer:
            return
        
        new_layer = layer.clone()
        index = self.layers.index(layer)
        self.add_layer(new_layer, index + 1)
    
    def save_state(self):
        """Lưu trạng thái hiện tại vào history"""
        # Remove all states after current index
        self.history = self.history[:self.history_index + 1]
        
        # Save current state
        state = self.to_dict()
        self.history.append(state)
        self.history_index += 1
        
        # Limit history size
        from ..utils.constants import MAX_HISTORY
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)
            self.history_index -= 1
    
    def undo(self):
        """Hoàn tác"""
        if self.history_index > 0:
            self.history_index -= 1
            self.load_from_dict(self.history[self.history_index])
            return True
        return False
    
    def redo(self):
        """Làm lại"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.load_from_dict(self.history[self.history_index])
            return True
        return False
    
    def can_undo(self):
        """Kiểm tra có thể undo không"""
        return self.history_index > 0
    
    def can_redo(self):
        """Kiểm tra có thể redo không"""
        return self.history_index < len(self.history) - 1
    
    def to_dict(self):
        """Chuyển project sang dictionary"""
        return {
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'background_color': self.background_color.name(),
            'layers': [layer.to_dict() for layer in self.layers],
            'selected_layer_id': self.selected_layer_id
        }
    
    def load_from_dict(self, data):
        """Load project từ dictionary"""
        self.name = data['name']
        self.width = data['width']
        self.height = data['height']
        self.background_color = QColor(data['background_color'])
        self.selected_layer_id = data.get('selected_layer_id')
        
        # Load layers
        self.layers = []
        from .image_layer import ImageLayer
        from .text_layer import TextLayer
        
        for layer_data in data['layers']:
            if layer_data['type'] == 'image':
                layer = ImageLayer.from_dict(layer_data)
            elif layer_data['type'] == 'text':
                layer = TextLayer.from_dict(layer_data)
            else:
                continue
            
            self.layers.append(layer)
    
    def save_to_file(self, file_path):
        """Lưu project ra file"""
        data = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, file_path):
        """Load project từ file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project = cls(data['width'], data['height'], data['name'])
        project.load_from_dict(data)
        return project
