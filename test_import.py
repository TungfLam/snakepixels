"""
Script test import các module chính
Chạy script này để kiểm tra tất cả dependencies đã được cài đặt đúng
"""
import sys

def test_imports():
    """Test tất cả imports"""
    print("🔍 Testing imports...")
    print("-" * 50)
    
    try:
        print("✓ Testing PyQt5...")
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtCore import Qt, QPointF
        from PyQt5.QtGui import QPainter, QColor, QPixmap
        print("  ✅ PyQt5 OK")
    except ImportError as e:
        print(f"  ❌ PyQt5 Error: {e}")
        return False
    
    try:
        print("✓ Testing Pillow (PIL)...")
        from PIL import Image, ImageEnhance, ImageFilter, ImageQt
        print("  ✅ Pillow OK")
    except ImportError as e:
        print(f"  ❌ Pillow Error: {e}")
        return False
    
    try:
        print("✓ Testing numpy...")
        import numpy as np
        print("  ✅ numpy OK")
    except ImportError as e:
        print(f"  ❌ numpy Error: {e}")
        return False
    
    print("-" * 50)
    print("✓ Testing project modules...")
    
    try:
        from src.core.project import Project
        from src.core.layer import Layer
        from src.core.image_layer import ImageLayer
        from src.core.text_layer import TextLayer
        from src.core.filters import apply_brightness, apply_contrast
        print("  ✅ Core modules OK")
    except ImportError as e:
        print(f"  ❌ Core modules Error: {e}")
        return False
    
    try:
        from src.ui.main_window import MainWindow
        from src.ui.canvas import Canvas
        from src.ui.layer_panel import LayerPanel
        from src.ui.properties_panel import PropertiesPanel
        from src.ui.toolbar import Toolbar
        print("  ✅ UI modules OK")
    except ImportError as e:
        print(f"  ❌ UI modules Error: {e}")
        return False
    
    try:
        from src.utils.constants import ASPECT_RATIOS, DEFAULT_FONTS
        from src.utils.helpers import hex_to_qcolor, generate_unique_name
        print("  ✅ Utils modules OK")
    except ImportError as e:
        print(f"  ❌ Utils modules Error: {e}")
        return False
    
    print("-" * 50)
    print("🎉 All imports successful!")
    print()
    print("📊 Module summary:")
    print("  - PyQt5: GUI framework")
    print("  - Pillow: Image processing")
    print("  - numpy: Array operations")
    print("  - Core: Project, Layer, Filters")
    print("  - UI: MainWindow, Canvas, Panels")
    print("  - Utils: Constants, Helpers")
    print()
    print("✅ Ready to run! Execute: python main.py")
    return True

if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  Photo Editor - Import Test")
    print("=" * 50)
    print()
    
    success = test_imports()
    
    print()
    print("=" * 50)
    
    if success:
        print("✅ TEST PASSED")
        sys.exit(0)
    else:
        print("❌ TEST FAILED")
        print()
        print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)
