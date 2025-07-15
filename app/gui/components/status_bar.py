"""
Status Bar Component for Image Format Converter
Shows status messages and progress
"""

from PyQt6.QtWidgets import QStatusBar, QProgressBar, QLabel
from PyQt6.QtCore import QTimer


class StatusBar(QStatusBar):
    """Status bar widget with progress and messages"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup status bar UI"""
        # Status message (main area)
        self.status_label = QLabel("Ready")
        self.addWidget(self.status_label)
        
        # Progress bar (permanent widget)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.addPermanentWidget(self.progress_bar)
        
        # File count label
        self.file_count_label = QLabel("0 files")
        self.addPermanentWidget(self.file_count_label)
        
    def show_message(self, message, timeout=0):
        """Show a status message"""
        self.status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.status_label.setText("Ready"))
            
    def set_progress(self, value):
        """Set progress bar value"""
        if value == 0:
            self.progress_bar.setVisible(False)
        else:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(value)
            
    def set_file_count(self, count):
        """Set file count display"""
        self.file_count_label.setText(f"{count} files") 