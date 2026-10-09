USE employee_management;

CREATE TABLE IF NOT EXISTS nguoi_dung (
    ma_nguoi_dung INT AUTO_INCREMENT PRIMARY KEY,
    ten_dang_nhap VARCHAR(50) NOT NULL UNIQUE,
    mat_khau_hash VARBINARY(32) NOT NULL,
    salt VARBINARY(16) NOT NULL,
    ho_ten VARCHAR(100) NOT NULL,
    vai_tro VARCHAR(20) NOT NULL DEFAULT 'user',
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'Hoat dong',
    ngay_tao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
