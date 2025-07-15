# Hướng Dẫn Build Executable

## Cách 1: Build Đơn Giản (Khuyến nghị)

```bash
python build_simple.py
```

## Cách 2: Build với Script Chi Tiết

```bash
python build_exe.py
```

## Cách 3: Build Thủ Công

### Bước 1: Cài đặt PyInstaller
```bash
pip install pyinstaller
```

### Bước 2: Build với PyInstaller
```bash
pyinstaller --onefile --windowed --name=ImageConverter --hidden-import=PIL._tkinter_finder --hidden-import=PyQt6.sip --hidden-import=pillow_avif --add-data="app/gui/styles;app/gui/styles" main.py
```

### Bước 3: Sử dụng file spec (nếu có)
```bash
pyinstaller ImageConverter.spec
```

## Kết Quả

Sau khi build thành công, bạn sẽ có:
- `dist/ImageConverter.exe` - File executable chính
- File này có thể chạy trên mọi máy Windows mà không cần cài Python

## Lưu Ý

1. **Kích thước file**: File exe sẽ khá lớn (50-100MB) vì nó chứa toàn bộ Python runtime và các thư viện
2. **Thời gian build**: Có thể mất 5-10 phút tùy thuộc vào máy tính
3. **Antivirus**: Một số antivirus có thể cảnh báo về file exe được tạo bởi PyInstaller, đây là bình thường
4. **Tương thích**: File exe chỉ chạy trên Windows, không chạy trên Linux/Mac

## Xử Lý Lỗi

### Lỗi Import
Nếu gặp lỗi import, thêm `--hidden-import` cho module bị thiếu:
```bash
pyinstaller --onefile --hidden-import=module_name main.py
```

### Lỗi File không tìm thấy
Nếu chương trình không tìm thấy file CSS hoặc resource khác, thêm `--add-data`:
```bash
pyinstaller --onefile --add-data="path/to/file;destination" main.py
```

### Lỗi UPX
Nếu gặp lỗi UPX, thêm `--upx-dir` hoặc tắt UPX:
```bash
pyinstaller --onefile --upx-dir=path/to/upx main.py
# hoặc
pyinstaller --onefile --upx-exclude=* main.py
```

## Tối Ưu Hóa

### Giảm kích thước file
```bash
pyinstaller --onefile --strip --upx-dir=path/to/upx main.py
```

### Build nhanh hơn (không nén)
```bash
pyinstaller --onefile --upx-exclude=* main.py
```

### Debug mode
```bash
pyinstaller --onefile --debug=all main.py
``` 