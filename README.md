# Phần mềm Quản lý Ngân hàng Câu hỏi & Tạo Đề thi LaTeX

Phần mềm giao diện đồ họa (GUI) hỗ trợ giáo viên tự động hóa quá trình quản lý ngân hàng câu hỏi trắc nghiệm/tự luận LaTeX và xuất đề thi ngẫu nhiên dựa trên cấu trúc ma trận. 

Giao diện được thiết kế hiện đại, hỗ trợ Dark Mode và tối ưu hóa trải nghiệm người dùng (UX) thông qua thư viện `customtkinter`.

---

## 🌟 Tính năng nổi bật

1. **Quét & Nạp dữ liệu tự động:** Tự động đọc hàng loạt tệp `.tex` trong thư mục, nhận diện các khối câu hỏi `\begin{ex}` và chuẩn hóa mã ID.
2. **Cơ sở dữ liệu thông minh:** Lưu trữ cục bộ toàn bộ câu hỏi vào tệp `database.json`, giúp việc truy xuất cực kỳ nhanh chóng.
3. **Bốc câu hỏi theo Ma trận:** Cho phép người dùng thiết lập số lượng câu hỏi cần bốc cho từng dạng (thông qua Tiền tố ID). Thuật toán bốc ngẫu nhiên đảm bảo các mã đề không bị trùng lặp câu hỏi.
4. **Phân loại tự động:** Tự động nhận diện câu hỏi Trắc nghiệm nhiều phương án (`\choice`), Đúng/Sai (`\choiceTF`) và Tự luận (Điền khuyết) để sắp xếp vào đúng bố cục.
5. **Xuất file LaTeX chuẩn:** Tạo ra các tệp `.tex` đề thi hoán vị sẵn sàng để biên dịch, tích hợp tự động mã đáp án.

---

## 📂 Cấu trúc thư mục dự án

Dự án được tổ chức theo chuẩn mô-đun hóa, tách biệt rõ ràng giữa Giao diện (Frontend) và Xử lý logic (Backend):

```text
📁 Thu-muc-du-an/
│
├── 📄 app.py               # Chạy phần mềm (Giao diện người dùng CTk)
├── 📄 data_process.py      # Module xử lý dữ liệu (Quét tệp, Đọc/Ghi JSON)
├── 📄 tao_de.py            # Module tạo đề (Lắp ráp khung LaTeX, phân loại)
│
├── 📄 database.json        # Cơ sở dữ liệu lưu trữ câu hỏi (Sinh tự động)
├── 📄 README.md            # Tài liệu hướng dẫn sử dụng
│
├── 📁 data/                # Nơi chứa các tệp .tex câu hỏi nguồn (Đầu vào)
└── 📁 output/              # Nơi chứa các tệp .tex đề thi đã tạo (Đầu ra)

```

---

## ⚙️ Hướng dẫn Cài đặt

Phần mềm yêu cầu Python 3.x và thư viện giao diện `customtkinter`.

**Bước 1:** Cài đặt thư viện yêu cầu thông qua Terminal / Command Prompt:

```bash
pip install customtkinter

```

**Bước 2:** Khởi chạy phần mềm:

```bash
python app.py

```

---

## 🚀 Hướng dẫn Sử dụng

### 1. Nạp Dữ Liệu Ngân Hàng

* Đặt các tệp LaTeX chứa câu hỏi (định dạng `.tex`) vào thư mục `data/` (hoặc bất kỳ thư mục nào trên máy).
* Mở phần mềm, chuyển sang Tab **Nạp Dữ Liệu**.
* Bấm **Mở Thư Mục** để trỏ đến thư mục chứa câu hỏi.
* Bấm **QUÉT VÀ CẬP NHẬT**. Phần mềm sẽ đọc và lưu toàn bộ câu hỏi vào hệ thống.

*Lưu ý về chuẩn dữ liệu:* Mỗi câu hỏi phải nằm trong môi trường `\begin{ex}... \end{ex}` và chứa mã ID ở dòng đầu tiên. Ví dụ: `\begin{ex}%[2D4H2-5]`

### 2. Tạo Đề Thi

* Chuyển sang Tab **Tạo Đề Thi**.
* Điền thông tin tiêu đề: Môn học, Tên đề, Mã đáp án gốc và số lượng đề cần tạo (số hoán vị).
* Thêm cấu trúc ma trận:
* Nhập **Tiền tố ID** (Ví dụ: `2D` để bốc câu hỏi Toán lớp 12 Giải tích, hoặc `2D4H` cho mức độ cụ thể hơn).
* Nhập **Số lượng** câu hỏi muốn bốc cho tiền tố đó.
* Bấm **Thêm**. Lặp lại cho đến khi đủ cấu trúc đề thi.


* Bấm **TẠO ĐỀ THI**. Các tệp kết quả sẽ xuất hiện trong thư mục `output/`.

---

## 🛠 Lỗi thường gặp

* **`PermissionError` khi lưu JSON:** Đảm bảo tệp `database.json` không bị mở bởi một phần mềm khác (như Excel hay Notepad) trong lúc bấm Nạp dữ liệu.
* **Không tìm thấy câu hỏi phù hợp:** Đảm bảo Tiền tố ID bạn nhập trên giao diện khớp chính xác với mã ID có trong các tệp `.tex` nguồn. Kiểm tra phân biệt chữ hoa/chữ thường.