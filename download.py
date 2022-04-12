import xlrd
import os
import requests


name_row = 0
url_row = 9
downLoadPath = './data_download'
table_name = 2
data_path = './SraRunInfo-wheat_20220412.xlsx'
speed = 1024*4
if(os.path.exists('./download.config')):
    iConfig = {}
    with open('./download.config','r',encoding='utf-8') as f:
        str = f.readline()
        str = str.strip()
        if(len(str) > 0):
            str = str.split('=')
            if(len(str) >= 2):
                iConfig[str[0].strip()] = str[1].strip()
    if ('name_row' in iConfig.keys()):
        name_row = int(iConfig['name_row'])
    if ('url_row' in iConfig.keys()):
        url_row = int(iConfig['url_row'])
    if ('data_path' in iConfig.keys()):
        data_path = iConfig['data']
    if ('downLoadPath' in iConfig.keys()):
        downLoadPath = iConfig['downLoadPath']
    if ('table_name' in iConfig.keys()):
        table_name = iConfig['table_name']
    if ('speed' in iConfig.keys()):
        speed = int(iConfig['speed'])

data = xlrd.open_workbook(data_path)
table = data.sheets()[table_name]
tables = []
def import_excel(excel):
    for rown in range(excel.nrows):
        array = {}
        array['road_name'] = table.cell_value(rown,name_row)
        array['download_rul'] = table.cell_value(rown,url_row)
        array['size'] = table.cell_value(rown,7)
        tables.append(array)



def download():
    if (not os.path.exists(downLoadPath)):
        os.mkdir(downLoadPath)
    for index in tables:
        file = downLoadPath+'/'+index['road_name']
        url = index['download_rul']
        if(len(url) == 0 or url[:4] != 'http'):
            continue

        response = requests.get(url,stream=True)
        if(response.status_code == 200):
            print(index['road_name'] + '开始下载')
        else:
            print(response.status_code)
            continue
        if('content-length' in response.headers):
            content_size = int(response.headers['content-length'])  # 内容体总大小
        else:
            content_size = -1
        chunk_size = speed  # 单次请求最大值
        with open(file, "wb") as f:
            data_count = 0
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                data_count = data_count + len(data)
                if(content_size == -1):
                    print("\r 文件下载进度：(%d/%s) 下载到: %s"
                          % (data_count, '未知', file), end=' ')
                else:
                    now_jd = (data_count / content_size) * 100
                    print("\r文件下载进度：%d%%(%d/%d) 下载到: %s"
                          % (now_jd, data_count, content_size, file), end=' ')
        print('\n'+index['road_name']+'下载完成\n')

if __name__ == '__main__':

    print('数据开始导出')
    #将excel表格的内容导入到列表中
    import_excel(table)
    print('数据导出完成')
    #print(tables)
    print('数据开始下载')
    #下载文件
    download()
    print('数据下载完成')










