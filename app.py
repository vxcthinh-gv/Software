import os
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog

# Nhập tất cả các hàm cần thiết từ các module đã chia nhỏ
from data_process import parse_latex_files, save_database
from tao_de import create_exam, load_database, auto_pick_questions

class AppTaoDe:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm Quản lý Ngân hàng Câu hỏi LaTeX")
        self.root.geometry("650x700")
        
        self.ma_tran_list = []
        self.db = load_database('database.json') or {}
        
        self.build_ui()

    def build_ui(self):
        # Tạo công cụ quản lý Tab (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tạo 2 Frame đại diện cho 2 Tab
        self.tab_tao_de = ttk.Frame(self.notebook)
        self.tab_nap_data = ttk.Frame(self.notebook)
        
        # Thêm Tab vào Notebook
        self.notebook.add(self.tab_tao_de, text="Tạo Đề Thi")
        self.notebook.add(self.tab_nap_data, text="Nạp Dữ Liệu Ngân Hàng")
        
        # Xây dựng nội dung cho từng Tab
        self.build_tab_tao_de()
        self.build_tab_nap_data()

    # ==========================================
    # TAB 1: TẠO ĐỀ THI
    # ==========================================
    def build_tab_tao_de(self):
        # --- Frame Thông tin chung ---
        frame_info = tk.LabelFrame(self.tab_tao_de, text="1. Thông tin Đề thi", padx=10, pady=10)
        frame_info.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_info, text="Môn học:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_mon_hoc = tk.Entry(frame_info, width=40)
        self.entry_mon_hoc.grid(row=0, column=1, pady=2)

        tk.Label(frame_info, text="Tên đề thi:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_ten_de = tk.Entry(frame_info, width=40)
        self.entry_ten_de.grid(row=1, column=1, pady=2)

        tk.Label(frame_info, text="Mã đáp án gốc:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_ma_dap_an = tk.Entry(frame_info, width=40)
        self.entry_ma_dap_an.grid(row=2, column=1, pady=2)
        
        tk.Label(frame_info, text="Số lượng đề (Hoán vị):").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_so_luong_de = tk.Entry(frame_info, width=10)
        self.entry_so_luong_de.insert(0, "1")
        self.entry_so_luong_de.grid(row=3, column=1, sticky="w", pady=2)

        # --- Frame Ma trận ---
        frame_matrix = tk.LabelFrame(self.tab_tao_de, text="2. Cấu trúc Ma trận", padx=10, pady=10)
        frame_matrix.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(frame_matrix, text="Tiền tố ID:").grid(row=0, column=0, sticky="w")
        self.entry_prefix = tk.Entry(frame_matrix, width=15)
        self.entry_prefix.grid(row=0, column=1, padx=5)

        tk.Label(frame_matrix, text="Số lượng:").grid(row=0, column=2, sticky="w")
        self.entry_count = tk.Entry(frame_matrix, width=10)
        self.entry_count.grid(row=0, column=3, padx=5)

        btn_add = tk.Button(frame_matrix, text="Thêm", command=self.add_to_matrix)
        btn_add.grid(row=0, column=4, padx=10)
        
        btn_clear = tk.Button(frame_matrix, text="Xóa", command=self.clear_matrix)
        btn_clear.grid(row=0, column=5, padx=5)

        self.listbox_matrix = tk.Listbox(frame_matrix, height=10)
        self.listbox_matrix.grid(row=1, column=0, columnspan=6, sticky="we", pady=10)

        # --- Frame Xử lý ---
        frame_action = tk.Frame(self.tab_tao_de, pady=10)
        frame_action.pack(fill="x")

        btn_generate = tk.Button(frame_action, text="TẠO ĐỀ THI", font=("Arial", 14, "bold"), bg="green", fg="white", command=self.generate_exams)
        btn_generate.pack(ipadx=20, ipady=10)

    def add_to_matrix(self):
        prefix = self.entry_prefix.get().strip()
        count_str = self.entry_count.get().strip()

        if not prefix or not count_str:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ Tiền tố và Số lượng.")
            return

        try:
            count = int(count_str)
            if count <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số lượng phải là số nguyên dương.")
            return

        self.ma_tran_list.append((prefix, count))
        self.listbox_matrix.insert(tk.END, f"Mã ID: {prefix} | Số lượng: {count} câu")
        
        self.entry_prefix.delete(0, tk.END)
        self.entry_count.delete(0, tk.END)
        self.entry_prefix.focus()
        
    def clear_matrix(self):
        self.ma_tran_list.clear()
        self.listbox_matrix.delete(0, tk.END)

    def generate_exams(self):
        if not self.db:
            messagebox.showerror("Lỗi", "Ngân hàng câu hỏi trống. Vui lòng sang Tab 'Nạp Dữ Liệu' để cập nhật.")
            return
            
        mon_hoc = self.entry_mon_hoc.get().strip()
        ten_de = self.entry_ten_de.get().strip()
        ma_dap_an = self.entry_ma_dap_an.get().strip()
        
        try:
            so_luong_de = int(self.entry_so_luong_de.get().strip())
            if so_luong_de < 1: raise ValueError
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số lượng đề phải là số nguyên lớn hơn 0.")
            return

        if not mon_hoc or not ten_de or not ma_dap_an:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ Thông tin Đề thi.")
            return

        if not self.ma_tran_list:
            messagebox.showwarning("Cảnh báo", "Danh sách ma trận đang trống.")
            return

        danh_sach_id_cuoi_cung = []
        for prefix, count in self.ma_tran_list:
            ids_duoc_chon = auto_pick_questions(self.db, prefix, count)
            danh_sach_id_cuoi_cung.extend(ids_duoc_chon)

        if not danh_sach_id_cuoi_cung:
            messagebox.showerror("Lỗi", "Không tìm thấy câu hỏi nào phù hợp với ma trận yêu cầu.")
            return

        thanh_cong = 0
        thu_muc_output = 'output'
        
        for i in range(1, so_luong_de + 1):
            ids_ban_sao = danh_sach_id_cuoi_cung.copy()
            if so_luong_de > 1:
                random.shuffle(ids_ban_sao)
                ten_file = f"dethi_moi_{i}.tex"
                ma_dap_an_hien_tai = f"{ma_dap_an}_{i}"
            else:
                ten_file = "dethi_moi.tex"
                ma_dap_an_hien_tai = ma_dap_an
                
            duong_dan_file = os.path.join(thu_muc_output, ten_file)
            kq = create_exam(ids_ban_sao, self.db, duong_dan_file, mon_hoc, ten_de, ma_dap_an_hien_tai)
            if kq: thanh_cong += 1

        messagebox.showinfo("Hoàn tất", f"Đã bốc tổng cộng {len(danh_sach_id_cuoi_cung)} câu hỏi.\nTạo thành công {thanh_cong}/{so_luong_de} đề thi trong thư mục 'output'.")

    # ==========================================
    # TAB 2: NẠP DỮ LIỆU
    # ==========================================
    def build_tab_nap_data(self):
        frame_nap = tk.Frame(self.tab_nap_data, padx=20, pady=20)
        frame_nap.pack(fill="both", expand=True)

        tk.Label(frame_nap, text="QUẢN LÝ NGÂN HÀNG CÂU HỎI", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Nhãn hiển thị trạng thái hiện tại
        so_luong_hien_tai = len(self.db)
        self.lbl_status = tk.Label(frame_nap, text=f"Số lượng câu hỏi hiện có trong hệ thống: {so_luong_hien_tai} câu", fg="blue", font=("Arial", 11))
        self.lbl_status.pack(pady=10)

        # Chọn thư mục
        frame_folder = tk.Frame(frame_nap)
        frame_folder.pack(fill="x", pady=10)
        
        tk.Label(frame_folder, text="Thư mục chứa file .tex:").pack(side="left")
        self.entry_folder = tk.Entry(frame_folder, width=40)
        self.entry_folder.insert(0, "data") # Mặc định là thư mục data
        self.entry_folder.pack(side="left", padx=10)
        
        btn_browse = tk.Button(frame_folder, text="Chọn Thư Mục...", command=self.browse_folder)
        btn_browse.pack(side="left")

        # Nút bấm thực thi
        btn_update = tk.Button(frame_nap, text="CẬP NHẬT DỮ LIỆU", font=("Arial", 12, "bold"), bg="orange", command=self.update_database)
        btn_update.pack(pady=30, ipadx=10, ipady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, folder_selected)

    def update_database(self):
        folder_path = self.entry_folder.get().strip()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showerror("Lỗi", "Đường dẫn thư mục không hợp lệ hoặc không tồn tại.")
            return
            
        messagebox.showinfo("Đang xử lý", "Hệ thống đang quét dữ liệu. Quá trình này có thể mất vài giây...")
        
        # Gọi hàm quét dữ liệu từ data_process.py
        du_lieu_moi = parse_latex_files(folder_path)
        so_luong = len(du_lieu_moi)
        
        if so_luong > 0:
            # Lưu ra file JSON
            save_database(du_lieu_moi, 'database.json')
            
            # Cập nhật bộ nhớ chương trình
            self.db = du_lieu_moi
            self.lbl_status.config(text=f"Số lượng câu hỏi hiện có trong hệ thống: {so_luong} câu")
            messagebox.showinfo("Thành công", f"Đã quét và cập nhật thành công {so_luong} câu hỏi vào ngân hàng!")
        else:
            messagebox.showwarning("Kết quả", "Không tìm thấy câu hỏi hợp lệ nào trong thư mục đã chọn.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTaoDe(root)
    root.mainloop()