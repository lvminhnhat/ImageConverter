# Image Format Converter

A modern, feature-rich image format converter built with Python and Qt6. Convert images between popular formats like PNG, JPEG, WebP, AVIF, and more with advanced compression and resizing options.

## Features

### 🎯 **Core Functionality**
- Convert between formats: PNG, JPEG, WebP, AVIF, BMP, TIFF, GIF
- Batch processing for multiple files and folders
- Drag-and-drop support
- Real-time preview
- Progress tracking with detailed statistics

### 🛠️ **Advanced Options**
- Quality control (10-100%)
- File size limits (KB)
- Compression percentage
- Image resizing with aspect ratio preservation
- Recursive folder processing

### 🎨 **Modern Interface**
- Clean, responsive GUI built with Qt6
- Dark/Light theme support
- Intuitive sidebar controls
- Quick preset configurations
- Comprehensive CLI interface

### 📊 **Smart Features**
- Automatic format optimization
- Batch conversion statistics
- Error handling and reporting
- Background processing (non-blocking UI)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Dependencies
- **PyQt6** - Modern GUI framework
- **Pillow** - Image processing library
- **pillow-avif-plugin** - AVIF format support
- **tqdm** - Progress bars
- **colorama** - Colored CLI output

## Usage

### GUI Mode (Default)
```bash
python main.py
```

### CLI Mode
```bash
python main.py cli [options]
```

## CLI Examples

### Basic Conversion
```bash
# Convert single file
python main.py cli -i photo.jpg -f webp -q 85

# Convert with size limit
python main.py cli -i image.png -f jpeg -s 500 -q 90
```

### Batch Processing
```bash
# Convert folder (non-recursive)
python main.py cli -i /path/to/images --folder -f avif -q 80

# Convert folder recursively
python main.py cli -i /path/to/images --folder -r -f webp -o /output

# Convert multiple specific files
python main.py cli -i "img1.jpg,img2.png,img3.gif" -f avif -q 85
```

### Advanced Options
```bash
# Resize and compress
python main.py cli -i photo.jpg -f webp --resize 800x600 -c 70

# High quality with size limit
python main.py cli -i image.png -f jpeg -q 95 -s 1000 --maintain-aspect
```

## CLI Options

### Input/Output
- `-i, --input` - Input file, folder, or comma-separated file list
- `-f, --format` - Output format (jpeg, png, webp, avif, bmp, tiff)
- `-o, --output` - Output directory
- `--folder` - Process entire folder
- `-r, --recursive` - Process subfolders recursively

### Quality Control
- `-q, --quality` - Image quality 10-100 (default: 90)
- `-s, --max-size` - Maximum file size in KB
- `-c, --compression` - Compress to percentage of original (10-100)

### Resize Options
- `--resize` - Resize format: WIDTHxHEIGHT (e.g., 800x600)
- `--maintain-aspect` - Maintain aspect ratio (default: True)

### Utility
- `--quiet` - Suppress progress bars and info messages
- `--version` - Show version information

## GUI Interface

### Main Features
1. **File Management**
   - Drag & drop files or folders
   - Browse files/folders
   - Preview selected images
   - Clear file list

2. **Format Settings**
   - Output format selection
   - Quality slider with real-time preview
   - Size compression options
   - Resize configurations

3. **Quick Presets**
   - Web Optimized (WebP, 500KB limit)
   - High Quality (PNG, no compression)
   - Small Size (JPEG, 50% compression)
   - Mobile Ready (WebP, 200KB limit)

4. **Results & Statistics**
   - Conversion progress
   - Detailed statistics
   - Error reporting
   - File size comparisons

## Supported Formats

### Input Formats
- PNG
- JPEG/JPG
- WebP
- AVIF
- BMP
- TIFF
- GIF

### Output Formats
- **JPEG** - Wide compatibility, good compression
- **PNG** - Lossless compression, transparency support
- **WebP** - Modern format, excellent compression
- **AVIF** - Next-gen format, best compression
- **BMP** - Uncompressed, large file sizes
- **TIFF** - High quality, professional use

## Performance Tips

### For Best Results
1. **WebP** for web images (best compression/quality ratio)
2. **AVIF** for cutting-edge applications (best compression)
3. **JPEG** for maximum compatibility
4. **PNG** for images requiring transparency

### Optimization Settings
- **Quality 85-95**: High quality, reasonable size
- **Quality 70-85**: Good quality, smaller size
- **Quality 50-70**: Acceptable quality, very small size

## Development

### Project Structure
```
convert/
├── app/
│   ├── controller/
│   │   └── convert.py          # Core conversion logic
│   ├── gui/
│   │   ├── components/         # GUI components
│   │   ├── styles/            # CSS styling
│   │   └── main_windows.py    # Main window
│   └── cmd/
│       └── cli.py             # CLI interface
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, feature requests, or questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include system information and error messages

## Changelog

### v1.0.0
- Initial release
- GUI and CLI interfaces
- Support for major image formats
- Advanced compression and resizing options
- Batch processing capabilities
- Modern, responsive interface 