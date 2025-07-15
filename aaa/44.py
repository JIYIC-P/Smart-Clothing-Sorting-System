import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QPushButton, QSlider, QCheckBox,
                             QWidget, QGroupBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap


class CameraControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB 相机控制程序")
        self.setGeometry(100, 100, 1000, 700)
        
        # 相机相关变量
        self.cap = None
        self.camera_opened = False
        self.current_frame = None
        
        # UI初始化
        self.init_ui()
        
        # 初始化相机
        self.init_camera()
        
    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # 左侧 - 视频显示区域
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        main_layout.addWidget(self.video_label, stretch=2)
        
        # 右侧 - 控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel, stretch=1)
        
        # 相机控制组
        camera_group = QGroupBox("相机控制")
        camera_layout = QVBoxLayout()
        
        # 分辨率选择
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "640x480", "800x600", "1024x768", 
            "1280x720", "1920x1080"
        ])
        camera_layout.addWidget(QLabel("分辨率:"))
        camera_layout.addWidget(self.resolution_combo)
        
        # 帧率选择
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["15", "30", "60"])
        camera_layout.addWidget(QLabel("帧率 (FPS):"))
        camera_layout.addWidget(self.fps_combo)
        
        # 曝光控制
        self.auto_exposure_check = QCheckBox("自动曝光")
        self.auto_exposure_check.setChecked(True)
        camera_layout.addWidget(self.auto_exposure_check)
        
        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setRange(-13, 1)
        self.exposure_slider.setValue(-6)
        self.exposure_slider.setEnabled(False)
        camera_layout.addWidget(QLabel("曝光值 (手动模式):"))
        camera_layout.addWidget(self.exposure_slider)
        
        # 其他参数
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(50)
        camera_layout.addWidget(QLabel("亮度:"))
        camera_layout.addWidget(self.brightness_slider)
        
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(50)
        camera_layout.addWidget(QLabel("对比度:"))
        camera_layout.addWidget(self.contrast_slider)
        
        # 应用设置按钮
        self.apply_btn = QPushButton("应用设置")
        camera_layout.addWidget(self.apply_btn)
        
        camera_group.setLayout(camera_layout)
        control_layout.addWidget(camera_group)
        
        # 连接信号
        self.auto_exposure_check.stateChanged.connect(self.toggle_exposure_control)
        self.apply_btn.clicked.connect(self.apply_camera_settings)
        
        # 定时器更新画面
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def init_camera(self):
        """初始化相机"""
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows使用DirectShow
            if not self.cap.isOpened():
                raise Exception("无法打开相机")
            
            self.camera_opened = True
            self.apply_camera_settings()
            self.timer.start(30)  # 30ms更新一次画面
        except Exception as e:
            print(f"相机初始化失败: {e}")
            self.video_label.setText("无法打开相机")
            self.camera_opened = False
    
    def toggle_exposure_control(self, state):
        """切换曝光控制模式"""
        self.exposure_slider.setEnabled(not bool(state))
    
    def apply_camera_settings(self):
        """应用相机设置"""
        if not self.camera_opened:
            return
            
        # 解析分辨率
        width, height = map(int, self.resolution_combo.currentText().split('x'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # 设置帧率
        fps = int(self.fps_combo.currentText())
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        # 设置曝光
        auto_exposure = self.auto_exposure_check.isChecked()
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1 if auto_exposure else 0)
        if not auto_exposure:
            exposure = self.exposure_slider.value()
            print("曝光：")
            print(exposure)
            self.cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        
        # 设置其他参数
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.brightness_slider.value())
        print("亮度：")
        print(self.brightness_slider.value())
        self.cap.set(cv2.CAP_PROP_CONTRAST, self.contrast_slider.value())
        print("对比度")
        print(self.contrast_slider.value())

        # 关闭自动白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)          # 0 = OFF
        # 关闭自动增益（部分相机把增益和曝光耦合在一起，也一起关掉）
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)        # 顺带关自动对焦，防止跑焦
        self.cap.set(cv2.CAP_PROP_GAIN, 0)             # 手动增益设为固定值
    
    def update_frame(self):
        """更新视频帧"""
        if not self.camera_opened:
            return
            
        ret, frame = self.cap.read()
        if ret:
            # 转换颜色空间 BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 获取当前分辨率
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            
            # 创建QImage并显示
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
    
    def closeEvent(self, event):
        """关闭窗口时释放资源"""
        if self.camera_opened:
            self.timer.stop()
            self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraControlApp()
    window.show()
    sys.exit(app.exec_())