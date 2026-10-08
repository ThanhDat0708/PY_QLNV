USE employee_management;

START TRANSACTION;

INSERT IGNORE INTO phong_ban (ten_phong_ban) VALUES
    ('Phong Ky thuat mau 1'),
    ('Phong Ky thuat mau 2'),
    ('Phong Ky thuat mau 3'),
    ('Phong Ky thuat mau 4'),
    ('Phong Ky thuat mau 5');

INSERT IGNORE INTO chuc_vu (ten_chuc_vu) VALUES
    ('Chuc vu mau 1'),
    ('Chuc vu mau 2'),
    ('Chuc vu mau 3'),
    ('Chuc vu mau 4'),
    ('Chuc vu mau 5');

INSERT INTO nhan_vien
    (ho_ten, so_dien_thoai, email, ma_phong_ban, ma_chuc_vu)
SELECT data.ho_ten, data.so_dien_thoai, data.email,
       (SELECT ma_phong_ban FROM phong_ban WHERE ten_phong_ban = data.ten_phong_ban),
       (SELECT ma_chuc_vu FROM chuc_vu WHERE ten_chuc_vu = data.ten_chuc_vu)
FROM (
    SELECT 'Nhan vien mau 1' AS ho_ten, '0900000001' AS so_dien_thoai,
           'mau1@example.com' AS email, 'Phong Ky thuat mau 1' AS ten_phong_ban,
           'Chuc vu mau 1' AS ten_chuc_vu
    UNION ALL SELECT 'Nhan vien mau 2', '0900000002', 'mau2@example.com',
           'Phong Ky thuat mau 2', 'Chuc vu mau 2'
    UNION ALL SELECT 'Nhan vien mau 3', '0900000003', 'mau3@example.com',
           'Phong Ky thuat mau 3', 'Chuc vu mau 3'
    UNION ALL SELECT 'Nhan vien mau 4', '0900000004', 'mau4@example.com',
           'Phong Ky thuat mau 4', 'Chuc vu mau 4'
    UNION ALL SELECT 'Nhan vien mau 5', '0900000005', 'mau5@example.com',
           'Phong Ky thuat mau 5', 'Chuc vu mau 5'
) AS data
WHERE NOT EXISTS (
    SELECT 1 FROM nhan_vien existing WHERE existing.email = data.email
);

INSERT INTO cham_cong
    (ma_nhan_vien, ngay_lam_viec, gio_vao, gio_ra, so_gio_lam,
     so_gio_tang_ca, ghi_chu, trang_thai)
SELECT nhan_vien.ma_nhan_vien, data.ngay_lam_viec, data.gio_vao, data.gio_ra,
       data.so_gio_lam, data.so_gio_tang_ca, data.ghi_chu, 'Co mat'
FROM (
    SELECT 'mau1@example.com' AS email, '2026-08-01' AS ngay_lam_viec,
           '08:00:00' AS gio_vao, '17:00:00' AS gio_ra, 8.00 AS so_gio_lam,
           1.00 AS so_gio_tang_ca, 'Hoan thanh cong viec' AS ghi_chu
    UNION ALL SELECT 'mau2@example.com', '2026-08-02', '08:00:00', '17:00:00',
           8.00, 0.00, 'Lam viec binh thuong'
    UNION ALL SELECT 'mau3@example.com', '2026-08-03', '08:00:00', '18:00:00',
           8.00, 2.00, 'Ho tro ngoai gio'
    UNION ALL SELECT 'mau4@example.com', '2026-08-04', '08:00:00', '17:00:00',
           8.00, 0.00, 'Du hop phong ban'
    UNION ALL SELECT 'mau5@example.com', '2026-08-05', '08:00:00', '19:00:00',
           8.00, 3.00, 'Hoan thanh bao cao'
) AS data
JOIN nhan_vien ON nhan_vien.email = data.email
WHERE NOT EXISTS (
    SELECT 1 FROM cham_cong existing
    WHERE existing.ma_nhan_vien = nhan_vien.ma_nhan_vien
      AND existing.ngay_lam_viec = data.ngay_lam_viec
);

INSERT INTO luong
    (ma_nhan_vien, thang, nam, luong_co_ban, so_ngay_cong, luong_theo_cong,
     tien_tang_ca, phu_cap, tien_thuong, tien_phat, bao_hiem, thue,
     trang_thai)
SELECT nhan_vien.ma_nhan_vien, data.thang, 2026, data.luong_co_ban,
       26.00, data.luong_theo_cong, data.tien_tang_ca, 500000.00,
       1000000.00, 0.00, 1250000.00, 0.00,
       'Chua thanh toan'
FROM (
    SELECT 'mau1@example.com' AS email, '9' AS thang,
           8000000.00 AS luong_co_ban, 8000000.00 AS luong_theo_cong,
           500000.00 AS tien_tang_ca
    UNION ALL SELECT 'mau2@example.com', '9', 8500000.00, 8500000.00,
           0.00
    UNION ALL SELECT 'mau3@example.com', '9', 9000000.00, 9000000.00,
           1000000.00
    UNION ALL SELECT 'mau4@example.com', '9', 9500000.00, 9500000.00,
           0.00
    UNION ALL SELECT 'mau5@example.com', '9', 10000000.00, 10000000.00,
           1500000.00
) AS data
JOIN nhan_vien ON nhan_vien.email = data.email
WHERE NOT EXISTS (
    SELECT 1 FROM luong existing
    WHERE existing.ma_nhan_vien = nhan_vien.ma_nhan_vien
      AND existing.thang = data.thang
);

COMMIT;
