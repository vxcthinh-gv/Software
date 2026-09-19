# Phần mềm Quản lý và Tạo đề thi LaTeX tự động

Dự án này là một bộ công cụ dòng lệnh (CLI) được viết bằng Python, giúp tự động hóa toàn bộ quy trình quản lý ngân hàng câu hỏi định dạng LaTeX. Phần mềm cho phép trích xuất dữ liệu, xây dựng cơ sở dữ liệu siêu tốc và tự động sinh đề thi theo ma trận cấu trúc với nhiều mã đề hoán vị.

## Tính năng nổi bật

* **Chuẩn hóa & Lưu trữ thông minh (Parsing & Storage):** Tự động quét các tệp `.tex` gốc, làm sạch các thẻ thông tin thừa để chỉ giữ lại mã ID chuẩn, và lưu vào cơ sở dữ liệu `database.json` giúp tốc độ truy xuất tức thì ở các lần chạy sau.
* **Sinh đề theo Ma trận (Matrix Auto-pick):** Bốc ngẫu nhiên số lượng câu hỏi chính xác dựa trên tiền tố ID (Ví dụ: `2D4H` - Lớp 12, Đại số, Chương 4, Thông hiểu) mà không bị trùng lặp.
* **Tự động phân loại (Auto-Categorization):** Nhận diện cú pháp LaTeX để tự động xếp câu hỏi vào 3 phần riêng biệt:
* Trắc nghiệm (Chứa thẻ `\choice`)
* Đúng/Sai (Chứa thẻ `\choiceTF` hoặc `\choicetf`)
* Điền khuyết (Không chứa thẻ trắc nghiệm)


* **Hoán vị đa dạng (Shuffle & Permutation):** Tự động xáo trộn vị trí câu hỏi và nhân bản thành nhiều mã đề thi khác nhau chỉ với một lần nhập lệnh.

## Cấu trúc thư mục

Để phần mềm hoạt động trơn tru, cấu trúc thư mục cần được tổ chức như sau:

```text
thu_muc_du_an/
│
├── data/                   # Thư mục chứa các tệp .tex gốc (Ngân hàng câu hỏi)
├── output/                 # Thư mục xuất các đề thi mới và file đáp án
│
├── main.py                 # Mã lệnh quét dữ liệu, làm sạch ID và tạo database
├── tao_de.py               # Mã lệnh tương tác nhập ma trận và tạo đề thi
├── database.json           # (Tự động sinh) Cơ sở dữ liệu lưu trữ
└── README.md               # Tệp tài liệu hướng dẫn

```

## Yêu cầu về cấu trúc câu hỏi gốc

Các câu hỏi đầu vào trong thư mục `data/` cần tuân thủ nghiêm ngặt định dạng sau:

1. Nằm trọn vẹn trong môi trường `\begin{ex}` và `\end{ex}`.
2. Chứa mã ID có định dạng `%[Tham số - Tham số]` (bắt buộc có dấu gạch ngang). Ví dụ: `%[2D4H2-5]`.
3. *Lưu ý:* Phần mềm sẽ tự động loại bỏ các tag thừa (như `%[Tên tác giả]`) nằm trước mã ID chính thức trong quá trình nạp dữ liệu.

## Hướng dẫn sử dụng

### Bước 1: Quét và Xây dựng Cơ sở dữ liệu

Thực hiện bước này lần đầu tiên hoặc mỗi khi bạn cập nhật thêm câu hỏi mới vào thư mục `data/`.

1. Chép tất cả các tệp `.tex` chứa ngân hàng câu hỏi vào thư mục `data/`.
2. Mở Terminal / Command Prompt tại thư mục dự án và chạy lệnh:
```bash
python main.py

```


3. Hệ thống sẽ báo cáo số lượng câu hỏi được trích xuất và tạo ra tệp `database.json`.

### Bước 2: Tạo đề thi tự động theo Ma trận

1. Chạy lệnh sau trên Terminal:
```bash
python tao_de.py

```


2. Cung cấp các thông số định dạng đề thi:
* **Môn học:** (VD: Toán)
* **Tên đề:** (VD: Đề kiểm tra Chương 2)
* **Mã gốc file đáp án:** (VD: De01)


3. Nhập ma trận đề thi:
* Nhập lần lượt các **Tiền tố ID** (VD: `2D4H`) và **Số lượng** mong muốn.
* Gõ `xong` khi đã hoàn tất việc nhập ma trận.


4. Nhập số lượng mã đề hoán vị cần tạo (VD: `4`).
5. Phần mềm sẽ tự động xáo trộn và sinh ra các tệp `.tex` hoàn chỉnh (ví dụ: `dethi_moi_1.tex`, `dethi_moi_2.tex`...) trong thư mục `output/`. Bạn chỉ cần biên dịch các tệp này để lấy file PDF.