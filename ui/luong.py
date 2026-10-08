"""Màn hình quản lý lương."""

from database.database import Database
from ui.table_view import TableView


class LuongView(TableView):
    def __init__(self, parent, db: Database) -> None:
        super().__init__(parent, db, {
            "title": "Lương", "table": "luong", "id_column": "ma_luong",
            "input_columns": [
                "ma_nhan_vien", "thang", "nam", "luong_co_ban", "so_ngay_cong",
                "luong_theo_cong", "tien_tang_ca", "phu_cap", "tien_thuong",
                "tien_phat", "bao_hiem", "thue", "luong_thuc_nhan", "trang_thai",
            ],
            "display_columns": [
                "ma_luong", "ho_ten", "thang", "nam", "luong_co_ban",
                "so_ngay_cong", "luong_theo_cong", "tien_tang_ca", "phu_cap",
                "tien_thuong", "tien_phat", "bao_hiem", "thue",
                "luong_thuc_nhan", "trang_thai",
            ],
            "labels": {
                "ma_luong": "Bảng lương", "ma_nhan_vien": "Nhân viên",
                "ho_ten": "Nhân viên", "thang": "Tháng", "nam": "Năm",
                "luong_co_ban": "Lương cơ bản", "so_ngay_cong": "Số ngày công",
                "luong_theo_cong": "Lương 1 ngày công", "tien_tang_ca": "Tiền tăng ca",
                "phu_cap": "Phụ cấp", "tien_thuong": "Tiền thưởng",
                "tien_phat": "Tiền phạt", "bao_hiem": "Bảo hiểm",
                "thue": "Thuế", "luong_thuc_nhan": "Lương thực nhận",
                "trang_thai": "Trạng thái",
            },
            "select": (
                "SELECT l.ma_luong, COALESCE(n.ho_ten, '') AS ho_ten, l.thang, "
                "l.nam, l.luong_co_ban, l.so_ngay_cong, l.luong_theo_cong, "
                "l.tien_tang_ca, l.phu_cap, l.tien_thuong, l.tien_phat, "
                "l.bao_hiem, l.thue, l.luong_thuc_nhan, l.trang_thai "
                "FROM luong l LEFT JOIN nhan_vien n "
                "ON n.ma_nhan_vien=l.ma_nhan_vien"
            ),
            "display_to_input": {"ho_ten": "ma_nhan_vien"},
            "foreign_keys": {"ma_nhan_vien": ("nhan_vien", "ma_nhan_vien", "ho_ten")},
            "computed_fields": {
                "luong_thuc_nhan": {
                    "sources": [
                        "so_ngay_cong", "luong_theo_cong", "tien_tang_ca", "phu_cap",
                        "tien_thuong", "tien_phat", "bao_hiem", "thue",
                    ],
                    "add": ["luong_theo_cong"],
                    "multiply": ["so_ngay_cong"],
                    "add_after_multiply": [
                        "tien_tang_ca", "phu_cap", "tien_thuong",
                    ],
                    "subtract": ["tien_phat", "bao_hiem", "thue"],
                },
            },
            "number_fields": [
                "nam", "luong_co_ban", "so_ngay_cong", "luong_theo_cong",
                "tien_tang_ca", "phu_cap", "tien_thuong", "tien_phat",
                "bao_hiem", "thue",
            ],
            "money_fields": [
                "luong_co_ban", "luong_theo_cong", "tien_tang_ca", "phu_cap",
                "tien_thuong", "tien_phat", "bao_hiem", "thue", "luong_thuc_nhan",
            ],
        })
