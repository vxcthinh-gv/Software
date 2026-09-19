import os
import random
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import customtkinter as ctk

from data_process import parse_latex_files, save_database, load_structure
from tao_de import load_database, auto_pick_questions, create_exam

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class AppTaoDe:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Ngân hàng Câu hỏi LaTeX")
        self.root.geometry("1150x820") 
        
        self.ma_tran_list = []
        self.db = load_database('database.json') or {}
        self.structure_data = load_structure('cau_truc_chuong_trinh.json')
        
        self.build_ui()

    def build_ui(self):
        self.font_title = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_main = ctk.CTkFont(family="Segoe UI", size=13)
        
        self.tabview = ctk.CTkTabview(self.root, corner_radius=10)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.tab_tao_de = self.tabview.add("Tạo Đề Thi")
        self.tab_nap_data = self.tabview.add("Nạp Dữ Liệu")
        
        self.build_tab_tao_de()
        self.build_tab_nap_data()

    def build_tab_tao_de(self):
        # --- CỘT TRÁI (CÂY THƯ MỤC) ---
        left_frame = ctk.CTkFrame(self.tab_tao_de, corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        ctk.CTkLabel(left_frame, text="📖 Cấu trúc Chương trình", font=self.font_title).pack(pady=(10, 5))
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, font=("Segoe UI", 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        tree_scroll = ctk.CTkScrollbar(left_frame)
        tree_scroll.pack(side="right", fill="y", pady=10)
        
        self.tree = ttk.Treeview(left_frame, yscrollcommand=tree_scroll.set, show="tree")
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        tree_scroll.configure(command=self.tree.yview)
        
        self.populate_tree()
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # --- CỘT PHẢI (THAO TÁC) ---
        right_frame = ctk.CTkFrame(self.tab_tao_de, width=450, corner_radius=10, fg_color="transparent")
        right_frame.pack(side="right", fill="y", expand=False, padx=(5, 10), pady=10)

        # 1. Thông tin Đề thi
        frame_info = ctk.CTkFrame(right_frame, corner_radius=10)
        frame_info.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(frame_info, text="1. Thông tin Đề thi", font=self.font_title).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 5))

        ctk.CTkLabel(frame_info, text="Môn học:", font=self.font_main).grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.entry_mon_hoc = ctk.CTkEntry(frame_info, width=250, font=self.font_main)
        self.entry_mon_hoc.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        ctk.CTkLabel(frame_info, text="Tên đề thi:", font=self.font_main).grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.entry_ten_de = ctk.CTkEntry(frame_info, width=250, font=self.font_main)
        self.entry_ten_de.grid(row=2, column=1, padx=15, pady=5, sticky="w")

        ctk.CTkLabel(frame_info, text="Mã đáp án:", font=self.font_main).grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.entry_ma_dap_an = ctk.CTkEntry(frame_info, width=250, font=self.font_main)
        self.entry_ma_dap_an.grid(row=3, column=1, padx=15, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_info, text="Số lượng đề:", font=self.font_main).grid(row=4, column=0, sticky="w", padx=15, pady=(5, 15))
        self.entry_so_luong_de = ctk.CTkEntry(frame_info, width=80, font=self.font_main)
        self.entry_so_luong_de.insert(0, "1")
        self.entry_so_luong_de.grid(row=4, column=1, sticky="w", padx=15, pady=(5, 15))

        # 2. Cấu trúc Ma trận
        frame_matrix = ctk.CTkFrame(right_frame, corner_radius=10)
        frame_matrix.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(frame_matrix, text="2. Cấu trúc Ma trận", font=self.font_title).pack(anchor="w", padx=15, pady=(10, 5))

        toolbar_frame = ctk.CTkFrame(frame_matrix, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(toolbar_frame, text="Tiền tố:", font=self.font_main).grid(row=0, column=0, padx=2, pady=5, sticky="e")
        self.entry_prefix = ctk.CTkEntry(toolbar_frame, width=90, font=self.font_main)
        self.entry_prefix.grid(row=0, column=1, padx=2, pady=5, sticky="w")

        ctk.CTkLabel(toolbar_frame, text="Mức độ:", font=self.font_main).grid(row=0, column=2, padx=(10, 2), pady=5, sticky="e")
        self.combo_muc_do = ctk.CTkOptionMenu(
            toolbar_frame, 
            values=["Bất kỳ (*)", "Nhận biết (Y)", "Thông hiểu (B)", "Vận dụng (K)", "Vận dụng cao (G)"],
            width=120, font=self.font_main
        )
        self.combo_muc_do.grid(row=0, column=3, padx=2, pady=5, sticky="w")

        ctk.CTkLabel(toolbar_frame, text="Số lượng:", font=self.font_main).grid(row=1, column=0, padx=2, pady=5, sticky="e")
        self.entry_count = ctk.CTkEntry(toolbar_frame, width=60, font=self.font_main)
        self.entry_count.grid(row=1, column=1, padx=2, pady=5, sticky="w")

        btn_add = ctk.CTkButton(toolbar_frame, text="Thêm", width=60, fg_color="#28A745", hover_color="#218838", font=self.font_main, command=self.add_to_matrix)
        btn_add.grid(row=1, column=2, padx=5, pady=5)
        
        btn_clear = ctk.CTkButton(toolbar_frame, text="Xóa", width=60, fg_color="#DC3545", hover_color="#C82333", font=self.font_main, command=self.clear_matrix)
        btn_clear.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.textbox_matrix = ctk.CTkTextbox(frame_matrix, height=150, font=self.font_main, state="disabled")
        self.textbox_matrix.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        btn_generate = ctk.CTkButton(right_frame, text="🚀 TẠO ĐỀ THI", height=45, font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), command=self.generate_exams)
        btn_generate.pack(fill="x", pady=15)

    def populate_tree(self):
        """Đổ dữ liệu từ file JSON vào cây thư mục và đếm số lượng câu hỏi."""
        # 1. Xóa toàn bộ dữ liệu cũ trên cây để làm mới
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.structure_data:
            self.tree.insert("", "end", text="Không tìm thấy cấu trúc dữ liệu!")
            return
            
        # 2. Duyệt qua từng cấp độ của cấu trúc JSON
        for mon in self.structure_data:
            node_mon = self.tree.insert("", "end", text=mon.get("tenMon", ""), open=False)
            for chuong in mon.get("danhSachChuong", []):
                node_chuong = self.tree.insert(node_mon, "end", text=chuong.get("tenChuong", ""), open=False)
                for bai in chuong.get("danhSachBai", []):
                    node_bai = self.tree.insert(node_chuong, "end", text=bai.get("tenBai", ""), open=False)
                    for dang in bai.get("danhSachDang", []):
                        ma_raw = dang.get("maChung", "")
                        ma_clean = ma_raw.replace("%[", "").replace("]", "").strip()
                        
                        if ma_clean or "Dạng" in dang.get("tenDang", ""):
                            # --- BẮT ĐẦU ĐẾM SỐ LƯỢNG CÂU HỎI ---
                            so_luong = 0
                            if ma_clean and self.db:
                                for q_id in self.db.keys():
                                    if len(q_id) >= len(ma_clean):
                                        match = True
                                        # So sánh bỏ qua dấu '*'
                                        for i in range(len(ma_clean)):
                                            if ma_clean[i] != '*' and ma_clean[i] != q_id[i]:
                                                match = False
                                                break
                                        if match:
                                            so_luong += 1
                            # ------------------------------------
                            
                            # Hiển thị tên Dạng kèm theo (số lượng)
                            ten_hien_thi = f"{dang.get('tenDang', '')} ({so_luong} câu)"
                            self.tree.insert(node_bai, "end", text=ten_hien_thi, values=(ma_clean,))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item.get("values")
            if values and values[0]:
                ma_id = values[0]
                self.entry_prefix.delete(0, tk.END)
                self.entry_prefix.insert(0, str(ma_id))

    def add_to_matrix(self):
        prefix_raw = self.entry_prefix.get().strip()
        count_str = self.entry_count.get().strip()
        muc_do_str = self.combo_muc_do.get()

        if not prefix_raw or not count_str:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ Tiền tố và Số lượng.")
            return

        try:
            count = int(count_str)
            if count <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số lượng phải là số nguyên dương.")
            return

        muc_do_char = "*"
        if "Nhận biết" in muc_do_str: muc_do_char = "Y"
        elif "Thông hiểu" in muc_do_str: muc_do_char = "B"
        elif "Vận dụng cao" in muc_do_str: muc_do_char = "G"
        elif "Vận dụng" in muc_do_str: muc_do_char = "K"
        
        prefix_final = prefix_raw
        if "*" in prefix_final and muc_do_char != "*":
            prefix_final = prefix_final.replace("*", muc_do_char)

        self.ma_tran_list.append((prefix_final, count))
        
        self.textbox_matrix.configure(state="normal")
        self.textbox_matrix.insert("end", f"  🔹 ID: {prefix_final:<12} | SL: {count} câu\n")
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

    def build_tab_nap_data(self):
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
                
                # --- GỌI LẠI HÀM LÀM MỚI CÂY SAU KHI NẠP DỮ LIỆU THÀNH CÔNG ---
                self.populate_tree()
                
                messagebox.showinfo("Thành công", f"Quét {so_file} file.\nThu được: {so_luong} câu hỏi.")
            else:
                self.lbl_status.configure(text="❌ Lỗi lưu dữ liệu!", text_color="#DC3545")
                messagebox.showerror("Lỗi", f"Chi tiết: {thong_bao_loi}")
        else:
            self.lbl_status.configure(text=f"Tổng số câu hỏi: {len(self.db)} câu", text_color="#DC3545")
            messagebox.showwarning("Kết quả", "Không tìm thấy câu hỏi hợp lệ.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = AppTaoDe(root)
    root.mainloop()