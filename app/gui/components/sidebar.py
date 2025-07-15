"""
Sidebar Component for Image Format Converter
Contains format selection and conversion options
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QComboBox, QSpinBox, QSlider, QCheckBox, 
                           QGroupBox, QFrame, QFormLayout, QScrollArea, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class Sidebar(QWidget):
    """Sidebar widget containing conversion settings"""
    
    # Signals
    format_changed = pyqtSignal(str)
    quality_changed = pyqtSignal(int)
    max_size_changed = pyqtSignal(int)
    compression_changed = pyqtSignal(int)
    resize_changed = pyqtSignal(int, int, bool)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the sidebar UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create scroll area for better UX
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Main content widget
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        
        # Content layout
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Conversion Settings")
        title.setObjectName("sidebarTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Output Format Group
        format_group = QGroupBox("Output Format")
        format_layout = QVBoxLayout(format_group)
        format_layout.setSpacing(10)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["webp", "jpeg", "png", "avif", "bmp", "tiff"])
        self.format_combo.setCurrentText("webp")
        format_layout.addWidget(self.format_combo)
        
        # Format info
        format_info = QLabel("• WebP: Best compression\n• JPEG: Wide compatibility\n• PNG: Lossless quality\n• AVIF: Modern format")
        format_info.setObjectName("formatInfo")
        format_info.setWordWrap(True)
        format_layout.addWidget(format_info)
        
        layout.addWidget(format_group)
        
        # Quality Group
        quality_group = QGroupBox("Quality Settings")
        quality_layout = QVBoxLayout(quality_group)
        quality_layout.setSpacing(15)
        
        # Quality slider
        quality_container = QWidget()
        quality_container_layout = QVBoxLayout(quality_container)
        quality_container_layout.setSpacing(8)
        
        quality_label_row = QHBoxLayout()
        quality_label_row.addWidget(QLabel("Quality:"))
        self.quality_label = QLabel("90")
        self.quality_label.setObjectName("qualityLabel")
        quality_label_row.addStretch()
        quality_label_row.addWidget(self.quality_label)
        quality_container_layout.addLayout(quality_label_row)
        
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(90)
        self.quality_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.quality_slider.setTickInterval(10)
        quality_container_layout.addWidget(self.quality_slider)
        
        quality_layout.addWidget(quality_container)
        layout.addWidget(quality_group)
        
        # Size Compression Group
        size_group = QGroupBox("Size Compression")
        size_layout = QVBoxLayout(size_group)
        size_layout.setSpacing(15)
        
        # Max size option
        max_size_container = QWidget()
        max_size_layout = QVBoxLayout(max_size_container)
        max_size_layout.setSpacing(8)
        
        self.max_size_check = QCheckBox("Limit file size")
        max_size_layout.addWidget(self.max_size_check)
        
        max_size_spin_container = QHBoxLayout()
        max_size_spin_container.addWidget(QLabel("Max size:"))
        self.max_size_spin = QSpinBox()
        self.max_size_spin.setRange(1, 10000)
        self.max_size_spin.setValue(500)
        self.max_size_spin.setSuffix(" KB")
        self.max_size_spin.setEnabled(False)
        max_size_spin_container.addWidget(self.max_size_spin)
        max_size_layout.addLayout(max_size_spin_container)
        
        size_layout.addWidget(max_size_container)
        
        # Compression percentage
        compression_container = QWidget()
        compression_layout = QVBoxLayout(compression_container)
        compression_layout.setSpacing(8)
        
        self.compression_check = QCheckBox("Compress to percentage")
        compression_layout.addWidget(self.compression_check)
        
        compression_spin_container = QHBoxLayout()
        compression_spin_container.addWidget(QLabel("Compression:"))
        self.compression_spin = QSpinBox()
        self.compression_spin.setRange(10, 100)
        self.compression_spin.setValue(70)
        self.compression_spin.setSuffix("%")
        self.compression_spin.setEnabled(False)
        compression_spin_container.addWidget(self.compression_spin)
        compression_layout.addLayout(compression_spin_container)
        
        size_layout.addWidget(compression_container)
        layout.addWidget(size_group)
        
        # Resize Group
        resize_group = QGroupBox("Resize Options")
        resize_layout = QVBoxLayout(resize_group)
        resize_layout.setSpacing(15)
        
        self.resize_check = QCheckBox("Resize images")
        resize_layout.addWidget(self.resize_check)
        
        # Dimensions container
        dimensions_container = QWidget()
        dimensions_layout = QVBoxLayout(dimensions_container)
        dimensions_layout.setSpacing(10)
        
        # Width
        width_container = QHBoxLayout()
        width_container.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(800)
        self.width_spin.setSuffix(" px")
        self.width_spin.setEnabled(False)
        width_container.addWidget(self.width_spin)
        dimensions_layout.addLayout(width_container)
        
        # Height
        height_container = QHBoxLayout()
        height_container.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(600)
        self.height_spin.setSuffix(" px")
        self.height_spin.setEnabled(False)
        height_container.addWidget(self.height_spin)
        dimensions_layout.addLayout(height_container)
        
        resize_layout.addWidget(dimensions_container)
        
        # Maintain aspect ratio
        self.aspect_check = QCheckBox("Maintain aspect ratio")
        self.aspect_check.setChecked(True)
        self.aspect_check.setEnabled(False)
        resize_layout.addWidget(self.aspect_check)
        
        layout.addWidget(resize_group)
        
        # Presets Group
        presets_group = QGroupBox("Quick Presets")
        presets_layout = QVBoxLayout(presets_group)
        presets_layout.setSpacing(8)
        
        preset_buttons = [
            ("Web Optimized", self.preset_web),
            ("High Quality", self.preset_high_quality),
            ("Small Size", self.preset_small_size),
            ("Mobile Ready", self.preset_mobile)
        ]
        
        for text, callback in preset_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setObjectName("presetButton")
            presets_layout.addWidget(btn)
        
        layout.addWidget(presets_group)
        
        # Add stretch at the end
        layout.addStretch()
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Format change
        self.format_combo.currentTextChanged.connect(self.format_changed.emit)
        
        # Quality change
        self.quality_slider.valueChanged.connect(self.on_quality_changed)
        
        # Size compression
        self.max_size_check.toggled.connect(self.max_size_spin.setEnabled)
        self.max_size_check.toggled.connect(self.on_max_size_changed)
        self.max_size_spin.valueChanged.connect(self.on_max_size_changed)
        
        self.compression_check.toggled.connect(self.compression_spin.setEnabled)
        self.compression_check.toggled.connect(self.on_compression_changed)
        self.compression_spin.valueChanged.connect(self.on_compression_changed)
        
        # Resize options
        self.resize_check.toggled.connect(self.on_resize_enabled)
        self.width_spin.valueChanged.connect(self.on_resize_changed)
        self.height_spin.valueChanged.connect(self.on_resize_changed)
        self.aspect_check.toggled.connect(self.on_resize_changed)
        
    def on_quality_changed(self, value):
        """Handle quality change"""
        self.quality_label.setText(str(value))
        self.quality_changed.emit(value)
        
    def on_max_size_changed(self):
        """Handle max size change"""
        if self.max_size_check.isChecked():
            self.max_size_changed.emit(self.max_size_spin.value())
        else:
            self.max_size_changed.emit(0)
            
    def on_compression_changed(self):
        """Handle compression change"""
        if self.compression_check.isChecked():
            self.compression_changed.emit(self.compression_spin.value())
        else:
            self.compression_changed.emit(0)
            
    def on_resize_enabled(self, enabled):
        """Handle resize enabled change"""
        self.width_spin.setEnabled(enabled)
        self.height_spin.setEnabled(enabled)
        self.aspect_check.setEnabled(enabled)
        self.on_resize_changed()
        
    def on_resize_changed(self):
        """Handle resize options change"""
        if self.resize_check.isChecked():
            self.resize_changed.emit(
                self.width_spin.value(),
                self.height_spin.value(),
                self.aspect_check.isChecked()
            )
        else:
            self.resize_changed.emit(0, 0, True)
    
    # Preset methods
    def preset_web(self):
        """Web optimized preset"""
        self.format_combo.setCurrentText("webp")
        self.quality_slider.setValue(85)
        self.max_size_check.setChecked(True)
        self.max_size_spin.setValue(500)
        self.compression_check.setChecked(False)
        self.resize_check.setChecked(True)
        self.width_spin.setValue(1920)
        self.height_spin.setValue(1080)
        self.aspect_check.setChecked(True)
        
    def preset_high_quality(self):
        """High quality preset"""
        self.format_combo.setCurrentText("png")
        self.quality_slider.setValue(95)
        self.max_size_check.setChecked(False)
        self.compression_check.setChecked(False)
        self.resize_check.setChecked(False)
        
    def preset_small_size(self):
        """Small size preset"""
        self.format_combo.setCurrentText("jpeg")
        self.quality_slider.setValue(70)
        self.max_size_check.setChecked(False)
        self.compression_check.setChecked(True)
        self.compression_spin.setValue(50)
        self.resize_check.setChecked(True)
        self.width_spin.setValue(800)
        self.height_spin.setValue(600)
        self.aspect_check.setChecked(True)
        
    def preset_mobile(self):
        """Mobile ready preset"""
        self.format_combo.setCurrentText("webp")
        self.quality_slider.setValue(80)
        self.max_size_check.setChecked(True)
        self.max_size_spin.setValue(200)
        self.compression_check.setChecked(False)
        self.resize_check.setChecked(True)
        self.width_spin.setValue(640)
        self.height_spin.setValue(480)
        self.aspect_check.setChecked(True) 