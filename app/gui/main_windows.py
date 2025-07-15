"""
Main Window for Image Format Converter
Modern and clean interface using PyQt6
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QFrame, QSizePolicy, QSplitter)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPixmap

from .components.central_widget import CentralWidget
from .components.sidebar import Sidebar
from .components.status_bar import StatusBar
from .components.menu_bar import MenuBar
from .components.tool_bar import ToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Format Converter")
        self.setMinimumSize(QSize(1200, 800))
        self.resize(1400, 900)
        
        # Setup components
        self.setup_ui()
        self.setup_styling()
        
        # Connect signals
        self.setup_connections()
        
        # Show maximized for better experience
        self.showMaximized()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create sidebar
        self.sidebar = Sidebar()
        self.sidebar.setMaximumWidth(400)
        self.sidebar.setMinimumWidth(350)
        
        # Create central widget
        self.central_widget = CentralWidget()
        
        # Add widgets to splitter
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.central_widget)
        
        # Set splitter proportions - more space for sidebar
        splitter.setSizes([380, 1020])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Create menu bar
        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        
        # Create tool bar
        self.tool_bar = ToolBar()
        self.addToolBar(self.tool_bar)
        
        # Create status bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
    
    def setup_styling(self):
        """Load and apply CSS styling"""
        try:
            css_path = os.path.join(os.path.dirname(__file__), "styles", "main_window.css")
            with open(css_path, "r", encoding="utf-8") as css_file:
                self.setStyleSheet(css_file.read())
        except FileNotFoundError:
            print("Warning: CSS file not found. Using default styling.")
    
    def setup_connections(self):
        """Connect signals between components"""
        # Connect sidebar signals to central widget
        self.sidebar.format_changed.connect(self.central_widget.set_output_format)
        self.sidebar.quality_changed.connect(self.central_widget.set_quality)
        self.sidebar.max_size_changed.connect(self.central_widget.set_max_size)
        self.sidebar.compression_changed.connect(self.central_widget.set_compression)
        self.sidebar.resize_changed.connect(self.central_widget.set_resize_options)
        
        # Connect central widget signals to status bar
        self.central_widget.status_message.connect(self.status_bar.show_message)
        self.central_widget.progress_changed.connect(self.status_bar.set_progress)
        
        # Connect tool bar signals
        self.tool_bar.convert_requested.connect(self.central_widget.start_conversion)
        self.tool_bar.clear_requested.connect(self.central_widget.clear_files)
        
        # Connect menu bar signals
        self.menu_bar.open_files_requested.connect(self.central_widget.add_files)
        self.menu_bar.open_folder_requested.connect(self.central_widget.add_folder)
        self.menu_bar.settings_requested.connect(self.show_settings)
        self.menu_bar.about_requested.connect(self.show_about)
    
    def show_settings(self):
        """Show settings dialog"""
        # TODO: Implement settings dialog
        self.status_bar.show_message("Settings dialog not implemented yet", 3000)
    
    def show_about(self):
        """Show about dialog"""
        # TODO: Implement about dialog
        self.status_bar.show_message("About dialog not implemented yet", 3000)
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save window state and settings
        # TODO: Save user preferences
        event.accept()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Image Format Converter")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Image Tools")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create main window
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 