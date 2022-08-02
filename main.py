from PyQt5.Qt import *  #-- 导入pyqt5的库
from PIL import Image,ImageQt,ImageGrab
import math
import win32api
#-- 建一个窗体
class Window(QWidget):  #-- 类名
    def __init__(self):
        super().__init__()
        self.setWindowTitle("一码一世界")  #-- 窗体的名字
        self.resize(500,500)   #-- 窗体的大小
        #-- 设置永久置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setup_ui()  #-- 窗体内部的东西

    def setup_ui(self):  #-- 窗体内部的东西
        self.btn_getImg = QPushButton('获取截图',self)  #-- 我要一个按钮
        self.btn_getImg.resize(100,30)  #-- 按钮大小
        self.btn_getImg.move(10,10) #-- 位置

        #建立一个画布
        self.label_img = QLabel(self) #-- 我要一个画布
        self.label_img.resize(400,300) #-- 大小
        self.label_img.move(10,50) #-- 位置
        self.label_img.setStyleSheet('border:1px solid black') #-- 画个边边

        #建立一个文字显示坐标点
        self.label_point = QLabel('中心点：',self)
        self.label_point.move(10,370)

#获取整个屏幕的截图
# def getImage():
#     #-- 我也背不过来那么多代码
#     img_area = ImageGrab.grab()
#     img_area.save("screenshot.jpg")
array_all = [] #-- 存放一堆红色的点

#获取区域的截图
def getImage():
    global array_all
    array_all = []
    #-- 我也背不过来那么多代码
    img_area = ImageGrab.grab(bbox=(700,400,1100,700))   #左  上   右  下 400X300
    #-- 画在窗体上
    img_area.load()
    width = img_area.size[0] #-- 像素点宽的数量
    height = img_area.size[1] #-- 像素点横的数量
    print(width, height)
    #-- 遍历所有像素点
    for x in range(width):
        for y in range(height):
            r, g, b = img_area.getpixel((x, y))
            # print(r,g,b)
            #筛选出红色的像素并 涂  绿色 r=148  g=53  b=48 ,还是给他一个范围
            if r > 128 and r < 168 and g > 33 and g < 73 and b > 28 and b < 68:
                #将符合条件的这些点上色
                img_area.putpixel((x, y), (0, 255, 0))
                array_all.append([x,y])  #将符合条件的点存进去
    #再赋值给label
    img_area.mode = 'RGBA'
    pixmap = ImageQt.toqpixmap(img_area).scaled(window.label_img.size(),aspectRatioMode=Qt.KeepAspectRatio)  # -- 适应画布大小
    # -- 赋予画布
    window.label_img.setPixmap(pixmap)
    #计算出中心点来
    point = get_max_point(array_all)
    window.label_point.setText('中心点：'+str(point[0])+" "+str(point[1]))
    #-- 自适应文字变多了
    window.label_point.adjustSize()
    #-- 加入偏移量
    point_x = point[0] + 700
    point_y = point[1] + 400
    #-- 把鼠标移过去
    win32api.SetCursorPos([point_x, point_y])
    #-- 点击鼠标右键
#自创的聚合方法 + 中心点算法，如有雷同，纯属巧合
def get_max_point(arr_all):  #-- 给他一堆点
    arr_group = [[0, 0, 2]]
    for item in arr_all:
        # print("新数组",item)
        # print('已存在',arr_group)
        save_flag = False
        for scale in arr_group:
            if math.fabs(scale[0] - item[0]) < 50 and math.fabs(scale[1] - item[1]) < 50:
                print(scale[0], item[0])
                scale[0] = round(scale[0] + (item[0] - scale[0]) / scale[2], 2)
                print(scale[0])
                scale[1] = round(scale[1] + (item[1] - scale[1]) / scale[2], 2)
                scale[2] = scale[2] + 1
                save_flag = True
                continue
        if save_flag == False:
            arr_group.append([item[0], item[1], 2])
    print(arr_group)
    max_point = [10, 10, 10]
    for scale in arr_group:  #-- 筛选出对的那堆点的中心点
        if scale[2] > max_point[2]:
            max_point[0] = round(scale[0])
            max_point[1] = round(scale[1])
            max_point[2] = round(scale[2])
    return max_point  #-- 返回一个中心点

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)  #-- 声明一个系统程序
    window = Window()  #-- 声明一个窗体
    window.btn_getImg.pressed.connect(getImage)
    window.show()  #-- 显示窗体
    sys.exit(app.exec_())  #-- 要求程序一直在运行