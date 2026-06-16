import os
from services.quan_ly_bai_xe import QuanLyBaiXe

class GiaoDienConsole:
    def __init__(self):
        self.service = QuanLyBaiXe()

    def xoa_man_hinh(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def hien_thi_menu(self):
        while True:
            print("\n" + "="*50)
            print(" HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE - ĐỀ TÀI 10")
            print("="*50)
            print("1. Nhận xe vào bãi (Check-in)")
            print("2. Trả xe xuất bãi & Tính tiền (Check-out)")
            print("3. Hiển thị danh sách xe đang gửi và xắp sếp xe")
            print("4. Tìm kiếm xe theo Mã vé / Biển số")
            print("5. Sửa thông tin phương tiện")
            print("6. [GIAO DỊCH] Gia hạn vé tháng & Áp mã giảm giá")
            print("7. Xem báo cáo thống kê doanh thu")
            print("8. Xuất file báo cáo doanh thu (CSV)")
            print("0. Thoát hệ thống")
            print("="*50)
            
            chon = input("Chọn chức năng hành động (0-8): ").strip()
            
            try:
                if chon == "1": self.xu_ly_check_in()
                elif chon == "2": self.xu_ly_check_out()
                elif chon == "3": self.xu_ly_hien_thi_danh_sach()
                elif chon == "4": self.xu_ly_tim_kiem()
                elif chon == "5": self.xu_ly_sua_thong_tin()
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
            print("❌ Hiện tại bãi xe trống!")
            return
        print(f"{'STT':<5}{'Mã Vé':<10}{'Loại Xe':<10}{'Biển Số':<15}{'Loại Vé':<10}{'Hạn Vé Tháng':<15}{'Thời Gian Vào':<20}")
        print("-" * 85)
        for idx, xe in enumerate(danh_sach, 1):
            han_ve = self.service.luu_tru_service.lay_han_the_thang(xe.get_ma_ve()) if xe.get_loai_ve() == "Tháng" else "N/A"
            print(f"{idx:<5}{xe.get_ma_ve():<10}{xe.__class__.__name__:<10}{xe.get_bien_so():<15}{xe.get_loai_ve():<10}{han_ve:<15}{xe.get_thoi_gian_vao().strftime('%Y-%m-%d %H:%M:%S'):<20}")

    def xu_ly_check_in(self):
        print("\n--- NHẬN XE VÀO BÃI ---")
        print("1. Xe Đạp | 2. Xe Máy | 3. Ô Tô")
        loai_xe = input("Chọn loại xe: ").strip()
        ma_ve = input("Nhập mã số vé xe: ").strip()
        bien_so = "Không có" if loai_xe == "1" else input("Nhập biển số: ").strip()
        loai_ve = "Tháng" if input("Loại vé (1. Lượt | 2. Tháng): ").strip() == "2" else "Lượt"

        thanh_cong, thong_bao = self.service.check_in(loai_xe, ma_ve, bien_so, loai_ve)
        print(f" {'✅' if thanh_cong else '❌'} {thong_bao}")

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