import argparse
import os
import sys
from pathlib import Path
from tqdm import tqdm
import colorama
from colorama import Fore, Style, Back

from app.controller.convert import ImageFormatConverter

# Initialize colorama for colored output
colorama.init()

def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════════════╗
║                            {Fore.YELLOW}IMAGE FORMAT CONVERTER{Fore.CYAN}                                     ║
║                        {Fore.GREEN}Convert images between formats with ease{Fore.CYAN}                           ║
║                            {Fore.BLUE}Supports: PNG, JPEG, WEBP, AVIF, BMP, TIFF{Fore.CYAN}                      ║
╚════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_success(message):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message"""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def validate_input_path(path):
    """Validate input path exists"""
    if not os.path.exists(path):
        print_error(f"Path does not exist: {path}")
        sys.exit(1)

def validate_output_path(path):
    """Validate and create output path if needed"""
    if path:
        try:
            os.makedirs(path, exist_ok=True)
            print_info(f"Output directory: {path}")
        except Exception as e:
            print_error(f"Cannot create output directory: {e}")
            sys.exit(1)

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def print_statistics(results):
    """Print conversion statistics in a beautiful format"""
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    if not results:
        print_warning("No files processed")
        return
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}                           CONVERSION RESULTS")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}Total files:{Style.RESET_ALL} {len(results)}")
    print(f"{Fore.GREEN}Successful:{Style.RESET_ALL} {len(successful)}")
    print(f"{Fore.RED}Failed:{Style.RESET_ALL} {len(failed)}")
    
    if successful:
        # Phân loại files theo loại thay đổi
        compressed_files = [r for r in successful if r.get("change_type") == "compressed"]
        expanded_files = [r for r in successful if r.get("change_type") == "expanded"]
        unchanged_files = [r for r in successful if r.get("change_type") == "unchanged"]
        
        total_original = sum(r["original_size"] for r in successful)
        total_new = sum(r["new_size"] for r in successful)
        
        print(f"\n{Fore.CYAN}📊 SIZE STATISTICS:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Original size:{Style.RESET_ALL} {format_file_size(total_original)}")
        print(f"{Fore.BLUE}New size:{Style.RESET_ALL} {format_file_size(total_new)}")
        
        # Hiển thị thông tin compression
        if compressed_files:
            total_saved = sum(r.get("space_change", 0) for r in compressed_files)
            avg_compression = sum(r["compression_ratio"] for r in compressed_files) / len(compressed_files)
            print(f"{Fore.GREEN}📉 Compressed files:{Style.RESET_ALL} {len(compressed_files)}")
            print(f"{Fore.GREEN}💾 Space saved:{Style.RESET_ALL} {format_file_size(total_saved)}")
            print(f"{Fore.YELLOW}📊 Average compression:{Style.RESET_ALL} {avg_compression:.2f}%")
        
        # Hiển thị thông tin expansion
        if expanded_files:
            total_increased = sum(r.get("space_change", 0) for r in expanded_files)
            print(f"{Fore.YELLOW}📈 Expanded files:{Style.RESET_ALL} {len(expanded_files)}")
            print(f"{Fore.YELLOW}📈 Space increased:{Style.RESET_ALL} {format_file_size(total_increased)}")
        
        # Hiển thị files không thay đổi
        if unchanged_files:
            print(f"{Fore.BLUE}➡️ Unchanged files:{Style.RESET_ALL} {len(unchanged_files)}")
        
        # Tổng kết
        total_saved = sum(r.get("space_change", 0) for r in compressed_files)
        total_increased = sum(r.get("space_change", 0) for r in expanded_files)
        net_change = total_saved - total_increased
        
        print(f"\n{Fore.CYAN}📋 SUMMARY:{Style.RESET_ALL}")
        if net_change > 0:
            print_success(f"Net space saved: {format_file_size(net_change)}")
        elif net_change < 0:
            print_warning(f"Net space increased: {format_file_size(abs(net_change))}")
        else:
            print_info("No net change in space")
    
    if failed:
        print(f"\n{Fore.RED}{'='*50}")
        print(f"{Fore.RED}FAILED FILES:")
        print(f"{Fore.RED}{'='*50}{Style.RESET_ALL}")
        for result in failed:
            filename = os.path.basename(result.get('input_path', 'Unknown'))
            error = result.get('error', 'Unknown error')
            print_error(f"{filename}: {error}")

def convert_single_file(args, converter):
    """Convert a single file"""
    input_file = args.input
    
    validate_input_path(input_file)
    
    if not os.path.isfile(input_file):
        print_error(f"'{input_file}' is not a file")
        sys.exit(1)
    
    # Determine output path
    output_path = None
    if args.output:
        validate_output_path(args.output)
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_path = os.path.join(args.output, f"{base}.{args.format}")
    
    print_info(f"Converting: {os.path.basename(input_file)}")
    
    # Convert with progress
    with tqdm(total=1, desc="Converting", unit="file") as pbar:
        # Map jpg to jpeg for PIL compatibility
        output_format = "jpeg" if args.format == "jpg" else args.format
        result = converter.convert(input_file, output_format, output_path=output_path)
        pbar.update(1)
    
    if result["success"]:
        print_success(f"Converted successfully!")
        print_info(f"Output: {result['output_path']}")
        print_info(f"Size: {format_file_size(result['original_size'])} → {format_file_size(result['new_size'])}")
        
        # Hiển thị thông tin theo loại thay đổi
        change_type = result.get("change_type", "unknown")
        if change_type == "compressed":
            print_success(f"Compression: {result['compression_ratio']:.2f}%")
            print_success(f"Space saved: {format_file_size(result['space_change'])}")
        elif change_type == "expanded":
            print_warning(f"File expanded: {result['compression_ratio']:.2f}%")
            print_warning(f"Space increased: {format_file_size(result['space_change'])}")
        elif change_type == "unchanged":
            print_info("File size unchanged")
        else:
            print_info(f"Compression ratio: {result['compression_ratio']:.2f}%")
    else:
        print_error(f"Conversion failed: {result['error']}")
        sys.exit(1)

def convert_folder(args, converter):
    """Convert all images in a folder"""
    input_folder = args.input
    
    validate_input_path(input_folder)
    
    if not os.path.isdir(input_folder):
        print_error(f"'{input_folder}' is not a directory")
        sys.exit(1)
    
    validate_output_path(args.output)
    
    print_info(f"Scanning folder: {input_folder}")
    
    # Get all image files
    image_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.avif', '.bmp', '.tiff', '.gif')
    image_files = []
    
    if args.recursive:
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(input_folder):
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(input_folder, file))
    
    if not image_files:
        print_warning("No image files found")
        return
    
    print_info(f"Found {len(image_files)} image files")
    
    # Convert files with progress bar
    results = []
    with tqdm(total=len(image_files), desc="Converting", unit="file") as pbar:
        for image_file in image_files:
            output_path = None
            if args.output:
                # Create relative path structure
                rel_path = os.path.relpath(image_file, input_folder)
                base_dir = os.path.dirname(rel_path)
                base_name = os.path.splitext(os.path.basename(rel_path))[0]
                
                target_dir = os.path.join(args.output, base_dir) if base_dir else args.output
                os.makedirs(target_dir, exist_ok=True)
                
                output_path = os.path.join(target_dir, f"{base_name}.{args.format}")
            
            # Map jpg to jpeg for PIL compatibility
            output_format = "jpeg" if args.format == "jpg" else args.format
            result = converter.convert(image_file, output_format, output_path)
            results.append(result)
            pbar.update(1)
    
    print_statistics(results)

def convert_multiple_files(args, converter):
    """Convert multiple selected files"""
    input_files = args.input.split(',')
    
    # Validate all files exist
    for file_path in input_files:
        file_path = file_path.strip()
        validate_input_path(file_path)
        if not os.path.isfile(file_path):
            print_error(f"'{file_path}' is not a file")
            sys.exit(1)
    
    if args.output:
        validate_output_path(args.output)
    
    print_info(f"Converting {len(input_files)} files")
    
    # Convert files with progress bar
    results = []
    with tqdm(total=len(input_files), desc="Converting", unit="file") as pbar:
        for file_path in input_files:
            file_path = file_path.strip()
            output_path = None
            if args.output:
                base = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(args.output, f"{base}.{args.format}")
            
            # Map jpg to jpeg for PIL compatibility
            output_format = "jpeg" if args.format == "jpg" else args.format
            result = converter.convert(file_path, output_format, output_path)
            results.append(result)
            pbar.update(1)
    
    print_statistics(results)

def main():
    """Main CLI function"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Convert images between different formats with advanced options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i photo.jpg -f webp -q 85 -s 500
  %(prog)s -i /path/to/images --folder -f avif -r -o /output
  %(prog)s -i "img1.jpg,img2.png" -f jpeg -q 90 -c 70
  %(prog)s -i photo.png -f webp --resize 800x600 --maintain-aspect
        """
    )
    
    # Input options
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to input file, folder, or comma-separated list of files"
    )
    
    parser.add_argument(
        "-f", "--format", required=True, 
        choices=["jpeg", "jpg", "png", "webp", "avif", "bmp", "tiff"],
        help="Output image format"
    )
    
    # Processing options
    parser.add_argument(
        "--folder", action="store_true",
        help="Process entire folder (use with -i pointing to folder)"
    )
    
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="Process subfolders recursively (use with --folder)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: same as input)"
    )
    
    # Quality options
    parser.add_argument(
        "-q", "--quality", type=int, default=90, choices=range(10, 101),
        help="Output image quality 10-100 (default: 90)"
    )
    
    parser.add_argument(
        "-s", "--max-size", type=int, default=None,
        help="Maximum output file size in KB"
    )
    
    parser.add_argument(
        "-c", "--compression", type=int, default=None, choices=range(10, 101),
        help="Compress to percentage of original size (10-100)"
    )
    
    # Resize options
    parser.add_argument(
        "--resize", 
        help="Resize images (format: WIDTHxHEIGHT, e.g., 800x600)"
    )
    
    parser.add_argument(
        "--maintain-aspect", action="store_true", default=True,
        help="Maintain aspect ratio when resizing (default: True)"
    )
    
    # Utility options
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress progress bars and info messages"
    )
    
    parser.add_argument(
        "--version", action="version", version="Image Format Converter 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Parse resize option
    target_width = None
    target_height = None
    if args.resize:
        try:
            width_str, height_str = args.resize.split('x')
            target_width = int(width_str)
            target_height = int(height_str)
        except ValueError:
            print_error("Invalid resize format. Use WIDTHxHEIGHT (e.g., 800x600)")
            sys.exit(1)
    
    # Create converter with options
    converter = ImageFormatConverter(
        max_size_kb=args.max_size,
        quality=args.quality,
        compression_percent=args.compression,
        target_width=target_width,
        target_height=target_height,
        maintain_aspect_ratio=args.maintain_aspect
    )
    
    # Suppress progress bars if quiet mode
    if args.quiet:
        import os
        os.environ['TQDM_DISABLE'] = '1'
    
    # Process based on input type
    try:
        if args.folder:
            convert_folder(args, converter)
        elif ',' in args.input:
            convert_multiple_files(args, converter)
        else:
            convert_single_file(args, converter)
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
