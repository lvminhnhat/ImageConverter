import os
from PIL import Image
import pillow_avif  # Đảm bảo đã cài pillow-avif-plugin

class ImageFormatConverter:
    def __init__(self, max_size_kb=None, quality=95, compression_percent=None, target_width=None, target_height=None, maintain_aspect_ratio=True):
        """
        :param max_size_kb: (int|None) Nén ảnh nhỏ hơn dung lượng này (KB). None = không nén.
        :param quality: Chất lượng ảnh (20-100), càng cao càng nét.
        :param compression_percent: (int|None) Nén ảnh xuống còn X% kích thước gốc (10-100).
        :param target_width: (int|None) Chiều rộng mục tiêu (px).
        :param target_height: (int|None) Chiều cao mục tiêu (px).
        :param maintain_aspect_ratio: (bool) Giữ tỷ lệ khung hình khi resize.
        """
        self.max_size_kb = max_size_kb
        self.quality = quality
        self.compression_percent = compression_percent
        self.target_width = target_width
        self.target_height = target_height
        self.maintain_aspect_ratio = maintain_aspect_ratio
        
        # Các định dạng hỗ trợ
        self.supported_formats = ["jpeg", "jpg", "png", "webp", "avif", "bmp", "tiff", "gif"]
        self.input_extensions = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".bmp", ".tiff", ".gif")

    def convert(self, input_path, output_format, output_path=None):
        """
        Chuyển đổi file ảnh sang định dạng chỉ định.
        :param input_path: Đường dẫn file ảnh nguồn
        :param output_format: Định dạng đích: "jpeg", "png", "webp", "avif",...
        :param output_path: Đường dẫn lưu ảnh đích (mặc định tạo thư mục convert)
        :return: dict với thông tin kết quả
        """
        if not os.path.exists(input_path):
            return {"success": False, "error": f"File không tồn tại: {input_path}"}
        
        if output_format.lower() not in self.supported_formats:
            return {"success": False, "error": f"Định dạng không hỗ trợ: {output_format}"}
        
        try:
            # Mở ảnh và chuyển sang RGB nếu cần
            img = Image.open(input_path)
            if img.mode in ("RGBA", "LA") and output_format.lower() in ["jpeg", "jpg"]:
                # Tạo nền trắng cho JPEG
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            
            # Lưu kích thước gốc
            original_size = os.path.getsize(input_path)
            original_width, original_height = img.size
            
            # Resize ảnh nếu cần
            img = self._resize_image(img)
            
            # Tạo đường dẫn output
            if output_path is None:
                # Tạo thư mục convert trong thư mục chứa file gốc
                input_dir = os.path.dirname(input_path)
                convert_dir = os.path.join(input_dir, "convert")
                os.makedirs(convert_dir, exist_ok=True)
                
                # Lấy tên file gốc (không có extension)
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(convert_dir, f"{base_name}.{output_format.lower()}")
            else:
                # Nếu có output_path được chỉ định, tạo thư mục nếu cần
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
            
            # Lưu ảnh
            img = self._save_with_compression(img, output_path, output_format, original_size)
            
            # Tính toán thống kê
            new_size = os.path.getsize(output_path)
            
            # Tính compression ratio (có thể âm nếu file tăng kích thước)
            if original_size > 0:
                compression_ratio = ((original_size - new_size) / original_size) * 100
            else:
                compression_ratio = 0
            
            # Xác định loại thay đổi
            if new_size < original_size:
                change_type = "compressed"
                space_change = original_size - new_size
            elif new_size > original_size:
                change_type = "expanded"
                space_change = new_size - original_size
            else:
                change_type = "unchanged"
                space_change = 0
            
            return {
                "success": True,
                "input_path": input_path,
                "output_path": output_path,
                "original_size": original_size,
                "new_size": new_size,
                "compression_ratio": compression_ratio,
                "change_type": change_type,
                "space_change": space_change,
                "original_dimensions": (original_width, original_height),
                "new_dimensions": img.size
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _resize_image(self, img):
        """Resize ảnh theo các tham số đã đặt"""
        if not self.target_width and not self.target_height:
            return img
        
        current_width, current_height = img.size
        
        if self.maintain_aspect_ratio:
            if self.target_width and self.target_height:
                # Tính toán để fit vào khung mục tiêu
                ratio_w = self.target_width / current_width
                ratio_h = self.target_height / current_height
                ratio = min(ratio_w, ratio_h)
                new_width = int(current_width * ratio)
                new_height = int(current_height * ratio)
            elif self.target_width:
                ratio = self.target_width / current_width
                new_width = self.target_width
                new_height = int(current_height * ratio)
            else:  # target_height
                ratio = self.target_height / current_height
                new_width = int(current_width * ratio)
                new_height = self.target_height
        else:
            new_width = self.target_width or current_width
            new_height = self.target_height or current_height
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _save_with_compression(self, img, output_path, output_format, original_size):
        """Lưu ảnh với các tùy chọn nén"""
        params = self._get_save_params(output_format)
        quality = self.quality
        
        # Nếu có compression_percent, tính toán target size
        target_size_kb = None
        if self.compression_percent:
            target_size_kb = (original_size * self.compression_percent / 100) / 1024
        elif self.max_size_kb:
            target_size_kb = self.max_size_kb
        
        # Nén theo target size
        if target_size_kb:
            temp_path = output_path + ".tmp"
            while quality >= 10:
                img.save(temp_path, output_format.upper(), quality=quality, **params)
                size_kb = os.path.getsize(temp_path) / 1024
                
                if size_kb <= target_size_kb:
                    os.rename(temp_path, output_path)
                    break
                quality -= 5
            else:
                # Nếu không đạt được target size, lưu với quality thấp nhất
                os.rename(temp_path, output_path)
        else:
            img.save(output_path, output_format.upper(), quality=quality, **params)
        
        return img

    def _get_save_params(self, fmt):
        """Trả về dict các params phù hợp định dạng."""
        params = {}
        fmt_lower = fmt.lower()
        
        if fmt_lower in ["jpeg", "jpg", "webp", "avif"]:
            params["optimize"] = True
        if fmt_lower == "jpeg":
            params["progressive"] = True
        if fmt_lower == "png":
            params["optimize"] = True
        if fmt_lower == "webp":
            params["method"] = 6  # Compression method (0-6)
        
        return params

    def convert_multiple(self, input_paths, output_format, output_folder=None):
        """
        Convert nhiều file ảnh được chọn
        :param input_paths: List đường dẫn các file ảnh
        :param output_format: Định dạng đích
        :param output_folder: Thư mục lưu kết quả (mặc định tạo thư mục convert cho từng file)
        :return: List kết quả cho từng file
        """
        results = []
        
        for input_path in input_paths:
            if not input_path.lower().endswith(self.input_extensions):
                results.append({
                    "success": False,
                    "input_path": input_path,
                    "error": "Định dạng file không hỗ trợ"
                })
                continue
            
            if output_folder:
                # Tạo thư mục output nếu được chỉ định
                os.makedirs(output_folder, exist_ok=True)
                filename = os.path.basename(input_path)
                base, _ = os.path.splitext(filename)
                output_path = os.path.join(output_folder, f"{base}.{output_format.lower()}")
            else:
                # Sử dụng logic mặc định (tạo thư mục convert)
                output_path = None
            
            result = self.convert(input_path, output_format, output_path)
            results.append(result)
        
        return results

    def convert_folder(self, input_folder, output_format, output_folder=None, recursive=False):
        """
        Convert toàn bộ file ảnh trong folder
        :param input_folder: Thư mục nguồn
        :param output_format: Định dạng đích
        :param output_folder: Thư mục lưu kết quả (mặc định tạo thư mục convert cho từng file)
        :param recursive: Duyệt đệ quy các thư mục con
        :return: List kết quả cho từng file
        """
        if not os.path.exists(input_folder):
            return [{"success": False, "error": f"Thư mục không tồn tại: {input_folder}"}]
        
        results = []
        
        for root, _, filenames in os.walk(input_folder):
            for filename in filenames:
                if filename.lower().endswith(self.input_extensions):
                    input_path = os.path.join(root, filename)
                    
                    if output_folder:
                        # Tạo cấu trúc thư mục tương ứng
                        rel_path = os.path.relpath(root, input_folder)
                        target_dir = os.path.join(output_folder, rel_path)
                        os.makedirs(target_dir, exist_ok=True)
                        
                        base, _ = os.path.splitext(filename)
                        output_path = os.path.join(target_dir, f"{base}.{output_format.lower()}")
                    else:
                        # Sử dụng logic mặc định (tạo thư mục convert)
                        output_path = None
                    
                    result = self.convert(input_path, output_format, output_path)
                    results.append(result)
            
            if not recursive:
                break
        
        return results

    def get_statistics(self, results):
        """Tính toán thống kê từ kết quả convert"""
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        
        if not successful:
            return {
                "total_files": len(results),
                "successful": 0,
                "failed": len(failed),
                "total_original_size": 0,
                "total_new_size": 0,
                "total_space_saved": 0,
                "total_space_increased": 0,
                "average_compression": 0,
                "compressed_files": 0,
                "expanded_files": 0,
                "unchanged_files": 0
            }
        
        total_original = sum(r["original_size"] for r in successful)
        total_new = sum(r["new_size"] for r in successful)
        
        # Tính toán theo loại thay đổi
        compressed_files = [r for r in successful if r.get("change_type") == "compressed"]
        expanded_files = [r for r in successful if r.get("change_type") == "expanded"]
        unchanged_files = [r for r in successful if r.get("change_type") == "unchanged"]
        
        total_space_saved = sum(r.get("space_change", 0) for r in compressed_files)
        total_space_increased = sum(r.get("space_change", 0) for r in expanded_files)
        
        # Tính compression ratio trung bình (chỉ cho files được nén)
        if compressed_files:
            avg_compression = sum(r["compression_ratio"] for r in compressed_files) / len(compressed_files)
        else:
            avg_compression = 0
        
        return {
            "total_files": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "total_original_size": total_original,
            "total_new_size": total_new,
            "total_space_saved": total_space_saved,
            "total_space_increased": total_space_increased,
            "average_compression": avg_compression,
            "compressed_files": len(compressed_files),
            "expanded_files": len(expanded_files),
            "unchanged_files": len(unchanged_files)
        }

    def print_statistics(self, results):
        """In thống kê ra màn hình"""
        stats = self.get_statistics(results)
        
        print(f"\n{'='*60}")
        print(f"KẾT QUẢ CHUYỂN ĐỔI")
        print(f"{'='*60}")
        print(f"Tổng số file: {stats['total_files']}")
        print(f"Thành công: {stats['successful']}")
        print(f"Thất bại: {stats['failed']}")
        
        if stats['successful'] > 0:
            print(f"\n📊 THỐNG KÊ KÍCH THƯỚC:")
            print(f"Dung lượng gốc: {stats['total_original_size']/1024:.2f} KB")
            print(f"Dung lượng mới: {stats['total_new_size']/1024:.2f} KB")
            
            # Hiển thị thông tin về compression/expansion
            if stats['compressed_files'] > 0:
                print(f"📉 Files được nén: {stats['compressed_files']}")
                print(f"💾 Tiết kiệm: {stats['total_space_saved']/1024:.2f} KB")
                print(f"📊 Tỷ lệ nén trung bình: {stats['average_compression']:.2f}%")
            
            if stats['expanded_files'] > 0:
                print(f"📈 Files tăng kích thước: {stats['expanded_files']}")
                print(f"📈 Tăng thêm: {stats['total_space_increased']/1024:.2f} KB")
            
            if stats['unchanged_files'] > 0:
                print(f"➡️ Files không thay đổi: {stats['unchanged_files']}")
            
            # Tổng kết
            net_change = stats['total_space_saved'] - stats['total_space_increased']
            if net_change > 0:
                print(f"\n✅ TỔNG KẾT: Tiết kiệm {net_change/1024:.2f} KB")
            elif net_change < 0:
                print(f"\n⚠️ TỔNG KẾT: Tăng thêm {abs(net_change)/1024:.2f} KB")
            else:
                print(f"\n➡️ TỔNG KẾT: Không thay đổi dung lượng")
        
        # In chi tiết file thất bại
        failed_results = [r for r in results if not r.get("success")]
        if failed_results:
            print(f"\n{'='*40}")
            print("❌ CHI TIẾT FILE THẤT BẠI:")
            print(f"{'='*40}")
            for result in failed_results:
                print(f"❌ {result.get('input_path', 'Unknown')}: {result.get('error', 'Unknown error')}")


# Ví dụ sử dụng
def main():
    # Ví dụ 1: Nén ảnh xuống 50% kích thước gốc
    converter1 = ImageFormatConverter(compression_percent=50, quality=85)
    
    # Ví dụ 2: Nén ảnh xuống dưới 500KB
    converter2 = ImageFormatConverter(max_size_kb=500, quality=90)
    
    # Ví dụ 3: Resize ảnh về 800x600 và nén xuống 70%
    converter3 = ImageFormatConverter(
        compression_percent=70,
        target_width=800,
        target_height=600,
        maintain_aspect_ratio=True
    )
    
    # Convert một file
    # result = converter1.convert("input.jpg", "webp", "output.webp")
    # print(result)
    
    # Convert nhiều file được chọn
    # files = ["image1.jpg", "image2.png", "image3.webp"]
    # results = converter2.convert_multiple(files, "avif", "output_folder")
    # converter2.print_statistics(results)
    
    # Convert cả thư mục
    # results = converter3.convert_folder("input_folder", "jpeg", "output_folder", recursive=True)
    # converter3.print_statistics(results)

if __name__ == "__main__":
    main()