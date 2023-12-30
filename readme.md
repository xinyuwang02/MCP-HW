#MCP2023 homework code

> mini-program 和 yolo 两部分

## /mini-program

### /frontend
小程序前端 project

### /backend

直接和小程序前端交互的后端
- main.py 后端程序，默认运行在本地8000端口
- /save 后端存储聊天文本和图像的空间

### /monitor
监测后端存储空间的文件新增并转发
- mnt_and_fwd.py 监测并转发

### /img_server
图像信息服务器
- img_server.py 运行在本地8080端口
- /save 图像信息服务器的存储空间

### /txt_server
文字信息服务器
- txt_server.py 运行在本地8081端口
- /save 文字信息服务器的存储空间

### /sniffer
嗅探三个端口数据包
- sniffer.py 嗅探数据包并存储捕获的信息
- plot_bar.py 绘制所捕获数据包的线状图
- plot_line.py 绘制根据抓到包估算的实时流量

## /yolo

用自定义数据集训练的yolov5目标检测识别猫和狗的代码包（不含数据集）
- train.py 运行此脚本训练
- detect.py 运行此脚本进行样例检测
