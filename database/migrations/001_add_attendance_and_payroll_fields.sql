USE employee_management;

ALTER TABLE cham_cong
    ADD COLUMN so_gio_lam DECIMAL(5, 2) NOT NULL DEFAULT 0 AFTER gio_ra,
    ADD COLUMN so_gio_tang_ca DECIMAL(5, 2) NOT NULL DEFAULT 0 AFTER so_gio_lam,
    ADD COLUMN ghi_chu VARCHAR(255) NULL AFTER so_gio_tang_ca;

ALTER TABLE luong
    ADD COLUMN nam YEAR NOT NULL AFTER thang,
    ADD COLUMN so_ngay_cong DECIMAL(5, 2) NOT NULL DEFAULT 0 AFTER luong_co_ban,
    ADD COLUMN luong_theo_cong DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER so_ngay_cong,
    ADD COLUMN tien_tang_ca DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER luong_theo_cong,
    ADD COLUMN phu_cap DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER tien_tang_ca,
    ADD COLUMN tien_phat DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER tien_thuong,
    ADD COLUMN bao_hiem DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER tien_phat,
    ADD COLUMN thue DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER bao_hiem,
    ADD COLUMN luong_thuc_nhan DECIMAL(15, 2) NOT NULL DEFAULT 0 AFTER thue,
    ADD COLUMN trang_thai VARCHAR(50) NOT NULL DEFAULT 'Chưa thanh toán' AFTER luong_thuc_nhan;
