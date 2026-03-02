"""
Panel thuộc tính cho layer
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QPushButton, QComboBox, QSpinBox,
                             QColorDialog, QGroupBox, QCheckBox, QLineEdit,
                             QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QColor
from ..utils.constants import (FONT_SIZES, DEFAULT_FONTS, PRESET_COLORS,
                               BRIGHTNESS_RANGE, CONTRAST_RANGE, SATURATION_RANGE, BLUR_RANGE)


class PropertiesPanel(QWidget):
    """Panel thuộc tính"""
    
    property_changed = pyqtSignal()
    
    def __init__(self, project):
        super().__init__()
        self.project = project
        self.current_layer = None
        self._updating_text = False  # Flag để tránh update properties khi đang gõ text
        
        # Timer để debounce text changes
        self.text_change_timer = QTimer()
        self.text_change_timer.setSingleShot(True)
        self.text_change_timer.setInterval(300)  # 300ms delay
        self.text_change_timer.timeout.connect(self.apply_text_change)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Main widget
        main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        main_widget.setLayout(self.main_layout)
        
        # Title
        title = QLabel("Properties")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        self.main_layout.addWidget(title)
        
        # Properties will be added dynamically
        self.main_layout.addStretch()
        
        scroll.setWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def clear_properties(self):
        """Xóa tất cả properties"""
        while self.main_layout.count() > 2:  # Keep title and stretch
            item = self.main_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
    
    def update_properties(self, layer):
        """Cập nhật properties cho layer"""
        # Không update nếu đang gõ text
        if self._updating_text:
            return
            
        self.current_layer = layer
        self.clear_properties()
        
        if not layer:
            no_selection = QLabel("No layer selected")
            no_selection.setStyleSheet("color: #888;")
            self.main_layout.insertWidget(1, no_selection)
            return
        
        # Block signals để tránh trigger khi update UI
        self.blockSignals(True)
        
        # Common properties
        self.add_common_properties()
        
        # Layer-specific properties
        if layer.layer_type == "image":
            self.add_image_properties()
        elif layer.layer_type == "text":
            self.add_text_properties()
        
        # Unblock signals
        self.blockSignals(False)
    
    def add_common_properties(self):
        """Thêm properties chung"""
        # Transform group
        transform_group = QGroupBox("Transform")
        transform_layout = QVBoxLayout()
        
        # Position
        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel("Position:"))
        
        self.pos_x = QSpinBox()
        self.pos_x.setRange(-10000, 10000)
        self.pos_x.setValue(int(self.current_layer.position.x()))
        self.pos_x.valueChanged.connect(self.on_position_changed)
        pos_layout.addWidget(QLabel("X:"))
        pos_layout.addWidget(self.pos_x)
        
        self.pos_y = QSpinBox()
        self.pos_y.setRange(-10000, 10000)
        self.pos_y.setValue(int(self.current_layer.position.y()))
        self.pos_y.valueChanged.connect(self.on_position_changed)
        pos_layout.addWidget(QLabel("Y:"))
        pos_layout.addWidget(self.pos_y)
        
        transform_layout.addLayout(pos_layout)
        
        # Scale
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Scale:"))
        
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(1, 500)
        self.scale_slider.setValue(int(self.current_layer.scale * 100))
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
        scale_layout.addWidget(self.scale_slider)
        
        self.scale_label = QLabel(f"{self.current_layer.scale * 100:.0f}%")
        scale_layout.addWidget(self.scale_label)
        
        transform_layout.addLayout(scale_layout)
        
        # Rotation
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation:"))
        
        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setValue(int(self.current_layer.rotation))
        self.rotation_slider.valueChanged.connect(self.on_rotation_changed)
        rotation_layout.addWidget(self.rotation_slider)
        
        self.rotation_label = QLabel(f"{self.current_layer.rotation:.0f}°")
        rotation_layout.addWidget(self.rotation_label)
        
        transform_layout.addLayout(rotation_layout)
        
        # Opacity
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(self.current_layer.opacity * 100))
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        opacity_layout.addWidget(self.opacity_slider)
        
        self.opacity_label = QLabel(f"{self.current_layer.opacity * 100:.0f}%")
        opacity_layout.addWidget(self.opacity_label)
        
        transform_layout.addLayout(opacity_layout)
        
        transform_group.setLayout(transform_layout)
        self.main_layout.insertWidget(1, transform_group)
    
    def add_image_properties(self):
        """Thêm properties cho image layer"""
        # Filters group
        filters_group = QGroupBox("Filters")
        filters_layout = QVBoxLayout()
        
        # Brightness
        brightness_layout = QHBoxLayout()
        brightness_layout.addWidget(QLabel("Brightness:"))
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(*BRIGHTNESS_RANGE)
        self.brightness_slider.setValue(self.current_layer.brightness)
        self.brightness_slider.valueChanged.connect(self.on_filter_changed)
        brightness_layout.addWidget(self.brightness_slider)
        self.brightness_label = QLabel(str(self.current_layer.brightness))
        brightness_layout.addWidget(self.brightness_label)
        filters_layout.addLayout(brightness_layout)
        
        # Contrast
        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(QLabel("Contrast:"))
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(*CONTRAST_RANGE)
        self.contrast_slider.setValue(self.current_layer.contrast)
        self.contrast_slider.valueChanged.connect(self.on_filter_changed)
        contrast_layout.addWidget(self.contrast_slider)
        self.contrast_label = QLabel(str(self.current_layer.contrast))
        contrast_layout.addWidget(self.contrast_label)
        filters_layout.addLayout(contrast_layout)
        
        # Saturation
        saturation_layout = QHBoxLayout()
        saturation_layout.addWidget(QLabel("Saturation:"))
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setRange(*SATURATION_RANGE)
        self.saturation_slider.setValue(self.current_layer.saturation)
        self.saturation_slider.valueChanged.connect(self.on_filter_changed)
        saturation_layout.addWidget(self.saturation_slider)
        self.saturation_label = QLabel(str(self.current_layer.saturation))
        saturation_layout.addWidget(self.saturation_label)
        filters_layout.addLayout(saturation_layout)
        
        # Blur
        blur_layout = QHBoxLayout()
        blur_layout.addWidget(QLabel("Blur:"))
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(*BLUR_RANGE)
        self.blur_slider.setValue(self.current_layer.blur)
        self.blur_slider.valueChanged.connect(self.on_filter_changed)
        blur_layout.addWidget(self.blur_slider)
        self.blur_label = QLabel(str(self.current_layer.blur))
        blur_layout.addWidget(self.blur_label)
        filters_layout.addLayout(blur_layout)
        
        filters_group.setLayout(filters_layout)
        self.main_layout.insertWidget(2, filters_group)
    
    def add_text_properties(self):
        """Thêm properties cho text layer"""
        # Text group
        text_group = QGroupBox("Text")
        text_layout = QVBoxLayout()
        
        # Text content
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.current_layer.text)
        self.text_edit.setMaximumHeight(100)
        # Dùng textChanged với timer debounce để không mất focus
        self.text_edit.textChanged.connect(self.on_text_changed_debounced)
        # Set tab change focus để dễ dàng chuyển giữa các fields
        self.text_edit.setTabChangesFocus(True)
        text_layout.addWidget(QLabel("Content:"))
        text_layout.addWidget(self.text_edit)
        
        # Font family
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(DEFAULT_FONTS)
        self.font_combo.setCurrentText(self.current_layer.font_family)
        self.font_combo.currentTextChanged.connect(self.on_font_changed)
        font_layout.addWidget(self.font_combo)
        text_layout.addLayout(font_layout)
        
        # Font size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems([str(s) for s in FONT_SIZES])
        self.font_size_combo.setCurrentText(str(self.current_layer.font_size))
        self.font_size_combo.currentTextChanged.connect(self.on_font_size_changed)
        size_layout.addWidget(self.font_size_combo)
        text_layout.addLayout(size_layout)
        
        # Font style
        style_layout = QHBoxLayout()
        self.bold_check = QCheckBox("Bold")
        self.bold_check.setChecked(self.current_layer.font_bold)
        self.bold_check.stateChanged.connect(self.on_font_style_changed)
        style_layout.addWidget(self.bold_check)
        
        self.italic_check = QCheckBox("Italic")
        self.italic_check.setChecked(self.current_layer.font_italic)
        self.italic_check.stateChanged.connect(self.on_font_style_changed)
        style_layout.addWidget(self.italic_check)
        
        self.underline_check = QCheckBox("Underline")
        self.underline_check.setChecked(self.current_layer.font_underline)
        self.underline_check.stateChanged.connect(self.on_font_style_changed)
        style_layout.addWidget(self.underline_check)
        text_layout.addLayout(style_layout)
        
        # Text color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.text_color_btn = QPushButton()
        self.text_color_btn.setStyleSheet(f"background-color: {self.current_layer.text_color.name()};")
        self.text_color_btn.setFixedSize(50, 25)
        self.text_color_btn.clicked.connect(self.on_text_color_clicked)
        color_layout.addWidget(self.text_color_btn)
        color_layout.addStretch()
        text_layout.addLayout(color_layout)
        
        # Outline
        self.outline_check = QCheckBox("Enable Outline")
        self.outline_check.setChecked(self.current_layer.outline_enabled)
        self.outline_check.stateChanged.connect(self.on_outline_changed)
        text_layout.addWidget(self.outline_check)
        
        text_group.setLayout(text_layout)
        self.main_layout.insertWidget(2, text_group)
    
    def on_position_changed(self):
        """Xử lý thay đổi position"""
        if self.current_layer:
            self.current_layer.set_position(self.pos_x.value(), self.pos_y.value())
            self.property_changed.emit()
    
    def on_scale_changed(self, value):
        """Xử lý thay đổi scale"""
        if self.current_layer:
            scale = value / 100.0
            self.current_layer.set_scale(scale)
            self.scale_label.setText(f"{value}%")
            self.property_changed.emit()
    
    def on_rotation_changed(self, value):
        """Xử lý thay đổi rotation"""
        if self.current_layer:
            self.current_layer.set_rotation(value)
            self.rotation_label.setText(f"{value}°")
            self.property_changed.emit()
    
    def on_opacity_changed(self, value):
        """Xử lý thay đổi opacity"""
        if self.current_layer:
            self.current_layer.opacity = value / 100.0
            self.opacity_label.setText(f"{value}%")
            self.property_changed.emit()
    
    def on_filter_changed(self):
        """Xử lý thay đổi filter"""
        if self.current_layer and self.current_layer.layer_type == "image":
            self.current_layer.brightness = self.brightness_slider.value()
            self.current_layer.contrast = self.contrast_slider.value()
            self.current_layer.saturation = self.saturation_slider.value()
            self.current_layer.blur = self.blur_slider.value()
            
            self.brightness_label.setText(str(self.current_layer.brightness))
            self.contrast_label.setText(str(self.current_layer.contrast))
            self.saturation_label.setText(str(self.current_layer.saturation))
            self.blur_label.setText(str(self.current_layer.blur))
            
            self.property_changed.emit()
    
    def on_text_changed_debounced(self):
        """Xử lý thay đổi text với debounce"""
        # Restart timer mỗi khi có thay đổi
        self.text_change_timer.stop()
        self.text_change_timer.start()
    
    def apply_text_change(self):
        """Apply text change sau debounce"""
        if self.current_layer and self.current_layer.layer_type == "text":
            # Chỉ update nếu text thực sự thay đổi
            new_text = self.text_edit.toPlainText()
            if new_text != self.current_layer.text:
                # Block update_properties để giữ focus
                self._updating_text = True
                self.current_layer.set_text(new_text)
                self.property_changed.emit()
                self._updating_text = False
    
    def on_font_changed(self, font):
        """Xử lý thay đổi font"""
        if self.current_layer and self.current_layer.layer_type == "text":
            self.current_layer.set_font_family(font)
            self.property_changed.emit()
    
    def on_font_size_changed(self, size):
        """Xử lý thay đổi font size"""
        if self.current_layer and self.current_layer.layer_type == "text":
            self.current_layer.set_font_size(int(size))
            self.property_changed.emit()
    
    def on_font_style_changed(self):
        """Xử lý thay đổi font style"""
        if self.current_layer and self.current_layer.layer_type == "text":
            self.current_layer.font_bold = self.bold_check.isChecked()
            self.current_layer.font_italic = self.italic_check.isChecked()
            self.current_layer.font_underline = self.underline_check.isChecked()
            self.current_layer.update_size()
            self.property_changed.emit()
    
    def on_text_color_clicked(self):
        """Xử lý chọn màu text"""
        if self.current_layer and self.current_layer.layer_type == "text":
            color = QColorDialog.getColor(self.current_layer.text_color, self)
            if color.isValid():
                self.current_layer.set_text_color(color)
                self.text_color_btn.setStyleSheet(f"background-color: {color.name()};")
                self.property_changed.emit()
    
    def on_outline_changed(self, state):
        """Xử lý thay đổi outline"""
        if self.current_layer and self.current_layer.layer_type == "text":
            self.current_layer.outline_enabled = (state == Qt.Checked)
            self.property_changed.emit()
