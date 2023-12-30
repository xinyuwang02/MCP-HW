from scapy.all import sniff, IP, TCP, Raw
import json

# 用于存储数据包信息的列表
packet_info_list = []

def packet_callback(packet):
    if(packet.haslayer(TCP)):
        if(packet[TCP].sport in {8080,8081,8000}):
            DRC='down'
            PORT=packet[TCP].sport
        elif(packet[TCP].dport in {8080,8081,8000}):
            DRC='up'
            PORT=packet[TCP].dport
        packet_info = {
            "DRC": DRC,
            "PORT":PORT,
            "TIME": packet.time,
            "SIZE": len(packet),
            "SRC_PORT": packet[TCP].sport,
            "DST_PORT": packet[TCP].dport,
            "TCP_FLAG": str(packet[TCP].flags),
        }
        packet_info_list.append(packet_info)
        print("A packet detected: ")
        for key, value in packet_info.items():
            print(f"{key}: {value}")
        print("="*30)


# 开始嗅探图像信息服务器/文字信息服务器以及小程序后端服务器的上下行流量
sniff(prn=packet_callback, iface="", store=0, 
      filter="tcp and (port 8080 or port 8081 or port 8000)",count=800)

with open("packet_info.json", "w") as json_file:
    json.dump(packet_info_list, json_file, indent=None)