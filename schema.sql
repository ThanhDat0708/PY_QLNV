CREATE DATABASE IF NOT EXISTS employee_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE employee_management;

CREATE TABLE IF NOT EXISTS phong_ban (
    ma_phong_ban INT AUTO_INCREMENT PRIMARY KEY,
    ten_phong_ban VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS chuc_vu (
    ma_chuc_vu INT AUTO_INCREMENT PRIMARY KEY,
    ten_chuc_vu VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS nhan_vien (
    ma_nhan_vien INT AUTO_INCREMENT PRIMARY KEY,
    ho_ten VARCHAR(150) NOT NULL,
    so_dien_thoai VARCHAR(30),
    email VARCHAR(150),
    ma_phong_ban INT,
    ma_chuc_vu INT,
    FOREIGN KEY (ma_phong_ban) REFERENCES phong_ban(ma_phong_ban) ON DELETE SET NULL,
    FOREIGN KEY (ma_chuc_vu) REFERENCES chuc_vu(ma_chuc_vu) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS cham_cong (
    ma_cham_cong INT AUTO_INCREMENT PRIMARY KEY,
    ma_nhan_vien INT NOT NULL,
    ngay_lam_viec DATE NOT NULL,
    gio_vao TIME,
    gio_ra TIME,
    trang_thai VARCHAR(50) NOT NULL DEFAULT 'Có mặt',
    FOREIGN KEY (ma_nhan_vien) REFERENCES nhan_vien(ma_nhan_vien) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS luong (
    ma_luong INT AUTO_INCREMENT PRIMARY KEY,
    ma_nhan_vien INT NOT NULL,
    thang CHAR(7) NOT NULL,
    luong_co_ban DECIMAL(15, 2) NOT NULL DEFAULT 0,
    tien_thuong DECIMAL(15, 2) NOT NULL DEFAULT 0,
    tong_luong DECIMAL(15, 2) GENERATED ALWAYS AS (luong_co_ban + tien_thuong) STORED,
    UNIQUE KEY duy_nhat_nhan_vien_thang (ma_nhan_vien, thang),
    FOREIGN KEY (ma_nhan_vien) REFERENCES nhan_vien(ma_nhan_vien) ON DELETE CASCADE
);
