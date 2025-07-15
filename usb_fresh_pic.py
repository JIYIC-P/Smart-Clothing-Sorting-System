import cv2
from threading import Thread
import time

class ThreadedCamera:
    def __init__(self, source=0):
        # 相机相关变量
        self.cap = None
        self.camera_opened = False
        self.current_frame = None

        self._running = True  # 控制线程运行的标志

        # 相机参数
        self.fps = 30
        self.exposure = -9
        self.resolution = [1920, 1080]
        self.brightness = 31
        self.contrast = 46


    def init_camera(self):
        """初始化相机"""
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows使用DirectShow
            if not self.cap.isOpened():
                raise Exception("无法打开相机")
            
            self.camera_opened = True
            self.apply_camera_settings()
            
            # 启动帧更新线程
            self.thread = Thread(target=self.update, daemon=True)
            self.thread.start()

        except Exception as e:
            print(f"相机初始化失败: {e}")
            self.camera_opened = False
            self._running = False

    def apply_camera_settings(self):
        """应用相机设置"""
        if not self.camera_opened:
            return

        print("应用相机设置")
        
        # 设置分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        # 设置帧率
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        # 设置曝光
        self.cap.set(cv2.CAP_PROP_EXPOSURE, self.exposure)
        
        # 设置其他参数
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.brightness)
        self.cap.set(cv2.CAP_PROP_CONTRAST, self.contrast)

        # 关闭自动白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)          # 0 = OFF
        # 关闭自动增益（部分相机把增益和曝光耦合在一起，也一起关掉）
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)        # 顺带关自动对焦，防止跑焦
        self.cap.set(cv2.CAP_PROP_GAIN, 0)             # 手动增益设为固定值

        print(f"分辨率: {self.resolution}, FPS: {self.fps}, 曝光: {self.exposure}, "
              f"亮度: {self.brightness}, 对比度: {self.contrast}")

    def update(self):
        """更新视频帧"""
        while self._running:
            if not self.camera_opened:
                try :
                    self.open_cam()
                    self.apply_camera_settings()
                except:
                    time.sleep(0.1)  # 避免空转消耗CPU
                    print("FAILD")
                    continue
                
            ret, frame = self.cap.read()
            if ret:
                # 转换颜色空间 BGR -> RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # 使用锁保护共享资源
                
                self.current_frame = frame.copy()
            else:
                print("读取帧失败")
                time.sleep(0.1)

    def grab_frame(self):
        """获取当前帧（线程安全）"""
        
        if self.current_frame is not None:
            return self.current_frame.copy()
        return None

    def close_cam(self):
        """关闭并释放资源"""
        self._running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.camera_opened:
            self.cap.release()
        self.camera_opened = False

    def open_cam(self):
        if self.capture == None:
            print("try open")
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 使用示例
if __name__ == '__main__':
    camera = ThreadedCamera()
    camera.init_camera()
    
    try:
        while True:
            frame = camera.grab_frame()
            if frame is not None:
                cv2.imshow("Camera Feed", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.close_cam()
        cv2.destroyAllWindows()