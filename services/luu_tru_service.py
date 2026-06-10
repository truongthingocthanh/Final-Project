import sqlite3
import os
from datetime import datetime
from models.phuong_tien import XeDap, XeMay, OTo

class LuuTruService:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join("data", "bai_xe.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.khoi_tao_database()

    def ket_noi(self):
        return sqlite3.connect(self.db_path)

    def khoi_tao_database(self):
        """Tạo các bảng dữ liệu nếu chưa tồn tại"""
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            # Bảng lưu xe đang có trong bãi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS xe_trong_bai (
                    ma_ve TEXT PRIMARY KEY,
                    class TEXT,
                    bien_so TEXT,
                    loai_ve TEXT,
                    thoi_gian_vao TEXT
                )
            ''')
            # Bảng lưu hạn thẻ tháng (Phục vụ Transaction Logic)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS the_thang (
                    ma_ve TEXT PRIMARY KEY,
                    ngay_het_han TEXT
                )
            ''')
            conn.commit()

    def luu_xe(self, xe):
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO xe_trong_bai (ma_ve, class, bien_so, loai_ve, thoi_gian_vao)
                VALUES (?, ?, ?, ?, ?)
            ''', (xe.get_ma_ve(), xe.__class__.__name__, xe.get_bien_so(), xe.get_loai_ve(), xe.get_thoi_gian_vao().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def xoa_xe(self, ma_ve):
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM xe_trong_bai WHERE ma_ve = ?', (ma_ve,))
            conn.commit()

    def cap_nhat_xe(self, xe):
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE xe_trong_bai 
                SET bien_so = ?, loai_ve = ? 
                WHERE ma_ve = ?
            ''', (xe.get_bien_so(), xe.get_loai_ve(), xe.get_ma_ve()))
            conn.commit()

    def tai_danh_sach_xe(self):
        """Đọc toàn bộ xe từ Database lên bộ nhớ khi bật app"""
        danh_sach_xe = []
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ma_ve, class, bien_so, loai_ve, thoi_gian_vao FROM xe_trong_bai')
            rows = cursor.fetchall()
            
            for row in rows:
                ma_ve, loai_class, bien_so, loai_ve, tg_vao_str = row
                if loai_class == "XeDap":
                    xe = XeDap(ma_ve, bien_so, loai_ve)
                elif loai_class == "XeMay":
                    xe = XeMay(ma_ve, bien_so, loai_ve)
                elif loai_class == "OTo":
                    xe = OTo(ma_ve, bien_so, loai_ve)
                
                xe._thoi_gian_vao = datetime.strptime(tg_vao_str, "%Y-%m-%d %H:%M:%S")
                danh_sach_xe.append(xe)
        return danh_sach_xe

    # --- CÁC HÀM XỬ LÝ THẺ THÁNG (CHO TRANSACTION LOGIC) ---
    def cap_nhat_the_thang(self, ma_ve, ngay_moi_str):
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR REPLACE INTO the_thang (ma_ve, ngay_het_han) VALUES (?, ?)', (ma_ve, ngay_moi_str))
            conn.commit()

    def lay_han_the_thang(self, ma_ve):
        with self.ket_noi() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ngay_het_han FROM the_thang WHERE ma_ve = ?', (ma_ve,))
            row = cursor.fetchone()
            return row[0] if row else "Chưa đăng ký"