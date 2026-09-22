"""Màn hình quản lý chức vụ."""

from database.database import Database
from ui.table_view import TableView


class ChucVuView(TableView):
    def __init__(self, parent, db: Database) -> None:
        super().__init__(parent, db, {
            "title": "Chức vụ", "table": "chuc_vu", "id_column": "ma_chuc_vu",
            "input_columns": ["ten_chuc_vu"], "display_columns": ["ma_chuc_vu", "ten_chuc_vu"],
            "labels": {"ma_chuc_vu": "Mã", "ten_chuc_vu": "Tên chức vụ"},
            "select": "SELECT ma_chuc_vu, ten_chuc_vu FROM chuc_vu",
        })
