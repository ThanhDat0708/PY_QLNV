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
4. Sao chép `.env.example` thành `.env`, rồi điền thông tin MySQL. Không đưa `.env` lên GitHub.
5. Chạy ứng dụng:

```powershell
python main.py
```

## Cấu trúc dữ liệu

- `phong_ban` và `chuc_vu` là danh mục được nhân viên tham chiếu.
- `nhan_vien` lưu thông tin nhân viên và liên kết đến hai danh mục trên.
- `cham_cong` và `luong` liên kết với `nhan_vien`, nên dữ liệu lịch sử bị xóa theo nhân viên.
- `luong.tong_luong` được MySQL tự tính bằng lương cơ bản cộng thưởng.

