"""Màn hình quản lý nhân viên."""

from database.database import Database
from ui.table_view import TableView


class NhanVienView(TableView):
    def __init__(self, parent, db: Database) -> None:
        super().__init__(parent, db, {
            "title": "Nhân viên",
            "table": "nhan_vien",
            "id_column": "ma_nhan_vien",
            "input_columns": ["ho_ten", "so_dien_thoai", "email", "ma_phong_ban", "ma_chuc_vu"],
            "display_columns": ["ma_nhan_vien", "ho_ten", "so_dien_thoai", "email", "ten_phong_ban", "ten_chuc_vu"],
            "labels": {"ma_nhan_vien": "Mã", "ho_ten": "Họ tên", "so_dien_thoai": "Điện thoại", "email": "Email", "ma_phong_ban": "Phòng ban", "ma_chuc_vu": "Chức vụ", "ten_phong_ban": "Phòng ban", "ten_chuc_vu": "Chức vụ"},
            "select": "SELECT n.ma_nhan_vien, n.ho_ten, n.so_dien_thoai, n.email, COALESCE(p.ten_phong_ban, '') AS ten_phong_ban, COALESCE(c.ten_chuc_vu, '') AS ten_chuc_vu FROM nhan_vien n LEFT JOIN phong_ban p ON p.ma_phong_ban=n.ma_phong_ban LEFT JOIN chuc_vu c ON c.ma_chuc_vu=n.ma_chuc_vu",
            "display_to_input": {"ten_phong_ban": "ma_phong_ban", "ten_chuc_vu": "ma_chuc_vu"},
            "foreign_keys": {"ma_phong_ban": ("phong_ban", "ma_phong_ban", "ten_phong_ban"), "ma_chuc_vu": ("chuc_vu", "ma_chuc_vu", "ten_chuc_vu")},
        })
