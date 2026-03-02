"""
Cửa sổ chính của ứng dụng
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QMessageBox, QDialog, QLabel,
                             QComboBox, QSpinBox, QDialogButtonBox, QPushButton,
                             QDockWidget, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from ..core.project import Project
from ..core.image_layer import ImageLayer
from ..core.text_layer import TextLayer
from ..utils.constants import (ASPECT_RATIOS, DEFAULT_RESOLUTIONS, 
                               SUPPORTED_IMAGE_FORMATS, DEFAULT_TEXT)
from ..utils.helpers import generate_unique_name

from .canvas import Canvas
from .layer_panel import LayerPanel
from .properties_panel import PropertiesPanel
from .toolbar import Toolbar


class NewProjectDialog(QDialog):
    """Dialog tạo project mới"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        layout = QVBoxLayout()
        
        # Project name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLabel()
        self.name_input.setText("Untitled Project")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Aspect ratio
        ratio_layout = QHBoxLayout()
        ratio_layout.addWidget(QLabel("Aspect Ratio:"))
        self.ratio_combo = QComboBox()
        self.ratio_combo.addItems(list(ASPECT_RATIOS.keys()))
        self.ratio_combo.setCurrentText("Instagram Post (1:1)")
        self.ratio_combo.currentTextChanged.connect(self.on_ratio_changed)
        ratio_layout.addWidget(self.ratio_combo)
        layout.addLayout(ratio_layout)
        
        # Resolution
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(1080)
        res_layout.addWidget(self.width_spin)
        
        res_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(1080)
        res_layout.addWidget(self.height_spin)
        layout.addLayout(res_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def on_ratio_changed(self, ratio_name):
        """Xử lý thay đổi aspect ratio"""
        if ratio_name in DEFAULT_RESOLUTIONS:
            width, height = DEFAULT_RESOLUTIONS[ratio_name]
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)
    
    def get_values(self):
        """Lấy các giá trị"""
        return {
            'name': self.name_input.text(),
            'width': self.width_spin.value(),
            'height': self.height_spin.value()
        }


class ExportDialog(QDialog):
    """Dialog xuất ảnh"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Image")
        self.file_path = None
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        layout = QVBoxLayout()
        
        # File path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Save to:"))
        self.path_label = QLabel("No file selected")
        path_layout.addWidget(self.path_label, 1)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)
        
        # Format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG", "BMP", "WEBP"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # Quality (for JPEG)
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality:"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(95)
        quality_layout.addWidget(self.quality_spin)
        layout.addLayout(quality_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def browse_file(self):
        """Chọn file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Image",
            "",
            SUPPORTED_IMAGE_FORMATS["Export"]
        )
        
        if file_path:
            self.file_path = file_path
            self.path_label.setText(file_path)
    
    def get_values(self):
        """Lấy các giá trị"""
        return {
            'file_path': self.file_path,
            'format': self.format_combo.currentText(),
            'quality': self.quality_spin.value()
        }


class MainWindow(QMainWindow):
    """Cửa sổ chính"""
    
    def __init__(self):
        super().__init__()
        self.project = None
        self.setup_ui()
        self.create_new_project()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.setWindowTitle("Photo Editor - Professional Image Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Toolbar
        self.toolbar = Toolbar()
        self.addToolBar(self.toolbar)
        
        # Connect toolbar signals
        self.toolbar.new_project.connect(self.on_new_project)
        self.toolbar.open_image.connect(self.on_open_image)
        self.toolbar.save_project.connect(self.on_save_project)
        self.toolbar.export_image.connect(self.on_export_image)
        self.toolbar.add_text.connect(self.on_add_text)
        self.toolbar.undo.connect(self.on_undo)
        self.toolbar.redo.connect(self.on_redo)
        self.toolbar.zoom_changed.connect(self.on_zoom_changed)
        
        # Central widget (canvas)
        self.canvas = None
        
        # Setup menu
        self.setup_menu()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def setup_menu(self):
        """Thiết lập menu"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Project")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.on_new_project)
        
        open_action = file_menu.addAction("Open Image")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open_image)
        
        save_action = file_menu.addAction("Save Project")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.on_save_project)
        
        file_menu.addSeparator()
        
        export_action = file_menu.addAction("Export Image")
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.on_export_image)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = edit_menu.addAction("Undo")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.on_undo)
        
        redo_action = edit_menu.addAction("Redo")
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.on_redo)
        
        # Layer menu
        layer_menu = menubar.addMenu("Layer")
        
        add_text_action = layer_menu.addAction("Add Text Layer")
        add_text_action.setShortcut("Ctrl+T")
        add_text_action.triggered.connect(self.on_add_text)
        
        duplicate_action = layer_menu.addAction("Duplicate Layer")
        duplicate_action.setShortcut("Ctrl+D")
        duplicate_action.triggered.connect(self.on_duplicate_layer)
        
        delete_action = layer_menu.addAction("Delete Layer")
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.on_delete_layer)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        zoom_in_action = view_menu.addAction("Zoom In")
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.on_zoom_in)
        
        zoom_out_action = view_menu.addAction("Zoom Out")
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.on_zoom_out)
        
        reset_zoom_action = view_menu.addAction("Reset Zoom")
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.on_reset_zoom)
        
        fit_action = view_menu.addAction("Fit to Window")
        fit_action.setShortcut("Ctrl+F")
        fit_action.triggered.connect(self.on_fit_to_window)
        
        view_menu.addSeparator()
        
        grid_action = view_menu.addAction("Show Grid")
        grid_action.setCheckable(True)
        grid_action.triggered.connect(self.on_toggle_grid)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.on_about)
    
    def create_new_project(self, width=1080, height=1080, name="Untitled"):
        """Tạo project mới"""
        self.project = Project(width, height, name)
        
        # Create canvas
        if self.canvas:
            self.canvas.deleteLater()
        
        self.canvas = Canvas(self.project)
        self.setCentralWidget(self.canvas)
        
        # Create side panels
        self.setup_panels()
        
        # Connect signals
        self.canvas.layer_selected.connect(self.on_layer_selected)
        self.canvas.layer_moved.connect(self.on_canvas_changed)
        self.canvas.layer_transformed.connect(self.on_canvas_changed)
        
        self.update_ui()
        self.statusBar().showMessage(f"New project created: {width}x{height}")
    
    def setup_panels(self):
        """Thiết lập các panel bên"""
        # Layer panel (right)
        self.layer_panel = LayerPanel(self.project)
        layer_dock = QDockWidget("Layers", self)
        layer_dock.setWidget(self.layer_panel)
        layer_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, layer_dock)
        
        self.layer_panel.layer_selected.connect(self.on_layer_panel_selected)
        self.layer_panel.layers_changed.connect(self.on_layers_changed)
        
        # Properties panel (right)
        self.properties_panel = PropertiesPanel(self.project)
        props_dock = QDockWidget("Properties", self)
        props_dock.setWidget(self.properties_panel)
        props_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, props_dock)
        
        self.properties_panel.property_changed.connect(self.on_property_changed)
    
    def on_new_project(self):
        """Tạo project mới"""
        dialog = NewProjectDialog(self)
        if dialog.exec_():
            values = dialog.get_values()
            self.create_new_project(
                values['width'],
                values['height'],
                values['name']
            )
    
    def on_open_image(self):
        """Mở ảnh"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open Images",
            "",
            SUPPORTED_IMAGE_FORMATS["Import"]
        )
        
        if file_paths:
            for file_path in file_paths:
                try:
                    # Generate unique name - sử dụng os.path để cross-platform
                    import os
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    existing_names = [layer.name for layer in self.project.layers]
                    layer_name = generate_unique_name(base_name, existing_names)
                    
                    # Create image layer
                    layer = ImageLayer(layer_name, file_path)
                    
                    # Kiểm tra xem ảnh có load thành công không
                    if layer.pixmap.isNull():
                        QMessageBox.warning(
                            self, 
                            "Warning", 
                            f"Cannot load image: {os.path.basename(file_path)}\nFile may be corrupted or unsupported format."
                        )
                        continue
                    
                    # Center on canvas
                    layer.set_position(
                        (self.project.width - layer.width) / 2,
                        (self.project.height - layer.height) / 2
                    )
                    
                    self.project.add_layer(layer)
                    
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to open image {os.path.basename(file_path)}:\n{str(e)}"
                    )
            
            self.update_ui()
            self.statusBar().showMessage(f"Opened {len(file_paths)} image(s)")
    
    def on_save_project(self):
        """Lưu project"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "Photo Editor Project (*.pep);;All Files (*.*)"
        )
        
        if file_path:
            try:
                self.project.save_to_file(file_path)
                self.statusBar().showMessage(f"Project saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
    
    def on_export_image(self):
        """Xuất ảnh"""
        dialog = ExportDialog(self)
        if dialog.exec_():
            values = dialog.get_values()
            
            if not values['file_path']:
                QMessageBox.warning(self, "Warning", "Please select a file path")
                return
            
            try:
                pixmap = self.canvas.render_to_pixmap()
                
                # Save based on format
                if values['format'] == 'JPEG':
                    pixmap.save(values['file_path'], 'JPEG', values['quality'])
                else:
                    pixmap.save(values['file_path'], values['format'])
                
                self.statusBar().showMessage(f"Image exported: {values['file_path']}")
                QMessageBox.information(self, "Success", "Image exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export image: {str(e)}")
    
    def on_add_text(self):
        """Thêm text layer"""
        existing_names = [layer.name for layer in self.project.layers]
        layer_name = generate_unique_name("Text", existing_names)
        
        layer = TextLayer(layer_name, DEFAULT_TEXT)
        layer.set_position(
            (self.project.width - layer.width) / 2,
            (self.project.height - layer.height) / 2
        )
        
        self.project.add_layer(layer)
        self.update_ui()
        self.statusBar().showMessage("Text layer added")
    
    def on_duplicate_layer(self):
        """Nhân đôi layer"""
        layer = self.project.get_selected_layer()
        if layer:
            self.project.duplicate_layer(layer.id)
            self.update_ui()
            self.statusBar().showMessage("Layer duplicated")
    
    def on_delete_layer(self):
        """Xóa layer"""
        layer = self.project.get_selected_layer()
        if layer:
            self.project.remove_layer(layer.id)
            self.update_ui()
            self.statusBar().showMessage("Layer deleted")
    
    def on_undo(self):
        """Hoàn tác"""
        if self.project.undo():
            self.update_ui()
            self.statusBar().showMessage("Undo")
    
    def on_redo(self):
        """Làm lại"""
        if self.project.redo():
            self.update_ui()
            self.statusBar().showMessage("Redo")
    
    def on_zoom_in(self):
        """Zoom in"""
        self.canvas.zoom_in()
        self.update_zoom_combo()
    
    def on_zoom_out(self):
        """Zoom out"""
        self.canvas.zoom_out()
        self.update_zoom_combo()
    
    def on_reset_zoom(self):
        """Reset zoom"""
        self.canvas.reset_zoom()
        self.toolbar.zoom_combo.setCurrentText("100%")
    
    def on_fit_to_window(self):
        """Fit to window"""
        self.canvas.fit_to_window()
        self.toolbar.zoom_combo.setCurrentText("Fit")
    
    def on_toggle_grid(self, checked):
        """Toggle grid"""
        self.canvas.show_grid = checked
        self.canvas.update()
    
    def on_zoom_changed(self, zoom_text):
        """Xử lý thay đổi zoom"""
        if zoom_text == "Fit":
            self.canvas.fit_to_window()
        else:
            try:
                zoom_value = int(zoom_text.replace("%", "")) / 100.0
                self.canvas.set_zoom(zoom_value)
            except:
                pass
    
    def update_zoom_combo(self):
        """Cập nhật zoom combo"""
        zoom_percent = int(self.canvas.zoom * 100)
        self.toolbar.zoom_combo.setCurrentText(f"{zoom_percent}%")
    
    def on_layer_selected(self, layer_id):
        """Xử lý chọn layer từ canvas"""
        self.layer_panel.update_layer_list()
        layer = self.project.get_layer_by_id(layer_id) if layer_id else None
        self.properties_panel.update_properties(layer)
    
    def on_layer_panel_selected(self, layer_id):
        """Xử lý chọn layer từ panel"""
        self.canvas.update()
        layer = self.project.get_layer_by_id(layer_id) if layer_id else None
        self.properties_panel.update_properties(layer)
    
    def on_layers_changed(self):
        """Xử lý thay đổi layers"""
        self.canvas.update()
    
    def on_canvas_changed(self):
        """Xử lý thay đổi canvas"""
        self.canvas.update()
        # Không update properties nếu đang edit text (để không mất focus)
        # Properties sẽ tự update qua on_property_changed()
    
    def on_property_changed(self):
        """Xử lý thay đổi property"""
        self.canvas.update()
        self.layer_panel.update_layer_list()
    
    def update_ui(self):
        """Cập nhật UI"""
        self.canvas.update()
        self.layer_panel.update_layer_list()
        self.properties_panel.update_properties(self.project.get_selected_layer())
        self.toolbar.update_undo_redo(self.project.can_undo(), self.project.can_redo())
    
    def on_about(self):
        """Hiển thị about dialog"""
        QMessageBox.about(
            self,
            "About Photo Editor",
            "<h2>Photo Editor</h2>"
            "<p>Professional image editing software</p>"
            "<p>Version 1.0</p>"
            "<p>Built with Python and PyQt5</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Multiple layer support</li>"
            "<li>Text editing with custom fonts</li>"
            "<li>Image filters and effects</li>"
            "<li>Export to multiple formats</li>"
            "<li>Undo/Redo support</li>"
            "</ul>"
        )
