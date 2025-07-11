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
    QObject
)
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
    QTableWidgetItem
)

# 本地应用/库特定导入 (Local application)
import mbs
from usb_fresh_pic  import ThreadedCamera
from ultralytics import YOLO


class Dialog(QDialog,Ui_Dialog):
    def __init__(self, parent=None):
        
        super(Dialog, self).__init__(parent)
        self.mode = "color"
        self.mbus = mbs.MBUS()
        self.camera = True
        self.Ui_init()
        self.Timer_init()
        self.camera_init()
        self.mbus.sender.start()
        self.show_btn_output()
        self.show_btn_input()
        self.init_trigger()
        self.detar = [0,0,0,0,0]


    def camera_init(self):
        if (self.camera):
            stream_link = "rtsp://192.168.1.100/user=admin&password=&channel=1&stream=0.sdp?"
            self.streamer = ThreadedCamera(stream_link)
            self.streamer.open_cam()
            self.streamer.source=0
            if self.mode == "shape":
                self.model = YOLO("yolov8n.pt")

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
          


    def Ui_init(self):
        self.setupUi(self)
        self.btn_output = []
        self.btn_input = []
        self.pushButton.clicked.connect(self.serial_connection)
        self.btn_motor_init()
        self.btn_input_init()
        self.setup_led_indicator()
        self.init_sys_tble()

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        self.groupBox_output.setTitle(_translate("Dialog", "motor"))
        self.groupBox_input.setTitle(_translate("Dialog", "input"))

        Dialog.setWindowTitle(_translate("Dialog", "MODBUS协议测试"))
        self.pushButton.setText(_translate("Dialog", "连接"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "YoLo检测"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "测试"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "设置"))
        self.btn_load.setText(_translate("Dialog", "加载设置"))
        self.btn_add.setText(_translate("Dialog", "添加一行"))
        self.btn_apply.setText(_translate("Dialog", "应用"))
        self.mode_shift.setText(_translate("Dialog", "模式切换"))
        self.label.setText(_translate("Dialog", "串口选择"))
        self.label_1.setText(_translate("Dialog", "波特率"))
        self.comboBox_1.setItemText(0, _translate("Dialog", "COM1"))
        self.comboBox_1.setItemText(1, _translate("Dialog", "COM2"))
        self.comboBox_1.setItemText(2, _translate("Dialog", "COM3"))
        self.comboBox_1.setItemText(3, _translate("Dialog", "COM4"))
        self.comboBox_1.setItemText(4, _translate("Dialog", "COM5"))
        self.comboBox_1.setItemText(5, _translate("Dialog", "COM6"))
        self.comboBox_1.setItemText(6, _translate("Dialog", "COM7"))
        self.comboBox_1.setItemText(7, _translate("Dialog", "COM8"))

        self.comboBox_2.setItemText(0, _translate("Dialog", "38400"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "9600"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "115200"))

    def init_sys_tble(self):
        # 设置表头字体样式
        font = QFont('微软雅黑', 20)
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
        self.tableWidget.setColumnWidth(0, 120)    # 参数名
        self.tableWidget.setColumnWidth(1, 160)   # 参数值
        self.tableWidget.setColumnWidth(2, 450)   # 备注
        
        # 禁用排序
        self.tableWidget.setSortingEnabled(False)
        
        # 初始化表头内容
        headers = ["参数名", "参数值", "备注"]
        for col, text in enumerate(headers):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)  # 文字居中
            self.tableWidget.setHorizontalHeaderItem(col, item)
        
        self.on_btn_load_clicked()

    def btn_input_init(self):
        index = 1
        for i in range(4):
            for j in range(2):
                btn = QPushButton('input'+str(index), self.groupBox_input)
                btn.setGeometry(70 + i * 110, 30 + j*50, 90, 50)
                self.btn_input.append(btn)
                index += 1

    def btn_motor_init(self):
        index = 1
        for i in range(5):
            btn = QPushButton('motor'+str(index), self.groupBox_output)
            btn.setGeometry(10 + i * 110, 50, 90, 50)
            btn.setAccessibleDescription("0")
            btn.setAccessibleName(str(index))
            self.btn_output.append(btn)
            index += 1 
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

        #TODO: 这里需要写各个传感器触发后对应机械臂的行为，入队在show_img()函数中判断下降沿=》如果能改成在这里入队会更好

        if self.mbus.trig_status[0] == 1:#下降沿
            self.mbus.cloth.append()
            self.detar[0] += 1

        for i in range(4):# i+1 ：【1，4】
            if self.mbus.trig_status[i+1] == 1:#下降沿
                self.detar[i+1] += self.mbus.count_trig_d[i+1]-self.mbus.count_trig_u[5]
            elif self.mbus.trig_status[i+1] == 2:#上升沿似乎无变化
                pass                

        if self.mbus.trig_status[5] == 2:#最后一个传感器上升沿出队
            self.mbus.cloth.pop(0)
    @pyqtSlot()
    def on_mode_shift_clicked(self):
        if self.mode == "color":
            self.mode = "shape"
            self.mode_shift.setText("形状检测")
        elif self.mode == "shape":
            self.mode = "color"
            self.mode_shift.setText("颜色检测")
    def show_btn_input(self):   
        text = 0     
        for i in range(3):            
            for j in range(2):
                if  self.mbus.registers[text] == 0:
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
                values = [62580]
                btn.setAccessibleDescription("1")
                self.mbus.coils[No] = 1
            else :
                values = [0]
                btn.setAccessibleDescription("0")
                self.mbus.coils[No] = 0
            self.mbus.set_coil(No,1,values,1)


    @pyqtSlot()
    def show_img(self):
        if self.camera:
            frame = self.streamer.grab_frame()
            if self.mode == "shape":
                self.shape(frame)
            elif self.mode == "color":
                self.color(frame)

    def shape(self,frame):
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

    def color(self,frame):
        if frame is None:
            time.sleep(0.1)
            return
        
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
        if frame is not None:
            classified = np.zeros_like(frame)
            classified[white_mask] = [255, 255, 255]  # 白色
            classified[light_mask] = [200, 200, 200]  # 浅色（灰色）
            classified[dark_mask] = [50, 50, 50]      # 深色（深灰）
            # 转换为QImage并显示
            height, width = classified.shape[:2]
            qimage = QImage(
                classified.data, 
                width, 
                height, 
                width * 3, 
                QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qimage).scaledToWidth(480)
            self.label_2.setPixmap(pixmap)

    def control(self,results):
        # 0号传感器下降沿触发
        if self.mbus.trig_status[0] == 1:
            if results:
                dominant_category = max(results, key=results.get)
                self.mbus.cloth.append(dominant_category)  # 添加到列表
                QTimer.singleShot(2500)
                print(self.mbus.obj)
            else:
                dominant_category = None  # 无分类结果

  # @pyqtSlot()
  # def showTime(self):
  #     """   
  #     Slot documentation goes here.
  #     """
  #     # TODO: not implemented yet
  #     self.run_time_sec=self.run_time_sec+1
  #     self.setWindowTitle(str(round(self.run_time_sec*0.1, 2)))
  #     try:     
  #         self.show_btn_output()
  #         self.show_btn_input()
  #     except:
  #          pass
           
    @pyqtSlot()
    def showTime(self):
        """   
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # self.run_time_base=self.run_time_base+1
        # self.run_time_sec=self.run_time_base*0.1
        # self.run_time_min=self.run_time_sec//60
        # self.run_time_hour=self.run_time_min//60
        # self.run_time_min=self.run_time_min%60
        # self.run_time_hour=self.run_time_hour%60
        #self.setWindowTitle(str(round(self.run_time_hour))+":"+str(round(self.run_time_min))+":"+str(round(self.run_time_sec)))
        self.run_time_base=self.run_time_base+1
        self.run_time_sec=self.run_time_base
        self.run_time_min=self.run_time_sec//60
        self.run_time_hour=self.run_time_min//60
        self.run_time_min=self.run_time_min%60
        self.run_time_hour=self.run_time_hour%60
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

            time.sleep(0.1)
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
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()