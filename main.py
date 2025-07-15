#!/usr/bin/env python3
"""
Image Format Converter
A modern image format converter with GUI and CLI interfaces

Usage:
    GUI Mode: python main.py
    CLI Mode: python main.py cli [options]
"""

import sys
import argparse
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for the application"""
    # Check if CLI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        # Remove 'cli' from arguments and run CLI
        sys.argv.pop(1)
        from app.cmd.cli import main as cli_main
        cli_main()
    else:
        # Run GUI mode
        try:
            from app.gui.main_windows import main as gui_main
            sys.exit(gui_main())
        except ImportError as e:
            print(f"Error importing GUI modules: {e}")
            print("Please install PyQt6: pip install PyQt6")
            sys.exit(1)

if __name__ == "__main__":
    main()
