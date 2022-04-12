本工具是用来批量下载Excel文件里的url的

其中download.config是配置文件，在里边可以写如下参数：

```
列号从0开始
name_row = 文件名字列
url_row = 下载文件url的列
downLoadPath = './data_download'   保存下载后的文件的路径
table_name = 2   要读取的Excel的工作表
data_path = './SraRunInfo-wheat_20220412.xlsx'   读取Excel文件的路径
speed = 1024*4   下载速度
```

运行文件需要安装如下包

```
import xlrd
import os
import requests
```

xlrd需要 >= 1.2.0

requests需要 >= 2.24.0

然后运行download.py即可