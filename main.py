from models.phuong_tien import XeMay, OTo
from datetime import datetime
import time

if __name__ == "__main__":
    print("--- BẮT ĐẦU KIỂM THỬ TẦNG MODELS ---")
    
    # 1. Thử tạo một chiếc xe máy vé lượt
    xe_may_cua_thanh = XeMay("M01", "73A-12345", "Lượt")
    print(f"Xe máy vào bãi lúc: {xe_may_cua_thanh.get_thoi_gian_vao()}")
    
    # Giả lập thời gian trôi qua 2 giây để test ô tô tính tiền theo thời gian
    print("Chờ 2 giây để giả lập ô tô đỗ xe...")
    time.sleep(2)
    
    # 2. Thử tạo một chiếc ô tô vé lượt
    oto_cua_thay_long = OTo("O01", "75A-99999", "Lượt")
    thoi_gian_ra_ao = datetime.now()
    
    # Kiểm tra tính Đa hình: Gọi cùng 1 hàm nhưng tính tiền khác nhau
    print(f"Phí gửi xe máy (Cố định): {xe_may_cua_thanh.tinh_phi_gui(thoi_gian_ra_ao)} VNĐ")
    print(f"Phí gửi ô tô (Theo giờ - Đã chờ 2s): {oto_cua_thay_long.tinh_phi_gui(thoi_gian_ra_ao)} VNĐ")