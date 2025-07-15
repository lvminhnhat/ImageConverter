"""
Tool Bar Component for Image Format Converter
Contains quick action buttons
"""

from PyQt6.QtWidgets import QToolBar, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon


class ToolBar(QToolBar):
    """Tool bar widget with quick actions"""
    
    # Signals
    convert_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setMovable(False)
        self.setup_actions()
        
    def setup_actions(self):
        """Setup toolbar actions"""
        # Convert button
        self.convert_btn = QPushButton("Convert Images")
        self.convert_btn.setObjectName("toolbarButton")
        self.convert_btn.clicked.connect(self.convert_requested.emit)
        self.addWidget(self.convert_btn)
        
        self.addSeparator()
        
        # Clear button
        self.clear_btn = QPushButton("Clear Files")
        self.clear_btn.setObjectName("toolbarButton")
        self.clear_btn.clicked.connect(self.clear_requested.emit)
        self.addWidget(self.clear_btn)
        
        self.addSeparator()
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("toolbarLabel")
        self.addWidget(self.status_label)
        
    def set_status(self, text):
        """Set status text"""
        self.status_label.setText(text) 