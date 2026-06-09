from services.quan_ly_bai_xe import QuanLyBaiXe

class GiaoDienConsole:
    def __init__(self):
        self.he_thong = QuanLyBaiXe()

    def hien_thi_menu(self):
        while True:
            print("\n=============================================")
            print("   HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE THÔNG MINH     ")
            print("=============================================")
            print("1. Xe VÀO bãi (Check-in)")
            print("2. Xe RA bãi (Check-out & Tính tiền)")
            print("3. Hiển thị danh sách xe đang gửi")
            print("4. Thoát chương trình")
            print("---------------------------------------------")
            
            # Xử lý ngoại lệ (try-except) chặn lỗi nhập liệu cơ bản của người dùng
            try:
                lua_chon = input("Nhập lựa chọn của bạn (1-4): ").strip()
                
                if lua_chon == "1":
                    print("\n--- CHỨC NĂNG XE VÀO BÃI ---")
                    print("Chọn loại phương tiện:")
                    print("1. Xe Đạp  | 2. Xe Máy  | 3. Ô Tô")
                    loai_xe = input("Lựa chọn (1-3): ").strip()
                    
                    ma_ve = input("Nhập mã vé xe: ").strip()
                    
                    bien_so = ""
                    if loai_xe != "1":
                        bien_so = input("Nhập biển số xe: ").strip()
                        
                    print("Chọn loại vé (1: Vé lượt | 2: Vé tháng): ")
                    chon_ve = input("Lựa chọn (1-2): ").strip()
                    loai_ve = "Tháng" if chon_ve == "2" else "Lượt"
                    
                    thanh_cong, thong_bao = self.he_thong.check_in(loai_xe, ma_ve, bien_so, loai_ve)
                    print(f"-> Kết quả: {thong_bao}")

                elif lua_chon == "2":
                    print("\n--- CHỨC NĂNG XE RA BÃI & TÍNH TIỀN ---")
                    ma_ve_ra = input("Nhập mã vé xe cần thanh toán: ").strip()
                    
                    thanh_cong, ket_qua = self.he_thong.check_out(ma_ve_ra)
                    
                    if thanh_cong:
                        print("\n=========================================")
                        print("          HÓA ĐƠN THANH TOÁN             ")
                        print("=========================================")
                        print(f" Biển số xe: {ket_qua['bien_so']}")
                        print(f" Loại vé:    {ket_qua['loai_ve']}")
                        print(f" THÀNH TIỀN: {ket_qua['phi']:,} VNĐ")
                        print("=========================================")
                        print("-> Cho xe xuất bến an toàn!")
                    else:
                        print(f"-> Thất bại: {ket_qua}")

                elif lua_chon == "3":
                    danh_sach = self.he_thong.lay_danh_sach()
                    if not danh_sach:
                        print("\n-> Bãi xe hiện đang trống rỗng.")
                    else:
                        print("\n=========================================================================")
                        print(f"{'DANH SÁCH PHƯƠNG TIỆN HIỆN CÓ TRONG BÃI':^70}")
                        print("=========================================================================")
                        print(f"{'Mã Vé':<10} | {'Biển Số':<15} | {'Loại Xe':<12} | {'Loại Vé':<10}")
                        print("-------------------------------------------------------------------------")
                        for xe in danh_sach:
                            print(f"{xe.get_ma_ve():<10} | {xe.get_bien_so():<15} | {xe.__class__.__name__:<12} | {xe.get_loai_ve():<10}")
                        print("=========================================================================")

                elif lua_chon == "4":
                    print("\n[Hệ thống] Đang đồng bộ dữ liệu và đóng bãi xe. Tạm biệt!")
                    break
                    
                else:
                    print("-> Lỗi: Lựa chọn không hợp lệ từ 1 đến 4. Vui lòng nhập lại!")
                    
            except Exception as e:
                print(f"-> Đã xảy ra lỗi hệ thống: {e}. Vui lòng thử lại!")