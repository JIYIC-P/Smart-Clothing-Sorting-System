import cv2
from threading import Thread
import time
from ultralytics import YOLO


class ThreadedCamera(object):
    def __init__(self, source=0):
        self.source = source
        self.capture = None
        self.status = False
        self.frame = None
        self._running = True  # 新增：线程运行控制标志
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        print("init ok")

    def close_cam(self):
        """安全关闭摄像头和线程"""
        self._running = False  # 通知线程退出
        if self.capture is not None:
            self.capture.release()  # 显式释放摄像头
        self.capture = None
        self.thread.join(timeout=1.0)  # 等待线程结束（最多1秒）

    def update(self):
        """改进后的更新循环，支持安全退出"""
        while self._running:  # 使用标志控制循环

            if self.capture is None:
                try :
                    self.open_cam()
                except:
                    time.sleep(0.1)  # 避免空转消耗CPU
                    print("FAILD")
                    continue
                
            if self.capture.isOpened():
                self.status, frame = self.capture.read()
                
                if self.status:
                    self.frame =  (frame)
                else:
                    self.capture.release()  # 释放旧资源
                    self.capture = cv2.VideoCapture(self.source)
            else:
                time.sleep(0.1)

    def open_cam(self):
        if self.capture == None:
            print("try open")
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        

    def grab_frame(self):
        """返回当前帧（已预处理）"""
        if self.status:  
            return self.frame 
        else :
            self.capture = None 
            return None

    def _process_frame(self, frame):
        """集中处理所有 cv2 相关的图像操作"""
        if frame is None:
            return None
        width = int(frame.shape[1])
        height = int(frame.shape[0])
        #frame= frame[int((height/2)-240):int((height/2)+240), int((width/2)-320):int((width/2)+320)]  # 裁剪中心区域
        return frame
 
 
if __name__ == '__main__':
    stream_link = "rtsp://192.168.1.100/user=admin&password=&channel=1&stream=0.sdp?"
    streamer = ThreadedCamera(stream_link)
    streamer.source=0
    #streamer.open_cam()
    index=0
    model = YOLO("yolov8n.pt",verbose=False)
    while True:
        index=index+1
        time.sleep(0.5)
        frame = streamer.grab_frame()
        if frame is not None:
            #cv2.imshow("Context", frame)
            img = model(frame, verbose=False)
            frame = img[0].plot()
        else:
            pass