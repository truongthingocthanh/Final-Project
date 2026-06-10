import os
import csv
from datetime import datetime

class ThongKeService:
    def __init__(self, lich_su_path=None):
        self.lich_su_path = lich_su_path or os.path.join("data", "lich_su_do_xe.json")
        os.makedirs(os.path.dirname(self.lich_su_path), exist_ok=True)

    def luu_lich_su_giao_dich(self, thong_tin_xe_ra):
        """Lưu lại lịch sử mỗi khi có xe check-out để phục vụ thống kê doanh thu"""
        lich_su = []
        if os.path.exists(self.lich_su_path) and os.stat(self.lich_su_path).st_size > 0:
            import json
            with open(self.lich_su_path, "r", encoding="utf-8") as f:
                lich_su = json.load(f)
        
        lich_su.append(thong_tin_xe_ra)
        
        import json
        with open(self.lich_su_path, "w", encoding="utf-8") as f:
            json.dump(lich_su, f, ensure_ascii=False, indent=4)

    def tinh_doanh_thu(self):
        """Thống kê tổng tiền thu được và số lượng xe theo từng loại"""
        import json
        thong_ke = {"TongDoanhThu": 0, "XeDap": 0, "XeMay": 0, "OTo": 0}
        
        if not os.path.exists(self.lich_su_path) or os.stat(self.lich_su_path).st_size == 0:
            return thong_ke

        with open(self.lich_su_path, "r", encoding="utf-8") as f:
            lich_su = json.load(f)

        for gd in lich_su:
            thong_ke["TongDoanhThu"] += gd["phi"]
            loai_class = gd["class"]
            if loai_class in thong_ke:
                thong_ke[loai_class] += 1
        return thong_ke

    def xuat_bao_cao_csv(self):
        """Xuất toàn bộ lịch sử giao dịch ra file CSV (Mở được bằng Excel)"""
        import json
        export_path = os.path.join("data", "bao_cao_doanh_thu.csv")
        
        if not os.path.exists(self.lich_su_path) or os.stat(self.lich_su_path).st_size == 0:
            return False, "Chưa có dữ liệu lịch sử để xuất báo cáo!"

        with open(self.lich_su_path, "r", encoding="utf-8") as f:
            lich_su = json.load(f)

        try:
            with open(export_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                # Viết tiêu đề cột
                writer.writerow(["Mã Vé", "Loại Xe", "Biển Số", "Loại Vé", "Giờ Vào", "Giờ Ra", "Phí Gửi (VND)"])
                
                for gd in lich_su:
                    writer.writerow([
                        gd["ma_ve"], gd["class"], gd["bien_so"], 
                        gd["loai_ve"], gd["thoi_gian_vao"], gd["thoi_gian_ra"], gd["phi"]
                    ])
            return True, f"Xuất báo cáo thành công tại: {export_path}"
        except Exception as e:
            return False, f"Lỗi khi xuất file CSV: {e}"