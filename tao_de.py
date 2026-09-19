import os
import json
import random

def load_database(filepath):
    if not os.path.exists(filepath):
        print(f"[LỖI] Không tìm thấy '{filepath}'. Hãy chạy main.py để quét dữ liệu trước.")
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def auto_pick_questions(database, prefix, count):
    matching_ids = [q_id for q_id in database.keys() if q_id.startswith(prefix)]
    
    if not matching_ids:
        print(f"  -> [CẢNH BÁO] Không có câu hỏi nào khớp với mã '{prefix}'.")
        return []
        
    if len(matching_ids) < count:
        print(f"  -> [CẢNH BÁO] Ngân hàng chỉ có {len(matching_ids)} câu cho mã '{prefix}' (Yêu cầu: {count}). Sẽ lấy tất cả.")
        return matching_ids
        
    return random.sample(matching_ids, count)

def read_matrix_from_excel(excel_path):
    try:
        import openpyxl
    except ImportError:
        print("[LỖI] Chưa cài đặt thư viện đọc Excel. Hãy chạy lệnh: pip install openpyxl")
        return []
        
    if not os.path.exists(excel_path):
        print(f"[LỖI] Không tìm thấy file Excel tại: '{excel_path}'")
        return []
        
    matrix_requests = []
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet = wb.active
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        prefix = str(row[0]).strip() if row[0] else ""
        try:
            count = int(row[1]) if row[1] else 0
        except (ValueError, TypeError):
            count = 0
            
        if prefix and count > 0:
            matrix_requests.append((prefix, count))
            
    return matrix_requests

def create_exam(question_ids, database, output_filepath, mon_hoc, ten_de, ma_dap_an):
    cau_hoi_tn, cau_hoi_ds, cau_hoi_tln = [], [], []
    missing_ids = []

    for q_id in question_ids:
        q_id = q_id.strip() 
        if q_id in database:
            content = database[q_id]
            if r'\choiceTF' in content or r'\choicetf' in content:
                cau_hoi_ds.append(content)
            elif r'\choice' in content:
                cau_hoi_tn.append(content)
            else:
                cau_hoi_tln.append(content)
        else:
            missing_ids.append(q_id)

    if not (cau_hoi_tn or cau_hoi_ds or cau_hoi_tln):
        print(f" -> [THẤT BẠI] Không có câu hỏi nào để tạo đề cho '{output_filepath}'.")
        return

    latex_template = r"""%%\def\linkdethi{https://toanvip307.blogspot.com/} %Đường kinh cần dẫn tới
%%\hienmaQR

\def\toanlop{12}
\def\thoigian{50}
\def\namhoc{2025 - 2026}

\begin{dethi}
	{GIA SƯ THỊNH XUI}
	{Lớp {MÔN_HỌC} 12 VIP}
	{{TÊN_ĐỀ}}
\end{dethi}

\subsubsection{Bài tập chọn đáp án đúng}
\setcounter{ex}{0}
\Opensolutionfile{ans}[ans/ans{MÃ_ĐÁP_ÁN}-TN]

{CÂU_HỎI_TRẮC_NGHIỆM}

\Closesolutionfile{ans}

\subsubsection{Bài tập đúng sai}
\setcounter{ex}{0}
\Opensolutionfile{ans}[ans/ans{MÃ_ĐÁP_ÁN}-DS]

{CÂU_HỎI_ĐÚNG_SAI}

\Closesolutionfile{ans}

\subsubsection{Bài tập điền khuyết}
\setcounter{ex}{0}
\Opensolutionfile{ans}[ans/ans{MÃ_ĐÁP_ÁN}-TLN]

{CÂU_HỎI_ĐIỀN_KHUYẾT}

\Closesolutionfile{ans}

\newpage
\indapan{8}{ans/ans{MÃ_ĐÁP_ÁN}-TN}
\indapan[TF]{2}{ans/ans{MÃ_ĐÁP_ÁN}-DS}
\indapan[SA]{4}{ans/ans{MÃ_ĐÁP_ÁN}-TLN}
%%%%%%%%%%%%%%
%%nhãn kết thúc đề (để đếm số trang tự động mỗi đề)
\label{B\thedeso}
"""
    
    final_latex = latex_template.replace("{MÔN_HỌC}", mon_hoc)
    final_latex = final_latex.replace("{TÊN_ĐỀ}", ten_de)
    final_latex = final_latex.replace("{MÃ_ĐÁP_ÁN}", ma_dap_an)
    final_latex = final_latex.replace("{CÂU_HỎI_TRẮC_NGHIỆM}", "\n\n".join(cau_hoi_tn))
    final_latex = final_latex.replace("{CÂU_HỎI_ĐÚNG_SAI}", "\n\n".join(cau_hoi_ds))
    final_latex = final_latex.replace("{CÂU_HỎI_ĐIỀN_KHUYẾT}", "\n\n".join(cau_hoi_tln))

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(final_latex)
    
    print(f" -> Đã tạo: '{output_filepath}' (Mã: {ma_dap_an})")