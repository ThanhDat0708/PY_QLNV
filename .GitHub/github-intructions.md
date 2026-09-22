PROMPT XÂY DỰNG DỰ ÁN HỆ THỐNG QUẢN LÝ NHÂN VIÊN

Bạn là một lập trình viên Python có kinh nghiệm trong việc xây dựng ứng dụng Desktop và hệ thống quản lý dữ liệu.

Hãy giúp tôi xây dựng một Hệ thống quản lý nhân viên chạy trên máy tính, sử dụng:

* Ngôn ngữ lập trình: Python
* Giao diện: Tkinter
* Database: MySQL
* Kết nối database: mysql-connector-python
* Chat Box AI: tích hợp trong giao diện Tkinter
* Dữ liệu chatbot: sử dụng dữ liệu từ chromedb.

Tôi là người mới học Python nên code phải đơn giản, dễ hiểu, có chú thích và giải thích từng phần. Không sử dụng kiến trúc hoặc kỹ thuật quá phức tạp nếu không cần thiết.

⸻

1. CHỨC NĂNG CHÍNH

Xây dựng hệ thống có các chức năng:

Quản lý nhân viên

* Thêm nhân viên
* Sửa thông tin nhân viên
* Xóa nhân viên
* Tìm kiếm nhân viên
* Xem danh sách nhân viên
* Xem thông tin chi tiết nhân viên
* Lọc nhân viên theo phòng ban
* Lọc nhân viên theo chức vụ

Quản lý phòng ban

* Thêm phòng ban
* Sửa phòng ban
* Xóa phòng ban
* Xem danh sách phòng ban

Quản lý chức vụ

* Thêm chức vụ
* Sửa chức vụ
* Xóa chức vụ
* Xem danh sách chức vụ

Quản lý chấm công

* Thêm dữ liệu chấm công
* Sửa dữ liệu chấm công
* Xóa dữ liệu chấm công
* Xem lịch sử chấm công của nhân viên

Quản lý lương

* Nhập lương
* Sửa lương
* Xóa lương
* Tính tổng lương
* Xem lịch sử lương của nhân viên

⸻

2. THIẾT KẾ DATABASE

XAMPP để chạy MySQL/MariaDB trên máy tính.
* HeidiSQL để tạo, quản lý và kiểm tra database.
* Database sử dụng MySQL.
* Python sẽ kết nối với MySQL ở bước triển khai sau.

Database gồm đúng 5 bảng chính:


### 1. Bảng Nhân viên

* Mã nhân viên
* Họ tên
* Số điện thoại
* Email
* Phòng ban
* Chức vụ

### 2. Bảng Phòng ban

* Mã phòng ban
* Tên phòng ban

### 3. Bảng Chức vụ

* Mã chức vụ
* Tên chức vụ

### 4. Bảng Chấm công

* Mã chấm công
* Mã nhân viên
* Ngày làm việc
* Giờ vào
* Giờ ra
* Trạng thái

### 5. Bảng Lương

* Mã lương
* Mã nhân viên
* Tháng
* Lương cơ bản
* Thưởng
* Tổng lương


Thiết lập Primary Key và Foreign Key hợp lý giữa các bảng.

Giải thích rõ quan hệ giữa các bảng.

⸻

3. GIAO DIỆN TKINTER

Thiết kế giao diện Tkinter hiện đại, dễ sử dụng.

Giao diện chính gồm:

+------------------------------------------------------+
|       HỆ THỐNG QUẢN LÝ NHÂN VIÊN                   |
+------------------------------------------------------+
| MENU              |                                  |
|                   |                                  |
| 👤 Nhân viên      |       Nội dung chính             |
| 🏢 Phòng ban      |                                  |
| 💼 Chức vụ        |                                  || 🕐 Chấm công      |                                  |
| 💰 Lương          |                                  |
| 🤖 Chat Box       |                                  |
|                   |                                  |
+------------------------------------------------------+

Có thể sử dụng ttk, ttk.Treeview, Frame, Label, Entry, Button, Combobox để tạo giao diện.

Giao diện cần:

* Dễ nhìn
* Bố cục rõ ràng
* Có menu điều hướng
* Có bảng hiển thị dữ liệu
* Có form nhập dữ liệu
* Có nút Thêm / Sửa / Xóa / Tìm kiếm
* Có thông báo khi thao tác thành công hoặc thất bại.

⸻

4. CHAT BOX AI

Tích hợp một Chat Box AI trực tiếp vào giao diện Tkinter.

Giao diện:

+------------------------------------------+
|              🤖 CHAT BOX                 |
+------------------------------------------+
|                                          |
| User: Công ty làm việc mấy giờ?         |
|                                          |
| AI: Công ty làm việc từ 8:00 đến 17:00, |
|     từ thứ 2 đến thứ 6.                 |
|                                          |
+------------------------------------------+
| Nhập câu hỏi...                [Gửi]     |
+------------------------------------------+

Chat Box sử dụng mô hình RAG (Retrieval-Augmented Generation) kết hợp với ChromaDB để tìm kiếm thông tin trong dữ liệu của công ty.

Nguồn dữ liệu

Tạo một thư mục:

company_data/

Trong thư mục có thể chứa:

company_data/
├── company_info.md
├── company_rules.md
└── company_policy.md

Có thể sử dụng .txt hoặc .md.

Các file này do người quản trị tự viết nội dung về công ty, ví dụ:

* Tên công ty
* Địa chỉ
* Giới thiệu công ty
* Thời gian làm việc
* Nội quy
* Chính sách
* Quy định nghỉ phép
* Quy định lương thưởng
* Thông tin phòng ban
* Quy định dành cho nhân viên
* Các thông tin khác.

ChromaDB

Khi hệ thống khởi động hoặc khi dữ liệu được cập nhật:

1. Đọc nội dung các file trong company_data.
2. Chia nội dung thành các đoạn nhỏ.
3. Đưa các đoạn dữ liệu vào ChromaDB.
4. ChromaDB tạo và lưu vector dữ liệu.
5. Khi người dùng đặt câu hỏi, hệ thống tìm kiếm các đoạn dữ liệu liên quan nhất.
6. Đưa những đoạn dữ liệu tìm được cho AI.
7. AI chỉ sử dụng những thông tin được tìm thấy để tạo câu trả lời.

Mục tiêu:

File công ty
      ↓
Đọc dữ liệu
      ↓
Chia thành các đoạn
      ↓
ChromaDB
      ↓
Người dùng đặt câu hỏi
      ↓
Tìm kiếm dữ liệu liên quan
      ↓
AI
      ↓
Câu trả lời

⸻

5. QUY TẮC TRẢ LỜI CỦA CHAT BOX

Chat Box phải tuân thủ nguyên tắc:

Chỉ trả lời dựa trên dữ liệu có trong file công ty và dữ liệu được phép truy cập từ hệ thống. Không tự bịa hoặc suy đoán thông tin.

Trường hợp 1: Có thông tin

File có:

Công ty làm việc từ 8:00 đến 17:00,
từ thứ 2 đến thứ 6.

Người dùng hỏi:

Công ty làm việc mấy giờ?

Chat Box trả lời:

Công ty làm việc từ 8:00 đến 17:00, từ thứ 2 đến thứ 6.

Trường hợp 2: Không có thông tin

File không chứa thông tin về chi nhánh Hà Nội.

Người dùng hỏi:

Công ty có chi nhánh ở Hà Nội không?

Chat Box không được tự suy đoán.

Trả lời:
Xin lỗi, tôi không tìm thấy thông tin này trong dữ liệu công ty được cung cấp.

Hoặc:

Tôi chưa có thông tin về vấn đề này trong dữ liệu hiện tại.

Trường hợp 3: Câu hỏi hoàn toàn không liên quan

Người dùng hỏi:

Thủ đô của Nhật Bản là gì?

Chat Box phải trả lời:

Xin lỗi, tôi chỉ có thể trả lời các câu hỏi dựa trên dữ liệu được cung cấp cho hệ thống.

Trường hợp 4: Có thông tin nhưng câu hỏi diễn đạt khác

Dữ liệu:

Nhân viên được nghỉ phép 12 ngày mỗi năm.

Người dùng hỏi:

Một năm nhân viên được nghỉ bao nhiêu ngày phép?

Chat Box phải tìm được nội dung tương ứng trong ChromaDB và trả lời:

Nhân viên được nghỉ phép 12 ngày mỗi năm.

Yêu cầu quan trọng

Không được để Chat Box:

* Tự bịa thông tin.
* Tự tạo dữ liệu không có trong file.
* Suy đoán khi dữ liệu không đủ.
* Trả lời như thể biết thông tin khi ChromaDB không tìm thấy dữ liệu liên quan.

Nếu không tìm thấy thông tin đủ để trả lời, phải sử dụng câu trả lời mặc định:

“Xin lỗi, tôi không tìm thấy thông tin này trong dữ liệu được cung cấp.”

Có thể cho phép thay đổi câu trả lời mặc định trong cấu hình của hệ thống.

⸻

6. KẾT HỢP VỚI MYSQL

Ngoài dữ liệu trong ChromaDB, Chat Box có thể truy vấn dữ liệu nhân viên trong MySQL khi câu hỏi liên quan đến hệ thống quản lý nhân viên.

Ví dụ:

Có bao nhiêu nhân viên trong phòng IT?

→ Truy vấn MySQL.

Nguyễn Văn A thuộc phòng ban nào?

→ Truy vấn MySQL.

Lương của Nguyễn Văn A tháng 9 là bao nhiêu?

→ Truy vấn MySQL.

Do đó Chat Box có hai nguồn dữ liệu:

                    CHAT BOX
                       │
             Phân tích câu hỏi
                       │
              ┌────────┴────────┐
              ↓                 ↓
       Dữ liệu công ty       Dữ liệu nhân viên
          ChromaDB                MySQL
              │                   │
              └────────┬──────────┘
                       ↓
                  Câu trả lời

Nếu câu hỏi thuộc dữ liệu công ty → tìm kiếm ChromaDB.

Nếu câu hỏi thuộc dữ liệu quản lý nhân viên → truy vấn MySQL.

Nếu không tìm thấy dữ liệu phù hợp ở cả hai nguồn → trả lời:

“Xin lỗi, tôi không tìm thấy thông tin này trong dữ liệu được cung cấp.”

7. AI CHATBOT

Nếu sử dụng API AI, hãy thiết kế phần chatbot sao cho API Key được lưu trong file .env, tuyệt đối không viết trực tiếp API Key vào source code.

Ví dụ:

.env
OPENAI_API_KEY=AIzaSyCBXtQslHCwamKTTXEB_Rw0DIZCiRUKp9Y
DATABASE_URL=your_database_url

Không được đưa API Key vào GitHub.


⸻

8. CẤU TRÚC PROJECT

Hãy tổ chức project rõ ràng, dễ hiểu và phù hợp với người mới học Python.

employee_management/
│
├── main.py
│
├── database/
│   └── database.py
│
├── ui/
│   ├── main_window.py
│   ├── nhanvien.py
│   ├── phongban.py
│   ├── chucvu.py
│   ├── chamcong.py
│   ├── luong.py
│   └── chatbot.py
│
├── services/
│   └── chatbot_service.py
│
├── company_data/
│   ├── company_info.md
│   ├── company_rules.md
│   └── company_policy.md
│
├── chroma_db/
│
├── .env
├── requirements.txt
└── README.md

Giải thích

main.py

File khởi động chương trình.

⸻

database/database.py

Phụ trách kết nối và thực hiện các thao tác với MySQL.

⸻

ui/

Chứa giao diện Tkinter:

* main_window.py → giao diện chính.
* nhanvien.py → giao diện quản lý nhân viên.
* phongban.py → giao diện quản lý phòng ban.
* chucvu.py → giao diện quản lý chức vụ.
* chamcong.py → giao diện chấm công.
* luong.py → giao diện quản lý lương.
* chatbot.py → giao diện Chat Box.

⸻

services/chatbot_service.py

Xử lý logic của Chat Box:

* Đọc file .md.
* Chia dữ liệu thành các đoạn.
* Lưu dữ liệu vào ChromaDB.
* Tìm kiếm dữ liệu phù hợp khi người dùng đặt câu hỏi.
* Gửi dữ liệu tìm được cho AI để tạo câu trả lời.
* Kiểm tra trường hợp không tìm thấy thông tin.

⸻

company_data/

Đây là nơi người quản trị tự viết dữ liệu về công ty.

Ví dụ:

company_info.md
company_rules.md
company_policy.md

Chat Box chỉ được sử dụng những thông tin có trong các file này.

⸻

chroma_db/

Lưu dữ liệu ChromaDB sau khi hệ thống xử lý các file trong company_data.

Không cần người dùng tự chỉnh sửa thư mục này.

⸻

9. YÊU CẦU CODE

Tôi là người mới học Python.

Vì vậy hãy viết code theo các yêu cầu:

* Code đơn giản, dễ hiểu.
* Giải thích bằng tiếng Việt.
* Giải thích chức năng của từng file.
* Giải thích các hàm quan trọng.
* Chú thích những đoạn code khó.
* Không sử dụng kiến trúc quá phức tạp nếu không cần thiết.
* Không viết toàn bộ chương trình vào một file duy nhất.
* Chia chương trình thành các file có chức năng rõ ràng.
* Code phải có thể chạy được.
* Không để các đoạn code giả.
* Không để các phần TODO quan trọng chưa thực hiện.
* Không tự ý thêm những công nghệ không cần thiết.
* Ưu tiên cách làm đơn giản để sinh viên có thể hiểu và trình bày.

Khi cung cấp code

Phải cung cấp từng file hoàn chỉnh.

Ví dụ:

main.py
sau đó đưa toàn bộ nội dung của main.py.

Tiếp theo:

database/database.py

và đưa toàn bộ nội dung của file.

Không chỉ đưa những đoạn code bị thiếu.

Sau mỗi bước, giải thích cách chạy và cách kiểm tra.

⸻

10. DATABASE

Sử dụng MySQL làm database.

Database được tạo và quản lý bằng:

* XAMPP: dùng để chạy MySQL trên máy tính.
* HeidiSQL: dùng để tạo, quản lý và kiểm tra database.

Tên database:

employee_management

Database gồm đúng 5 bảng chính:

1. Nhân Viên
2. Phòng Ban
3. Chức Vụ
4. Chấm Công
5. Lương

Hãy cung cấp SQL hoàn chỉnh để tạo database và các bảng.

SQL phải bao gồm:

* CREATE DATABASE
* CREATE TABLE
* PRIMARY KEY
* FOREIGN KEY
* NOT NULL
* UNIQUE
* Kiểu dữ liệu phù hợp.
* Quan hệ giữa các bảng.
* Một số dữ liệu mẫu để kiểm tra chương trình.

Ví dụ:

CREATE DATABASE employee_management;

Sau đó tạo lần lượt 5 bảng và thiết lập khóa chính, khóa ngoại phù hợp.

Yêu cầu

Không sử dụng PostgreSQL.

Toàn bộ hệ thống database phải sử dụng MySQL.

Python sẽ kết nối với MySQL ở bước triển khai sau.

Không cần quyết định thư viện kết nối database ngay ở bước thiết kế database.

11. CHỨC NĂNG TÌM KIẾM

Hệ thống phải có chức năng tìm kiếm nhân viên theo:

* Mã nhân viên.
* Họ tên.
* Số điện thoại.
* Email.
* Phòng ban.
* Chức vụ.

Kết quả tìm kiếm được hiển thị bằng ttk.Treeview.

Có thể cho phép người dùng nhập từ khóa và tìm kiếm theo nhiều thông tin của nhân viên.

⸻

12. DASHBOARD

Tạo màn hình Dashboard bằng Tkinter để hiển thị các thông tin tổng quan:

* Tổng nhân viên.
* Tổng số phòng ban.
* Số nhân viên có mặt hôm nay.
* Số nhân viên nghỉ hôm nay.

Ví dụ:

+------------------------------------------+
|              DASHBOARD                   |
+------------------------------------------+
| Tổng nhân viên:       100                |
| Phòng ban:              5                |
| Có mặt hôm nay:        85                |
| Nghỉ hôm nay:          15                |
+------------------------------------------+

Các số liệu trên phải được lấy trực tiếp từ cơ sở dữ liệu MySQL, không được cố định trong code.

Có thể thêm biểu đồ nếu phù hợp và không làm hệ thống quá phức tạp.

⸻

13. VALIDATION

Khi người dùng nhập dữ liệu, hệ thống phải kiểm tra:

* Không được bỏ trống họ tên.
* Mã nhân viên không được trùng.
* Email phải đúng định dạng cơ bản.
* Số điện thoại phải hợp lệ.
* Lương phải là số.
* Ngày tháng phải đúng định dạng.
* Các trường bắt buộc không được để trống.
* Không cho phép nhập dữ liệu sai kiểu.

Khi dữ liệu không hợp lệ, sử dụng messagebox của Tkinter để thông báo lỗi cho người dùng.

Ví dụ:

Mã nhân viên đã tồn tại.

hoặc:

Vui lòng nhập họ tên.

⸻

14. BẢO MẬT

Không được viết trực tiếp mật khẩu MySQL hoặc API Key vào code Python.

Sử dụng file .env để lưu thông tin cấu hình.

Ví dụ:

DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_management
DB_USER=root
DB_PASSWORD=your_password

Nếu sử dụng API AI cho Chat Box, API Key cũng phải được lưu trong .env.

Ví dụ:

AI_API_KEY=your_api_key

Không được đưa file .env lên GitHub.

Có thể thêm .env vào .gitignore.

⸻

15. HƯỚNG DẪN CÀI ĐẶT

Sau khi hoàn thành code, hãy hướng dẫn tôi từng bước:

1. Cài Python.
2. Cài XAMPP.
3. Khởi động MySQL bằng XAMPP.
4. Cài HeidiSQL nếu cần để quản lý cơ sở dữ liệu.
5. Tạo database MySQL.
6. Tạo project Python.
7. Tạo virtual environment.
8. Cài các thư viện cần thiết.
9. Thiết lập file .env.
10. Tạo các bảng trong MySQL.
11. Chạy chương trình.
12. Kiểm tra chức năng CRUD.
13. Kiểm tra Dashboard.
14. Kiểm tra Chat Box.

Cung cấp file:

requirements.txt
và hướng dẫn chính xác các lệnh cài đặt thư viện.

Các thư viện chỉ nên được lựa chọn khi cần thiết và phải giải thích ngắn gọn công dụng của từng thư viện.

⸻

16. TEST

Hãy tạo dữ liệu mẫu để tôi có thể kiểm tra hệ thống.

Cần hướng dẫn kiểm tra:

* Thêm nhân viên.
* Sửa nhân viên.
* Xóa nhân viên.
* Tìm kiếm nhân viên.
* Thêm phòng ban.
* Thêm chức vụ.
* Chấm công.
* Nhập lương.
* Kiểm tra Dashboard.
* Hỏi Chat Box thông tin trong file công ty.
* Hỏi Chat Box thông tin nhân viên trong database MySQL.

Ví dụ:

Câu hỏi:

Nguyễn Văn A thuộc phòng nào?

Kết quả:

Nguyễn Văn A thuộc phòng IT.

Nếu thông tin không tồn tại trong dữ liệu công ty hoặc database thì Chat Box không được tự đoán.

Ví dụ:

Xin lỗi, tôi chưa tìm thấy thông tin này trong dữ liệu hiện tại.

⸻

17. CÁCH TRẢ LỜI VÀ XÂY DỰNG DỰ ÁN

Hãy xây dựng dự án theo từng bước, không đưa toàn bộ code của dự án trong một lần.

Sau mỗi bước:

* Giải thích đơn giản, dễ hiểu.
* Cung cấp đầy đủ code của bước đó.
* Giải thích các file được tạo.
* Giải thích các phần code quan trọng.
* Hướng dẫn cách chạy.
* Hướng dẫn cách kiểm tra.
* Chỉ chuyển sang bước tiếp theo khi bước hiện tại đã hoàn thành.

Thứ tự thực hiện

Bước 1

Phân tích yêu cầu và thiết kế hệ thống.

Bước 2

Thiết kế ERD và giải thích quan hệ giữa 5 bảng:

* Nhân viên
* Phòng ban
* Chức vụ
* Chấm công
* Lương


Bước 3

Viết SQL MySQL để:

* Tạo database employee_management.
* Tạo 5 bảng.
* Tạo Primary Key.
* Tạo Foreign Key.
* Tạo các ràng buộc cần thiết.
* Thêm dữ liệu mẫu.

Bước 4

Tạo cấu trúc project Python.

Bước 5

Kết nối Python với MySQL.

Không sử dụng PostgreSQL.

Bước 6

Làm chức năng quản lý nhân viên:

* Thêm.
* Sửa.
* Xóa.
* Xem.
* Tìm kiếm.

Bước 7

Làm quản lý phòng ban và chức vụ.

Bước 8

Làm chức năng chấm công.

Bước 9

Làm quản lý lương.

Bước 10

Làm Dashboard.

Bước 11

Làm Chat Box đọc dữ liệu từ các file công ty bằng ChromaDB.

Bước 12

Cho Chat Box truy vấn dữ liệu nhân viên từ MySQL.

Bước 13

Tích hợp tất cả thành một ứng dụng Tkinter hoàn chỉnh.

Bước 14

Kiểm thử toàn bộ hệ thống và sửa lỗi.

Yêu cầu quan trọng

* Sử dụng Python + Tkinter + MySQL.
* MySQL được chạy thông qua XAMPP.
* Có thể sử dụng HeidiSQL để quản lý database.
* Chat Box sử dụng ChromaDB để tìm kiếm dữ liệu trong các file .md hoặc .txt.
* Chat Box có thể lấy dữ liệu nhân viên từ MySQL.
* AI không được tự bịa thông tin.
* Nếu không tìm thấy dữ liệu thì phải thông báo rõ ràng.
* Code phải đơn giản, dễ hiểu đối với người mới học Python.
* Không sử dụng kiến trúc quá phức tạp nếu không cần thiết.
* Không để mật khẩu database hoặc API Key trực tiếp trong code.
* Sử dụng .env để lưu thông tin bảo mật.
* Các chức năng phải hoạt động thực tế, không dùng dữ liệu giả cố định trong giao diện.

Ở mỗi bước, hãy giải thích tại sao làm như vậy và hướng dẫn tôi chạy thử trước khi chuyển sang bước tiếp theo.

Mục tiêu cuối cùng là tạo một ứng dụng Desktop quản lý nhân viên hoàn chỉnh bằng Python + Tkinter + Mysql, có Chat Box AI có khả năng sử dụng dữ liệu công ty và dữ liệu nhân viên để trả lời câu hỏi.