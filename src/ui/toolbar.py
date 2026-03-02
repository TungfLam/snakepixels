"""
Thanh công cụ
"""
from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QComboBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence


class Toolbar(QToolBar):
    """Thanh công cụ chính"""
    
    new_project = pyqtSignal()
    open_image = pyqtSignal()
    save_project = pyqtSignal()
    export_image = pyqtSignal()
    add_text = pyqtSignal()
    undo = pyqtSignal()
    redo = pyqtSignal()
    zoom_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setMovable(False)
        self.setup_actions()
    
    def setup_actions(self):
        """Thiết lập các action"""
        # New project
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setToolTip("Create new project (Ctrl+N)")
        new_action.triggered.connect(self.new_project.emit)
        self.addAction(new_action)
        
        # Open image
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setToolTip("Open image (Ctrl+O)")
        open_action.triggered.connect(self.open_image.emit)
        self.addAction(open_action)
        
        # Save
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setToolTip("Save project (Ctrl+S)")
        save_action.triggered.connect(self.save_project.emit)
        self.addAction(save_action)
        
        # Export
        export_action = QAction("Export", self)
        export_action.setShortcut("Ctrl+E")
        export_action.setToolTip("Export image (Ctrl+E)")
        export_action.triggered.connect(self.export_image.emit)
        self.addAction(export_action)
        
        self.addSeparator()
        
        # Undo
        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.undo_action.setToolTip("Undo (Ctrl+Z)")
        self.undo_action.triggered.connect(self.undo.emit)
        self.undo_action.setEnabled(False)
        self.addAction(self.undo_action)
        
        # Redo
        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut(QKeySequence.Redo)
        self.redo_action.setToolTip("Redo (Ctrl+Y)")
        self.redo_action.triggered.connect(self.redo.emit)
        self.redo_action.setEnabled(False)
        self.addAction(self.redo_action)
        
        self.addSeparator()
        
        # Add text
        text_action = QAction("Add Text", self)
        text_action.setShortcut("Ctrl+T")
        text_action.setToolTip("Add text layer (Ctrl+T)")
        text_action.triggered.connect(self.add_text.emit)
        self.addAction(text_action)
        
        self.addSeparator()
        
        # Zoom
        self.addWidget(QLabel("  Zoom: "))
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems([
            "25%", "50%", "75%", "100%", "125%", "150%", "200%", "300%", "Fit"
        ])
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.currentTextChanged.connect(self.zoom_changed.emit)
        self.addWidget(self.zoom_combo)
    
    def update_undo_redo(self, can_undo, can_redo):
        """Cập nhật trạng thái undo/redo"""
        self.undo_action.setEnabled(can_undo)
        self.redo_action.setEnabled(can_redo)
