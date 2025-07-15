"""
Central Widget for Image Format Converter
Handles file selection, preview, and conversion process
"""

import os
import threading
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QListWidget, QListWidgetItem, QPushButton, 
                           QProgressBar, QFrame, QSplitter, QTextEdit,
                           QFileDialog, QMessageBox, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QFont

from ...controller.convert import ImageFormatConverter


class ConversionThread(QThread):
    """Thread for handling image conversion without blocking UI"""
    progress_changed = pyqtSignal(int)
    status_message = pyqtSignal(str)
    conversion_finished = pyqtSignal(list)
    
    def __init__(self, files, output_format, converter_options):
        super().__init__()
        self.files = files
        self.output_format = output_format
        self.converter_options = converter_options
    
    def run(self):
        """Run conversion in background thread"""
        converter = ImageFormatConverter(**self.converter_options)
        results = []
        
        for i, file_path in enumerate(self.files):
            self.status_message.emit(f"Converting: {os.path.basename(file_path)}")
            
            result = converter.convert(file_path, self.output_format)
            results.append(result)
            
            progress = int((i + 1) / len(self.files) * 100)
            self.progress_changed.emit(progress)
        
        self.conversion_finished.emit(results)


class FileListWidget(QListWidget):
    """Custom file list widget with drag and drop support"""
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.DropOnly)
        self.setObjectName("fileList")
        
        # Add placeholder text
        self.setStyleSheet("""
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path and os.path.isfile(file_path):
                files.append(file_path)
        
        if files:
            # Find the CentralWidget parent
            parent = self.parent()
            while parent and not isinstance(parent, CentralWidget):
                parent = parent.parent()
            
            if parent:
                parent.add_files(files)
        
        event.acceptProposedAction()


class CentralWidget(QWidget):
    """Central widget containing file list and conversion controls"""
    
    # Signals
    status_message = pyqtSignal(str)
    progress_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_default_options()
        self.files = []
        self.conversion_thread = None
        
    def setup_ui(self):
        """Setup the central widget UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Image Format Converter")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Main content area
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - File list
        left_group = QGroupBox("Files to Convert")
        left_layout = QVBoxLayout(left_group)
        
        # File list
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(300)
        left_layout.addWidget(self.file_list)
        
        # File control buttons
        file_buttons = QHBoxLayout()
        
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.setObjectName("primaryButton")
        self.add_files_btn.clicked.connect(self.browse_files)
        file_buttons.addWidget(self.add_files_btn)
        
        self.add_folder_btn = QPushButton("Add Folder")
        self.add_folder_btn.clicked.connect(self.browse_folder)
        file_buttons.addWidget(self.add_folder_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_files)
        file_buttons.addWidget(self.clear_btn)
        
        left_layout.addLayout(file_buttons)
        
        # Right side - Preview and results
        right_group = QGroupBox("Preview & Results")
        right_layout = QVBoxLayout(right_group)
        
        # Preview area
        self.preview_label = QLabel("Select a file to preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setObjectName("previewLabel")
        right_layout.addWidget(self.preview_label)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        self.results_text.setReadOnly(True)
        self.results_text.setObjectName("resultsText")
        right_layout.addWidget(self.results_text)
        
        # Add groups to splitter
        splitter.addWidget(left_group)
        splitter.addWidget(right_group)
        splitter.setSizes([400, 400])
        
        layout.addWidget(splitter)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progressBar")
        layout.addWidget(self.progress_bar)
        
        # Convert button
        self.convert_btn = QPushButton("Convert Images")
        self.convert_btn.setObjectName("convertButton")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        layout.addWidget(self.convert_btn)
        
        # Connect file list selection
        self.file_list.currentItemChanged.connect(self.update_preview)
    
    def setup_default_options(self):
        """Setup default conversion options"""
        self.output_format = "webp"
        self.converter_options = {
            "quality": 90,
            "max_size_kb": None,
            "compression_percent": None,
            "target_width": None,
            "target_height": None,
            "maintain_aspect_ratio": True
        }
    
    def browse_files(self):
        """Browse and select files"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Image Files", "",
            "Image Files (*.png *.jpg *.jpeg *.webp *.avif *.bmp *.tiff *.gif)"
        )
        if files:
            self.add_files(files)
    
    def browse_folder(self):
        """Browse and select folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.add_folder(folder)
    
    def add_files(self, files):
        """Add files to the list"""
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.file_list.addItem(item)
        
        self.convert_btn.setEnabled(len(self.files) > 0)
        self.status_message.emit(f"Added {len(files)} files")
    
    def add_folder(self, folder_path):
        """Add all images from folder"""
        image_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.avif', '.bmp', '.tiff', '.gif')
        files = []
        
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.lower().endswith(image_extensions):
                    files.append(os.path.join(root, filename))
        
        if files:
            self.add_files(files)
        else:
            QMessageBox.information(self, "No Images", "No image files found in the selected folder.")
    
    def clear_files(self):
        """Clear all files from the list"""
        self.files.clear()
        self.file_list.clear()
        self.convert_btn.setEnabled(False)
        self.preview_label.setText("Select a file to preview")
        self.results_text.clear()
        self.status_message.emit("Files cleared")
    
    def update_preview(self, current, previous):
        """Update preview when file selection changes"""
        if current is None:
            return
        
        file_path = current.data(Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            try:
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        200, 200, Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.preview_label.setPixmap(scaled_pixmap)
                else:
                    self.preview_label.setText("Cannot preview this file")
            except Exception as e:
                self.preview_label.setText(f"Preview error: {str(e)}")
    
    def start_conversion(self):
        """Start the conversion process"""
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add files to convert.")
            return
        
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.results_text.clear()
        
        # Start conversion thread
        self.conversion_thread = ConversionThread(
            self.files, self.output_format, self.converter_options
        )
        self.conversion_thread.progress_changed.connect(self.progress_bar.setValue)
        self.conversion_thread.status_message.connect(self.status_message.emit)
        self.conversion_thread.conversion_finished.connect(self.conversion_finished)
        self.conversion_thread.start()
    
    def conversion_finished(self, results):
        """Handle conversion completion"""
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        
        # Display results
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        
        result_text = f"🎉 Conversion completed!\n"
        result_text += f"✅ Successful: {len(successful)}\n"
        result_text += f"❌ Failed: {len(failed)}\n\n"
        
        if successful:
            # Phân loại files theo loại thay đổi
            compressed_files = [r for r in successful if r.get("change_type") == "compressed"]
            expanded_files = [r for r in successful if r.get("change_type") == "expanded"]
            unchanged_files = [r for r in successful if r.get("change_type") == "unchanged"]
            
            total_original = sum(r["original_size"] for r in successful)
            total_new = sum(r["new_size"] for r in successful)
            
            result_text += f"📊 SIZE STATISTICS:\n"
            result_text += f"Original: {total_original / 1024:.2f} KB\n"
            result_text += f"New: {total_new / 1024:.2f} KB\n\n"
            
            # Hiển thị thông tin compression
            if compressed_files:
                total_saved = sum(r.get("space_change", 0) for r in compressed_files)
                avg_compression = sum(r["compression_ratio"] for r in compressed_files) / len(compressed_files)
                result_text += f"📉 Compressed: {len(compressed_files)} files\n"
                result_text += f"💾 Saved: {total_saved / 1024:.2f} KB\n"
                result_text += f"📊 Avg compression: {avg_compression:.2f}%\n\n"
            
            # Hiển thị thông tin expansion
            if expanded_files:
                total_increased = sum(r.get("space_change", 0) for r in expanded_files)
                result_text += f"📈 Expanded: {len(expanded_files)} files\n"
                result_text += f"📈 Increased: {total_increased / 1024:.2f} KB\n\n"
            
            # Hiển thị files không thay đổi
            if unchanged_files:
                result_text += f"➡️ Unchanged: {len(unchanged_files)} files\n\n"
            
            # Tổng kết
            total_saved = sum(r.get("space_change", 0) for r in compressed_files)
            total_increased = sum(r.get("space_change", 0) for r in expanded_files)
            net_change = total_saved - total_increased
            
            result_text += f"📋 SUMMARY:\n"
            if net_change > 0:
                result_text += f"✅ Net saved: {net_change / 1024:.2f} KB\n"
            elif net_change < 0:
                result_text += f"⚠️ Net increased: {abs(net_change) / 1024:.2f} KB\n"
            else:
                result_text += f"➡️ No net change\n"
        
        if failed:
            result_text += f"\n❌ FAILED FILES:\n"
            for result in failed:
                result_text += f"❌ {os.path.basename(result.get('input_path', 'Unknown'))}: {result.get('error', 'Unknown error')}\n"
        
        self.results_text.setText(result_text)
        self.status_message.emit("Conversion completed!")
    
    # Slots for settings from sidebar
    def set_output_format(self, format_name):
        """Set output format"""
        self.output_format = format_name
        self.status_message.emit(f"Output format set to: {format_name}")
    
    def set_quality(self, quality):
        """Set quality"""
        self.converter_options["quality"] = quality
    
    def set_max_size(self, max_size_kb):
        """Set maximum size in KB"""
        self.converter_options["max_size_kb"] = max_size_kb if max_size_kb > 0 else None
    
    def set_compression(self, compression_percent):
        """Set compression percentage"""
        self.converter_options["compression_percent"] = compression_percent if compression_percent > 0 else None
    
    def set_resize_options(self, width, height, maintain_aspect):
        """Set resize options"""
        self.converter_options["target_width"] = width if width > 0 else None
        self.converter_options["target_height"] = height if height > 0 else None
        self.converter_options["maintain_aspect_ratio"] = maintain_aspect 