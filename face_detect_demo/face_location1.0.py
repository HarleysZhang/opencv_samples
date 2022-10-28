#encoding:utf-8
#filename:face_location.py
#environment:OpenCV3.4,python2,windows10 
import cv2  
import numpy as np 
      
#create a window that can resize the window
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

#cv2.ResizeWindow("image", 600, 600)

#找到设备对象  
capture = cv2.VideoCapture(0) 
   
    #检测人脸函数  
      
def repeat():      
        #每次从摄像头获取一张图片  
    ret, frame = capture.read()

    #image_size = cv2.GetSize(frame)#获取图片的大小  
    #print image_size
    greyscale = np.zeros(frame.shape, np.uint8)  #建立一个相同大小的灰度图像
    greyscale = frame.copy() #建立一个相同大小的灰度图像
    greyscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #将获取的彩色图像，转换成灰度图像
    #storage = cv2.CreateMemStorage(0)#创建一个内存空间，人脸检测时要利用，具体作用不清楚     
    #equ_greyscale = cv2.equalizeHist(greyscale)#将灰度图像直方图均衡化，貌似可以使灰度图像信息量减少，加快检测速度
    #画图像分割线
         
    cv2.line(frame, (210,0),(210,480), (0,255,255),1) 
    cv2.line(frame, (420,0),(420,480), (0,255,255),1) 
    cv2.line(frame, (0,160),(640,160), (0,255,255),1) 
    cv2.line(frame, (0,320),(640,320), (0,255,255),1) 
    # detect objects  
    cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt2.xml')
    #加载Intel公司的训练库  
      
    #检测图片中的人脸，并返回一个包含了人脸信息的对象faces  
  
    faces = cascade.detectMultiScale(frame, scaleFactor=1.2, 
                                        minNeighbors=2, minSize=(100,100), 
                                        flags=cv2.CASCADE_SCALE_IMAGE)   
    #获得人脸所在位置的数据,在图像人脸位置画矩形框
    for (x,y,w,h) in faces:
       # print x,y
        if x<200:
            print("right")
        elif x>320:
            print("left")
        else:
            print("middle")
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,128,0),2)#在相应位置标识一个矩形 边框属性(0,0,255)红色 20宽度
          
        cv2.imshow("image", greyscale)#显示互有边框的图片
          
    cv2.imshow("image", frame)  
      
    #循环检测每一帧的图片 ESC键退出程序  
while True:  
    repeat()  
    c = cv2.waitKey(10)  
    if c == 27:  
        #cv2.VideoCapture(0).release()  
        cv2.destroyWindow("image")  
        break
capture.release()
