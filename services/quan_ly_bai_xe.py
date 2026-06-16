from datetime import datetime, timedelta
from models.phuong_tien import XeDap, XeMay, OTo
from services.luu_tru_service import LuuTruService
from services.thong_ke_service import ThongKeService

class QuanLyBaiXe:
    def __init__(self):
        self.luu_tru_service = LuuTruService()
        self.thong_ke_service = ThongKeService()
        self.danh_sach_xe = self.luu_tru_service.tai_danh_sach_xe()

def check_in(self, loai_xe, ma_ve, bien_so, loai_ve):
        ma_ve = ma_ve.strip()
        
        if loai_xe == "1" and not ma_ve.upper().startswith('B'):
            return False, "Mã vé Xe đạp bắt buộc phải bắt đầu bằng chữ 'B'!"
        elif loai_xe == "2" and not ma_ve.upper().startswith('M'):
            return False, "Mã vé Xe máy bắt buộc phải bắt đầu bằng chữ 'M'!"
        elif loai_xe == "3" and not ma_ve.upper().startswith('C'):
            return False, "Mã vé Ô tô bắt buộc phải bắt đầu bằng chữ 'C'!"

        for xe in self.danh_sach_xe:
            if xe.get_ma_ve().upper() == ma_ve.upper():
                return False, "Mã vé này hiện đang được sử dụng trong bãi!"

        for xe in self.danh_sach_xe:
            if xe.get_ma_ve().upper() == ma_ve.upper():
                return False, "Mã vé này hiện đang được sử dụng trong bãi!"

        if loai_xe == "1": xe_moi = XeDap(ma_ve, "Không có", loai_ve)
        elif loai_xe == "2": xe_moi = XeMay(ma_ve, bien_so, loai_ve)
        elif loai_xe == "3": xe_moi = OTo(ma_ve, bien_so, loai_ve)
        else: return False, "Loại phương tiện sai!"

        self.danh_sach_xe.append(xe_moi)
        self.luu_tru_service.luu_xe(xe_moi) # Ghi trực tiếp vào SQLite
        
        # Nếu gửi vé tháng, tự động kích hoạt hạn 30 ngày từ hôm nay
        if loai_ve == "Tháng":
            ngay_het_han = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            self.luu_tru_service.cap_nhat_the_thang(ma_ve, ngay_het_han)

        return True, f"Xếp xe vào bãi thành công! Mã vé: {ma_ve}"

    def check_out(self, ma_ve):
        for xe in self.danh_sach_xe:
            if xe.get_ma_ve().upper() == ma_ve.upper():
                thoi_gian_ra = datetime.now()
                phi_gui = xe.tinh_phi_gui(thoi_gian_ra)
                
                thong_tin_ra = {
                    "ma_ve": xe.get_ma_ve(),
                    "class": xe.__class__.__name__,
                    "bien_so": xe.get_bien_so(),
                    "loai_ve": xe.get_loai_ve(),
                    "thoi_gian_vao": xe.get_thoi_gian_vao().strftime("%Y-%m-%d %H:%M:%S"),
                    "thoi_gian_ra": thoi_gian_ra.strftime("%Y-%m-%d %H:%M:%S"),
                    "phi": phi_gui
                }
                
                self.thong_ke_service.luu_lich_su_giao_dich(thong_tin_ra)
                self.danh_sach_xe.remove(xe) 
                self.luu_tru_service.xoa_xe(ma_ve) # Xóa khỏi SQLite     
                return True, thong_tin_ra
        return False, "Không tìm thấy mã vé này!"

    def cap_nhat_thong_tin(self, ma_ve, bien_so_moi, loai_ve_moi):
        for xe in self.danh_sach_xe:
            if xe.get_ma_ve().upper() == ma_ve.upper():
                try:
                    if xe.__class__.__name__ != "XeDap" and bien_so_moi:
                        xe.set_bien_so(bien_so_moi)
                    if loai_ve_moi:
                        xe.set_loai_ve(loai_ve_moi)
                    self.luu_tru_service.cap_nhat_xe(xe) # Cập nhật SQLite
                    return True, "Cập nhật thông tin xe thành công!"
                except ValueError as e:
                    return False, str(e)
        return False, "Không tìm thấy xe!"

    # ==========================================
    # CẢI TIẾN: NGHIỆP VỤ GIAO DỊCH PHỨC TẠP (Transaction Logic)
    # ==========================================
    def gia_han_the_thang_giao_dich(self, ma_ve, ma_giam_gia):
        """Xử lý quy trình phức tạp: Kiểm tra xe -> Tính giá -> Áp mã -> Kéo dài hạn -> Xuất hóa đơn"""
        xe_tim_thay = None
        for xe in self.danh_sach_xe:
            if xe.get_ma_ve().upper() == ma_ve.upper():
                xe_tim_thay = xe
                break
        
        if not xe_tim_thay:
            return False, "Không tìm thấy phương tiện đang ở trong bãi để gia hạn!"
            
        if xe_tim_thay.get_loai_ve() != "Tháng":
            return False, "Xe này đang gửi theo lượt, cần đổi sang loại Vé Tháng trước!"

        # 1. Định giá gốc theo loại xe
        loai_xe = xe_tim_thay.__class__.__name__
        gia_goc = 50000 if loai_xe == "XeDap" else (100000 if loai_xe == "XeMay" else 500000)
        
        # 2. Xử lý mã giảm giá phức tạp
        giam_gia = 0
        ma_giam_gia = ma_giam_gia.strip().upper()
        if ma_giam_gia == "GIAM20":
            giam_gia = int(gia_goc * 0.20)
        elif ma_giam_gia == "SVKHOADD": # Ưu đãi sinh viên
            giam_gia = int(gia_goc * 0.50)

        tong_tien = gia_goc - giam_gia

        # 3. Tiến hành cập nhật ngày gia hạn mới vào SQLite (Cộng thêm 30 ngày)
        han_cu_str = self.luu_tru_service.lay_han_the_thang(ma_ve)
        try:
            ngay_goc = datetime.strptime(han_cu_str, "%Y-%m-%d")
            if ngay_goc < datetime.now(): ngay_goc = datetime.now()
        except:
            ngay_goc = datetime.now()
            
        han_moi = (ngay_goc + timedelta(days=30)).strftime("%Y-%m-%d")
        self.luu_tru_service.cap_nhat_the_thang(ma_ve, han_moi)

        # 4. Ghi nhận doanh thu vào file thống kê lịch sử chung
        thong_tin_hoa_don = {
            "ma_ve": ma_ve,
            "class": loai_xe,
            "bien_so": xe_tim_thay.get_bien_so(),
            "loai_ve": "Gia Hạn Thẻ Tháng",
            "thoi_gian_vao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "thoi_gian_ra": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "phi": tong_tien
        }
        self.thong_ke_service.luu_lich_su_giao_dich(thong_tin_hoa_don)

        # Trả về kết quả hóa đơn giao dịch thành công
        hoa_don = {
            "ma_ve": ma_ve,
            "loai_xe": loai_xe,
            "gia_goc": gia_goc,
            "giam_gia": giam_gia,
            "tong_tien": tong_tien,
            "han_moi": han_moi
        }
        return True, hoa_don

    def tim_kiem_xe(self, tu_khoa):
        return [xe for xe in self.danh_sach_xe if tu_khoa.strip().lower() in xe.get_ma_ve().lower() or tu_khoa.strip().lower() in xe.get_bien_so().lower()]

    def lay_danh_sach_sap_xep(self, giam_dan=True):
        return sorted(self.danh_sach_xe, key=lambda x: x.get_thoi_gian_vao(), reverse=giam_dan)