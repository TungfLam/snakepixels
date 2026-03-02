"""
Photo Editor - Professional Image Editing Software
Main entry point
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from src.ui.main_window import MainWindow


def set_dark_theme(app):
    """Thiết lập dark theme cho ứng dụng"""
    dark_palette = QPalette()
    
    # Colors
    dark_color = QColor(45, 45, 45)
    disabled_color = QColor(127, 127, 127)
    
    dark_palette.setColor(QPalette.Window, dark_color)
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.AlternateBase, dark_color)
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, disabled_color)
    dark_palette.setColor(QPalette.Button, dark_color)
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, disabled_color)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, disabled_color)
    
    app.setPalette(dark_palette)
    
    # Stylesheet
    app.setStyleSheet("""
        QToolTip {
            color: #ffffff;
            background-color: #2a82da;
            border: 1px solid white;
        }
        QGroupBox {
            border: 1px solid #555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: white;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            background-color: #505050;
            border: 1px solid #666;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #606060;
        }
        QPushButton:pressed {
            background-color: #404040;
        }
        QPushButton:disabled {
            background-color: #3a3a3a;
            color: #666;
        }
        QComboBox {
            background-color: #505050;
            border: 1px solid #666;
            padding: 3px;
            border-radius: 3px;
        }
        QComboBox:hover {
            border: 1px solid #888;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #505050;
            selection-background-color: #007acc;
        }
        QSpinBox, QDoubleSpinBox {
            background-color: #505050;
            border: 1px solid #666;
            padding: 3px;
            border-radius: 3px;
        }
        QSlider::groove:horizontal {
            border: 1px solid #666;
            height: 6px;
            background: #404040;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #007acc;
            border: 1px solid #007acc;
            width: 14px;
            margin: -5px 0;
            border-radius: 7px;
        }
        QSlider::handle:horizontal:hover {
            background: #0098ff;
        }
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QCheckBox::indicator:unchecked {
            border: 1px solid #666;
            background: #404040;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            border: 1px solid #007acc;
            background: #007acc;
            border-radius: 3px;
        }
        QTextEdit {
            background-color: #2b2b2b;
            border: 1px solid #666;
            border-radius: 3px;
            padding: 5px;
        }
        QLineEdit {
            background-color: #2b2b2b;
            border: 1px solid #666;
            border-radius: 3px;
            padding: 5px;
        }
        QScrollBar:vertical {
            border: none;
            background: #2b2b2b;
            width: 12px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #505050;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #606060;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            border: none;
            background: #2b2b2b;
            height: 12px;
            margin: 0;
        }
        QScrollBar::handle:horizontal {
            background: #505050;
            border-radius: 6px;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #606060;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """)


def main():
    """Main function"""
    app = QApplication(sys.argv)
    app.setApplicationName("Photo Editor")
    app.setOrganizationName("Photo Editor")
    
    # Set dark theme
    set_dark_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
