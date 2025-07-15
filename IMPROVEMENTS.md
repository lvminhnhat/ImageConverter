# Image Format Converter - Improvements & Features

## 🎯 Tính năng chính

### 1. Chuyển đổi định dạng ảnh
- **Hỗ trợ định dạng**: PNG, JPEG, WEBP, AVIF, BMP, TIFF, GIF
- **Chất lượng cao**: Tùy chỉnh quality từ 10-100
- **Nén thông minh**: Tự động nén theo kích thước mục tiêu
- **Resize linh hoạt**: Thay đổi kích thước với giữ tỷ lệ khung hình

### 2. Giao diện người dùng hiện đại
- **GUI PyQt6**: Giao diện đẹp, dễ sử dụng
- **CLI mạnh mẽ**: Dòng lệnh với progress bar và màu sắc
- **Responsive design**: Tương thích mọi kích thước màn hình

### 3. Xử lý file thông minh
- **Tự động tạo thư mục**: Tạo thư mục `convert` tại vị trí file gốc
- **Tên file gốc**: Giữ nguyên tên file (không thêm `_converted`)
- **Batch processing**: Xử lý nhiều file cùng lúc
- **Folder processing**: Xử lý toàn bộ thư mục

## 🔧 Cải tiến gần đây

### 1. Sửa lỗi tính toán compression ratio
- **Vấn đề**: Hiển thị sai thống kê khi file tăng kích thước
- **Giải pháp**: 
  - Tính toán chính xác compression ratio
  - Phân loại files: compressed, expanded, unchanged
  - Hiển thị thống kê chi tiết và tổng kết

### 2. Cải thiện logic lưu file
- **Trước**: Lưu cùng thư mục với tên `_converted`
- **Sau**: Tạo thư mục `convert` và giữ tên gốc
- **Lợi ích**: Tổ chức file tốt hơn, dễ quản lý

### 3. Nâng cấp thống kê
- **Chi tiết hơn**: Phân loại theo loại thay đổi
- **Trực quan**: Sử dụng emoji và màu sắc
- **Tổng kết**: Net space saved/increased

## 📊 Ví dụ thống kê mới

```
================================================================================
                           CONVERSION RESULTS
================================================================================
Total files: 2
Successful: 2
Failed: 0

📊 SIZE STATISTICS:
Original size: 37.24 KB
New size: 14.94 KB
📉 Compressed files: 2
💾 Space saved: 22.30 KB
📊 Average compression: 41.56%

📋 SUMMARY:
✅ Net space saved: 22.30 KB
```

## 🚀 Cách sử dụng

### GUI Mode
```bash
python main.py
```

### CLI Mode - Single File
```bash
python main.py cli -i image.png -f webp -q 85
```

### CLI Mode - Multiple Files
```bash
python main.py cli -i "img1.png,img2.jpg" -f webp -q 90
```

### CLI Mode - Folder
```bash
python main.py cli -i /path/to/folder --folder -f jpg -r
```

## 🎨 Giao diện

### Sidebar (350-400px width)
- **File Settings**: Chọn định dạng, quality, compression
- **Size Settings**: Resize options với maintain aspect ratio
- **Output Settings**: Thư mục output tùy chọn

### Central Widget
- **File List**: Drag & drop hoặc browse files
- **Preview**: Xem trước ảnh được chọn
- **Progress**: Progress bar và thống kê real-time

### Modern Styling
- **CSS Styling**: Giao diện hiện đại với shadows và gradients
- **Responsive**: Tự động điều chỉnh theo kích thước
- **Color Scheme**: Professional color palette

## 🔧 Technical Details

### Architecture
- **Modular Design**: Tách biệt GUI, CLI, và core logic
- **Error Handling**: Xử lý lỗi toàn diện
- **Memory Efficient**: Xử lý file lớn mà không tốn RAM

### Performance
- **Progress Tracking**: Real-time progress với tqdm
- **Batch Processing**: Xử lý song song khi có thể
- **Optimized Compression**: Tự động điều chỉnh quality

### Compatibility
- **Cross-platform**: Windows, macOS, Linux
- **Python 3.7+**: Hỗ trợ Python phiên bản mới
- **Dependencies**: Minimal dependencies

## 📝 Changelog

### v1.1.0 (Latest)
- ✅ Sửa lỗi tính toán compression ratio
- ✅ Cải thiện logic lưu file (thư mục convert)
- ✅ Nâng cấp thống kê chi tiết
- ✅ Fix format mapping (jpg → jpeg)
- ✅ Cải thiện error handling

### v1.0.0
- ✅ GUI PyQt6 hoàn chỉnh
- ✅ CLI với progress bar
- ✅ Batch và folder processing
- ✅ Compression và resize options
- ✅ Modern styling và responsive design

## 🎯 Roadmap

### Planned Features
- [ ] Drag & drop support cho GUI
- [ ] Preview real-time khi thay đổi settings
- [ ] Export/Import settings
- [ ] Batch rename options
- [ ] Metadata preservation
- [ ] Advanced compression algorithms

### Performance Improvements
- [ ] Multi-threading cho batch processing
- [ ] GPU acceleration cho resize
- [ ] Memory optimization cho large files
- [ ] Caching system cho repeated operations 