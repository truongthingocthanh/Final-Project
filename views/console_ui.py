import os
import re  
from services.quan_ly_bai_xe import QuanLyBaiXe

class MauSac:
    DO = '\033[91m'      
    XANH_LA = '\033[92m' 
    VANG = '\033[93m'    
    XANH_DUONG = '\033[94m' 
    RESET = '\033[0m'

class GiaoDienConsole:
    def __init__(self):
        self.service = QuanLyBaiXe()

    def xoa_man_hinh(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def hien_thi_menu(self):
        while True:
            print(f"\n{MauSac.XANH_DUONG}" + "="*50)
            print(f"{MauSac.VANG} HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE - ĐỀ TÀI 10{MauSac.XANH_DUONG}")
            print("="*50 + MauSac.RESET)
            print("1. Nhận xe vào bãi (Check-in)")
            print("2. Trả xe xuất bãi & Tính tiền (Check-out)")
            print("3. Hiển thị danh sách xe đang gửi và xắp sếp xe")
            print("4. Tìm kiếm xe theo Mã vé / Biển số")
            print("5. Sửa thông tin phương tiện")
            print("6. [GIAO DỊCH] Gia hạn vé tháng & Áp mã giảm giá")
            print("7. Xem báo cáo thống kê doanh thu")
            print("8. Xuất file báo cáo doanh thu (CSV)")
            print("0. Thoát hệ thống")
            print(f"{MauSac.XANH_DUONG}" + "="*50 + MauSac.RESET)
            
            chon = input(f"{MauSac.VANG}Chọn chức năng hành động: {MauSac.RESET}")
            
            try:
                if chon == "1": self.xu_ly_check_in()
                elif chon == "2": self.xu_ly_check_out()
                elif chon == "3": self.xu_ly_hien_thi_danh_sach()
                elif chon == "4": self.xu_ly_tim_kiem()
                elif chon == "5": self.xu_ly_su_thong_tin()
                elif chon == "6": self.xu_ly_giao_dich_gia_han()
                elif chon == "7": self.xu_ly_thong_ke()
                elif chon == "8": self.xu_ly_xuat_csv()
                elif chon == "0":
                    print("\nTạm biệt! hẹn gặp lại!")
                    break
                else:
                    print("⚠️ Lựa chọn không đúng, mời nhập lại.")
            except Exception as e:
                print(f"❌ Lỗi hệ thống: {e}")
            
            input("\nNhấn Enter để tiếp tục...")
            self.xoa_man_hinh()

    def in_danh_sach_xe_dang_bang(self, danh_sach):
        if not danh_sach:
            print(f"{MauSac.DO}❌ Hiện tại bãi xe trống!{MauSac.RESET}")
            return
        
        # In tiêu đề bảng với màu Xanh Dương
        print(f"{MauSac.XANH_DUONG}{'STT':<5}{'Mã Vé':<10}{'Loại Xe':<10}{'Biển Số':<15}{'Loại Vé':<10}{'Hạn Vé Tháng':<15}{'Thời Gian Vào':<20}")
        print("-" * 85 + MauSac.RESET)
        
        # In dữ liệu
        for idx, xe in enumerate(danh_sach, 1):
            han_ve = self.service.luu_tru_service.lay_han_the_thang(xe.get_ma_ve()) if xe.get_loai_ve() == "Tháng" else "N/A"
            print(f"{MauSac.XANH_LA}{idx:<5}{xe.get_ma_ve():<10}{xe.__class__.__name__:<10}{xe.get_bien_so():<15}{xe.get_loai_ve():<10}{han_ve:<15}{xe.get_thoi_gian_vao().strftime('%Y-%m-%d %H:%M:%S'):<20}{MauSac.RESET}")

    def xu_ly_check_in(self):
        print("\n--- NHẬN XE VÀO BÃI ---")
        print("1. Xe Đạp | 2. Xe Máy | 3. Ô Tô")
        
        # 1. CHỌN LOẠI XE
        chon_xe = input("Chọn loại xe: ").strip()
        if chon_xe not in ['1', '2', '3']:
            print(f"{MauSac.DO}❌ Lựa chọn loại xe không hợp lệ! Vui lòng nhập 1, 2 hoặc 3.{MauSac.RESET}")
            return
            
        # 2. KIỂM TRA ĐỊNH DẠNG MÃ VÉ
        while True:
            ma_ve = input("Nhập mã số vé xe: ").strip()
            if not ma_ve:
                print(f"{MauSac.DO}❌ Mã vé không được để trống!{MauSac.RESET}")
                continue
                
            # Kiểm tra bằng Regular Expression (re.match)
            if chon_xe == '1' and not re.match(r'^B\d+$', ma_ve.upper()):
                print(f"{MauSac.DO}❌ Mã vé Xe Đạp phải bắt đầu bằng chữ 'B' và theo sau là số (VD: B01, B123).{MauSac.RESET}")
                continue
            elif chon_xe == '2' and not re.match(r'^M\d+$', ma_ve.upper()):
                print(f"{MauSac.DO}❌ Mã vé Xe Máy phải bắt đầu bằng chữ 'M' và theo sau là số (VD: M01, M123).{MauSac.RESET}")
                continue
            elif chon_xe == '3' and not re.match(r'^C\d+$', ma_ve.upper()):
                print(f"{MauSac.DO}❌ Mã vé Ô Tô phải bắt đầu bằng chữ 'C' và theo sau là số (VD: C01, C123).{MauSac.RESET}")
                continue
                
            ma_ve = ma_ve.upper() # Chuẩn hóa in hoa toàn bộ mã vé
            break # Định dạng đúng -> Thoát vòng lặp hỏi mã vé

        # 3. KIỂM TRA ĐỊNH DẠNG BIỂN SỐ
        if chon_xe == '1':
            bien_so = "Không có" # Xe đạp không cần biển số
        else:
            while True:
                bien_so = input("Nhập biển số (VD: 75AB12345): ").strip()
                
                # Loại bỏ khoảng trắng hoặc dấu gạch ngang (nếu người dùng lỡ nhập) để dễ kiểm tra
                bien_so_clean = bien_so.replace("-", "").replace(".", "").replace(" ", "").upper()
                
                # Rule: 2 số (\d{2}) + 2 chữ ([A-Z]{2}) + 5 số (\d{5})
                if not re.match(r'^\d{2}[A-Z]{2}\d{5}$', bien_so_clean):
                    print(f"{MauSac.DO}❌ Biển số sai định dạng! Yêu cầu: 2 Số + 2 Chữ cái + 5 Số (VD: 75AB12345).{MauSac.RESET}")
                    continue
                
                bien_so = bien_so.upper() # Chuẩn hóa biển số in hoa
                break # Định dạng đúng -> Thoát vòng lặp hỏi biển số

        # 4. CHỌN LOẠI VÉ VÀ ĐẨY VÀO SERVICE
        while True:
            loai_ve_input = input("Loại vé (1. Lượt | 2. Tháng): ").strip()
            if loai_ve_input not in ['1', '2']:
                print(f"{MauSac.DO}❌ Loại vé không hợp lệ! Vui lòng nhập 1 hoặc 2.{MauSac.RESET}")
                continue
            loai_ve_str = "Lượt" if loai_ve_input == '1' else "Tháng"
            break
            
        try:
            thanh_cong, thong_bao = self.service.check_in(chon_xe, ma_ve, bien_so, loai_ve_str)
            
            if thanh_cong:
                print(f"{MauSac.XANH_LA}✅ {thong_bao}{MauSac.RESET}")
            else:
                print(f"{MauSac.DO}❌ Thất bại: {thong_bao}{MauSac.RESET}")
        except Exception as e:
            print(f"{MauSac.DO}❌ Lỗi hệ thống: {str(e)}{MauSac.RESET}")
        
    def xu_ly_check_out(self):
        ma_ve = input("\nNhập mã vé xuất bãi: ").strip()
        thanh_cong, ket_qua = self.service.check_out(ma_ve)
        if thanh_cong:
            print("\n" + "*"*30 + "\n   HÓA ĐƠN XUẤT BÃI\n" + "*"*30)
            print(f"Biển số: {ket_qua['bien_so']}\nLoại vé: {ket_qua['loai_ve']}\nThành tiền: {ket_qua['phi']:,} VND\n" + "*"*30)
        else: print(f"❌ {ket_qua}")

    def xu_ly_hien_thi_danh_sach(self):
        giam_dan = False if input("Sắp xếp (1. Mới vào trước | 2. Cũ vào trước): ").strip() == "2" else True
        self.in_danh_sach_xe_dang_bang(self.service.lay_danh_sach_sap_xep(giam_dan))

    def xu_ly_tim_kiem(self):
        tu_khoa = input("Nhập từ khóa tìm kiếm: ").strip()
        self.in_danh_sach_xe_dang_bang(self.service.tim_kiem_xe(tu_khoa))

    def xu_ly_sua_thong_tin(self):
        ma_ve = input("Nhập mã vé cần sửa: ").strip()
        bien_so_moi = input("Biển số mới (Bỏ trống nếu không đổi): ").strip()
        nhap_ve = input("Loại vé mới (1. Lượt | 2. Tháng | Bỏ trống nếu không đổi): ").strip()
        loai_ve_moi = "Lượt" if nhap_ve == "1" else ("Tháng" if nhap_ve == "2" else None)
        thanh_cong, thong_bao = self.service.cap_nhat_thong_tin(ma_ve, bien_so_moi, loai_ve_moi)
        print(f" {'✅' if thanh_cong else '❌'} {thong_bao}")

    def xu_ly_giao_dich_gia_han(self):
        print("\n--- GIAO DỊCH GIA HẠN THẺ THÁNG ---")
        ma_ve = input("Nhập mã vé xe cần gia hạn: ").strip()
        print("Mã ưu đãi gợi ý: GIAM20 (Giảm 20%) | SVKHOADD (Giảm 50% cho sinh viên)")
        ma_giam_gia = input("Nhập mã giảm giá (Nếu có): ").strip()

        thanh_cong, ket_qua = self.service.gia_han_the_thang_giao_dich(ma_ve, ma_giam_gia)
        if thanh_cong:
            print("\n" + "$"*35)
            print("   HÓA ĐƠN GIAO DỊCH GIA HẠN THẺ")
            print("$"*35)
            print(f"Mã Vé:          {ket_qua['ma_ve']}")
            print(f"Loại phương tiện:{ket_qua['loai_xe']}")
            print(f"Giá niêm yết:   {ket_qua['gia_goc']:,} VND")
            print(f"Số tiền giảm:   -{ket_qua['giam_gia']:,} VND")
            print(f"TỔNG THANH TOÁN: {ket_qua['tong_tien']:,} VND")
            print(f"Hạn dùng mới:   {ket_qua['han_moi']}")
            print("$"*35)
        else:
            print(f"❌ Thất bại: {ket_qua}")

    def xu_ly_thong_ke(self):
        data = self.service.thong_ke_service.tinh_doanh_thu()
        print(f"\n💰 Tổng doanh thu bãi: {data['TongDoanhThu']:,} VND\n🚲 Xe Đạp: {data['XeDap']} lượt | 🏍️ Xe Máy: {data['XeMay']} lượt | 🚗 Ô Tô: {data['OTo']} lượt")

    def xu_ly_xuat_csv(self):
        thanh_cong, thong_bao = self.service.thong_ke_service.xuat_bao_cao_csv()
        print(f" {'✅' if thanh_cong else '❌'} {thong_bao}")