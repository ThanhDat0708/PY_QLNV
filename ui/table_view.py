"""Các thao tác giao diện dùng chung cho một bảng dữ liệu."""

import tkinter as tk
from datetime import datetime
import re
from tkinter import messagebox, ttk
from typing import Any

from tkcalendar import DateEntry

from database.database import Database

class TableView(ttk.Frame):
    """Màn hình CRUD dùng chung cho từng bảng."""

    def __init__(self, parent: tk.Misc, db: Database, config: dict[str, Any]) -> None:
        super().__init__(parent)
        self.db = db
        self.config = config
        self.widgets: dict[str, ttk.Entry | ttk.Combobox | DateEntry | TimePicker] = {}
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
                widget: ttk.Entry | ttk.Combobox | DateEntry = ttk.Combobox(form, state="readonly", width=22)
                self.load_foreign_options(widget, column)
            elif column in self.config.get("time_fields", []):
                widget = TimePicker(form)
            elif column in self.config.get("date_fields", {}):
                widget = DateEntry(
                    form,
                    width=22,
                    date_pattern=self.config["date_fields"][column],
                    locale="vi_VN",
                )
            else:
                widget = ttk.Entry(form, width=24)
            if column in self.config.get("computed_fields", {}):
                widget.configure(state="readonly")
            widget.grid(row=index // 3 * 2 + 1, column=index % 3 * 2, sticky="ew", padx=(0, 14), pady=(0, 8))
            self.widgets[column] = widget
            if column in self.config.get("computed_fields", {}):
                for source_column in self.config["computed_fields"][column]["sources"]:
                    self.widgets[source_column].bind(
                        "<KeyRelease>", lambda _event: self.update_computed_fields()
                    )

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text="Thêm", command=self.add).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Sửa", command=self.edit).pack(side="left", padx=6)
        ttk.Button(actions, text="Xóa", command=self.remove).pack(side="left", padx=6)
        ttk.Button(actions, text="Làm mới", command=self.refresh).pack(side="left", padx=6)
        self.search_entry = ttk.Entry(actions, width=26)
        self.search_entry.pack(side="right", padx=(6, 0))
        ttk.Button(actions, text="Tìm kiếm", command=lambda: self.load_rows(self.search_entry.get())).pack(side="right")

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame, columns=self.config["display_columns"], show="headings")
        for column in self.config["display_columns"]:
            self.tree.heading(column, text=self.config["labels"][column])
            self.tree.column(column, width=135, anchor="w")
        self.tree.pack(side="top", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", before=self.tree)
        horizontal_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.configure(xscrollcommand=horizontal_scrollbar.set)
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
                values = [
                    self.format_display_value(column, row[column])
                    for column in self.config["display_columns"]
                ]
                text = " ".join(str(value or "") for value in values).lower()
                if not keyword or keyword in text:
                    self.tree.insert("", "end", values=values)
        except RuntimeError as error:
            messagebox.showerror("Lỗi kết nối", str(error))

    def refresh(self) -> None:
        """Tải lại dữ liệu và đưa form về trạng thái nhập mới."""
        self.search_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        for column, widget in self.widgets.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            elif column in self.config.get("time_fields", []):
                widget.delete()
            elif column in self.config.get("date_fields", {}):
                widget.set_date(datetime.now().date())
            elif column in self.config.get("computed_fields", {}):
                self.set_widget_value(widget, "")
            else:
                widget.delete(0, tk.END)
        self.update_computed_fields()
        self.load_rows()

    def select_row(self, _event: object) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        for column, value in zip(self.config["display_columns"][1:], values[1:]):
            input_column = self.config.get("display_to_input", {}).get(column, column)
            widget = self.widgets.get(input_column)
            if widget is not None:
                if input_column in self.config.get("date_fields", {}):
                    text_value = str(value)
                    if input_column in self.config.get("month_fields", []):
                        text_value = f"{text_value[:7]}-01"
                    widget.set_date(datetime.strptime(text_value[:10], "%Y-%m-%d").date())
                elif input_column in self.config.get("time_fields", []):
                    widget.set(str(value)[:5])
                elif isinstance(widget, ttk.Combobox):
                    widget.set(str(value))
                elif input_column in self.config.get("computed_fields", {}):
                    self.set_widget_value(widget, str(value))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)
        self.update_computed_fields()

    def set_widget_value(self, widget: ttk.Entry, value: str) -> None:
        widget.configure(state="normal")
        widget.delete(0, tk.END)
        widget.insert(0, value)
        widget.configure(state="readonly")

    def update_computed_fields(self) -> None:
        for target, formula in self.config.get("computed_fields", {}).items():
            total = sum(
                self.number_value(column) for column in formula.get("add", [])
            )
            for multiplier in formula.get("multiply", []):
                total *= self.number_value(multiplier)
            total += sum(
                self.number_value(column)
                for column in formula.get("add_after_multiply", [])
            )
            total -= sum(self.number_value(column) for column in formula["subtract"])
            self.set_widget_value(self.widgets[target], f"{total:,.2f}")

    def number_value(self, column: str) -> float:
        value = self.widgets[column].get().replace(",", "").strip()
        try:
            return float(value or 0)
        except ValueError:
            return 0.0

    def value(self, column: str) -> Any:
        value = self.widgets[column].get().strip()
        if column in self.config.get("number_fields", []):
            value = value.replace(",", "").replace(".", "") if self.config.get(
                "decimal_separator"
            ) == "," else value.replace(",", "")
        if column in self.config.get("month_fields", []):
            return datetime.strptime(value, "%d/%m/%Y").strftime("%Y-%m")
        if column in self.config.get("date_fields", {}):
            pattern = self.config["date_fields"][column]
            if pattern == "dd/mm/yyyy":
                return datetime.strptime(value, "%d/%m/%Y").strftime("%Y-%m-%d")
        return self.foreign_values.get(column, {}).get(value, value or None)

    def format_display_value(self, column: str, value: Any) -> Any:
        if value is None or column not in self.config.get("money_fields", []):
            return value
        try:
            return f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return value

    def missing_required_columns(self) -> list[str]:
        missing = []
        required_columns = self.config.get(
            "required_columns",
            [
                column for column in self.config["input_columns"]
                if column not in self.config.get("computed_fields", {})
            ],
        )
        for column in required_columns:
            widget = self.widgets[column]
            if not widget.get().strip():
                missing.append(self.config["labels"][column])
        return missing

    def invalid_columns(self) -> list[str]:
        errors = []
        for column, rule in self.config.get("validation", {}).items():
            value = self.widgets[column].get().strip()
            if rule == "name" and not re.fullmatch(r"[^\W\d_]{2,}(?:[\s'-]+[^\W\d_]{2,})+", value, re.UNICODE):
                errors.append(f"{self.config['labels'][column]} (nhập ít nhất họ và tên, chỉ dùng chữ)")
            elif rule == "phone" and not re.fullmatch(r"0\d{9}", value):
                errors.append(f"{self.config['labels'][column]} (phải đúng 10 chữ số và bắt đầu bằng 0)")
            elif rule == "email" and not re.fullmatch(r"[a-z0-9][a-z0-9._%+-]*@[a-z0-9.-]+\.[a-z]{2,}", value):
                errors.append(f"{self.config['labels'][column]} (phải viết thường, ví dụ: ten@congty.com)")
        return errors

    def selected_id(self) -> Any:
        selected = self.tree.selection()
        return self.tree.item(selected[0], "values")[0] if selected else None

    def add(self) -> None:
        missing = self.missing_required_columns()
        if missing:
            messagebox.showwarning(
                "Thiếu thông tin",
                "Vui lòng nhập/chọn: " + ", ".join(missing),
            )
            return
        invalid = self.invalid_columns()
        if invalid:
            messagebox.showwarning(
                "Dữ liệu không hợp lệ",
                "Vui lòng kiểm tra: " + ", ".join(invalid),
            )
            return
        columns = [
            column for column in self.config["input_columns"]
            if column not in self.config.get("computed_fields", {})
        ]
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
        missing = self.missing_required_columns()
        if missing:
            messagebox.showwarning(
                "Thiếu thông tin",
                "Vui lòng nhập/chọn: " + ", ".join(missing),
            )
            return
        invalid = self.invalid_columns()
        if invalid:
            messagebox.showwarning(
                "Dữ liệu không hợp lệ",
                "Vui lòng kiểm tra: " + ", ".join(invalid),
            )
            return
        columns = [
            column for column in self.config["input_columns"]
            if column not in self.config.get("computed_fields", {})
        ]
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


class TimePicker(ttk.Frame):
    """Bộ chọn giờ đơn giản gồm giờ và phút như TimePicker."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.hour = tk.StringVar(value="08")
        self.minute = tk.StringVar(value="00")
        ttk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hour, width=4, format="%02.0f").pack(side="left")
        ttk.Label(self, text=":", padding=(3, 0)).pack(side="left")
        ttk.Spinbox(self, from_=0, to=59, increment=1, wrap=True, textvariable=self.minute, width=4, format="%02.0f").pack(side="left")

    def get(self) -> str:
        return f"{int(self.hour.get()):02d}:{int(self.minute.get()):02d}"

    def delete(self, _start: int = 0, _end: str | None = None) -> None:
        self.hour.set("08")
        self.minute.set("00")

    def insert(self, _index: int, value: str) -> None:
        parts = str(value).split(":")
        self.hour.set(parts[0].zfill(2))
        self.minute.set((parts[1] if len(parts) > 1 else "00").zfill(2))

    def set(self, value: str) -> None:
        self.insert(0, value)