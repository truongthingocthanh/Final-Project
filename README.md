# 🅿️ Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking Management System)

Đây là đồ án ứng dụng Console (CLI) được xây dựng bằng Python, áp dụng triệt để Mô hình Lập trình Hướng đối tượng (OOP) nhằm quản lý quá trình ra vào và tính phí đỗ xe cho các phương tiện.

**Thông tin đồ án:**
* **Học phần:** Phương pháp Lập trình
* **Giảng viên:** TS. Trần Văn Long
* **Sinh viên thực hiện:** Ngọc Thanh
* **Git Identity:** `truongthingocthanh` (<truongthingocthanh111106@gmail.com>)

---

## 🚀 1. Giới thiệu chương trình (Topic 10)

Chương trình cho phép người dùng (nhân viên giữ xe/quản lý) thực hiện các thao tác quản lý luồng xe ra vào (Xe đạp, Xe máy, Ô tô), tự động tính toán cước phí dựa trên thời gian đỗ, phân loại vé tháng/vé lượt và xuất báo cáo thống kê doanh thu. Dữ liệu được lưu trữ an toàn qua **Cơ sở dữ liệu SQLite** và **JSON**.

---

## ⚙️ 2. Yêu cầu & Cách cài đặt

* **Yêu cầu hệ thống:** Máy tính cần cài đặt sẵn **Python 3.x**. Không yêu cầu cài đặt thêm thư viện ngoài (sử dụng thư viện chuẩn `sqlite3`, `re`, `datetime`, `csv`, `json` của Python).
* **Cách cài đặt & Chạy chương trình:**
    1. Clone kho lưu trữ này về máy:
       ```bash
       git clone [https://github.com/truongthingocthanh/Final-Project.git](https://github.com/truongthingocthanh/Final-Project.git)
       ```
    2. Mở Terminal (hoặc Command Prompt, PowerShell) tại thư mục chứa dự án.
    3. Gõ lệnh sau để khởi chạy:
       ```bash
       python main.py
       ```

---

## 📖 3. Cách sử dụng chương trình

Sau khi khởi chạy, chương trình tự động nạp dữ liệu từ `bai_xe.db` và hiển thị Bảng Menu chính gồm 9 lựa chọn. Giao diện dòng lệnh được tích hợp mã màu ANSI mang lại trải nghiệm trực quan.

1. **Nhận xe vào bãi (Check-in):** Nhập loại xe, mã vé và biển số. Hệ thống tích hợp Regex để bắt lỗi định dạng (VD: Xe máy phải bắt đầu bằng `M`, Ô tô bắt đầu bằng `C`, biển số phải đúng format `75AB12345`).
2. **Trả xe xuất bãi (Check-out):** Nhập mã vé, hệ thống tự động tính tiền dựa vào loại xe và thời gian lưu bãi, sau đó in hóa đơn.
3. **Hiển thị & Sắp xếp:** Xem danh sách xe đang đỗ dưới dạng bảng căn lề chuẩn xác. Hỗ trợ sắp xếp theo thời gian mới/cũ.
4. **Tìm kiếm:** Tra cứu trạng thái phương tiện thông qua Mã vé hoặc Từ khóa biển số.
5. **Sửa thông tin:** Cập nhật lại biển số hoặc loại vé trong trường hợp nhập sai.
6. **Giao dịch gia hạn:** Gia hạn thẻ tháng, có hỗ trợ xử lý mã giảm giá (Discount logic).
7. **Thống kê:** Xem tổng doanh thu và số lượt xe ra vào.
8. **Xuất CSV:** Kết xuất toàn bộ lịch sử giao dịch ra file `.csv` phục vụ báo cáo.

---

## 🧩 4. Cấu trúc Kiến trúc Phân tầng (Layered Architecture)

Dự án tuân thủ nguyên lý Clean Code (SRP), phân chia rõ ràng trách nhiệm của từng tầng:

* **`models/`**: Chứa các bản thiết kế đối tượng. File `phuong_tien.py` định nghĩa Abstract Class và các Subclass (XeDap, XeMay, OTo).
* **`services/`**: Xử lý logic nghiệp vụ, giao tiếp với Data.
    * `quan_ly_bai_xe.py`: Logic luồng xe ra/vào, tìm kiếm.
    * `luu_tru_service.py`: Tương tác trực tiếp với CSDL SQLite.
    * `thong_ke_service.py`: Tính toán doanh thu và File I/O (JSON/CSV).
* **`views/`**: File `console_ui.py` đảm nhận vòng lặp vô hạn vẽ menu, xử lý thao tác người dùng (try-except) và điều hướng.
* **`main.py`**: Điểm neo khởi chạy trung tâm (Entry-point).

---

## 💎 5. Thể hiện 4 Đặc trưng Hướng đối tượng (OOP)

1. **Đóng gói (Encapsulation):** Toàn bộ thuộc tính nhạy cảm (`__ma_ve`, `__bien_so`) đều là Private. Việc truy cập và chỉnh sửa được thông qua các hàm Getters/Setters có kèm logic xác thực (VD: Không cho phép đổi biển số rỗng).
2. **Kế thừa (Inheritance):** Thiết lập cấu trúc phân cấp: Lớp cha `PhuongTien` -> Lớp con `XeDap`, `XeMay`, `Oto` giúp giảm thiểu tối đa việc lặp mã nguồn.
3. **Đa hình (Polymorphism):** Lớp con ghi đè (Override) phương thức `tinh_phi_gui()` của lớp cha để có hành vi tính toán riêng biệt theo từng hệ số giá.
4. **Trừu tượng (Abstraction):** Lớp `PhuongTien` kế thừa từ `ABC` (Abstract Base Class), bắt buộc các phương tiện khai báo mới phải tuân thủ việc định nghĩa hàm tính tiền.

---

## 🏆 6. BẢNG TỰ CHẤM ĐIỂM DỰ ÁN (Dựa trên Rubric)

| Phân loại | Tiêu chí chi tiết (Detailed Criteria) | Minh chứng trong mã nguồn (Implementation Details) | Điểm tự chấm |
| :--- | :--- | :--- | :---: |
| **CƠ BẢN** | 1. Tính Đóng gói (Encapsulation) | Sử dụng `__attribute` cho các biến trong `PhuongTien`, có Setter chặn lỗi dữ liệu trống/sai định dạng. | 0.5 / 0.5 |
| | 2. Tính Kế thừa (Inheritance) | Cấu trúc Parent-Child hợp lý giữa `PhuongTien` và 3 class `XeDap`, `XeMay`, `OTo`. | 0.5 / 0.5 |
| | 3. Đa hình & Trừu tượng | Sử dụng thư viện `abc`, có `@abstractmethod` cho `tinh_phi_gui()`. Các Subclass ghi đè công thức thành công. | 1.0 / 1.0 |
| | 4. Phân tầng Kiến trúc (Layered) | Chia rõ 3 thư mục `models/`, `services/`, `views/`. Import chéo chuẩn xác, không bị circular import. | 1.0 / 1.0 |
| | 5. Clean Code (Nguyên lý SRP) | Đặt tên hàm `snake_case`, tên lớp `CamelCase`. Mỗi hàm/module đảm nhiệm đúng một chức năng. | 0.5 / 0.5 |
| | 6. Xử lý ngoại lệ (Exception Handling) | Có khối `try-except` ngoài menu, dùng `re.match` bắt lỗi nhập sai định dạng mã vé/biển số. Không crash app. | 0.5 / 0.5 |
| | 7. Nghiệp vụ Cơ bản (CRUD) | Thêm, sửa, xóa (check-out) hoạt động trơn tru. Hiển thị danh sách định dạng bảng f-string ngay ngắn. | 1.0 / 1.0 |
| | 8. Tìm kiếm & Sắp xếp | Hỗ trợ tìm kiếm theo chuỗi con và sắp xếp danh sách xe theo thời gian vào bãi (Mới nhất/Cũ nhất). | 1.0 / 1.0 |
| | 9. Lưu trữ vĩnh viễn (File I/O) | Nạp xuất dữ liệu song song qua SQLite (`bai_xe.db`) và JSON (`lich_su_do_xe.json`). | 1.0 / 1.0 |
| **NÂNG CAO**| 10. Logic Giao dịch phức tạp | Giao dịch "Gia hạn vé tháng" nhận diện thời gian, cộng dồn ngày và áp dụng mã giảm giá (`GIAM20`, `SVKHOADD`). | 1.0 / 1.0 |
| | 11. Thống kê nâng cao & Export | Nhóm dữ liệu tính tổng doanh thu theo loại xe, hỗ trợ kết xuất báo cáo chuẩn định dạng ra tệp `.csv`. | 1.0 / 1.0 |
| | 12. Công nghệ mở rộng | Sử dụng trực tiếp hệ quản trị **SQLite Database** thay cho file TXT thông thường để quản lý xe trong bãi. | 0.5 / 0.5 |
| | 13. Quản lý Git & GitHub | Kho lưu trữ Public. Có File `README.md` rõ ràng. Commit history chia nhỏ theo từng luồng tính năng. | 0.5 / 0.5 |
| **TỔNG** | | | **10.0 / 10.0** |
