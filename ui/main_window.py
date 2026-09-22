"""Cửa sổ chính và menu điều hướng."""

import tkinter as tk
from tkinter import ttk

from database.database import Database
from ui.chamcong import ChamCongView
from ui.chucvu import ChucVuView
from ui.luong import LuongView
from ui.nhanvien import NhanVienView
from ui.phongban import PhongBanView


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Hệ thống quản lý nhân viên")
        self.root.geometry("1150x680")
        self.db = Database()
        self.content = ttk.Frame(self.root)
        self.build_layout()
        self.show_view(NhanVienView, "Nhân viên")

    def build_layout(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#17324d")
        style.configure("Menu.TButton", anchor="w", padding=10)

        header = ttk.Frame(self.root, padding=(20, 16))
        header.pack(fill="x")
        ttk.Label(header, text="HỆ THỐNG QUẢN LÝ NHÂN VIÊN", style="Title.TLabel").pack(side="left")

        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        menu = ttk.LabelFrame(body, text="Menu", padding=10)
        menu.pack(side="left", fill="y", padx=(0, 12))
        buttons = [
            ("Nhân viên", NhanVienView),
            ("Phòng ban", PhongBanView),
            ("Chức vụ", ChucVuView),
            ("Chấm công", ChamCongView),
            ("Lương", LuongView),
        ]
        for title, view_class in buttons:
            ttk.Button(menu, text=title, style="Menu.TButton", command=lambda c=view_class, t=title: self.show_view(c, t)).pack(fill="x", pady=3)
        self.content = ttk.Frame(body)
        self.content.pack(side="left", fill="both", expand=True)

    def show_view(self, view_class: type[ttk.Frame], _title: str) -> None:
        for widget in self.content.winfo_children():
            widget.destroy()
        view = view_class(self.content, self.db)
        view.pack(fill="both", expand=True)

    def run(self) -> None:
        self.root.mainloop()
