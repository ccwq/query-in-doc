# 概述

这款基于Python开发的软件利用everything提供的API接口实现了对本地电脑特定文档的扫描功能。

用户首先需要运行output-files\Everything.exe启动everything，并等待缓存重建完成。然后双击"开始搜索.exe"开始按预设规则查找文件，在终端窗口上可以看到文件检查和进度。搜索完成后，logs/result-*.csv会列出搜索结果。

用户可以在.env文件中修改配置，同时也可以通过conda create命令重建环境，通过python main.py命令进行调试和开发。

最后，如果修改了源码,可以通过python __.build.py命令构建可执行文件。

# 使用

1. 首先运行 output-files\Everything.exe, everything启动,此时界面的下面会显示"正在重建缓存",等待建立完成之后,应该显示"6,66,,666个对象"
2. 此时双击"开始搜索.exe", 开始按照预设的规则查找所电脑上的文件, 在终端窗口上,会显示当正在检查的文件和进度
3. 在搜索完成之后, logs/result-*.csv会列出搜索结果

# 配置
在.env中修改响应的配置

# 环境重建

```bash
conda create --name query-in-file --file requirements.txt
```

# 调试和开发
```bash
python main.py
```


# 构建
构建可以执行的exe
```bash
python __.build.py
```