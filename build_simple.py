#!/usr/bin/env python3
"""
Simple build script for creating executable
"""

import os
import sys
import subprocess

def main():
    print("🚀 Bắt đầu build executable...")
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
        print("✅ PyInstaller đã sẵn sàng")
    except ImportError:
        print("📦 Cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ImageConverter",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=PyQt6.sip", 
        "--hidden-import=pillow_avif",
        "--add-data=app/gui/styles;app/gui/styles",
        "main.py"
    ]
    
    print(f"🔨 Chạy: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ BUILD THÀNH CÔNG!")
        print("📁 File exe: dist/ImageConverter.exe")
        print("💡 Có thể chạy trên mọi máy Windows mà không cần Python")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build thất bại: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 