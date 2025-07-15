#!/usr/bin/env python3
"""
Build script for creating a single executable file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller đã được cài đặt")
    except ImportError:
        print("📦 Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller đã được cài đặt thành công")

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Đang xóa thư mục {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for spec_file in Path(".").glob("*.spec"):
        print(f"🧹 Đang xóa file {spec_file}...")
        spec_file.unlink()

def build_exe():
    """Build the executable"""
    print("🔨 Bắt đầu build executable...")
    
    # PyInstaller command with options for single file
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tạo 1 file exe duy nhất
        "--windowed",                   # Không hiển thị console window (cho GUI)
        "--name=ImageConverter",        # Tên file exe
        "--icon=app/gui/styles/icon.ico" if os.path.exists("app/gui/styles/icon.ico") else None,  # Icon nếu có
        "--add-data=app/gui/styles;app/gui/styles",  # Include CSS files
        "--hidden-import=PIL._tkinter_finder",  # Fix PIL import issues
        "--hidden-import=PyQt6.sip",    # Fix PyQt6 import issues
        "--hidden-import=pillow_avif",  # Include AVIF support
        "--collect-all=PIL",            # Collect all PIL modules
        "--collect-all=PyQt6",          # Collect all PyQt6 modules
        "main.py"                       # Entry point
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    print(f"🚀 Chạy lệnh: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build thất bại:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def create_cli_exe():
    """Create a separate CLI executable"""
    print("🔨 Tạo CLI executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=ImageConverterCLI",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=PyQt6.sip",
        "--hidden-import=pillow_avif",
        "--collect-all=PIL",
        "main.py",
        "cli"  # Add CLI argument
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ CLI executable tạo thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ CLI build thất bại:")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Main build process"""
    print("🚀 BẮT ĐẦU QUÁ TRÌNH BUILD EXECUTABLE")
    print("=" * 50)
    
    # Step 1: Install PyInstaller
    install_pyinstaller()
    
    # Step 2: Clean previous builds
    clean_build_dirs()
    
    # Step 3: Build main executable
    if build_exe():
        print("\n✅ BUILD HOÀN THÀNH!")
        print("📁 File executable được tạo tại: dist/ImageConverter.exe")
        print("💡 Bạn có thể chạy file này trên bất kỳ máy Windows nào mà không cần cài Python")
        
        # Optional: Create CLI version
        print("\n🔧 Tạo thêm CLI executable...")
        create_cli_exe()
        print("📁 CLI executable được tạo tại: dist/ImageConverterCLI.exe")
        
        print("\n📋 HƯỚNG DẪN SỬ DỤNG:")
        print("- ImageConverter.exe: Chạy giao diện đồ họa")
        print("- ImageConverterCLI.exe: Chạy giao diện dòng lệnh")
        print("- Cả hai file đều có thể chạy độc lập trên Windows")
        
    else:
        print("❌ BUILD THẤT BẠI!")
        sys.exit(1)

if __name__ == "__main__":
    main() 