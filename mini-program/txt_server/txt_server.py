from fastapi import FastAPI, File, UploadFile

app_text = FastAPI()


# 存储文字信息的服务器
@app_text.post("/upload_text")
async def upload_text(text: UploadFile = File(...)):
    # 保存到本地
    file_bytes=text.file.read()
    tempfile='C:/Users/SF/Desktop/mini-program/txt_server/save/' + text.filename
    with open(tempfile,'wb') as f:
        f.write(file_bytes)
    return {"text": text.filename}

if __name__ == "__main__":
    import uvicorn

    # 启动文字信息服务器，监听在8081端口
    uvicorn.run(app_text, host="127.0.0.1", port=8081, log_level="info")
