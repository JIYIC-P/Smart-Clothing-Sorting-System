import time
import sys
from Ui_main_form import Ui_Dialog 
import cv2
import numpy as np
#颜色范围定义
color_ranges = {
    1 : ([0, 100, 100], [10, 255, 255]),      # 红色范围
    2 : ([40, 50, 50], [80, 255, 255]),       # 绿色范围
    3 : ([90, 50, 50], [130, 255, 255]),      # 蓝色范围
    4 : ([20, 100, 100], [30, 255, 255]),     # 黄色范围
}
# 定义阈值（可根据需求调整）
s_low = 30    # 低饱和度阈值（白色）
s_high = 150  # 高饱和度阈值（深色）
v_low = 50    # 低明度阈值（深色）
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
        self.mode = None
        self.mbus = mbs.MBUS()
        self.camera = True
        self.Ui_init()
        self.Timer_init()
        self.camera_init()
        self.mbus.sender.start()
        self.show_btn_output()
        self.show_btn_input()
        self.init_trigger()


    def camera_init(self):
        if (self.camera):
            stream_link = "rtsp://192.168.1.100/user=admin&password=&channel=1&stream=0.sdp?"
            self.streamer = ThreadedCamera(stream_link)
            self.streamer.open_cam()
            self.streamer.source=0


    def Timer_init(self):
        #加入小时，分钟，和一个base作为基准
        self.run_time_base=0
        self.run_tinme_hour=0
        self.run_time_min=0
        self.run_time_sec=0
        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)
        self.t_YoLo=QTimer()
        self.t_YoLo.timeout.connect(self.show_img)
        self.t_YoLo.start(100)
        self.t_back=QTimer()
        self.t_back.timeout.connect(self.back)
        self.t_back.start(100)
        
          
    def back(self):
        if self.mode is not None:
            t = time.time()
            signal = 0
            for i in range(5):
                if self.mbus.coils[i] == 1:
                    if t - self.mbus.t1[i] > 0.7:
                        signal = 1
                        self.mbus.values[i] = 0
                        self.btn_output[i].setAccessibleDescription("0")
            if signal == 1:
                self.mbus.func = 1


    def Ui_init(self):
        self.setupUi(self)
        self.btn_output = []
        self.btn_input = []
        self.pushButton.clicked.connect(self.serial_connection)
        self.btn_motor_init()
        self.btn_input_init()
        self.setup_led_indicator()
        self.init_sys_tble()
        self.update_all_fonts()
        # 在 Ui_init 或 setupUi 后添加
        self.label_2.setAlignment(Qt.AlignCenter)



    def resizeEvent(self, event):
        self.update_all_fonts()
        super().resizeEvent(event)



    def update_all_fonts(self):
        """根据窗口大小动态调整所有控件字体大小"""
        # 以1920x1080为基准，20为基准字号
        scale_factor = min(self.width() / 1440, self.height() / 900)
        font_size = max(12, int(20 * scale_factor * 1.2))  # 最小12
        font = QFont('微软雅黑', font_size)
        font.setBold(True)
        self.setFont(font)
        # 只想让表格内容和表头都变大，可以单独设置
        self.tableWidget.setFont(font)
        self.tableWidget.horizontalHeader().setFont(font)



    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "img"))
        self.btn_start.setText(_translate("Dialog", "开始"))
        self.btn_reset.setText(_translate("Dialog", "重置"))
        self.comboBox_mode.setItemText(0, _translate("Dialog", "颜色"))
        self.comboBox_mode.setItemText(1, _translate("Dialog", "白浅深"))
        self.comboBox_mode.setItemText(2, _translate("Dialog", "形状"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Tab 1"))
        self.groupBox_output.setTitle(_translate("Dialog", "GroupBox"))
        self.groupBox_input.setTitle(_translate("Dialog", "GroupBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))
        self.btn_load.setText(_translate("Dialog", "加载设置"))
        self.btn_add.setText(_translate("Dialog", "添加一行"))
        self.btn_apply.setText(_translate("Dialog", "应用"))
        self.label_1.setText(_translate("Dialog", "波特率"))
        self.label.setText(_translate("Dialog", "串口选择"))
        self.Light.setText(_translate("Dialog", "TextLabel"))
        self.pushButton.setText(_translate("Dialog", "连接"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "9600"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "38400"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "115200"))
        self.comboBox_1.setItemText(0, _translate("Dialog", "COM1"))
        self.comboBox_1.setItemText(1, _translate("Dialog", "COM2"))
        self.comboBox_1.setItemText(2, _translate("Dialog", "COM3"))
        self.comboBox_1.setItemText(3, _translate("Dialog", "COM4"))
        self.comboBox_1.setItemText(4, _translate("Dialog", "COM5"))
        self.comboBox_1.setItemText(5, _translate("Dialog", "COM6"))
        self.comboBox_1.setItemText(6, _translate("Dialog", "COM7"))
        self.comboBox_1.setItemText(7, _translate("Dialog", "COM8"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Tab3"))
        


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
            each.clicked.connect(lambda: self.out_btn_clicked(self.sender()))



    def init_trigger(self):
        """
        初始化触发器
        """
        self.reg_trigger = QTimer()
        self.reg_trigger.timeout.connect(self.trigger_check)
        self.reg_trigger.start(100)



    def trigger_check(self):
        """
        触发检查
        """
        for i in range(1,5):
            if self.mbus.trig_status[i] == 1: #trig_down
                t = self.mbus.count_trig_u[i]-self.mbus.count_trig_u[5]
                print("trig :",self.mbus.trig_status)
                print(f"tu[{i}]:",self.mbus.count_trig_u[i],"tu[5]",self.mbus.count_trig_u[5],"\ni:",i)

                if len(self.mbus.cloth)>0 :
                    if self.mbus.cloth[t] == i : #TODO:==推杆推动的条件 
                        self.mbus.values[i-1] = 62580
                        btn = self.btn_output[i-1]
                        if  btn.accessibleDescription()=='0':
                            btn.setAccessibleDescription("1")
                        self.mbus.func = 1
                        print("cloth before pop:",self.mbus.cloth)
                        self.mbus.cloth.pop(t)
                        print("cloth after  pop:",self.mbus.cloth)
                        time.sleep(0.2)
                        self.mbus.count_trig_u[5] += 1#在实际运行是该函数比控制更快，导致可能出现减两次,暂时使用延时等待策略，保证数据正确
                        

        if self.mbus.trig_status[5] == 1:
            if len(self.mbus.cloth)>0 :
                if self.mbus.cloth[0] < 0 : #TODO:==推杆推动的条件 
                    self.mbus.values[4] = 62580
                    self.mbus.func = 1
                    self.mbus.cloth.pop(0)
                    self.mbus.count_trig_u[5] += 1
        elif self.mbus.trig_status[5] == 2: #trig_up
            self.mbus.cloth.pop(0)



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
    def  out_btn_clicked(self, btn):
        if not self.mbus.isopend:
            QMessageBox.warning(self, "提示", "未连接串口")
        else:
            No = int(btn.accessibleName())-1
            if  btn.accessibleDescription()=='0':
                self.mbus.values[No] = 62580
                btn.setAccessibleDescription("1")
            self.mbus.func = 1



    @pyqtSlot()
    def  out_btn_start_clicked(self):
        #开始运行识别
        self.mode = self.comboBox_mode.currentText()
        if self.mode == "形状":
            self.model = YOLO("yolov8n.pt")




    @pyqtSlot()
    def  out_btn_reset_clicked(self):
        #重置所有动态参数，电机归位
        pass



    @pyqtSlot()
    def show_img(self):
        if self.mode is not None:
            if self.camera:
                frame = self.streamer.grab_frame()
                if self.mode == "形状":
                    self.match_shape(frame)
                elif self.mode == "颜色":
                    self.match_color(frame)




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
        if frame is not None:
            img = frame
            show_image =img
            len_x = show_image.shape[1]  # 获取图像大小
            wid_y = show_image.shape[0]
            frame = QImage(show_image.data, len_x, wid_y, len_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
            pix = QPixmap.fromImage(frame)   
            pix = pix.scaledToWidth(480)
            self.label_2.setPixmap (pix)  # 在label上显示图片




    def match_color(self,frame):
        if frame is None:
            time.sleep(0.1)
            return
                # 显示原始彩色图像（新增部分）
        height, width = frame.shape[:2]
        bytes_per_line = 3 * width
        qimg_original = QImage(
            frame.data, 
            width, 
            height, 
            bytes_per_line, 
            QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg_original).scaledToWidth(max(480, width))
        self.label_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_2.setMinimumSize(800, 660)  # 可根据需要设置更大
        self.label_2.setPixmap(pixmap)   # 显示原始图像

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        s = hsv[:, :, 1]  # 饱和度通道
        v = hsv[:, :, 2]  # 明度通道
        # 分类掩膜
        white_mask = (s < s_low) & (v > 200)      # 白色：低饱和度 + 高明度
        light_mask = (s >= s_low) & (s < s_high)  # 浅色：中等饱和度
        dark_mask = (s >= s_high) | (v < v_low)   # 深色：高饱和度 或 低明度

        # 统计各类像素数量
        results = {
            1: cv2.countNonZero(white_mask.astype(np.uint8)),#大白
            2: cv2.countNonZero(light_mask.astype(np.uint8)),#二白
            3: cv2.countNonZero(dark_mask.astype(np.uint8))#其他
        }
        self.control(results)
        # 显示图像（可选：用颜色标记分类结果）
        #if frame is not None:
        #    classified = np.zeros_like(frame)
        #    classified[white_mask] = [255, 255, 255]  # 白色
        #    classified[light_mask] = [200, 200, 200]  # 浅色（灰色）
        #    classified[dark_mask] = [50, 50, 50]      # 深色（深灰）
        #    # 转换为QImage并显示
            #height, width = classified.shape[:2]
            #qimage = QImage(
            #    classified.data, 
            #    width, 
            #    height, 
            #    width * 3, 
            #    QImage.Format_RGB888
            #)
            #pixmap = QPixmap.fromImage(qimage).scaledToWidth(480)
            #self.label_2.setPixmap(pixmap)




    def control(self,results):
        # 0号传感器下降沿触发
        if self.mbus.trig_status[0] == 1:
            if results:
                dominant_category = max(results, key=results.get)
                self.mbus.cloth.append(dominant_category)  # 添加到列表
            else:
                dominant_category = None  # 无分类结果



    @pyqtSlot()
    def showTime(self):
        """   
        Slot documentation goes here.
        """
        #self.setWindowTitle(str(round(self.run_time_hour))+":"+str(round(self.run_time_min))+":"+str(round(self.run_time_sec)))
        self.run_time_base=self.run_time_base+1
        self.run_time_sec=self.run_time_base
        self.run_time_min=self.run_time_sec//60
        self.run_time_hour=self.run_time_min//60
        self.run_time_min=self.run_time_min%60
        self.run_time_hour=self.run_time_hour%60
        self.run_time_sec=self.run_time_sec%60
        #self.run_time_sec=self.run_time_sec+1
        self.setWindowTitle(str(round(self.run_time_hour*0.1))+":"+str(round(self.run_time_min*0.1))+":"+str(round(self.run_time_sec*0.1, 2)))
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
        self.Light.setFixedSize(20, 20)
        
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(255, 0, 0))  # 红色
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 18, 18)  # 留1像素边距
        painter.end()
        
        self.Light.setPixmap(pixmap)
        self.Light.setScaledContents(True)



    def update_led(self, color):
        """更新LED颜色"""
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 18, 18)
        painter.end()
        self.Light.setPixmap(pixmap)



    @pyqtSlot()
    def serial_connection(self):
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
            if self.camera:
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



def main():
    app = QApplication(sys.argv)
    window = Dialog()  
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()