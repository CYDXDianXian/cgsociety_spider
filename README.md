# cgsociety_spider
cgsociety图片爬虫程序

cgsociety提供了大量高清图片以供艺术工作者进行参考，而首页精选图片数以万计，手动下载起来很不方便，故该爬虫提供了高效的首页精选图片下载服务

# 特点

- 支持多线程下载，下载速度拉满
- 可自定义要爬取的页面数量
- 下载图片为原图，无压缩
- 重复图片不会进行下载
- 下载完成后生成报告

# 使用方法

在[Releases](https://github.com/CYDXDianXian/cgsociety_spider/releases)中获取应用程序，运行后按提示操作。

或者下载仓库后按照以下方法使用：

1. 该程序需在python环境下运行，请先安装pyhton，并勾选添加到path
2. 安装依赖：install_requirements.bat
3. 运行程序：run.bat
4. 按提示输入你要爬取的页面数量，回车
5. 下载的图片保存在文件运行目录下的cgsociety_download文件夹中