"""Các thao tác giao diện dùng chung cho một bảng dữ liệu."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any

from database.database import Database


class TableView(ttk.Frame):
    """Màn hình CRUD dùng chung cho từng bảng."""

    def __init__(self, parent: tk.Misc, db: Database, config: dict[str, Any]) -> None:
        super().__init__(parent)
        self.db = db
        self.config = config
        self.widgets: dict[str, ttk.Entry | ttk.Combobox] = {}
        self.foreign_values: dict[str, dict[str, int]] = {}
        self.tree: ttk.Treeview
        self.search_entry: ttk.Entry
        self.build_form()
        self.load_rows()

    def build_form(self) -> None:
        ttk.Label(self, text=self.config["title"], style="Title.TLabel").pack(anchor="w", pady=(0, 10))
        form = ttk.LabelFrame(self, text="Thông tin", padding=10)
        form.pack(fill="x")

        for index, column in enumerate(self.config["input_columns"]):
            ttk.Label(form, text=self.config["labels"][column]).grid(
                row=index // 3 * 2, column=index % 3 * 2, sticky="w", padx=(0, 6)
            )
            if column in self.config.get("foreign_keys", {}):
                widget: ttk.Entry | ttk.Combobox = ttk.Combobox(form, state="readonly", width=22)
                self.load_foreign_options(widget, column)
            else:
                widget = ttk.Entry(form, width=24)
            widget.grid(row=index // 3 * 2 + 1, column=index % 3 * 2, sticky="ew", padx=(0, 14), pady=(0, 8))
            self.widgets[column] = widget

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text="Thêm", command=self.add).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Sửa", command=self.edit).pack(side="left", padx=6)
        ttk.Button(actions, text="Xóa", command=self.remove).pack(side="left", padx=6)
        ttk.Button(actions, text="Làm mới", command=self.load_rows).pack(side="left", padx=6)
        self.search_entry = ttk.Entry(actions, width=26)
        self.search_entry.pack(side="right", padx=(6, 0))
        ttk.Button(actions, text="Tìm kiếm", command=lambda: self.load_rows(self.search_entry.get())).pack(side="right")

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame, columns=self.config["display_columns"], show="headings")
        for column in self.config["display_columns"]:
            self.tree.heading(column, text=self.config["labels"][column])
            self.tree.column(column, width=135, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", self.select_row)

    def load_foreign_options(self, widget: ttk.Combobox, column: str) -> None:
        table, id_column, name_column = self.config["foreign_keys"][column]
        try:
            rows = self.db.fetch_all(f"SELECT {id_column}, {name_column} FROM {table} ORDER BY {name_column}")
            widget["values"] = [str(row[name_column]) for row in rows]
            self.foreign_values[column] = {str(row[name_column]): row[id_column] for row in rows}
        except RuntimeError:
            widget["values"] = []

    def load_rows(self, keyword: str = "") -> None:
        try:
            rows = self.db.fetch_all(self.config["select"])
            self.tree.delete(*self.tree.get_children())
            keyword = keyword.lower().strip()
            for row in rows:
                values = [row[column] for column in self.config["display_columns"]]
                text = " ".join(str(value or "") for value in values).lower()
                if not keyword or keyword in text:
                    self.tree.insert("", "end", values=values)
        except RuntimeError as error:
            messagebox.showerror("Lỗi kết nối", str(error))

    def select_row(self, _event: object) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        for column, value in zip(self.config["display_columns"][1:], values[1:]):
            input_column = self.config.get("display_to_input", {}).get(column, column)
            widget = self.widgets.get(input_column)
            if widget is not None:
                widget.delete(0, tk.END)
                widget.insert(0, value)

    def value(self, column: str) -> Any:
        value = self.widgets[column].get().strip()
        return self.foreign_values.get(column, {}).get(value, value or None)

    def selected_id(self) -> Any:
        selected = self.tree.selection()
        return self.tree.item(selected[0], "values")[0] if selected else None

    def add(self) -> None:
        columns = self.config["input_columns"]
        values = tuple(self.value(column) for column in columns)
        try:
            self.db.execute(
                f"INSERT INTO {self.config['table']} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})",
                values,
            )
            self.load_rows()
            messagebox.showinfo("Thành công", "Đã thêm dữ liệu.")
        except RuntimeError as error:
            messagebox.showerror("Lỗi", str(error))

    def edit(self) -> None:
        record_id = self.selected_id()
        if not record_id:
            messagebox.showwarning("Thiếu dữ liệu", "Hãy chọn bản ghi cần sửa.")
            return
        columns = self.config["input_columns"]
        try:
            self.db.execute(
                f"UPDATE {self.config['table']} SET {', '.join(f'{column}=%s' for column in columns)} "
                f"WHERE {self.config['id_column']}=%s",
                tuple(self.value(column) for column in columns) + (record_id,),
            )
            self.load_rows()
            messagebox.showinfo("Thành công", "Đã cập nhật dữ liệu.")
        except RuntimeError as error:
            messagebox.showerror("Lỗi", str(error))

    def remove(self) -> None:
        record_id = self.selected_id()
        if not record_id:
            messagebox.showwarning("Thiếu dữ liệu", "Hãy chọn bản ghi cần xóa.")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa bản ghi này không?"):
            return
        try:
            self.db.execute(
                f"DELETE FROM {self.config['table']} WHERE {self.config['id_column']}=%s",
                (record_id,),
            )
            self.load_rows()
        except RuntimeError as error:
            messagebox.showerror("Lỗi", str(error))