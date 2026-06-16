from abc import ABC, abstractmethod
from datetime import datetime

class PhuongTien(ABC):
    def __init__(self, ma_ve, bien_so, loai_ve="Lượt"):
        # Chuyển thành Private __attribute
        self.__ma_ve = ma_ve
        self.__bien_so = bien_so
        self.__loai_ve = loai_ve  
        self.__thoi_gian_vao = datetime.now() 

    # --- GETTERS ---
    def get_ma_ve(self): return self.__ma_ve
    def get_bien_so(self): return self.__bien_so
    def get_loai_ve(self): return self.__loai_ve
    def get_thoi_gian_vao(self): return self.__thoi_gian_vao

    # --- SETTERS (kiểm tra tính hợp lệ) ---
    def set_bien_so(self, bien_so_moi):
        if not bien_so_moi or bien_so_moi.strip() == "":
            raise ValueError("Biển số xe không được để trống!")
        self.__bien_so = bien_so_moi.strip()

    def set_loai_ve(self, loai_ve_moi):
        if loai_ve_moi not in ["Lượt", "Tháng"]:
            raise ValueError("Loại vé phải là 'Lượt' hoặc 'Tháng'!")
        self.__loai_ve = loai_ve_moi

    @abstractmethod
    def tinh_phi_gui(self, thoi_gian_ra):
        pass

class XeDap(PhuongTien):
    def tinh_phi_gui(self, thoi_gian_ra):
        if self.get_loai_ve() == "Tháng": return 0 
        return 2000   

class XeMay(PhuongTien):
    def tinh_phi_gui(self, thoi_gian_ra):
        if self.get_loai_ve() == "Tháng": return 0
        return 5000   

class OTo(PhuongTien):
    def tinh_phi_gui(self, thoi_gian_ra):
        if self.get_loai_ve() == "Tháng": return 0
        
        thoi_gian_gui = thoi_gian_ra - self.get_thoi_gian_vao()
        so_giay = thoi_gian_gui.total_seconds()
        so_gio = max(1, int(so_giay)) 
        
        return 20000 + (so_gio - 1) * 10000