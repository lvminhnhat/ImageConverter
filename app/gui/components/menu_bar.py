"""
Menu Bar Component for Image Format Converter
Contains File, Edit, View, and Help menus
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence


class MenuBar(QMenuBar):
    """Menu bar widget"""
    
    # Signals
    open_files_requested = pyqtSignal()
    open_folder_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    about_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_menus()
        
    def setup_menus(self):
        """Setup menu bar menus"""
        # File Menu
        file_menu = self.addMenu("&File")
        
        # Open Files
        open_files_action = QAction("Open Files...", self)
        open_files_action.setShortcut(QKeySequence.StandardKey.Open)
        open_files_action.setStatusTip("Open image files")
        open_files_action.triggered.connect(self.open_files_requested.emit)
        file_menu.addAction(open_files_action)
        
        # Open Folder
        open_folder_action = QAction("Open Folder...", self)
        open_folder_action.setShortcut(QKeySequence("Ctrl+Shift+O"))
        open_folder_action.setStatusTip("Open folder containing images")
        open_folder_action.triggered.connect(self.open_folder_requested.emit)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.exit_application)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = self.addMenu("&Edit")
        
        # Settings
        settings_action = QAction("Settings...", self)
        settings_action.setShortcut(QKeySequence.StandardKey.Preferences)
        settings_action.setStatusTip("Open settings")
        settings_action.triggered.connect(self.settings_requested.emit)
        edit_menu.addAction(settings_action)
        
        # View Menu
        view_menu = self.addMenu("&View")
        
        # Refresh
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut(QKeySequence.StandardKey.Refresh)
        refresh_action.setStatusTip("Refresh file list")
        view_menu.addAction(refresh_action)
        
        # Help Menu
        help_menu = self.addMenu("&Help")
        
        # About
        about_action = QAction("About", self)
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.about_requested.emit)
        help_menu.addAction(about_action)
    
    def exit_application(self):
        """Handle exit action"""
        QApplication.quit() 