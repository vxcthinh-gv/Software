import os
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk

# Nhập hàm từ các module lõi (Giữ nguyên cấu trúc dự án của bạn)
from data_process import parse_latex_files, save_database
from tao_de import load_database, auto_pick_questions, create_exam

# Thiết lập UI mặc định: Chế độ Tối và tông màu Xanh dương
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class AppTaoDe:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Ngân hàng Câu hỏi LaTeX")
        self.root.geometry("750x820")
        
        self.ma_tran_list = []
        self.db = load_database('database.json') or {}
        
        self.build_ui()

    def build_ui(self):
        # Font chữ dùng chung
        self.font_title = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_main = ctk.CTkFont(family="Segoe UI", size=13)
        
        # Tabview hiện đại
        self.tabview = ctk.CTkTabview(self.root, width=700, height=750, corner_radius=10)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tab_tao_de = self.tabview.add("Tạo Đề Thi")
        self.tab_nap_data = self.tabview.add("Nạp Dữ Liệu")
        
        self.build_tab_tao_de()
        self.build_tab_nap_data()

    # ==========================================
    # TAB 1: TẠO ĐỀ THI
    # ==========================================
    def build_tab_tao_de(self):
        # --- Khung 1: Thông tin Đề thi ---
        frame_info = ctk.CTkFrame(self.tab_tao_de, corner_radius=10)
        frame_info.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_info, text="1. Thông tin Đề thi", font=self.font_title).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 5))

        ctk.CTkLabel(frame_info, text="Môn học:", font=self.font_main).grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.entry_mon_hoc = ctk.CTkEntry(frame_info, width=350, font=self.font_main)
        self.entry_mon_hoc.grid(row=1, column=1, padx=15, pady=5)

        ctk.CTkLabel(frame_info, text="Tên đề thi:", font=self.font_main).grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.entry_ten_de = ctk.CTkEntry(frame_info, width=350, font=self.font_main)
        self.entry_ten_de.grid(row=2, column=1, padx=15, pady=5)

        ctk.CTkLabel(frame_info, text="Mã đáp án gốc:", font=self.font_main).grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.entry_ma_dap_an = ctk.CTkEntry(frame_info, width=350, font=self.font_main)
        self.entry_ma_dap_an.grid(row=3, column=1, padx=15, pady=5)
        
        ctk.CTkLabel(frame_info, text="Số lượng đề (Hoán vị):", font=self.font_main).grid(row=4, column=0, sticky="w", padx=15, pady=(5, 15))
        self.entry_so_luong_de = ctk.CTkEntry(frame_info, width=100, font=self.font_main)
        self.entry_so_luong_de.insert(0, "1")
        self.entry_so_luong_de.grid(row=4, column=1, sticky="w", padx=15, pady=(5, 15))

        # --- Khung 2: Ma trận ---
        frame_matrix = ctk.CTkFrame(self.tab_tao_de, corner_radius=10)
        frame_matrix.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(frame_matrix, text="2. Cấu trúc Ma trận", font=self.font_title).pack(anchor="w", padx=15, pady=(10, 5))

        toolbar_frame = ctk.CTkFrame(frame_matrix, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(toolbar_frame, text="Tiền tố ID:", font=self.font_main).pack(side="left")
        self.entry_prefix = ctk.CTkEntry(toolbar_frame, width=120, font=self.font_main)
        self.entry_prefix.pack(side="left", padx=10)

        ctk.CTkLabel(toolbar_frame, text="Số lượng:", font=self.font_main).pack(side="left")
        self.entry_count = ctk.CTkEntry(toolbar_frame, width=80, font=self.font_main)
        self.entry_count.pack(side="left", padx=10)

        btn_add = ctk.CTkButton(toolbar_frame, text="Thêm", width=80, fg_color="#28A745", hover_color="#218838", font=self.font_main, command=self.add_to_matrix)
        btn_add.pack(side="left", padx=5)
        
        btn_clear = ctk.CTkButton(toolbar_frame, text="Xóa", width=80, fg_color="#DC3545", hover_color="#C82333", font=self.font_main, command=self.clear_matrix)
        btn_clear.pack(side="left", padx=5)

        # Hộp hiển thị danh sách (Dùng Textbox thay thế cho Listbox cũ)
        self.textbox_matrix = ctk.CTkTextbox(frame_matrix, height=120, font=self.font_main, state="disabled")
        self.textbox_matrix.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        # --- Nút Xử lý ---
        btn_generate = ctk.CTkButton(self.tab_tao_de, text="🚀 TẠO ĐỀ THI", height=50, font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), command=self.generate_exams)
        btn_generate.pack(fill="x", padx=10, pady=15)

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
        
        # Mở khóa Textbox, thêm nội dung, khóa lại
        self.textbox_matrix.configure(state="normal")
        self.textbox_matrix.insert("end", f"  🔹 Mã ID: {prefix:<15} | Số lượng: {count} câu\n")
        self.textbox_matrix.configure(state="disabled")
        
        self.entry_prefix.delete(0, tk.END)
        self.entry_count.delete(0, tk.END)
        self.entry_prefix.focus()
        
    def clear_matrix(self):
        self.ma_tran_list.clear()
        self.textbox_matrix.configure(state="normal")
        self.textbox_matrix.delete("1.0", "end")
        self.textbox_matrix.configure(state="disabled")

    def generate_exams(self):
        if not self.db:
            messagebox.showerror("Lỗi", "Ngân hàng trống. Hãy sang Tab 'Nạp Dữ Liệu'.")
            return
            
        mon_hoc = self.entry_mon_hoc.get().strip()
        ten_de = self.entry_ten_de.get().strip()
        ma_dap_an = self.entry_ma_dap_an.get().strip()
        
        try:
            so_luong_de = int(self.entry_so_luong_de.get().strip())
            if so_luong_de < 1: raise ValueError
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số lượng đề phải lớn hơn 0.")
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
            messagebox.showerror("Lỗi", "Không tìm thấy câu hỏi phù hợp với ma trận.")
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

        messagebox.showinfo("Hoàn tất", f"Tạo thành công {thanh_cong}/{so_luong_de} đề thi.")

    # ==========================================
    # TAB 2: NẠP DỮ LIỆU
    # ==========================================
    def build_tab_nap_data(self):
        # Khung chứa nội dung tab 2
        frame_nap = ctk.CTkFrame(self.tab_nap_data, corner_radius=10)
        frame_nap.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_nap, text="🗄️ QUẢN LÝ NGÂN HÀNG DỮ LIỆU", font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")).pack(pady=(30, 20))
        
        so_luong_hien_tai = len(self.db) if self.db else 0
        self.lbl_status = ctk.CTkLabel(frame_nap, text=f"Tổng số câu hỏi: {so_luong_hien_tai} câu", text_color="#28A745", font=self.font_title)
        self.lbl_status.pack(pady=10)

        frame_folder = ctk.CTkFrame(frame_nap, fg_color="transparent")
        frame_folder.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(frame_folder, text="Thư mục chứa file .tex:", font=self.font_main).pack(anchor="w", pady=(0, 5))
        
        box_folder = ctk.CTkFrame(frame_folder, fg_color="transparent")
        box_folder.pack(fill="x")
        self.entry_folder = ctk.CTkEntry(box_folder, font=self.font_main)
        self.entry_folder.insert(0, "data")
        self.entry_folder.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_browse = ctk.CTkButton(box_folder, text="Mở Thư Mục", width=100, font=self.font_main, command=self.browse_folder)
        btn_browse.pack(side="right")

        btn_update = ctk.CTkButton(frame_nap, text="🔄 QUÉT VÀ CẬP NHẬT", height=50, font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), command=self.update_database)
        btn_update.pack(pady=40)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, folder_selected)

    def update_database(self):
        folder_path = self.entry_folder.get().strip()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showerror("Lỗi", "Đường dẫn thư mục không hợp lệ.")
            return
            
        self.lbl_status.configure(text="⏳ Đang xử lý...", text_color="#FFC107")
        self.root.update()
            
        du_lieu_moi, so_file = parse_latex_files(folder_path)
        so_luong = len(du_lieu_moi)
        
        if so_luong > 0:
            thanh_cong, thong_bao_loi = save_database(du_lieu_moi, 'database.json')
            if thanh_cong:
                self.db = du_lieu_moi
                self.lbl_status.configure(text=f"Tổng số câu hỏi: {so_luong} câu", text_color="#28A745")
                messagebox.showinfo("Thành công", f"Quét {so_file} file.\nThu được: {so_luong} câu hỏi.")
            else:
                self.lbl_status.configure(text="❌ Lỗi lưu dữ liệu!", text_color="#DC3545")
                messagebox.showerror("Lỗi", f"Chi tiết: {thong_bao_loi}")
        else:
            self.lbl_status.configure(text=f"Tổng số câu hỏi: {len(self.db)} câu", text_color="#DC3545")
            messagebox.showwarning("Kết quả", "Không tìm thấy câu hỏi hợp lệ.")

if __name__ == "__main__":
    # Khởi tạo cửa sổ chính bằng CTk
    root = ctk.CTk()
    app = AppTaoDe(root)
    root.mainloop()