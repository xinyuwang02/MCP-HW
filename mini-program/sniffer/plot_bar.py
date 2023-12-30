import json
import matplotlib.pyplot as plt

# 从JSON文件加载数据
with open("packet_info.json", "r") as json_file:
    packet_info_list = json.load(json_file)

# 准备绘图数据
time_list_up = []  # 上行时间
size_list_up = []  # 上行大小
port_list_up = []  # 上行端口
flag_list_up = []  #上行标记
time_list_down = []  # 下行时间
size_list_down = []  # 下行大小
port_list_down = []  # 下行端口
flag_list_down = []  #下行标记

# 设置端口颜色映射
port_color_mapping = {8000: 'r', 8080: 'g', 8081: 'b'}

# 遍历数据包信息
for packet_info in packet_info_list:
    time = packet_info["TIME"] - 1703071287
    size = packet_info["SIZE"]
    drc = packet_info["DRC"]
    port = packet_info["PORT"]
    flag = packet_info["TCP_FLAG"]

    # 将数据添加到相应的列表中
    #宽度0.00001 
    #图像（15.832，15.84） 
    #文字（27.879,27.95） 
    #后端5.37-5.38 5.42-5.50

    if drc == 'up' and time>0.1 and time<0.7:
        time_list_up.append(time)
        size_list_up.append(size)
        port_list_up.append(port)
        flag_list_up.append(flag)
        
    elif drc == 'down'and time>0.1 and time<0.7:
        time_list_down.append(time)
        size_list_down.append(-size)  # 下行大小为负数
        port_list_down.append(port)
        flag_list_down.append(flag)
        

# 绘制图表
plt.bar(time_list_up, size_list_up, width=0.00001, color=[port_color_mapping[port] for port in port_list_up])
plt.bar(time_list_down, size_list_down, width=0.00001, color=[port_color_mapping[port] for port in port_list_down])
plt.yscale('symlog', linthresh=1)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)

# 在每个柱子的上方添加标签
for i in range(len(time_list_up)):
    plt.text(time_list_up[i], size_list_up[i], f"{int(size_list_up[i])}\n{flag_list_up[i]}", ha='center', va='bottom', fontsize=6)

for i in range(len(time_list_down)):
    plt.text(time_list_down[i], size_list_down[i], f"{int(size_list_down[i])}\n{flag_list_down[i]}", ha='center', va='top', fontsize=6)

# 添加图表标签
plt.xlabel("Time")
plt.ylabel("Size(Bytes)")
plt.show()
