import json
import os
from datetime import datetime
from models.phuong_tien import XeDap, XeMay, OTo

class QuanLyBaiXe:
    def __init__(self):
        self.danh_sach_xe = []
        self.file_path = os.path.join("data", "bai_xe.json")
        self.doc_du_lieu_json()

    def check_in(self, loai_xe, ma_ve, bien_so, loai_ve):
        for xe in self.danh_sach_xe:
            if xe.get_ma_ve() == ma_ve:
                return False, "Mã vé này hiện đang được sử dụng trong bãi!"
            if bien_so and loai_xe != "1" and xe.get_bien_so() == bien_so:
                return False, f"Xe có biển số {bien_so} hiện đã ở trong bãi rồi!"

        if loai_xe == "1":
            xe_moi = XeDap(ma_ve, "Không có", loai_ve)
        elif loai_xe == "2":
            xe_moi = XeMay(ma_ve, bien_so, loai_ve)
        elif loai_xe == "3":
            xe_moi = OTo(ma_ve, bien_so, loai_ve)
        else:
            return False, "Loại phương tiện không hợp lệ!"

        self.danh_sach_xe.append(xe_moi)
        self.luu_du_lieu_json()
        return True, f"Xếp xe vào bãi thành công! Mã vé: {ma_ve}"

    def check_out(self, ma_ve):
        for xe in self.danh_sach_xe:
            if xe.get_ma_ve() == ma_ve:
                thoi_gian_ra = datetime.now()
                phi_gui = xe.tinh_phi_gui(thoi_gian_ra)
                
                thong_tin_ra = {
                    "bien_so": xe.get_bien_so(),
                    "loai_ve": xe.get_loai_ve(),
                    "phi": phi_gui
                }
                
                self.danh_sach_xe.remove(xe) 
                self.luu_du_lieu_json()      
                return True, thong_tin_ra
                
        return False, "Không tìm thấy xe nào tương ứng với mã vé này!"

    def lay_danh_sach(self):
        return self.danh_sach_xe

    # ==========================================
    # LOGIC LƯU TRỮ FILE VĨNH VIỄN (FILE I/O)
    # ==========================================
    def luu_du_lieu_json(self):
        data_to_save = []
        for xe in self.danh_sach_xe:
            data_to_save.append({
                "class": xe.__class__.__name__,
                "ma_ve": xe.get_ma_ve(),
                "bien_so": xe.get_bien_so(),
                "loai_ve": xe.get_loai_ve(),
                "thoi_gian_vao": xe.get_thoi_gian_vao().strftime("%Y-%m-%d %H:%M:%S")
            })
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    def doc_du_lieu_json(self):
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data_loaded = json.load(f)
                
            for item in data_loaded:
                if item["class"] == "XeDap":
                    xe = XeDap(item["ma_ve"], item["bien_so"], item["loai_ve"])
                elif item["class"] == "XeMay":
                    xe = XeMay(item["ma_ve"], item["bien_so"], item["loai_ve"])
                elif item["class"] == "OTo":
                    xe = OTo(item["ma_ve"], item["bien_so"], item["loai_ve"])
                
                xe._thoi_gian_vao = datetime.strptime(item["thoi_gian_vao"], "%Y-%m-%d %H:%M:%S")
                self.danh_sach_xe.append(xe)
        except Exception as e:
            print(f"Lỗi tự động nạp dữ liệu: {e}")