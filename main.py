from services.quan_ly_bai_xe import QuanLyBaiXe

if __name__ == "__main__":
    print("--- BẮT ĐẦU KIỂM THỬ TẦNG SERVICES ---")
    
    # Khởi tạo bộ não quản lý bãi xe
    he_thong = QuanLyBaiXe()
    
    # 1. Thử đưa 1 xe máy và 1 ô tô vào bãi (Check-in)
    print("\n[Thử nghiệm Check-in]")
    ok1, msg1 = he_thong.check_in(loai_xe="2", ma_ve="V01", bien_so="75F1-1234", loai_ve="Lượt")
    print(msg1)
    
    ok2, msg2 = he_thong.check_in(loai_xe="3", ma_ve="V02", bien_so="75A-5555", loai_ve="Tháng")
    print(msg2)
    
    # 2. Thử cho xe máy ra bãi (Check-out) xem có tính tiền được không
    print("\n[Thử nghiệm Check-out xe máy V01]")
    thanh_cong, ket_qua = he_thong.check_out("V01")
    if thanh_cong:
        print(f"Xe ra thành công! Biển số: {ket_qua['bien_so']} | Phí gửi: {ket_qua['phi']} VNĐ")
    else:
        print(ket_qua)