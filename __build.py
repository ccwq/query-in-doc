import subprocess
from os import path
import shutil
# 定义要打包的 Python 文件名
file_name = "main.py"

# 使用 subprocess 模块调用 PyInstaller 进行打包
subprocess.call(['pyinstaller', "-F", file_name])

# copy dist/main.exe to output-fiels dir and cover 
# the old file, windows

copy_arguments = ['copy', "", path.abspath(R'dist\main.exe'), path.abspath(R'output-files\开始搜索.exe')]
shutil.copy(R"dist\main.exe", R"output-files\开始搜索.exe")
