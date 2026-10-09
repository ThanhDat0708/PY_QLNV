"""Màn hình tổng quan số liệu nhân sự và chi phí tiền lương."""

import tkinter as tk
import os
from tkinter import filedialog, messagebox, ttk
from typing import Any

from database.database import Database
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class TongQuanView(ttk.Frame):
    def __init__(self, parent: tk.Misc, db: Database) -> None:
        super().__init__(parent)
        self.db = db
        self.chart: tk.Canvas
        self.salary_distribution: list[dict[str, Any]] = []
        self.build_layout()
        self.load_dashboard()

    def build_layout(self) -> None:
        ttk.Label(self, text="TỔNG QUAN", style="Title.TLabel").pack(anchor="w", pady=(0, 10))
        self.cards = ttk.Frame(self)
        self.cards.pack(fill="x", pady=(0, 12))
        self.card_values: dict[str, ttk.Label] = {}
        for key, title in (
            ("employees", "Tổng nhân viên"),
            ("departments", "Tổng phòng ban"),
            ("paid", "Tổng tiền chi trả"),
        ):
            card = ttk.LabelFrame(self.cards, text=title, padding=14, style=f"{key}.TLabelframe")
            card.pack(side="left", fill="x", expand=True, padx=(0, 10))
            value = ttk.Label(card, text="Đang tải...", style=f"{key}.TLabel")
            value.pack(anchor="w")
            self.card_values[key] = value

        chart_frame = ttk.LabelFrame(
            self, text="Phân bố tổng lương thực nhận theo nhân viên", padding=10
        )
        chart_frame.pack(fill="both", expand=True)
        self.chart = tk.Canvas(chart_frame, background="#fbfdff", highlightthickness=0)
        self.chart.pack(fill="both", expand=True)
        self.chart.bind(
            "<Configure>", lambda _event: self.draw_chart(self.salary_distribution)
        )
        ttk.Button(self, text="Làm mới tổng quan", command=self.load_dashboard).pack(
            side="right", pady=(8, 0)
        )
        ttk.Button(self, text="Xuất PDF", style="Info.TButton",
                   command=self.export_pdf).pack(
            side="right", padx=(0, 8), pady=(8, 0)
        )

    def load_dashboard(self) -> None:
        try:
            summary = self.db.fetch_all(
                "SELECT "
                "(SELECT COUNT(*) FROM nhan_vien) AS so_nhan_vien, "
                "(SELECT COUNT(*) FROM phong_ban) AS so_phong_ban, "
                "(SELECT COALESCE(SUM(luong_thuc_nhan), 0) FROM luong) AS tong_chi_tra"
            )[0]
            salary_rows = self.db.fetch_all(
                "SELECT n.ho_ten, COALESCE(SUM(l.luong_thuc_nhan), 0) AS tong_luong "
                "FROM nhan_vien n "
                "LEFT JOIN luong l ON l.ma_nhan_vien=n.ma_nhan_vien "
                "GROUP BY n.ma_nhan_vien, n.ho_ten"
            )
        except RuntimeError as error:
            messagebox.showerror("Lỗi kết nối", str(error))
            return

        self.card_values["employees"].configure(text=f"{summary['so_nhan_vien']:,}")
        self.card_values["departments"].configure(text=f"{summary['so_phong_ban']:,}")
        self.card_values["paid"].configure(text=self.format_money(summary["tong_chi_tra"]))
        self.salary_distribution = self.build_salary_distribution(salary_rows)
        self.draw_chart(self.salary_distribution)

    @staticmethod
    def format_money(value: Any) -> str:
        try:
            return f"{float(value or 0):,.0f} VNĐ"
        except (TypeError, ValueError):
            return "0 VNĐ"

    @staticmethod
    def build_salary_distribution(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Gom dữ liệu thành 6 khoảng để biểu đồ không phụ thuộc số nhân viên."""
        ranges = [
            ("Chưa có lương", lambda value: value <= 0),
            ("Dưới 5 triệu", lambda value: 0 < value < 5_000_000),
            ("5 - 10 triệu", lambda value: 5_000_000 <= value < 10_000_000),
            ("10 - 15 triệu", lambda value: 10_000_000 <= value < 15_000_000),
            ("15 - 20 triệu", lambda value: 15_000_000 <= value < 20_000_000),
            ("Từ 20 triệu", lambda value: value >= 20_000_000),
        ]
        distribution = [
            {"nhom": label, "so_nhan_vien": 0, "tong_luong": 0.0}
            for label, _ in ranges
        ]
        for row in rows:
            value = float(row["tong_luong"] or 0)
            for index, (_, matches) in enumerate(ranges):
                if matches(value):
                    distribution[index]["so_nhan_vien"] += 1
                    distribution[index]["tong_luong"] += value
                    break
        return distribution

    def draw_chart(self, rows: list[dict[str, Any]]) -> None:
        self.chart.delete("all")
        width = max(self.chart.winfo_width(), 600)
        height = max(self.chart.winfo_height(), 300)
        if not rows or not any(row["so_nhan_vien"] for row in rows):
            self.chart.create_text(
                width / 2, height / 2, text="Chưa có dữ liệu lương để hiển thị"
            )
            return
        left, right, top, bottom = 70, 20, 25, 55
        max_value = max(row["so_nhan_vien"] for row in rows) or 1
        plot_width = width - left - right
        bar_width = max(18, plot_width / len(rows) - 12)
        baseline = height - bottom
        self.chart.create_line(left, top, left, baseline, fill="#9aa9ba")
        self.chart.create_line(left, baseline, width - right, baseline, fill="#9aa9ba")
        for index, row in enumerate(rows):
            employee_count = row["so_nhan_vien"]
            x = left + index * (plot_width / len(rows)) + 6
            bar_height = (baseline - top - 10) * employee_count / max_value
            self.chart.create_rectangle(
                x, baseline - bar_height, x + bar_width, baseline,
                fill=("#ef8354", "#3fa7d6", "#59c3c3", "#7bc96f", "#9b8afb", "#f2c14e")[index],
                outline=""
            )
            self.chart.create_text(
                x + bar_width / 2, baseline + 15, text=row["nhom"], angle=45, anchor="w"
            )
            self.chart.create_text(
                x + bar_width / 2, baseline - bar_height - 8,
                text=f"{employee_count} NV", fill="#17324d"
            )

    def export_pdf(self) -> None:
        """Xuất các chỉ số tổng quan và phân bố lương ra PDF."""
        if not self.salary_distribution:
            messagebox.showwarning(
                "Chưa có dữ liệu", "Vui lòng tải dữ liệu tổng quan trước khi xuất file."
            )
            return
        file_path = filedialog.asksaveasfilename(
            title="Lưu báo cáo tổng quan",
            defaultextension=".pdf",
            filetypes=[("Tệp PDF", "*.pdf"), ("Tất cả tệp", "*.*")],
            initialfile="bao_cao_tong_quan.pdf",
        )
        if not file_path:
            return
        try:
            font_name = self.pdf_font_name()
            styles = getSampleStyleSheet()
            styles["Title"].fontName = font_name
            styles["Heading2"].fontName = font_name
            document = SimpleDocTemplate(
                file_path, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
                topMargin=16 * mm, bottomMargin=16 * mm,
            )
            content = [
                Paragraph("BÁO CÁO TỔNG QUAN", styles["Title"]),
                Spacer(1, 8),
                Table(
                    [
                        ["Chỉ số", "Giá trị"],
                        ["Tổng nhân viên", self.card_values["employees"].cget("text")],
                        ["Tổng phòng ban", self.card_values["departments"].cget("text")],
                        ["Tổng tiền chi trả", self.card_values["paid"].cget("text")],
                    ],
                    colWidths=[80 * mm, 80 * mm],
                    style=self.pdf_table_style(font_name),
                ),
                Spacer(1, 14),
                Paragraph("Phân bố tổng lương thực nhận theo nhân viên", styles["Heading2"]),
                Spacer(1, 6),
                Table(
                    [["Nhóm lương", "Số nhân viên", "Tổng lương trong nhóm"]]
                    + [
                        [row["nhom"], row["so_nhan_vien"], self.format_money(row["tong_luong"])]
                        for row in self.salary_distribution
                    ],
                    colWidths=[70 * mm, 40 * mm, 50 * mm],
                    style=self.pdf_table_style(font_name),
                ),
            ]
            document.build(content)
        except (OSError, ImportError, ValueError) as error:
            messagebox.showerror("Không thể xuất file", f"Không thể lưu báo cáo:\n{error}")
            return
        messagebox.showinfo("Xuất PDF thành công", f"Đã lưu báo cáo tại:\n{file_path}")

    @staticmethod
    def pdf_font_name() -> str:
        """Dùng Arial để PDF hiển thị đúng tiếng Việt trên Windows."""
        font_path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "arial.ttf")
        if os.path.exists(font_path):
            if "ArialUnicode" not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))
            return "ArialUnicode"
        return "Helvetica"

    @staticmethod
    def pdf_table_style(font_name: str = "Helvetica") -> TableStyle:
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324d")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTNAME", (0, 0), (-1, 0), f"{font_name}-Bold" if font_name == "Helvetica" else font_name),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b8c7d9")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f8")]),
            ("PADDING", (0, 0), (-1, -1), 7),
        ])
