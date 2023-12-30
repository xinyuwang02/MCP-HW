import json
import numpy as np
import matplotlib.pyplot as plt

# 从JSON文件加载数据
with open("packet_info.json", "r") as json_file:
    packet_info_list = json.load(json_file)

# 准备绘图数据
time_step=0.1
time_vec = np.arange(0, 51, time_step)
stream_8000_up =np.zeros(int(51/time_step))
stream_8000_down =np.zeros(int(51/time_step))
stream_8080_up =np.zeros(int(51/time_step))
stream_8080_down =np.zeros(int(51/time_step))
stream_8081_up =np.zeros(int(51/time_step))
stream_8081_down =np.zeros(int(51/time_step))

# 遍历数据包信息
for packet_info in packet_info_list:
    time = packet_info["TIME"] - 1703071287
    size = packet_info["SIZE"]
    drc = packet_info["DRC"]
    port = packet_info["PORT"]


    if drc == 'up' and port == 8000:
        stream_8000_up[int(time/time_step)]+=size
    elif drc == 'down' and port == 8000:
        stream_8000_down[int(time/time_step)]+=size
    if drc == 'up' and port == 8080:
        stream_8080_up[int(time/time_step)]+=size
    elif drc == 'down' and port == 8080:
        stream_8080_down[int(time/time_step)]+=size
    if drc == 'up' and port == 8081:
        stream_8081_up[int(time/time_step)]+=size
    elif drc == 'down' and port == 8081:
        stream_8081_down[int(time/time_step)]+=size

plt.plot(time_vec,stream_8080_up/1000,color='green', label='Img_server_uplink',alpha=1)
plt.plot(time_vec,-stream_8080_down/1000, color='lightgreen', label='Img_server_downlink',alpha=1)    
plt.plot(time_vec,stream_8081_up/1000,color='blue', label='Txt_server_uplink',alpha=1)
plt.plot(time_vec,-stream_8081_down/1000, color='lightblue', label='Txt_server_downlink',alpha=1)
plt.plot(time_vec,stream_8000_up/1000,color='red', label='Backend_server_uplink',alpha=0.8)
plt.plot(time_vec,-stream_8000_down/1000, color='lightcoral', label='Backend_server_downlink',alpha=0.8)
plt.yscale('symlog', linthresh=1)

# 添加图表标签
plt.xlabel("Time")
plt.ylabel("MBps")
plt.legend(framealpha=0.5, fontsize='8')
plt.title("Estimation of Data Uplink and Downlink Rates for the Servers")
plt.show()
