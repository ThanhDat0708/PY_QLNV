"""Màn hình đăng nhập và đăng ký tài khoản."""

import re
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from database.database import Database


class LoginView(ttk.Frame):
    def __init__(self, parent: tk.Misc, db: Database, on_success: Callable[[dict], None]) -> None:
        super().__init__(parent, padding=30)
        self.db = db
        self.on_success = on_success
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self._build()

    def _build(self) -> None:
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="ĐĂNG NHẬP", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )
        self._field("Tên đăng nhập", self.username, 1)
        self._field("Mật khẩu", self.password, 2, show="*")
        ttk.Button(self, text="Đăng nhập", style="Login.TButton", command=self.login).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(12, 6)
        )
        ttk.Button(self, text="Đăng ký tài khoản", command=self.open_register).grid(
            row=4, column=0, columnspan=2, sticky="ew"
        )

    def _field(self, label: str, variable: tk.StringVar, row: int, show: str = "") -> None:
        ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", pady=6, padx=(0, 12))
        ttk.Entry(self, textvariable=variable, show=show, width=28).grid(
            row=row, column=1, sticky="ew", pady=6
        )

    def login(self) -> None:
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        try:
            account = self.db.authenticate_user(username, password)
        except RuntimeError as error:
            messagebox.showerror("Lỗi kết nối", str(error))
            return
        if account is None:
            messagebox.showerror("Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
            return
        self.on_success(account)

    def open_register(self) -> None:
        RegisterWindow(self.winfo_toplevel(), self.db)


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc, db: Database) -> None:
        super().__init__(parent)
        self.db = db
        self.title("Đăng ký tài khoản")
        self.resizable(False, False)
        self.username = tk.StringVar()
        self.full_name = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm = tk.StringVar()
        self._build()
        self.grab_set()

    def _build(self) -> None:
        form = ttk.Frame(self, padding=24)
        form.pack()
        fields = [
            ("Họ và tên", self.full_name, ""),
            ("Tên đăng nhập", self.username, ""),
            ("Mật khẩu", self.password, "*"),
            ("Nhập lại mật khẩu", self.confirm, "*"),
        ]
        for row, (label, variable, show) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=6, padx=(0, 12))
            ttk.Entry(form, textvariable=variable, show=show, width=28).grid(
                row=row, column=1, pady=6
            )
        ttk.Button(form, text="Tạo tài khoản", command=self.register).grid(
            row=len(fields), column=0, columnspan=2, sticky="ew", pady=(12, 0)
        )

    def register(self) -> None:
        full_name = self.full_name.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        if not full_name or not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.", parent=self)
            return
        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,50}", username):
            messagebox.showwarning(
                "Dữ liệu không hợp lệ",
                "Tên đăng nhập dài 3-50 ký tự, chỉ gồm chữ, số, dấu chấm, gạch ngang hoặc gạch dưới.",
                parent=self,
            )
            return
        if len(password) < 8:
            messagebox.showwarning("Mật khẩu yếu", "Mật khẩu phải có ít nhất 8 ký tự.", parent=self)
            return
        if password != self.confirm.get():
            messagebox.showwarning("Mật khẩu không khớp", "Vui lòng nhập lại mật khẩu.", parent=self)
            return
        try:
            self.db.register_user(username, password, full_name)
        except ValueError as error:
            messagebox.showwarning("Không thể đăng ký", str(error), parent=self)
            return
        except RuntimeError as error:
            messagebox.showerror("Lỗi kết nối", str(error), parent=self)
            return
        messagebox.showinfo("Thành công", "Đăng ký thành công. Bạn có thể đăng nhập.", parent=self)
        self.destroy()
