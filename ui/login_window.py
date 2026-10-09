"""Cửa sổ xác thực trước khi vào hệ thống."""

import tkinter as tk
from tkinter import ttk

from database.database import Database
from ui.login import LoginView


class LoginWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Đăng nhập - Quản lý nhân viên")
        self.root.geometry("430x300")
        self.root.resizable(False, False)
        style = ttk.Style(self.root)
        style.theme_use("clam")
        self.root.configure(background="#eef3f8")
        style.configure("TFrame", background="#eef3f8")
        style.configure("TLabel", background="#eef3f8", foreground="#243447")
        style.configure("Title.TLabel", background="#eef3f8", foreground="#17324d",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Login.TButton", padding=9, background="#2f80ed",
                        foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Login.TButton", background=[("active", "#2166c2")])
        self.view = LoginView(self.root, Database(), self.open_main_window)
        self.view.pack(fill="both", expand=True)

    def open_main_window(self, account: dict) -> None:
        self.root.destroy()
        from ui.main_window import MainWindow
        MainWindow(account).run()

    def run(self) -> None:
        self.root.mainloop()
