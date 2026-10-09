"""Các thao tác kết nối và truy vấn MySQL."""

import os
import hashlib
import hmac
import secrets
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
    """Kết nối MySQL"""

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

    def register_user(self, username: str, password: str, full_name: str) -> None:
        """Tạo tài khoản mới với mật khẩu đã được băm và salt riêng."""
        salt = secrets.token_bytes(16)
        password_hash = _hash_password(password, salt)
        try:
            self.execute(
                "INSERT INTO nguoi_dung "
                "(ten_dang_nhap, mat_khau_hash, salt, ho_ten, vai_tro) "
                "VALUES (%s, %s, %s, %s, %s)",
                (username, password_hash, salt, full_name, "user"),
            )
        except RuntimeError as error:
            if "Duplicate entry" in str(error):
                raise ValueError("Tên đăng nhập đã tồn tại.") from error
            raise

    def authenticate_user(self, username: str, password: str) -> dict[str, Any] | None:
        """Trả về tài khoản hợp lệ, hoặc None nếu thông tin đăng nhập sai."""
        rows = self.fetch_all(
            "SELECT ma_nguoi_dung, ten_dang_nhap, mat_khau_hash, salt, ho_ten, vai_tro "
            "FROM nguoi_dung WHERE ten_dang_nhap=%s AND trang_thai='Hoat dong'",
            (username,),
        )
        if not rows:
            return None
        account = rows[0]
        expected = _hash_password(password, account["salt"])
        if not hmac.compare_digest(expected, account["mat_khau_hash"]):
            return None
        return account

    def test_connection(self) -> tuple[bool, str]:
        try:
            with self.connection() as connection:
                if connection.is_connected():
                    return True, "Đã kết nối MySQL"
        except (RuntimeError, Error) as error:
            return False, str(error)
        return False, "Không thể kết nối MySQL"


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 600_000
    )
