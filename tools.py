from PyPDF2 import PdfReader
import subprocess
import docx2txt
from dotenv import load_dotenv, dotenv_values
import os
import logging
import time


# 加载.env文件中的环境变量
load_dotenv()
env_dict = dotenv_values()


ES_EXE_PATH = env_dict["ES_EXE_PATH"]
print("ES_EXE_PATH: %s" % ES_EXE_PATH)

def ex_search(name_str, amount=None):
    """
    执行对外部程序es.exe的调用，进行文件搜索。

    Parameters:
    name_str: str - 要搜索的文件名字符串。
    amount: int - 可选参数，限制搜索结果的数量。

    Returns:
    list of list - 搜索结果的列表，每个元素是包含文件名和修改日期的列表。
    """

    # 构建命令
    # command = [ES_EXE_PATH, '-s', f'"{name_str}"', '-sort', 'date-modified-descending', '-n', str(amount), '-dm']
    # command = [ES_EXE_PATH, '-s', f'"{name_str}"', '-sort', 'date-modified-descending', '-n', str(amount), '-dm']
    command = [ES_EXE_PATH, '-s', f'{name_str}', '-sort', 'date-modified-descending', '-dm']
    
    print(f"查找命令:{' '.join(command)}")
    # 追加个数限制
    if amount:
        command.append('-n')
        command.append(str(amount))
        
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    
    
    # 调用es.exe执行搜索
    # result = subprocess.run(command, capture_output=True, text=True)
    
    # log error
    if result.returncode!= 0:
        logging.error("err-code:%s", result.returncode)
        logging.error("err-content:%s", result.stderr)
        return None
    
    # 解析结果并转为二维数组
    lines = result.stdout.strip().split('\n')
    
    file_list = []
    for line in lines:
        parts = line.split(' ', 2)
        if len(parts) >= 3:
            file_name = parts[2].strip()
            date_modified = parts[0] + ' ' + parts[1]
            file_list.append([file_name, date_modified])
    
    # 对数组的每个元素进行trim操作
    file_list_trimmed = [[item.strip() for item in row] for row in file_list]
    
    return file_list_trimmed



# 日志创建
def get_result_logger():
    LOGING_PATH = os.path.abspath(R"logs\result.log")
    result_logger = logging.getLogger('result_logger')
    result_logger.setLevel(logging.INFO)

    # 结果日志
    file_handler = logging.FileHandler(LOGING_PATH)
    file_handler.setLevel(logging.INFO)

    # 创建一个格式化器，并将其添加到处理程序
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将处理程序添加到Logger实例
    result_logger.addHandler(file_handler)
    
    # clear log file
    with open(LOGING_PATH, 'w', encoding='utf-8') as f:
        f.write('')
    
    return result_logger



def parse_document_pdf(doc_path):
    reader = PdfReader(doc_path)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        all_text += text
    return all_text


def parse_document(doc_path, type="docx", key_words_list=[]):
    """
    Parse a document and search for specified keywords.

    Args:
    doc_path (str): The path to the document file.
    type (str, optional): The type of the document file. Defaults to "docx".
    key_words_list (list, optional): List of keywords to search for in the document. Defaults to [].

    Returns:
    tuple: A tuple containing error message (if any), document path, hit keyword, and the number of times the keyword was found.
    """
    
    time_start = time.time()
    time_cost_in_second = 0;
    
    hit_key_word = None
    hit_line_num = None
    try:
        # docx文档
        if type == "docx":
            text = docx2txt.process(doc_path)

        # pdf解析
        elif type == "pdf":
            text = parse_document_pdf(doc_path)

        # 其他纯文本解析
        else:
            # raise Exception("type error")        
            text = open(doc_path, 'r', encoding='utf-8').read()
    except Exception as e:
        time_cost_in_second = round(time.time() - time_start, 2)
        logging.error("err-file:%s", doc_path)
        logging.error('err-content:%s', e)
        return e, None, None, None, time_cost_in_second
    
    for key_word in key_words_list:
        if key_word in text:
            hit_key_word = key_word
            hit_line_num = text.count(key_word)
            break
        
    time_cost_in_second = round(time.time() - time_start, 2)
    if hit_key_word:
        return None, doc_path, hit_key_word, hit_line_num,time_cost_in_second
    else:
        return None, doc_path, "clear", 0, time_cost_in_second
    
def output_to_csv(result_logger):
    """
    将结果数据输出到CSV文件中。

    参数:
    - result_logger: 结果列表，每个结果包含关键字、命中的行号和文档路径。

    返回值:
    - 无
    """
    
    # 打开结果文件，准备写入
    with open(R'logs\result.csv', 'w', encoding='utf-8') as f:
        # 写入CSV文件的头部
        f.write('key_word,hit_line_num,doc_path\n')
        # 遍历结果列表，将每个结果写入CSV文件
        for result in result_list:
            f.write(f'{result[0]},{result[1]},{result[2]}\n')
            
            