import time
import requests
from pathlib import Path
import asyncio
import aiohttp

path = "cgsociety_download"  # 设置图片的保存地址，相对路径，会在文件运行目录下创建该位置
Path(path).mkdir(parents = True, exist_ok = True) # 不能用__file__获取绝对路径，否则打包exe后运行文件会在缓存目录下创建保存地址

while True: # while True表示永远循环，while False表示它不会执行
    try:
        page_config = int(input('请输入您要爬取的页面数量：')) # input函数返回的是用户输入内容，为字符串类型
    except ValueError:
        print("输入错误请重新输入")
        continue
    if type(page_config) == int:
        print(f'您输入的页面数量为：{page_config}页，即将开始进行爬取')
        time.sleep(3)
        break

url_pages = []
for page in range(page_config):
    page += 1
    url_page = f'https://cgsociety.org/api/channels/featured/images?category=&channel_slug=featured&genre=&page={page}&per_page=20'
    url_pages.append(url_page)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
}

proxy = {}
# 设置代理地址

def get_urls():
    global get_urls_msg
    start_time = time.time()

    urls = {}
    page_num = 0 
    img_url_num = 0
    error_num = 0
    for url in url_pages:
        page_num += 1
        try:
            resp = requests.get(url, headers = headers, proxies = proxy, timeout = 30)
        except:
            print(f'第{page_num}页访问超时，请检查链接地址是否正确，或开启代理！')
            continue
        resp.encoding = 'utf-8'

        data = resp.json()

        try:
            for i in data['data']:
                img_url = i['attributes']['original_url']
                img_type = img_url.split(".")[-1] # 拿到url中的最后一个.以后的内容(图片扩展名)
                name = f"{i['id']}.{img_type}"
                img_url_num += 1
                urls[name] = img_url # 通过使用新的索引键并为其赋值，可以将项目添加到字典中

                print(f'图片地址爬取成功{img_url_num}个')
        except:
            error_num += 1
            print(f'图片地址爬取失败{error_num}个')
    
    end_time = time.time()
    use_time = int(end_time - start_time)
    
    print(f'共爬取到{img_url_num}个文件，即将开始下载！')
    get_urls_msg = f'共爬取成功{img_url_num}个文件，失败{error_num}个，爬取用时{use_time}秒'
    time.sleep(3)

    return urls

async def aiodownload(name, url):
    global success_download, error_download # 必须加全局声明，否则下载计数会出现错误
    
    success_download = 0
    error_download = 0
    try:
        if not Path(path, name).exists(): # 文件不存在则进行下载。Path(path, name)拼接路径与文件名
            async with aiohttp.ClientSession(headers = headers) as session:
                async with session.get(url) as resp:
                    Path(path, name).write_bytes(await resp.content.read())
                    success_download += 1
                    print(f'图片下载成功{success_download}个：{name}')
        else:
            print(f'文件 {name} 已存在，不再进行下载')
    except:
        error_download += 1
        print(f'图片下载失败{error_download}个：{name}')

# 主协程对象
async def main():
    urls = get_urls()
    
    start = time.time() 
    tasks = [aiodownload(k, v) for k, v in urls.items()] # 生成执行任务的列表。items()，返回包含每个键值对的元组的列表，通过使用items()函数遍历键和值
    await asyncio.wait(tasks)
    
    end = time.time()

# 报告部分
    time_str = time.strftime('%Y-%m-%d %H:%M:%S') # 获取当前日期和时间
    comp_msg = '本次任务完成！'
    download_msg = f'共下载成功{success_download}个文件，失败{error_download}个，下载用时{int(end - start)}秒'
    print(comp_msg)
    print(get_urls_msg)
    print(download_msg)
    with Path('report.txt').open(mode='a', encoding='utf-8') as f:
        f.write(f'-----【{time_str}】-----\n{comp_msg}\n{get_urls_msg}\n{download_msg}\n\n')
    print('程序将在10秒后结束......')
    time.sleep(10) # 等10s再结束程序，让用户看到报告

if __name__ == "__main__":
    asyncio.run(main())