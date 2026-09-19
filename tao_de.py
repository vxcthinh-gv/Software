import os
import json
import random

def load_database(filepath):
    """Nạp ngân hàng câu hỏi từ file JSON vào bộ nhớ."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def auto_pick_questions(database, prefix, count):
    """Lọc và chọn ngẫu nhiên câu hỏi, hỗ trợ ký tự đại diện '*'."""
    matching_ids = []
    
    # Duyệt qua toàn bộ ngân hàng câu hỏi
    for q_id in database.keys():
        # Nếu mã trong ngân hàng ngắn hơn tiền tố yêu cầu thì bỏ qua
        if len(q_id) < len(prefix):
            continue
            
        match = True
        # So sánh từng ký tự giữa mã câu hỏi và tiền tố yêu cầu
        for i in range(len(prefix)):
            if prefix[i] != '*' and prefix[i] != q_id[i]:
                match = False
                break
                
        if match:
            matching_ids.append(q_id)
    
    if not matching_ids:
        return []
    if len(matching_ids) < count:
        return matching_ids
        
    return random.sample(matching_ids, count)

def create_exam(question_ids, database, output_filepath, mon_hoc, ten_de, ma_dap_an):
    """Phân loại câu hỏi và tạo file LaTeX hoàn chỉnh."""
    cau_hoi_tn, cau_hoi_ds, cau_hoi_tln = [], [], []
    
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

    if not (cau_hoi_tn or cau_hoi_ds or cau_hoi_tln):
        return False

    latex_template = r"""%%\def\linkdethi{https://toanvip307.blogspot.com/}
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
        
    return True