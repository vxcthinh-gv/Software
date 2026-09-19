import os
import re
import json

# Nạp dữ liệu vào DB
def parse_latex_files(folder_path):
    """Quét thư mục, tìm, làm sạch khối câu hỏi và đếm số file đã xử lý."""
    question_bank = {}
    files_scanned = 0  # Biến đếm số lượng file .tex
    
    ex_pattern = re.compile(r'(\\begin\{ex\}.*?\\end\{ex\})', re.DOTALL)
    id_pattern = re.compile(r'%\[([A-Za-z0-9]+-[A-Za-z0-9]+)\]')

    if not os.path.exists(folder_path):
        return question_bank, files_scanned

    for filename in os.listdir(folder_path):
        if filename.endswith('.tex'):
            files_scanned += 1
            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for match in ex_pattern.finditer(content):
                        question_content = match.group(1)
                        id_match = id_pattern.search(question_content)
                        
                        if id_match:
                            question_id = id_match.group(1)
                            lines = question_content.split('\n')
                            lines[0] = f"\\begin{{ex}}%[{question_id}]"
                            cleaned_content = '\n'.join(lines)
                            question_bank[question_id] = cleaned_content.strip()
            except Exception as e:
                print(f"Lỗi khi đọc file {filename}: {e}")

    # Trả về cả dữ liệu câu hỏi và số file đã quét
    return question_bank, files_scanned

def save_database(data, output_file):
    """Lưu dữ liệu ngân hàng câu hỏi vào file JSON và báo lỗi chi tiết."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True, "Thành công"
    except Exception as e:
        # Bắt lỗi thực tế từ hệ điều hành và trả về
        return False, str(e)