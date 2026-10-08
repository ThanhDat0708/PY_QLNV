USE employee_management;

ALTER TABLE luong
    MODIFY COLUMN luong_thuc_nhan DECIMAL(15, 2)
    GENERATED ALWAYS AS (
        (luong_theo_cong * so_ngay_cong) + tien_tang_ca + phu_cap + tien_thuong
        - tien_phat - bao_hiem - thue
    ) STORED;
