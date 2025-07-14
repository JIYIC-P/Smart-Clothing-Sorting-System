import time
import sys
from Ui_main_form import Ui_Dialog 
import cv2
import matplotlib.pyplot as plt
import numpy as np
import configparser
import json
#颜色范围定义
color_ranges = {
    0 : ([0, 0, 200], [180, 50, 255]),        # 白色范围
    1 : ([0, 100, 100], [10, 255, 255]),      # 红色范围
    2 : ([40, 50, 50], [80, 255, 255]),       # 绿色范围
    3 : ([90, 50, 50], [130, 255, 255]),      # 蓝色范围
    4 : ([20, 100, 100], [30, 255, 255]),     # 黄色范围
}
colors = {
    0 :"白色",
    1 :"红色",
    2 :"绿色",
    3 :"蓝色",
    4 :"黄色",
}

# 定义阈值（可根据需求调整）
s_low = 30    # 低饱和度阈值（白色）
s_high = 150  # 高饱和度阈值（深色）
v_low = 50    # 低明度阈值（深色）
# Qt核心模块
from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
    QEvent,
    QCoreApplication,
    QTimer,
    QObject,
    QSize
)
from PyQt5.QtCore import QSize
# Qt GUI模块
from PyQt5.QtGui import (
    QImage,
    QColor,
    QPainter,
    QPixmap,
    QFont,
    QPalette
)
# Qt Widgets模块 (按使用频率排序)
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QComboBox,
    QWidget,
    QTableWidgetItem,
    QSizePolicy,
    QHBoxLayout,  # <-- Add this line
    QVBoxLayout,
    QGridLayout
    
)

# 本地应用/库特定导入 (Local application)
import mbs
from usb_fresh_pic  import ThreadedCamera
from ultralytics import YOLO


class Dialog(QDialog,Ui_Dialog):
    def __init__(self, parent=None):
        
        super(Dialog, self).__init__(parent)


        self.cloth = []
        self.average_hsv=0
        self.worker=[[],[],[],[],[],[],[]]
        self.t_put = [time.time() for _ in range(5)] #推杆出杆计时


        self.mode = None
        self.mbus = mbs.MBUS()
        self.Ui_init()
        self.Timer_init()
        self.camera_init()
        self.mbus.sender.start()
        self.show_btn_output()
        self.show_btn_input()
        #self.init_trigger()
        self.installEventFilter(self)
        self.key_pressed = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            self.key_pressed = event.key()
        elif event.type() == QEvent.KeyRelease:
            self.key_pressed = None
        return super().eventFilter(obj, event)

    def camera_init(self):
        stream_link = "rtsp://192.168.1.100/user=admin&password=&channel=1&stream=0.sdp?"
        self.streamer = ThreadedCamera(stream_link)
        self.streamer.open_cam()
        self.streamer.source=0
        self.frame = None


    def Timer_init(self):
        #加入小时，分钟，和一个base作为基准
        self.base = 0
        self.hour=0
        self.min=0
        self.sec=0
        self.timer=QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(100)

        self.t_YoLo=QTimer()
        #self.t_YoLo.timeout.connect(self.show_img)
        self.t_YoLo.timeout.connect(self.update)
        self.t_YoLo.start(100)

        self.t_back=QTimer()
        self.t_back.timeout.connect(self.back)
        self.t_back.start(100)


    def Ui_init(self):
        self.setupUi(self)
        self.btn_output = []
        self.btn_input = []
        self.pushButton.clicked.connect(self.serial_connect)
        self.btn_output_init()
        self.btn_input_init()
        self.setup_led_indicator()
        self.init_sys_tble()
        self.read_colors()
        
        self.Hmin_slider.setRange(0, 179)
        self.Hmin_slider.setValue(0)
        self.Hmax_slider.setRange(0, 179)
        self.Hmax_slider.setValue(179)
        self.Hmin_slider.valueChanged.connect(self.update_HSV_values)
        self.Hmax_slider.valueChanged.connect(self.update_HSV_values)

        self.Smin_slider.setRange(0, 255)
        self.Smin_slider.setValue(0)
        self.Smax_slider.setRange(0, 255)
        self.Smax_slider.setValue(255)
        self.Smin_slider.valueChanged.connect(self.update_HSV_values)
        self.Smax_slider.valueChanged.connect(self.update_HSV_values)

        self.Vmin_slider.setRange(0, 255)
        self.Vmin_slider.setValue(0)
        self.Vmax_slider.setRange(0, 255)
        self.Vmax_slider.setValue(255)
        self.Vmin_slider.valueChanged.connect(self.update_HSV_values)
        self.Vmax_slider.valueChanged.connect(self.update_HSV_values)
        self.update_HSV_values()
            

    #@pyqtSlot()
    #def on_applay_clicked(self):
    #    global color_ranges  # 声明使用全局变量
    #    range_col= self.average_hsv.tolist()
    #    #uper_num=self.uper.toPlainText()
    #    #down_num=self.downer.toPlainText()
    #    uper_num= 30
    #    down_num= 30
    #    index= self.choice_push.currentIndex()
    #    print(index)
    #    for i in range(3):
    #        color_ranges[index][0][i]= range_col[i]-int(down_num)
    #        color_ranges[index][1][i]= range_col[i]+int(uper_num)
    #    print("color_ranges:",color_ranges)
    #    # 读取 color.ini 并还原 color_ranges
    #    cfg = configparser.ConfigParser()
    #    cfg.read('color.ini', encoding='utf-8')
    #    ranges_str = cfg['COLOR_RANGES']['ranges']
    #    color_ranges = json.loads(ranges_str)  # 还原为 dict
#
    #    # 如果你需要把键从 str 转回 int：
    #    color_ranges = {int(k): v for k, v in color_ranges.items()}
#
    #    # 调试打印
    #    print("已重新加载 color_ranges:", color_ranges)

    @pyqtSlot()
    def on_btn_save_colors_clicked(self):
        global color_ranges  # 声明使用全局变量
        
        # 1. 获取当前颜色范围和阈值
        range_col = self.average_hsv.tolist()
        uper_num = 30  # self.uper.toPlainText()
        down_num = 30  # self.downer.toPlainText()
        index = self.comBox_pusher.currentIndex()
        print(index)
        
        # 2. 更新颜色范围
        for i in range(3):
            color_ranges[index][0][i] = max(0, range_col[i] - int(down_num))  # 确保不低于0
            color_ranges[index][1][i] = min(255, range_col[i] + int(uper_num))  # 确保不超过255
        
        print("更新后的color_ranges:", color_ranges)
        
        # 3. 写入配置文件
        self.save_color()
        
        # 4. 重新读取验证（可选）
        self.load_color()
        print("重新加载后的color_ranges:", color_ranges)

    def save_color(self):
        """将color_ranges保存到color.ini文件"""
        cfg = configparser.ConfigParser()
        
        # 将color_ranges转换为可序列化的格式
        ranges_str = json.dumps(color_ranges)
        
        # 写入配置
        cfg['COLOR_RANGES'] = {
            'ranges': ranges_str
        }
        
        # 写入文件
        with open('color.ini', 'w', encoding='utf-8') as configfile:
            cfg.write(configfile)
        
        print("颜色范围已保存到color.ini")

    def load_color(self):
        """从color.ini加载color_ranges"""
        global color_ranges
        
        cfg = configparser.ConfigParser()
        cfg.read('color.ini', encoding='utf-8')
        
        if 'COLOR_RANGES' in cfg:
            ranges_str = cfg['COLOR_RANGES']['ranges']
            color_ranges = json.loads(ranges_str)
            # 将字典键转换为int（如果需要）
            color_ranges = {int(k): v for k, v in color_ranges.items()}
        else:
            print("警告: color.ini中没有找到COLOR_RANGES配置")
            color_ranges = {}  # 默认值


    def resizeEvent(self, event):
            self.update_all_fonts()
            super().resizeEvent(event)


    def update_all_fonts(self):
        """根据窗口大小动态调整所有控件字体大小"""
        scale_factor = min(self.width() / 1440, self.height() / 820)
        font_size = max(10, int(20 * scale_factor * 1))  # 最小10
        font = QFont('微软雅黑', font_size)
        font.setBold(True)
        self.setFont(font)
        # 只想让表格内容和表头都变大，可以单独设置
        self.tableWidget.setFont(font)
        self.tableWidget.horizontalHeader().setFont(font)


    def init_sys_tble(self):
        grid = QGridLayout(self.tabWidget)
        grid.addLayout(grid, 0, 0)  # 将主水平布局放入网格
        # 设置表头字体样
        font = QFont('微软雅黑', 10)
        font.setPointSize(40)  # 设置字体大小
        font.setFamily('微软雅黑')  # 设置字体
        font.setBold(True)
        
        # 设置水平表头样式
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            "background-color: rgb(0, 255, 0);"  # 绿色背景
            "padding: 5px;"  # 增加内边距
            "border: 1px solid #cccccc;"  # 边框
            "}"
        )

        
        # 初始化表格结构
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        
        # 设置列宽
        self.tableWidget.setColumnWidth(0, 100)    # 参数名
        self.tableWidget.setColumnWidth(1, 250)    # 参数值
        self.tableWidget.setColumnWidth(2, 700)    # 备注
        
        # 禁用排序
        self.tableWidget.setSortingEnabled(False)
        
        # 初始化表头内容
        headers = ["参数名", "参数值", "备注"]
        for col, text in enumerate(headers):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)  # 文字居中
            item.setSizeHint(QSize(80,80) )
            self.tableWidget.setHorizontalHeaderItem(col, item)
        
        self.on_btn_load_clicked()


    def btn_input_init(self):
        # 1. 创建主水平布局（用于放置4组垂直布局）
        main_hbox = QHBoxLayout()
        main_hbox.setSpacing(100)  # 设置列间距为10像素
        index = 1
        for col in range(3):  # 共4列
            # 2. 为每一列创建垂直布局
            vbox = QVBoxLayout()
            vbox.setSpacing(100)  # 设置按钮之间的间距为10像素
            # 3. 每列添加2个按钮
            for row in range(2):
                btn = QPushButton('input' + str(index), self.groupBox_input)
                self.btn_input.append(btn)
                font = QFont('微软雅黑', 50)
                font.setPointSize(55)  # 设置字体大小
                btn.setFont(font)
                # 设置按钮的大小策略
                btn.setSizePolicy(
                    QSizePolicy.Expanding,  # 水平扩展
                    QSizePolicy.Expanding   # 垂直扩展
                )
                # 固定高度和最小宽度
                btn.setFixedHeight(40)      # 固定高度40px
                btn.setMinimumWidth(80)     # 最小宽度80px
            
                # 设置按钮样式（可选）
                btn.setStyleSheet("""
                    QPushButton {
                       margin: 2px;         /* 按钮内边距 */
                      padding: 10px;        /* 文字内边距 */
                     font-size: 35px;
                  }
                """)
                # 设置按钮的最大高度和最小尺寸
                btn.setMaximumHeight(120)  # 设置最大高度为40px
                btn.setMinimumSize(80, 30)  # 最小宽度80px，高度30px

                vbox.addWidget(btn)
                index += 1
            
            # 4. 将垂直布局添加到主水平布局
            main_hbox.addLayout(vbox)
            main_hbox.setSpacing(10)  # 列间距

        # 5. 创建栅格布局作为容器
        grid = QGridLayout(self.groupBox_input)
        grid.addLayout(main_hbox, 0, 0)  # 将主水平布局放入网格
        
        # 6. 设置拉伸比例
        grid.setRowStretch(0, 1)
        grid.setColumnStretch(0, 1)
        
        # 7. 调整边距和间距
        grid.setContentsMargins(5, 5, 5, 5)  # 外边框
        main_hbox.setContentsMargins(0, 0, 0, 0)  # 列组内边距
        
         # 8. 应用布局
        self.groupBox_input.setLayout(grid)


    def btn_output_init(self):
        # 1. 创建水平布局 hbox 并添加按钮
        hbox = QHBoxLayout()
        hbox.setSpacing(300)  # 按钮之间的固定间距（可根据需要调整）
        hbox.setContentsMargins(400, 0, 400, 0)  # 左右边距40px（保持两侧对称）
        index = 1
        for i in range(5):
            btn = QPushButton('motor'+str(index), self.groupBox_output)
            font = QFont('微软雅黑', 50)
            font.setPointSize(55)  # 设置字体大小
            btn.setFont(font)
            btn.setAccessibleDescription("0")
            btn.setAccessibleName(str(index))
            self.btn_output.append(btn)
            
            # 设置按钮的大小策略（水平+垂直均扩展）
            btn.setSizePolicy(
                QSizePolicy.Expanding,  # 水平策略：尽量扩展
                QSizePolicy.Maximum    # 垂直策略：不超过最大高度
            )

            # 设置按钮的最大高度和最小尺寸
            #btn.setFixedHeight(80)      # 固定高度80px
            btn.setMaximumHeight(150)  # 设置最大高度为80px
            #btn.setMaximumWidth(200)  # 设置最小高度为40px
            btn.setMinimumSize(80, 30)  # 最小宽度80px，高度30px
            
            # 可选：设置最小大小（避免按钮过小）
            # btn.setMinimumSize(60, 30)  # 最小宽度60px，高度30px
            
            hbox.addWidget(btn)
            index += 1

        # 2. 创建栅格布局 grid，并让 hbox 占据整个空间
        grid = QGridLayout(self.groupBox_output)  # 直接关联到 groupBox_output
        grid.addLayout(hbox, 0, 0)  # hbox 添加到 grid 的第0行第0列

        # 3. 关键：设置行和列的拉伸比例，让 hbox 充满整个 groupBox_output
        grid.setRowStretch(0, 1)    # 第0行拉伸
        grid.setColumnStretch(0, 1)  # 第0列拉伸

        # 4. 可选：去掉布局边距和间距，确保完全填满
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(5)  # 按钮之间的间距

        # 5. 设置 groupBox_output 的布局为 grid
        self.groupBox_output.setLayout(grid)
        
        # 连接按钮点击信号
        for each in self.btn_output:
            each.clicked.connect(lambda: self.btn_output_clicked(self.sender()))


    def show_btn_input(self):   
        text = 0     
        for i in range(3):            
            for j in range(2):
                if  self.mbus.cur_reg[text] == 0:
                    self.btn_input[text].setStyleSheet("background-color:green")
                else:
                    self.btn_input[text].setStyleSheet("background-color:red")
                text += 1  


    @pyqtSlot()
    def on_btn1_clicked(self):
          self.trig_pusher( 1)
          time.sleep(0.5)
          self.trig_pusher( 2)
          time.sleep(0.5)
          self.trig_pusher( 3)
          print("btn1 clicked ") 


    def trig_pusher(self,num):
        btn=self.btn_output[num] 
        No = int(btn.accessibleName())-1
        if  btn.accessibleDescription()=='0':
            self.mbus.VALUES[No] = 62580
            btn.setAccessibleDescription("1")
        self.mbus.func = 1



    def back(self):#推杆返回控制 通过定时器轮询实现
        t = time.time()
        signal = 0
        for i in range(5):
            if self.mbus.coils[i] == 1:
                if t - self.t_put[i] > 0.7:
                    signal = 1
                    self.mbus.VALUES[i] = 0
                    self.btn_output[i].setAccessibleDescription("0")
        if signal == 1:
            self.mbus.func = 1


    @pyqtSlot()
    def btn_output_clicked(self, btn):
        if not self.mbus.isopend:
            QMessageBox.warning(self, "提示", "未连接串口")
        else:
            No = int(btn.accessibleName())-1
            if  btn.accessibleDescription()=='0':
                self.mbus.COIL_VALUE[No] = 62580
                btn.setAccessibleDescription("1")
            self.mbus.func = 1


    @pyqtSlot()
    def on_btn_start_clicked(self):
        print("btn_start do")
        #print(self.width(),self.height())
        #开始运行识别
        self.load_HSV_ranges()
        self.mode = self.comboBox_mode.currentText()
        if self.mode == "形状":
            self.model = YOLO("yolov8n.pt")
        if not self.mbus.isopend:
            self.serial_connect()
            if self.mbus.isopend:
                port = self.comboBox_1.currentText()
                QMessageBox.warning(self, f"提示", "未提前设置串口，已自动连接{text}")
            else :
                QMessageBox.warning(self, f"错误", "未提前设置串口，自动连接{text}失败")


    def read_colors(self):
         # 读取 color.ini 并还原 color_ranges
        cfg = configparser.ConfigParser()
        cfg.read('color.ini', encoding='utf-8')
        ranges_str = cfg['COLOR_RANGES']['ranges']
        color_ranges = json.loads(ranges_str)  # 还原为 dict

        # 如果你需要把键从 str 转回 int：
        color_ranges = {int(k): v for k, v in color_ranges.items()}

        # 调试打印
        print("已重新加载 color_ranges:", color_ranges) 

    @pyqtSlot()
    def on_btn_reset_clicked(self):
        print("btn_reset do")
        
        self.read_colors()
        self.mode = None
        self.mbus.func = 0  
        self.mbus.config = []
        self.t_put = [time.time() for _ in range(5)]
        self.mbus.count_trig_u = [0]*6
        cloth = []
        if self.mbus.isopend :
            signal = False
            for i in self.mbus.coils:
                if i > 0 :
                    signal = True
            if signal :
                self.mbus.VALUES[0] = 0
                self.btn_output_clicked(self.btn_output[0])



    # @pyqtSlot()
    # def show_img(self):
        if self.mode is not None:
            frame = self.streamer.grab_frame() 
            if frame is not None:
                print("Top-left pixel (B,G,R):", frame[0, 0])  # OpenCV默认是BGR
                len_x = frame.shape[1]  # 获取图像大小
                wid_y = frame.shape[0]
                frame11 = QImage(frame.data, len_x, wid_y, len_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
                pix = QPixmap.fromImage(frame11)   
                pix = pix.scaledToWidth(345)
                self.img_orign.setPixmap (pix)  # 在label上显示图片

                #koutu  zai koutu_img  shang xianshi 
                # 定义裁剪区域
                # 格式：[起始x坐标, 起始y坐标, 宽度, 高度]
                # 注意：坐标从左上角开始，x向右增加，y向下增加
                crop_x = 100  # 起始x坐标
                crop_y = 0   # 起始y坐标
                crop_width = 500  # 裁剪宽度
                crop_height = 400  # 裁剪高度

                # 裁剪图片
                # OpenCV 的裁剪操作是通过 NumPy 的数组切片实现的
                frame_koutu = frame[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]


                frame_koutu=self.tune_hsv_threshold(frame_koutu)
                #在此处更新了self.average_hsv，现在的抠图算法，手动识别

                #frame_koutu=self.cutoff_img(frame_koutu)
                #在此处更新了self.average_hsv，原本的抠图算法，自动识别

                len_koutu_x = frame_koutu.shape[1]  # 获取图像大小
                wid_koutu_y = frame_koutu.shape[0]
                frame_koutu = QImage(frame_koutu.data, len_koutu_x, wid_koutu_y, len_koutu_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
                pix_koutu = QPixmap.fromImage(frame_koutu)   
                pix_koutu = pix_koutu.scaledToWidth(345)
                self.txt_hsv.setPlainText(str(self.average_hsv))
                self.koutu_img.setPixmap (pix_koutu)  
                # # 在label上显示图片,koutu_img函数是返回

                #此处是已经处理好的图片，正将其显示出来，并且更新均值hsv

                #return

                #判断下降沿与上升沿
                if  self.mbus.trig_status[0]==1 :
                    #print(self.average_hsv.tolist())e
                    self.worker[1]=self.average_hsv.tolist()

                for i in range(5):
                    try:
                        print("workers",self.worker)
                        b=i+1
                        if  self.mbus.trig_status[b]==1  :
                            print("worker:",self.worker[b])
                            print("index :",b)
                        
                            if self.hsv_in_range(self.worker[b],color_ranges[i][0],color_ranges[i][1]):
                                self.trig_pusher(i)#推杆推出，信号变化
                                # self.t_put[i] = time.time()#记录推杆推出的时间
                                # self.mbus.coils[i] = 1 #记录线圈变化状态



                        if  self.mbus.trig_status[b]==2  :
                            self.worker[b+1]=self.worker[b]
                            self.worker[b] = []
                    except:
                        continue


    # @pyqtSlot()
    # def update(self):
    #     if self.mode is not None:
    #         frame = self.streamer.grab_frame() 
    #         if frame is not None:
    #             self.show_orin_img(frame)#在Qt上显示原图
    #             frame_koutu = self.cut_img(frame)#裁剪图片
    #             frame_koutu=self.tune_hsv_threshold(frame_koutu)#若触发相机位传感器下降沿则调色
    #             self.average_hsv = np.mean(frame_koutu, axis=0)
    #             non_zero_pixels = frame_koutu[]
    #             self.show_fix_img(frame_koutu)

    #             #判断下降沿与上升沿
    #             if  self.mbus.trig_status[0]==1 :

    #                 #在此处更新了self.average_hsv，现在的抠图算法，手动识别
    #                 #frame_koutu=self.cutoff_img(frame_koutu)
    #                 #在此处更新了self.average_hsv，原本的抠图算法，自动识别
    #                 #此处是已经处理好的图片，正将其显示出来，并且更新均值hsv
    #                 #print(self.average_hsv.tolist())
    #                 self.worker[1]=self.average_hsv.tolist()

    #             for i in range(5):
    #                 try:
    #                     #print("workers",self.worker)
    #                     b=i+1
    #                     if  self.mbus.trig_status[b]==1  :
    #                         print("worker:",self.worker[b])
    #                         print("index :",b)
                        
    #                         if self.hsv_in_range(self.worker[b],color_ranges[i][0],color_ranges[i][1]):
    #                             self.trig_pusher(i)#推杆推出，信号变化
    #                             # self.t_put[i] = time.time()#记录推杆推出的时间
    #                             # self.mbus.coils[i] = 1 #记录线圈变化状态
    #                     if  self.mbus.trig_status[b]==2  :
    #                         self.worker[b+1]=self.worker[b]
    #                         self.worker[b] = []
    #                 except:
    #                     continue


    @pyqtSlot()
    def update(self):
        if self.mode is not None:
            frame = self.streamer.grab_frame() 
            if frame is not None:
                self.show_orin_img(frame)  # 在Qt上显示原图
                frame_koutu = self.cut_img(frame)  # 裁剪图片
                frame_koutu = self.tune_hsv_threshold(frame_koutu)  # 切图
                
                self.calculate_ave_hsv(frame_koutu) # 计算平均值
                self.show_fix_img(frame_koutu) # 在Qt上显示切完的图

                # 判断下降沿与上升沿
                if self.mbus.trig_status[0] == 1:
                    self.worker[1] = self.average_hsv.tolist()
                for i in range(5):
                    try:
                        b = i + 1
                        if self.mbus.trig_status[b] == 1:
                            print("worker:", self.worker[b])
                            print("index:", b)
                            
                            if self.hsv_in_range(self.worker[b], color_ranges[i][0], color_ranges[i][1]):
                                self.trig_pusher(i)  # 推杆推出，信号变化
                        if self.mbus.trig_status[b] == 2:
                            self.worker[b+1] = self.worker[b]
                            self.worker[b] = []
                    except:
                        continue


    def calculate_ave_hsv(self,frame_koutu):
        # 使用改进的HSV均值计算方法（原cutoff_img的逻辑）
        gray_image = cv2.cvtColor(frame_koutu, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        masked_image = cv2.bitwise_and(frame_koutu, frame_koutu, mask=binary)
        non_zero_pixels = masked_image[binary > 0]
                
        # 计算HSV平均值
        if len(non_zero_pixels) > 0:
            hsv_pixels = cv2.cvtColor(non_zero_pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2HSV)
            self.average_hsv = np.mean(hsv_pixels, axis=0).flatten()
        else:
            self.average_hsv = np.array([0, 0, 0])  # 默认值
                


    def cut_img(self,frame):
        #koutu  zai koutu_img  shang xianshi 
        # 定义裁剪区域
        # 格式：[起始x坐标, 起始y坐标, 宽度, 高度]
        # 注意：坐标从左上角开始，x向右增加，y向下增加
        crop_x = 100  # 起始x坐标
        crop_y = 0   # 起始y坐标
        crop_width = 500  # 裁剪宽度
        crop_height = 400  # 裁剪高度

        # 裁剪图片
        # OpenCV 的裁剪操作是通过 NumPy 的数组切片实现的
        return frame[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
        



    def show_orin_img(self, frame_orin):
        # 将 BGR 转换为 RGB
        rgb_image = cv2.cvtColor(frame_orin, cv2.COLOR_BGR2RGB)
        len_x = rgb_image.shape[1]  # 获取图像宽度
        wid_y = rgb_image.shape[0]  # 获取图像高度
        
        # 创建 QImage，使用 RGB888 格式
        frame = QImage(rgb_image.data, len_x, wid_y, len_x * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        pix = pix.scaledToWidth(345)
        self.img_orign.setPixmap(pix)  # 在label上显示图片


    def show_fix_img(self,frame_fix):
        """
        在text_hsv上显示图片
        """
        rgb_image = cv2.cvtColor(frame_fix, cv2.COLOR_BGR2RGB)
        len_x = rgb_image.shape[1]  # 获取图像宽度
        wid_y = rgb_image.shape[0]  # 获取图像高度
        
        # 创建 QImage，使用 RGB888 格式
        frame = QImage(rgb_image.data, len_x, wid_y, len_x * 3, QImage.Format_RGB888)
        #frame_fix = QImage(frame_fix.data, len_koutu_x, wid_koutu_y, len_koutu_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
        pix_koutu = QPixmap.fromImage(frame)   
        pix_koutu = pix_koutu.scaledToWidth(345)

        #print(self.average_hsv)
        self.txt_hsv.setPlainText(str(self.average_hsv))
        self.koutu_img.setPixmap (pix_koutu)  
        # # 在label上显示图片,koutu_img函数是返回


    def hsv_in_range(self, average,lower,upper):
        print("average111：",average,len(average))

        if (lower[0] <= average[0] <= upper[0] and
            lower[1] <= average[1] <= upper[1] and
            lower[2] <= average[2] <= upper[2]):
            return True
        return False # 如果没有匹配的颜色范围，返回 None


              #jisuan pingjun hsv 
              #txt_hsv.setPlainText(str_trig)


             
            #if self.mode == "形状":
            #    self.match_shape(frame)
            #elif self.mode == "白浅深":
            #    self.match_color(frame)
           
             #self.trig_pusher  
        # str_trig="trig= "+str(self.mbus.trig_status[0])+str(self.mbus.trig_status[1])+str(self.mbus.trig_status[2])+str(self.mbus.trig_status[3])+str(self.mbus.trig_status[4])+str(self.mbus.trig_status[5]) 
        # self.txt_trg_state.setPlainText(str_trig)
        #koutu deidao  img_koutu


    def tune_hsv_threshold(self,img):
        """
        手动调整HSV阈值并返回处理后的图像
        """
        #img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError('图片没找到')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (self.hmin, self.smin, self.vmin), (self.hmax, self.smax, self.vmax))
        mask = cv2.bitwise_not(mask)  # 1=衣物区域
        vis = cv2.bitwise_and(img, img, mask=mask)
        return vis  # 返回处理后的图像


    # def cutoff_img(self,img):
    #     # 读取灰度图
    #     #img = cv2.imread('333.jpg', 0)
    #     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     # Otsu自动阈值分割
    #     _, binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #     masked_image = cv2.bitwise_and(img, img, mask=binary)
    #     non_zero_pixels = masked_image[binary > 0]

    #     # 计算平均值
    #     self.average_hsv = np.mean(non_zero_pixels, axis=0)
    #     return  masked_image
        

    def match_shape(self,frame):
        img_yolo = self.model(frame, verbose=False)
        for result in img_yolo:
        # 获取检测到的类别、置信度、边界框
            for box in result.boxes:
                class_id = int(box.cls)  # 类别ID
                class_name = self.model.names[class_id]  # 类别名称（如 'person', 'car'）
                confidence = float(box.conf)  # 置信度（0~1）
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # 边界框坐标（左上、右下）
                print(f"检测到: {class_name}, 可信度: {confidence:.2f}, 位置: {x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}")                  
                # 可以在这里做进一步处理，比如筛选高置信度的目标
                if confidence > 0.6:
                    print(f"高可信度目标: {class_name} ({confidence:.2f})")

        frame = img_yolo[0].plot()    
       



    @pyqtSlot()
    def show_time(self):
        """更新并显示时间的槽函数"""
        # 更新时间
        self.base += 1
        if self.base >= 10:  # 改为 >= 更安全
            self.sec += self.base // 10  # 处理base超过10的情况
            self.base %= 10
        
        if self.sec >= 60:  # 改为 >= 更安全
            self.min += self.sec // 60
            self.sec %= 60
        
        if self.min >= 60:  # 改为 >= 更安全
            self.hour += self.min // 60
            self.min %= 60
        
        # 使用f-string格式化字符串更简洁高效
        self.setWindowTitle(f"{self.hour:02d}:{self.min:02d}:{self.sec:02d}:{self.base:01d}")
        try:     
            self.show_btn_output()
            self.show_btn_input()
        except:
            pass



    def show_btn_output(self):   
        for i in range(5):            
            if  self.mbus.coils[i] == 0:
                self.btn_output[i].setStyleSheet("background-color:red")
            else:
                self.btn_output[i].setStyleSheet("background-color:green")



    def setup_led_indicator(self):
        """设置圆形LED指示灯"""
        self.Light.setText("")  # 清空文本
        self.Light.setFixedSize(40, 40)
        
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(255, 0, 0))  # 红色
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 38, 38)  # 留1像素边距
        painter.end()
        
        self.Light.setPixmap(pixmap)
        self.Light.setScaledContents(True)



    def update_led(self, color):
        """更新LED颜色"""
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 38, 38)
        painter.end()
        self.Light.setPixmap(pixmap)



    @pyqtSlot()
    def serial_connect(self):
        """连接/断开MODBUS设备"""
        if not self.mbus.isopend:
            try:
                self.mbus.PORT = self.comboBox_1.currentText()
                self.mbus.BOARD_RATE = int(self.comboBox_2.currentText())
                self.mbus.open()
                if self.mbus.isopend:
                    self.pushButton.setText("断开")
                    self.update_led(Qt.green)  # 绿色表示已连接                    
                else:
                    QMessageBox.warning(self, "错误", "连接失败!")
            except Exception as e:
                QMessageBox.critical(self, "异常", f"连接错误: {str(e)}")
        else:
            if  self.mbus.isopend:
                self.mbus.close()
                self.pushButton.setText("连接")
                self.update_led(Qt.red)  # 红色表示未连接



    @pyqtSlot()
    def serial_close(self):
        if  self.mbus.isopend:
            self.mbus.close()
            self.pushButton.setText("连接")
            self.update_led(Qt.red)  # 红色表示未连接



    @pyqtSlot()    
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,
            '本程序',
            "是否要退出程序？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.streamer.close_cam()
            self.mbus.end = True
            event.accept()
            time.sleep(0.1)
        else:
            event.ignore()   



    def save(self):
        print("保存配置")
        rows=self.tableWidget.rowCount()
        cols=self.tableWidget.columnCount()
        try:  
            data=""
            for i in range(rows):
                data=data+str(i+1)+","
                for j in range(0, cols, 1):
                    data=data+self.tableWidget.item(i, j).text()+","
                data = data +"\n"
                
            data=data+"\r\n"
            f = open(r'config.ini','w+', encoding='utf-8')
            f.write(data)
            f.close()
        except:
            QMessageBox.critical(self, "配置错误", " 无法保存配置文件！")   



    @pyqtSlot()
    def on_btn_load_clicked(self):
        print('加载配置')
        self.tableWidget.setRowCount(0)  # 清空表格
        try: 
            with open('config.ini', 'r', encoding='utf-8') as f:
                for line in f:  # 直接遍历文件对象
                    line = line.strip()  # 去除首尾空白字符
                    if not line:  # 跳过空行
                        continue
                        
                    print('读取行:', line)
                    cells = line.split(",")
                    
                    # 确保有足够的列数
                    if len(cells) >= 4:  # 假设需要4列数据
                        self.insert_sys_cfg_line(cells[1], cells[2],cells[3])  #cells[0]  == 序号 == sid
                    else:
                        print(f"忽略不完整的行: {line}")

                    d = list(filter(None, cells[2].split(" ")))  # 过滤掉空字符串

                    if len(d) >= 2:  # 确保至少有2个有效值
                        self.mbus.config.append([int(cells[0]),int(d[0]),int(d[1]),int(d[2])])#sid
                    else :
                        pass
        except FileNotFoundError:
            QMessageBox.critical(self, "配置错误", "配置文件不存在！")
        except Exception as e:
            QMessageBox.critical(self, "配置错误", f"读取配置文件时出错: {str(e)}")
       # print(self.mbus.speed)



    @pyqtSlot()
    def on_btn_add_clicked(self):
        self.insert_sys_cfg_line("NAME","DATA","TIPS")



    @pyqtSlot()
    def on_btn_apply_clicked(self):
        if not self.mbus.isopend:
            QMessageBox.warning(self, "提示", "未连接串口")
        else:
            self.save()
            self.on_btn_load_clicked()
            print("设置电机：")
            self.mbus.func = 2

    # @pyqtSlot()
    # def on_btn_load_2_clicked(self):
    #     print("back to zero")
    #     self.mbus1 = mbs.MBUS(PORT='COM3')
    #     self.mbus1.open()
    #     if self.mbus1.isopend:
    #         time.sleep(0.1)
    #         self.mbus1.PORT = self.comboBox_1.currentText()
    #         self.mbus1.BOARD_RATE = int(self.comboBox_2.currentText())
    #         self.mbus1.back()
    #         time.sleep(0.1)
    #     self.mbus1.close()



    def insert_sys_cfg_line(self, cfg_name, cfg_dat, cfg_beizhu):
        print("插入行:", cfg_name, cfg_dat, cfg_beizhu)
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)  # 使用insertRow而不是setRowCount
        # 设置各列数据
        self.tableWidget.setItem(row, 0, QTableWidgetItem(cfg_name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(cfg_dat))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(cfg_beizhu))


    def update_HSV_values(self):
        # 1. 读取滑条值
        self.hmin = self.Hmin_slider.value()
        self.hmax = self.Hmax_slider.value()
        self.smin = self.Smin_slider.value()
        self.smax = self.Smax_slider.value()
        self.vmin = self.Vmin_slider.value()
        self.vmax = self.Vmax_slider.value()
        

    def save_HSV_ranges(self):
        cfg = configparser.ConfigParser()
        cfg['HSV'] = {
            'hmin': str(self.hmin),
            'hmax': str(self.hmax),
            'smin': str(self.smin),
            'smax': str(self.smax),
            'vmin': str(self.vmin),
            'vmax': str(self.vmax)
        }
        with open('ranges.ini', 'w', encoding='utf-8') as f:
            cfg.write(f)


    def load_HSV_ranges(self):
        import configparser
        cfg = configparser.ConfigParser()
        try:
            cfg.read('ranges.ini', encoding='utf-8')

            # 读取并转换成 int，再设置到滑条
            self.Hmin_slider.setValue(int(cfg['HSV']['hmin']))
            self.Hmax_slider.setValue(int(cfg['HSV']['hmax']))
            self.Smin_slider.setValue(int(cfg['HSV']['smin']))
            self.Smax_slider.setValue(int(cfg['HSV']['smax']))
            self.Vmin_slider.setValue(int(cfg['HSV']['vmin']))
            self.Vmax_slider.setValue(int(cfg['HSV']['vmax']))
        except (FileNotFoundError, KeyError, ValueError):
            # 文件不存在或字段缺失时使用默认值
            self.Hmin_slider.setValue(0)
            self.Hmax_slider.setValue(179)
            self.Smin_slider.setValue(0)
            self.Smax_slider.setValue(255)
            self.Vmin_slider.setValue(0)
            self.Vmax_slider.setValue(255)


def main():
    app = QApplication(sys.argv)
    window = Dialog()  
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()