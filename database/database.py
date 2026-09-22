"""Các thao tác kết nối và truy vấn MySQL."""

import os
from contextlib import contextmanager
from typing import Any, Iterator

from dotenv import load_dotenv

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:  # Cho phép mở giao diện trước khi cài dependency.
    mysql = None
    Error = Exception

load_dotenv()


class Database:
    """Kết nối MySQL đơn giản, dùng lại cho các màn hình quản lý."""

    def __init__(self) -> None:
        self.config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "employee_management"),
        }

    @contextmanager
    def connection(self) -> Iterator[Any]:
        if "mysql" not in globals() or mysql is None:
            raise RuntimeError(
                "Chưa cài mysql-connector-python. Hãy chạy: pip install -r requirements.txt"
            )
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
            yield connection
        except Error as error:
            raise RuntimeError(f"Không thể kết nối MySQL: {error}") from error
        finally:
            if connection and connection.is_connected():
                connection.close()

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        with self.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            return list(rows)

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> int:
        with self.connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows

    def test_connection(self) -> tuple[bool, str]:
        try:
            with self.connection() as connection:
                if connection.is_connected():
                    return True, "Đã kết nối MySQL"
        except (RuntimeError, Error) as error:
            return False, str(error)
        return False, "Không thể kết nối MySQL"
