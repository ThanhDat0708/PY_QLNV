# Hệ thống quản lý nhân viên

Ứng dụng desktop Python/Tkinter, dùng MySQL để lưu dữ liệu nhân viên.

## Cài đặt

1. Cài Python 3.10 trở lên và khởi động MySQL/MariaDB bằng XAMPP.
2. Tạo môi trường ảo và cài thư viện:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Mở `schema.sql` bằng HeidiSQL hoặc MySQL client để tạo database và 5 bảng.
4. Nếu database đã được tạo từ phiên bản cũ, chạy thêm `database/migrations/001_add_attendance_and_payroll_fields.sql`.
5. Chạy `database/migrations/002_calculate_net_salary.sql` để tự tính lương thực nhận.
6. Sao chép `.env.example` thành `.env`, rồi điền thông tin MySQL. Không đưa `.env` lên GitHub.
7. Chạy ứng dụng:

```powershell
python main.py
```

## Cấu trúc dữ liệu

- `phong_ban` và `chuc_vu` là danh mục được nhân viên tham chiếu.
- `nhan_vien` lưu thông tin nhân viên và liên kết đến hai danh mục trên.
- `cham_cong` và `luong` liên kết với `nhan_vien`, nên dữ liệu lịch sử bị xóa theo nhân viên.
- `cham_cong` lưu thêm số giờ làm, số giờ tăng ca và ghi chú.
- `luong` lưu đầy đủ thông tin bảng lương: ngày công, lương theo công, tăng ca,
  phụ cấp, thưởng, phạt, bảo hiểm, thuế, lương thực nhận và trạng thái.
