import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    # Loại bỏ khoảng trắng thừa và xuống dòng không cần thiết
    text = re.sub(r'\n+', '\n', text.strip())
    text = re.sub(r' +', ' ', text)
    # Loại bỏ các dòng trống liên tiếp
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text

def format_chapter_content(text):
    # Tách các đoạn văn và format lại
    paragraphs = text.split('\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        if para.strip():  # Chỉ xử lý các đoạn không rỗng
            # Thêm khoảng trống đầu dòng cho mỗi đoạn văn
            formatted_para = '    ' + para.strip()
            formatted_paragraphs.append(formatted_para)
    
    # Nối các đoạn văn với 2 dòng trống ở giữa để dễ đọc
    return '\n\n'.join(formatted_paragraphs)

def fetch_and_extract_content(url, output_file):
    try:
        # Thiết lập headers để giả lập trình duyệt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Gửi GET request
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        # Parse HTML với BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm phần tử có class "watch-page-fiction-content"
        content_div = soup.find(class_='watch-page-fiction-content')
        
        if content_div:
            # Lấy text và loại bỏ các thẻ HTML
            content = content_div.get_text(separator='\n', strip=True)
            
            # Clean và format text
            cleaned_content = clean_text(content)
            formatted_content = format_chapter_content(cleaned_content)
            
            # Thêm header vào nội dung
            chapter_title = soup.find('h1')
            header = f"{'='*50}\n{chapter_title.text if chapter_title else 'Chương 1'}\n{'='*50}\n\n"
            final_content = header + formatted_content
            
            # Lưu vào file với encoding utf-8
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
                
            print(f"Đã lưu nội dung thành công vào file {output_file}")
            
        else:
            print("Không tìm thấy nội dung với class 'watch-page-fiction-content'")
            
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải trang: {str(e)}")
    except Exception as e:
        print(f"Lỗi: {str(e)}")

# URL và tên file output
url = "https://www.linhthanhnguyet.com/nh-hng-yu-6-c-ng/chuong-1"
output_file = "chapter_content.txt"

# Thực thi
fetch_and_extract_content(url, output_file)