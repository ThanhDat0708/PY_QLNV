"""Màn hình quản lý chấm công."""

from database.database import Database
from ui.table_view import TableView


class ChamCongView(TableView):
    def __init__(self, parent, db: Database) -> None:
        super().__init__(parent, db, {
            "title": "Chấm công", "table": "cham_cong", "id_column": "ma_cham_cong",
            "input_columns": ["ma_nhan_vien", "ngay_lam_viec", "gio_vao", "gio_ra", "trang_thai"],
            "display_columns": ["ma_cham_cong", "ho_ten", "ngay_lam_viec", "gio_vao", "gio_ra", "trang_thai"],
            "labels": {"ma_cham_cong": "Mã", "ma_nhan_vien": "Nhân viên", "ho_ten": "Nhân viên", "ngay_lam_viec": "Ngày làm việc", "gio_vao": "Giờ vào", "gio_ra": "Giờ ra", "trang_thai": "Trạng thái"},
            "select": "SELECT cc.ma_cham_cong, COALESCE(n.ho_ten, '') AS ho_ten, cc.ngay_lam_viec, cc.gio_vao, cc.gio_ra, cc.trang_thai FROM cham_cong cc LEFT JOIN nhan_vien n ON n.ma_nhan_vien=cc.ma_nhan_vien",
            "display_to_input": {"ho_ten": "ma_nhan_vien"},
            "foreign_keys": {"ma_nhan_vien": ("nhan_vien", "ma_nhan_vien", "ho_ten")},
        })
