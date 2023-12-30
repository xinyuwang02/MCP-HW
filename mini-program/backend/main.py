from typing import Union
from fastapi import FastAPI, Response, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
from pydantic import BaseModel

import logging


#创建一个对象
app=FastAPI()

#一条消息的组成
class One_Message(BaseModel):
    text: str
    timestamp: str
    type: int
    sender: int

# 为两个用户分别定义历史消息列表
Alice_message_lib = []
Bob_message_lib = []

#后端视角中,A和B有没有应该转发的新消息
A_new_msg=False
B_new_msg=False

#后端视角中，A和B该发送的消息位置指针（索引）
A_pointer=0
B_pointer=0

#后端存储的图片总数量
img_counter=0
#后端存储的消息总数量
msg_counter=0

#记录后端视角中A和B最后上传/请求过的图片序号
A_last_up=-1
B_last_up=-1
A_last_down=-1
B_last_down=-1


#定义路径操作
@app.get("/")
def read_root():
    return{"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id:int):
    return {"item_id": item_id}

#处理是否有新消息的轮询请求
@app.get("/new_msg_polling/{id}")
def new_msg_polling(id:int):
    global A_new_msg, B_new_msg 
    if id==0:
        return B_new_msg
    elif id==1:
        print(A_new_msg)
        return A_new_msg

#处理对新消息的请求
@app.get("/download_messages/{id}")
def download_massages(id:int):
    global A_pointer,B_pointer,Alice_message_lib,Bob_message_lib,A_new_msg,B_new_msg
    list_to_send=[]
    if id==0:
        list_to_send=Bob_message_lib[B_pointer:]
        B_pointer=len(Bob_message_lib)
        B_new_msg=False
    elif id==1:
        list_to_send=Alice_message_lib[A_pointer:]
        A_pointer=len(Alice_message_lib)
        A_new_msg=False
    return list_to_send

#处理对某个图片的请求
@app.get("/get_image/{uid}/{img_id}")
async def get_image(uid:int,img_id:str):
    global A_last_down, B_last_down
    if uid==0:
        A_last_down=img_id
        print("A_last_down ",A_last_down)
    elif uid==1:
        B_last_down=img_id
        print("B_last_down ",B_last_down)
    img_path='C:/Users/SF/Desktop/mini-program/backend/save/' + img_id + '.jpg'
    return FileResponse(img_path,media_type="image/jpeg")

#处理对密钥初始化时下载图片的请求
@app.get("/init_keys/{id}/{tp}")
async def init_keys(id:int,tp:int):
    #tp 自己0 对方 1
    #注意，初始的对方密钥是收到过的最后一张
    #初始的自己密钥是自己发出过的最后一张
    img_to_reply=-1
    if id==0:
        if tp==0:#即A请求自己上传的最后一张
            img_to_reply=A_last_up
        elif tp==1:#即A请求自己下载过的最后一张
            img_to_reply=A_last_down
    elif id==1:
        if tp==0:#即B请求自己上传的最后一张
            img_to_reply=B_last_up
        elif tp==1:#即B请求自己下载过的最后一张
            img_to_reply=B_last_down
    print("img_to_reply ",img_to_reply)
    if img_to_reply==-1:#不合法的请求return为空
        return
    else:
        img_path='C:/Users/SF/Desktop/mini-program/backend/save/' + str(img_to_reply)+ '.jpg'
        return FileResponse(img_path,media_type="image/jpeg")


#接收前端上传的图片
@app.post("/upload_image/")
async def upload_image(image: UploadFile=File(...),timestamp: str=Form(),sender: int=Form()):
    global A_new_msg, B_new_msg,Alice_message_lib,Bob_message_lib, img_counter,A_last_up,B_last_up
    print(timestamp,' ',sender)
    print('Backend successfully received!')
    img_id=str(img_counter)
    img_counter += 1
    received_img=One_Message(
        text= img_id,
        timestamp=timestamp,
        type=1,
        sender=sender
    )
    if sender==0:
        A_last_up=int(img_id)
        print("A_last_up ",A_last_up)
        Alice_message_lib.append(received_img)
        A_new_msg=True
        print(Alice_message_lib)
    elif sender==1:
        B_last_up=int(img_id)
        print("B_last_up ",B_last_up)
        Bob_message_lib.append(received_img)
        B_new_msg=True
        print(Bob_message_lib)
    else:
        return {"status": "error", "message": "Invalid sender"}
    file_bytes=image.file.read()
    tempfile='C:/Users/SF/Desktop/mini-program/backend/save/' + img_id + '.jpg'
    with open(tempfile,'wb') as f:
        f.write(file_bytes)

    return JSONResponse(content={'result':"OK"})


# 后端收到不同用户的消息，并分别添加到消息列表
@app.post("/upload_message/{id}")
async def upload_message(id: int, received_message: One_Message):
    global A_new_msg, B_new_msg,Alice_message_lib,Bob_message_lib,msg_counter  # 声明为全局变量
    #新消息写入txt
    # 配置消息日志，使用不同的文件名
    try:
        print("msg_counter:", msg_counter)
        log_file_path = 'C:/Users/SF/Desktop/mini-program/backend/save/' + str(msg_counter) + '.txt'
        print(f"Attempting to create file: {log_file_path}")
        logging.getLogger().handlers = []
        logging.basicConfig(
            filename=log_file_path, 
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        log_message = f"Text: {received_message.text}, Timestamp: {received_message.timestamp}, Type: {received_message.type}, Sender: {received_message.sender}"
        logging.info(log_message)
        msg_counter+=1
    except Exception as e:
        print(f"Exception: {e}")

    if id==0:
        Alice_message_lib.append(received_message)
        A_new_msg=True #A有新消息该发送了
        print(A_new_msg)
        print(Alice_message_lib)
    elif id==1:
        Bob_message_lib.append(received_message)
        B_new_msg=True #B有新消息该发了
        print(Bob_message_lib)
    else:
        return {"status": "error", "message": "Invalid user_id"}
    return {"status": "success"}