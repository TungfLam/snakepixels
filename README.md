# 🎨 Photo Editor - Phần mềm chỉnh sửa ảnh chuyên nghiệp

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Phần mềm chỉnh sửa ảnh **miễn phí, mã nguồn mở**, với giao diện đẹp và dễ sử dụng tương tự Canva. Chạy hoàn toàn **offline**, không giới hạn export!

<img width="1920" height="1048" alt="image" src="https://github.com/user-attachments/assets/838ccde0-92c7-410e-9d80-5593c5780329" />

## Tính năng chính

### 🎨 Quản lý dự án
- Tạo dự án mới với nhiều tỷ lệ khung hình: 16:9, 4:3, 1:1, 9:16, v.v.
- Tùy chỉnh độ phân giải tự do
- Lưu và mở dự án

### 🖼️ Xử lý ảnh
- Import ảnh nhiều định dạng: JPG, PNG, BMP, GIF, WEBP
- Kéo thả ảnh vào canvas
- Phóng to, thu nhỏ, xoay ảnh
- Di chuyển ảnh tự do
- Crop và resize ảnh

### ✏️ Chỉnh sửa văn bản
- Thêm text lên ảnh
- Chọn nhiều font chữ khác nhau
- Tùy chỉnh kích thước chữ (10-200px)
- Chọn màu chữ tự do
- Kéo thả khung text
- Căn chỉnh text (trái, giữa, phải)
- Text có viền ngoài (outline)

### 📑 Quản lý Layer
- Tab layer trực quan
- Kéo thả để sắp xếp thứ tự layer
- Hiện/ẩn layer
- Xóa layer
- Đổi tên layer
- Layer trên cùng sẽ đè lên layer dưới

### 🎨 Bộ lọc và hiệu ứng
- Điều chỉnh độ sáng
- Điều chỉnh độ tương phản
- Điều chỉnh độ bão hòa
- Làm mờ (Blur)
- Làm sắc nét (Sharpen)
- Chuyển đen trắng (Grayscale)
- Sepia tone
- Invert colors
- Thêm viền cho ảnh

### 💾 Xuất file
- Xuất nhiều định dạng: PNG, JPG, BMP, WEBP
- Chọn chất lượng khi xuất
- Xem trước trước khi xuất

### 🎯 Tính năng khác
- Undo/Redo không giới hạn
- Zoom in/out canvas
- Grid và hướng dẫn căn chỉnh
- Shortcuts keyboard tiện lợi
- Giao diện theme hiện đại

## Cài đặt

### 1. Tạo môi trường ảo (Python 3.13.7)
```bash
python -m venv venv
```

### 2. Kích hoạt môi trường ảo

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

## Sử dụng

```bash
python main.py
```

## Phím tắt

- `Ctrl+N`: Tạo dự án mới
- `Ctrl+O`: Mở ảnh
- `Ctrl+S`: Lưu dự án
- `Ctrl+E`: Xuất ảnh
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Ctrl+T`: Thêm text
- `Delete`: Xóa layer đang chọn
- `Ctrl++`: Zoom in
- `Ctrl+-`: Zoom out
- `Ctrl+0`: Reset zoom

## Cấu trúc dự án

```
photo-editor/
├── main.py                 # File chính
├── requirements.txt        # Thư viện cần thiết
├── README.md              # Tài liệu
├── src/
│   ├── ui/
│   │   ├── main_window.py     # Cửa sổ chính
│   │   ├── canvas.py          # Canvas vẽ
│   │   ├── layer_panel.py     # Panel quản lý layer
│   │   ├── properties_panel.py # Panel thuộc tính
│   │   └── toolbar.py         # Thanh công cụ
│   ├── core/
│   │   ├── project.py         # Quản lý dự án
│   │   ├── layer.py           # Xử lý layer
│   │   ├── image_layer.py     # Layer ảnh
│   │   ├── text_layer.py      # Layer text
│   │   └── filters.py         # Bộ lọc và hiệu ứng
│   └── utils/
│       ├── constants.py       # Hằng số
│       └── helpers.py         # Hàm hỗ trợ
└── venv/                      # Môi trường ảo
```

## Yêu cầu hệ thống

- Python 3.13.7
- RAM: >= 4GB
- Hệ điều hành: Windows, Linux, MacOS
