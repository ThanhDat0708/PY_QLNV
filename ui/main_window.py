"""Cửa sổ chính và menu điều hướng."""

import tkinter as tk
from tkinter import ttk

from database.database import Database
from ui.chamcong import ChamCongView
from ui.chucvu import ChucVuView
from ui.luong import LuongView
from ui.nhanvien import NhanVienView
from ui.phongban import PhongBanView
from ui.tong_quan import TongQuanView


class MainWindow:
    def __init__(self, account: dict) -> None:
        self.root = tk.Tk()
        self.root.title("Hệ thống quản lý nhân viên")
        self.root.geometry("1150x680")
        self.db = Database()
        self.account = account
        self.content = ttk.Frame(self.root)
        self.build_layout()
        self.show_view(NhanVienView, "Nhân viên")

    def build_layout(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        self.root.configure(background="#eef3f8")
        style.configure("TFrame", background="#eef3f8")
        style.configure("TLabel", background="#eef3f8", foreground="#243447")
        style.configure("Title.TLabel", background="#eef3f8", foreground="#17324d",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Header.TFrame", background="#17324d")
        style.configure("Header.TLabel", background="#17324d", foreground="white")
        style.configure("Menu.TLabelframe", background="#ffffff", foreground="#17324d")
        style.configure("Menu.TLabelframe.Label", background="#ffffff", foreground="#17324d",
                        font=("Segoe UI", 10, "bold"))
        style.configure("Menu.TButton", anchor="w", padding=10, background="#ffffff",
                        foreground="#17324d", font=("Segoe UI", 10))
        style.map("Menu.TButton", background=[("active", "#dcecff")],
                  foreground=[("active", "#145da0")])
        style.configure("Logout.TButton", padding=(12, 7), background="#e85d75",
                        foreground="white", font=("Segoe UI", 9, "bold"))
        style.map("Logout.TButton", background=[("active", "#c9435c")])
        for key, color in (
            ("employees", "#2f80ed"), ("departments", "#00a896"), ("paid", "#f28f3b"),
        ):
            style.configure(f"{key}.TLabelframe", background="#ffffff", foreground=color,
                            bordercolor=color)
            style.configure(f"{key}.TLabelframe.Label", background="#ffffff",
                            foreground=color, font=("Segoe UI", 10, "bold"))
            style.configure(f"{key}.TLabel", background="#ffffff", foreground=color,
                            font=("Segoe UI", 16, "bold"))
        style.configure("Success.TButton", background="#2a9d8f", foreground="white")
        style.configure("Info.TButton", background="#2f80ed", foreground="white")
        style.configure("Danger.TButton", background="#e85d75", foreground="white")
        style.map("Success.TButton", background=[("active", "#21867a")])
        style.map("Info.TButton", background=[("active", "#2166c2")])
        style.map("Danger.TButton", background=[("active", "#c9435c")])

        header = ttk.Frame(self.root, padding=(20, 16), style="Header.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="HỆ THỐNG QUẢN LÝ NHÂN VIÊN",
                  style="Header.TLabel", font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Label(header, text=f"Xin chào, {self.account['ho_ten']}",
                  style="Header.TLabel").pack(side="right", padx=12)
        ttk.Button(header, text="Đăng xuất", style="Logout.TButton",
                   command=self.logout).pack(side="right")

        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        menu = ttk.LabelFrame(body, text="ĐIỀU HƯỚNG", padding=10, style="Menu.TLabelframe")
        menu.pack(side="left", fill="y", padx=(0, 12))
        buttons = [
            ("Tổng quan", TongQuanView),
            ("Nhân viên", NhanVienView),
            ("Phòng ban", PhongBanView),
            ("Chức vụ", ChucVuView),
            ("Chấm công", ChamCongView),
            ("Lương", LuongView),
        ]
        for title, view_class in buttons:
            ttk.Button(menu, text=title, 
                       style="Menu.TButton",
                        command=lambda c=view_class,
                        t=title: self.show_view(c, t)).pack(fill="x", pady=3)
        self.content = ttk.Frame(body, padding=(4, 0, 0, 0))
        self.content.pack(side="left", fill="both", expand=True)

    def show_view(self, view_class: type[ttk.Frame], _title: str) -> None:
        for widget in self.content.winfo_children():
            widget.destroy()
        view = view_class(self.content, self.db)
        view.pack(fill="both", expand=True)

    def run(self) -> None:
        self.root.mainloop()

    def logout(self) -> None:
        self.root.destroy()
        from ui.login_window import LoginWindow
        LoginWindow().run()
