from fastapi import FastAPI, File, UploadFile

app_image = FastAPI()

# 存储图像的服务器
@app_image.post("/upload_image")
async def upload_image(image: UploadFile = File(...)):
    # 保存到本地
    file_bytes=image.file.read()
    tempfile='C:/Users/SF/Desktop/mini-program/img_server/save/' + image.filename
    with open(tempfile,'wb') as f:
        f.write(file_bytes)
    return {"filename": image.filename, "content_type": image.content_type}


if __name__ == "__main__":
    import uvicorn

    # 启动图像信息服务器，监听在8080端口
    uvicorn.run(app_image, host="127.0.0.1", port=8080, log_level="info")

