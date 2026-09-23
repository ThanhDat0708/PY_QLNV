"""Màn hình quản lý lương."""

from database.database import Database
from ui.table_view import TableView


class LuongView(TableView):
    def __init__(self, parent, db: Database) -> None:
        super().__init__(parent, db, {
            "title": "Lương", "table": "luong", "id_column": "ma_luong",
            "input_columns": ["ma_nhan_vien", "thang", "luong_co_ban", "tien_thuong"],
            "display_columns": ["ma_luong", "ho_ten", "thang", "luong_co_ban", "tien_thuong", "tong_luong"],
            "labels": {"ma_luong": "Mã", "ma_nhan_vien": "Nhân viên", "ho_ten": "Nhân viên", "thang": "Tháng (YYYY-MM)", "luong_co_ban": "Lương cơ bản", "tien_thuong": "Thưởng", "tong_luong": "Tổng lương"},
            "select": "SELECT l.ma_luong, COALESCE(n.ho_ten, '') AS ho_ten, l.thang, l.luong_co_ban, l.tien_thuong, l.tong_luong FROM luong l LEFT JOIN nhan_vien n ON n.ma_nhan_vien=l.ma_nhan_vien",
            "display_to_input": {"ho_ten": "ma_nhan_vien"},
            "foreign_keys": {"ma_nhan_vien": ("nhan_vien", "ma_nhan_vien", "ho_ten")},
            "date_fields": {"thang": "dd/mm/yyyy"},
            "month_fields": ["thang"],
        })
