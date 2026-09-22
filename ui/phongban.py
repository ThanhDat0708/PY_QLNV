"""Màn hình quản lý phòng ban."""

from database.database import Database
from ui.table_view import TableView


class PhongBanView(TableView):
    def __init__(self, parent, db: Database) -> None:
        super().__init__(parent, db, {
            "title": "Phòng ban", "table": "phong_ban", "id_column": "ma_phong_ban",
            "input_columns": ["ten_phong_ban"], "display_columns": ["ma_phong_ban", "ten_phong_ban"],
            "labels": {"ma_phong_ban": "Mã", "ten_phong_ban": "Tên phòng ban"},
            "select": "SELECT ma_phong_ban, ten_phong_ban FROM phong_ban",
        })
