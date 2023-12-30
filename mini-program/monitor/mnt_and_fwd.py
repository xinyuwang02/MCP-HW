import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mimetypes
import requests

class FileHandler(FileSystemEventHandler):
    IMAGE_SERVER = "http://127.0.0.1:8080/upload_image"
    TEXT_SERVER = "http://127.0.0.1:8081/upload_text"

    def __init__(self):
        super(FileHandler, self).__init__()
        self.last_content = ""

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_type, encoding = mimetypes.guess_type(file_path)

        if file_type is not None:
            print(f"Detected {file_type} file: {file_path}")
            if file_type.startswith('image'):#转发到图像信息服务器
                try:
                    files = {'image': open(file_path, 'rb')}
                    response = requests.post(self.IMAGE_SERVER, files=files)
                    response.raise_for_status()
                    print(f"成功转发 Server response: {response.text}")
                except Exception as e:
                    print(f"转发失败 Error: {e}")
                    print(f"Server response: {response.status_code} - {response.text}")
                
            elif file_type.startswith('text'):#转发到文字信息服务器
                try:
                    files = {'text': open(file_path, 'rb')}
                    response = requests.post(self.TEXT_SERVER, files=files)
                    response.raise_for_status()
                    print(f"成功转发 Server response: {response.text}")
                except Exception as e:
                    print(f"转发失败 Error: {e}")
                    print(f"Server response: {response.status_code} - {response.text}")
                

if __name__ == "__main__":
    folder_to_watch = "C:/Users/SF/Desktop/mini-program/backend/save" 
    #被监测的文件夹
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    
    try:
        observer.start()
        print(f"正在监测文件夹: {folder_to_watch}")
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
