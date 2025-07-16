import time
import sys
from Ui_main_form import Ui_Dialog 
import cv2
import matplotlib.pyplot as plt
import numpy as np
import configparser
import json
import os
from datetime import datetime


# 1. 可调参数 -----------------------------------------------------------
CANNY_LOW   = 50
CANNY_HIGH  = 150
MIN_AREA    = 8000          # 衣物最小面积（像素），根据实际图片分辨率调整
CLOSE_KSIZE = (15, 15)      # 闭运算核大小
RESIZE_MAX  = 1024          # 最长边缩放（防止大图太慢，0 表示不缩放）
# -----------------------------------------------------------------------





# Qt核心模块
from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
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

        #颜色范围定义
        self.color_ranges = {
            0 : ([0, 0, 200], [180, 50, 255]),        # 白色范围
            1 : ([0, 100, 100], [10, 255, 255]),      # 红色范围
            2 : ([40, 50, 50], [80, 255, 255]),       # 绿色范围
            3 : ([90, 50, 50], [130, 255, 255]),      # 蓝色范围
            4 : ([20, 100, 100], [30, 255, 255]),     # 黄色范围
        }
        self.standrad_color = [[],[],[],[],[]]
        self.index=1
        self.list_hsv = []
        self.mode = None
        self.mbus = mbs.MBUS()
        self.Ui_init()
        self.Timer_init()
        self.camera_init()
        self.mbus.sender.start()
        self.show_btn_output()
        self.show_btn_input()
#        self.init_trigger()
        self.average_hsv = None
        self.worker=[-1,-1,-1,-1,-1,-1]
        self.pusher = [0,1,2,3,4]
       


    def camera_init(self):
        self.streamer = ThreadedCamera()
        self.streamer.init_camera()
        self.frame = None


    def Timer_init(self):
        #加入小时，分钟，和一个base作为基准
        self.base = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.timer=QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(100)
        self.t_YoLo=QTimer()
        self.t_YoLo.timeout.connect(self.show_img)
        self.t_YoLo.start(75)
        self.t_back=QTimer()
        self.t_back.timeout.connect(self.back)
        self.t_back.start(80)
        
          
    def back(self):
        t = time.time()
        signal = 0
        for i in range(5):
            if self.mbus.coils[i] == 1:
                if t - self.mbus.t1[i] > 0.6:
                    signal = 1
                    self.mbus.values[i] = 0
                    self.btn_output[i].setAccessibleDescription("0")
        if signal == 1:
            self.mbus.func = 1


    def Ui_init(self):
        self.setupUi(self)
        self.btn_output = []
        self.btn_input = []
        self.pushButton.clicked.connect(self.serial_connect)
        self.btn_motor_init()
        self.btn_input_init()
        self.setup_led_indicator()
        self.init_sys_tble()
        

    @pyqtSlot()
    def on_applay_clicked(self):

        
        range_col= self.average_hsv
        uper_num=self.float_value.toPlainText()
        down_num=self.float_value.toPlainText()
        index= self.choice_push.currentIndex()
        for i in range(3):
            self.color_ranges[index][0][i]= round(range_col[i]-int(down_num),2)
            self.color_ranges[index][1][i]= round(range_col[i]+int(uper_num),2)

        #print("self.color_ranges:",self.color_ranges)
        # 将字典转为字符串后写入 INI
        cfg = configparser.ConfigParser()
        cfg['COLOR_RANGES'] = {'ranges': json.dumps(self.color_ranges)}
        with open('color.ini', 'w', encoding='utf-8') as f:
            cfg.write(f)


        self.txt_hsv_3.setPlainText(str(self.standrad_color))


    def resizeEvent(self, event):
        self.update_all_fonts()
        super().resizeEvent(event)

    def get_std_color(self):
        for i in range(5):
            for j in range(3):
                self.standrad_color[i].append(round((self.color_ranges[i][0][j]+self.color_ranges[i][1][j])/2,2))


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



    def btn_motor_init(self):
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
            each.clicked.connect(lambda: self.btn_out_clicked(self.sender()))

     



    # def init_trigger(self):
    #     """
    #     初始化触发器
    #     """
        #self.reg_trigger = QTimer()
        #self.reg_trigger.timeout.connect(self.trigger_check)
        #self.reg_trigger.start(100)



    # def trigger_check(self):
    #     """
    #     触发检查
    #     """
    #     for i in range(1,5):
    #         if self.mbus.trig_status[i] == 1: #trig_down
    #             t = self.mbus.count_trig_u[i]-self.mbus.count_trig_u[5]
    #             print("trig :",self.mbus.trig_status)
    #             print(f"tu[{i}]:",self.mbus.count_trig_u[i],"tu[5]",self.mbus.count_trig_u[5],"\ni:",i)

    #             if len(cloth)>0 :
    #                 if cloth[t] == i : #TODO:==推杆推动的条件 
    #                     self.mbus.values[i-1] = 62580
    #                     btn = self.btn_output[i-1]
    #                     if  btn.accessibleDescription()=='0':
    #                         btn.setAccessibleDescription("1")
    #                     self.mbus.func = 1
    #                     print("cloth before pop:",cloth)
    #                     cloth.pop(t)
    #                     print("cloth after  pop:",cloth)
    #                     time.sleep(0.2)
    #                     self.mbus.count_trig_u[5] += 1#在实际运行是该函数比控制更快，导致可能出现减两次,暂时使用延时等待策略，保证数据正确
                        

    #     if self.mbus.trig_status[5] == 1:
    #         if len(cloth)>0 :
    #             if cloth[0] < 0 : #TODO:==推杆推动的条件 
    #                 self.mbus.values[4] = 62580
    #                 self.mbus.func = 1
    #                 cloth.pop(0)
    #                 self.mbus.count_trig_u[5] += 1
    #     elif self.mbus.trig_status[5] == 2: #trig_up
    #         cloth.pop(0)



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
                self.mbus.values[No] = 62580
                btn.setAccessibleDescription("1")
          self.mbus.func = 1
          

    @pyqtSlot()
    def btn_out_clicked(self, btn):
        if not self.mbus.isopend:
            QMessageBox.warning(self, "提示", "未连接串口")
        else:
            No = int(btn.accessibleName())-1
            if  btn.accessibleDescription()=='0':
                self.mbus.values[No] = 62580
                btn.setAccessibleDescription("1")
            self.mbus.func = 1


    @pyqtSlot()
    def on_btn_start_clicked(self):
        print("btn_start do")
        #print(self.width(),self.height())
        #开始运行识别
        time.sleep(0.1)
        self.load_color_range()
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
        self.txt_hsv_3.setPlainText(str(self.standrad_color))


    def load_color_range(self):
         # 读取 color.ini 并还原 self.color_ranges
        cfg = configparser.ConfigParser()
        cfg.read('color.ini', encoding='utf-8')
        ranges_str = cfg['COLOR_RANGES']['ranges']
        self.color_ranges = json.loads(ranges_str)  # 还原为 dict

        # 如果你需要把键从 str 转回 int：
        self.color_ranges = {int(k): v for k, v in self.color_ranges.items()}

        # 调试打印
        print("已重新加载 self.color_ranges:", self.color_ranges)
        self.get_std_color()


    @pyqtSlot()
    def on_btn_reset_clicked(self):
        print("btn_reset do")
        
        self.standrad_color = [[],[],[],[],[]]
        self.mode = None
        self.mbus.func = 0  
        self.mbus.config = []
        self.mbus.t1 = [time.time() for _ in range(5)]
        self.mbus.count_trig_u = [0]*6
        self.worker=[-1,-1,-1,-1,-1,-1]
        if self.mbus.isopend :
            signal = False
            for i in self.mbus.coils:
                if i > 0 :
                    signal = True
            if signal :
                self.mbus.values[0] = 0
                self.btn_out_clicked(self.btn_output[0])


    def segment_one(self,img_in, out_dir):
        #img_bgr = cv2.imread(path)
        img_bgr=img_in
        img_bgr = cv2.cvtColor(img_in,cv2.COLOR_RGB2BGR)
        #if img_bgr is None:
        #    print(f'[WARN] 无法读取 {path}')
        #    return
        orig = img_bgr.copy()
        #img_bgr = auto_resize(img_bgr, RESIZE_MAX)

        # ========== 1. HSV 颜色分割：把传送带区域排除 ==========
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        # 以下范围需要根据自己传送带颜色再微调，这里给出一套“通用传送带”示例
        # 如果传送带是灰色/米色，低饱和低亮度；衣物花色/白色则相反
        # lower_belt = np.array([57, 0, 17])        # 低饱和、中低亮度
        # upper_belt = np.array([180, 170, 230])    # 高亮度或低饱和均判为传送带

        lower_belt = np.array([30, 0, 0])        # 低饱和、中低亮度
        upper_belt = np.array([80, 255, 255])    # 高亮度或低饱和均判为传送带
        belt_mask  = cv2.inRange(hsv, lower_belt, upper_belt)

        # 反转：1 = 衣物，0 = 传送带
        fg_mask = cv2.bitwise_not(belt_mask)

        # ========== 2. 形态学闭运算，填补衣物内部空洞 ==========
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, CLOSE_KSIZE)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # ========== 3. 轮廓过滤（同原逻辑） ==========
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            #print(f'[WARN] 未检测到衣物 {os.path.basename(path)}')  报错
            print(f'[WARN] 未检测到衣物 ')   
            pass

        mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)
        for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
            area = cv2.contourArea(cnt)
            if area < MIN_AREA:
                break
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = max(w, h) / (min(w, h) + 1e-5)
            if ratio > 5:
                continue
            cv2.drawContours(mask, [cnt], -1, 255, -1)


        # ========== 4. 输出透明 PNG ==========
        h, w = orig.shape[:2]
        scale = img_bgr.shape[1] / w
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
        b, g, r = cv2.split(orig)
        rgba = cv2.merge((b, g, r, mask))

        masked_image = cv2.bitwise_and(orig, orig, mask=mask)
        non_zero_pixels = masked_image[mask > 0]
        # if non_zero_pixels[:, 0].max() > 180:  # 检查 H 是否被错误缩放
        #     non_zero_pixels[:, 0] = (non_zero_pixels[:, 0] / 255) * 180  # 从 0-255 映射回 0-180
        # 计算平均值
        if len(non_zero_pixels) > 0:  # 检查数组是否非空
    
            self.average_hsv = np.mean(non_zero_pixels, axis=0)

        if  self.mbus.trig_status[0] == 1:
             out_dir  = 'result'
             path= datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
             path1= datetime.now().strftime("%Y-%m-%d-%H-%M-%S-1")
             os.makedirs(out_dir, exist_ok=True)
             out_path = os.path.join(out_dir, os.path.splitext(os.path.basename(path))[0] + '.png')
             out_path1 = os.path.join(out_dir, os.path.splitext(os.path.basename(path))[0] + '.png')
             cv2.imwrite(out_path, masked_image)
             cv2.imwrite(out_path1, orig)
             print(self.average_hsv)
             print(f'[OK] 已保存 {out_path}')

        
        return masked_image

    @pyqtSlot()
    def show_img11(self):
        if self.mode is not None:
            myimg = self.streamer.grab_frame() 
           
            if myimg is not None:
                frame = cv2.cvtColor(myimg,cv2.COLOR_BGR2RGB)
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


                crop_x = 960  # 起始x坐标
                crop_y = 0   # 起始y坐标
                crop_width = 384  # 裁剪宽度
                crop_height = 270  # 裁剪高度

                # 裁剪图片
                # OpenCV 的裁剪操作是通过 NumPy 的数组切片实现的
                frame_koutu = frame[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
                frame_koutu = self.segment_one(frame_koutu,"sds")#在此处更新了self.average_hsv
                len_koutu_x = frame_koutu.shape[1]  # 获取图像大小
                wid_koutu_y = frame_koutu.shape[0]
                frame_koutu = QImage(frame_koutu.data, len_koutu_x, wid_koutu_y, len_koutu_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
                  
                pix_koutu = QPixmap.fromImage(frame_koutu)   
                pix_koutu = pix_koutu.scaledToWidth(345)

                self.koutu_img.setPixmap (pix_koutu)  # 在label上显示图片
                if self.average_hsv is not None:
                    self.list_hsv = self.average_hsv.tolist()
                    if self.average_hsv is not None:
                        self.list_hsv = [round(x, 2) for x in self.average_hsv.tolist()]
                self.txt_hsv.setPlainText(str(self.list_hsv))
                #return


                if  self.mbus.trig_status[0] == 2 :
                    #print(self.average_hsv.tolist())
                    for i in range(5):
                        if self.hsv_in_range(self.list_hsv,self.color_ranges[i][0],self.color_ranges[i][1]):
                            self.worker[1] = i
                text = self.worker[1:6]+1
                self.txt_hsv_2.setPlainText(str(text))


                for i in range(5):
                    try:
                        b=i+1
                        if  self.mbus.trig_status[b] == 2  :  
                            if i!=self.worker[b]:
                                self.worker[b+1]=self.worker[b]
                                self.worker[b] = -1


                        if  self.mbus.trig_status[b] == 1  :
                            if self.worker[b] !=-1 :
                                self.trig_pusher(i)


                    except:
                        continue

    @pyqtSlot()
    def show_img(self):
       
        if self.mode is not None:
            myimg = self.streamer.grab_frame() 
            if myimg is not None:
                frame = cv2.cvtColor(myimg,cv2.COLOR_BGR2RGB)
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


                crop_x = 960  # 起始x坐标
                crop_y = 0   # 起始y坐标
                crop_width = 384  # 裁剪宽度
                crop_height = 270  # 裁剪高度

                # 裁剪图片
                # OpenCV 的裁剪操作是通过 NumPy 的数组切片实现的
                frame_koutu = frame[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
                frame_koutu = self.segment_one(frame_koutu,"sds")#在此处更新了self.average_hsv
                len_koutu_x = frame_koutu.shape[1]  # 获取图像大小
                wid_koutu_y = frame_koutu.shape[0]
                frame_koutu = QImage(frame_koutu.data, len_koutu_x, wid_koutu_y, len_koutu_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
                  
                pix_koutu = QPixmap.fromImage(frame_koutu)   
                pix_koutu = pix_koutu.scaledToWidth(345)

                self.koutu_img.setPixmap (pix_koutu)  # 在label上显示图片
                if self.average_hsv is not None:
                    self.list_hsv = self.average_hsv.tolist()
                    if self.average_hsv is not None:
                        self.list_hsv = [round(x, 2) for x in self.average_hsv.tolist()]
                self.txt_hsv.setPlainText(str(self.list_hsv))
                #return


                if  self.mbus.trig_status[0] == 2 :
                    print(self.list_hsv)
                    for i in range(5):
                        if self.hsv_in_range(self.list_hsv,self.color_ranges[i][0],self.color_ranges[i][1]):
                            self.worker[0] = i
                text = self.worker
                self.txt_hsv_2.setPlainText(str(text))


                for i in range(5):
                    try:

                        if  self.mbus.trig_status[i+1] == 2  :  
                            if self.worker[i] != -1:
                                self.worker[i+1] = self.worker[i]
                                self.worker[i] = -1


                        if  self.mbus.trig_status[i+1] == 1  :
                            if self.worker[i+1] == self.pusher[i] :#i是推杆的值
                                self.trig_pusher(i)
                                self.worker[i+1] = -1



                    except:
                        continue

    def hsv_in_range(self, average,lower,upper):
        #print("average111：",average)

        # if (lower[0] <= average[0] <= upper[0] and
        #     lower[1] <= average[1] <= upper[1] and
        #     lower[2] <= average[2] <= upper[2]):
        #     return True
        # return False # 如果没有匹配的颜色范围，返回 None
        if len(average)>0:
            if lower[0] <= average[0] <= upper[0] :
                if lower[1] <= average[1] <= upper[1] :
                    return True

                if lower[2] <= average[2] <= upper[2] :
                    return True

        return False # 如果没有匹配的颜色范围，返回 None


        



    def cutoff_img(self,img):
        # 读取灰度图
        #img = cv2.imread('333.jpg', 0)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Otsu自动阈值分割
        _, binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        masked_image = cv2.bitwise_and(img, img, mask=binary)
        non_zero_pixels = masked_image[binary > 0]

        # 计算平均值
        self.average_hsv = np.mean(non_zero_pixels, axis=0)
        return  masked_image
        




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



    def insert_sys_cfg_line(self, cfg_name, cfg_dat, cfg_beizhu):
        print("插入行:", cfg_name, cfg_dat, cfg_beizhu)
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)  # 使用insertRow而不是setRowCount
        # 设置各列数据
        self.tableWidget.setItem(row, 0, QTableWidgetItem(cfg_name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(cfg_dat))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(cfg_beizhu))



def main():
    app = QApplication(sys.argv)
    window = Dialog()  
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()