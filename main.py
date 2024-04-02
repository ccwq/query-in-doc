
from tqdm import tqdm
import time
import logging
from dotenv import load_dotenv, dotenv_values
import os

from tools import ES_EXE_PATH,ex_search, get_result_logger, parse_document, output_to_csv

# 加载.env文件中的环境变量
load_dotenv()

env_dict = dotenv_values()

# 配置日志
LOGING_PATH = R"logs/main.log"
# if dir not exist create it
if not os.path.exists("logs"):
    os.mkdir("logs")
logging.basicConfig(filename=LOGING_PATH, level=logging.DEBUG)
logging.info("ES_EXE_PATH: %s", ES_EXE_PATH)

# 文件类型列表
FILE_PARTTEN = env_dict["FILE_PARTTEN"].split(",")

print(f"文件类型:{FILE_PARTTEN}")

# 所有文件列表
file_list = []
for partten in FILE_PARTTEN:
    file_list.extend(ex_search(partten))

# file_list = ex_search(name_str, None)

# 测试数据
# file_list_for_process = file_list[0:3]
file_list_for_process = file_list
result_logger = get_result_logger()

print(f"总结:{len(file_list)}个文件")

# exit()
key_words_list = os.environ.get("KEY_WORDS_LIST").split(',')

# 进度条
progress_bar = tqdm(total=len(file_list_for_process))

# 结果统计
result_list = []

# 排除的文件
EXDLOUD_FILES = os.environ.get("EXDLOUD_FILES").split(',')
print(f"排除文件:{EXDLOUD_FILES}")


DATA_TIME_STR = time.strftime('%Y-%m-%d_%H-%M-%S')

# 输出的路径
RESULT_CSV_PATH = os.path.abspath(FR"logs/result_{DATA_TIME_STR}.csv")

print(f"输出路径:{RESULT_CSV_PATH}")


try:
    with open(RESULT_CSV_PATH, 'w', encoding='utf-8') as f:
        f.write('关键字,耗时,命中次数,文件路径\n')
except Exception as e:
    logging.error("err-file:%s", RESULT_CSV_PATH)
    logging.error('err-content:%s', e)
    print(f"打开结果文件错误:{e}")
    exit()
    
# 开始解析结果
for i in range(len(file_list_for_process)):
    doc_path = file_list_for_process[i][0]

    # 排除文件    
    for exdloud_file in EXDLOUD_FILES:
        if exdloud_file in doc_path:
            result_logger.info("%s|%s:[%s]", "exdloud", doc_path, 0)
            continue
        

    progress_bar.set_description(f"file {doc_path}")
    progress_bar.update(1)

    
    file_type= doc_path.split(".")[-1]
    
    # 解析文档内容
    (error, _,key_word, hit_line_num, time_cost) = parse_document(doc_path, file_type, key_words_list)
    
    if error:
        logging.error("err-file:%s", doc_path)
        logging.error('err-content:%s', error)
    else:
        if key_word!="clear":
            result_logger.info("%s|%s:(%ss)[%s]",key_word,hit_line_num, time_cost, doc_path)
            result_list.append([ key_word, hit_line_num, doc_path, time_cost, ])
            
            # 写入csv
            try:
                with open(RESULT_CSV_PATH, 'a', encoding='utf-8') as f:
                    f.write(f'{key_word},{time_cost},{hit_line_num},{doc_path}\n')
            except Exception as e:
                print(e)
                logging.error(f"error to write log: {doc_path}")
        else:
            result_logger.info("%s|%s:[%s]",key_word, doc_path, 0)
    
# output_to_csv(result_logger)




 




    


