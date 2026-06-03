# Import tầng giao diện vào file chính
from views.console_ui import GiaoDienConsole

if __name__ == "__main__":
    # Khởi tạo giao diện người dùng
    app = GiaoDienConsole()
    
    # Kích hoạt vòng lặp ứng dụng hoạt động
    app.hien_thi_menu()