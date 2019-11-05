#coding=utf-8
import cv2 
import time
 
if __name__ == '__main__':
 
    cv2.namedWindow("camera",1)
    #开启ip摄像头
    video="http://admin:admin@10.28.138.238:8081/"   #此处@后的ipv4 地址需要修改为自己的地址
    capture =cv2.VideoCapture(video)
 
    num = 0;
    while True:
        success,img = capture.read()
        cv2.imshow("camera",img)
 
    #按键处理，注意，焦点应当在摄像头窗口，不是在终端命令行窗口
        key = cv2.waitKey(10) 
        #print(key)
        if key == 27:
        #esc键退出
            print("esc break...")
            break
        if key & 0xFF == ord('p'):#按键p
             #保存一张图像
            print("save a pic!")
            num = num+1
            filename = "frames_%s.jpg" % num
            #cv2.imwrite("/Users/jiaxin/Documents/研一/人机交互/camera"+filename,img)
            cv2.imwrite("/Users/jiaxin/Documents/研一/人机交互/camera/frames_{}.jpg".format(num),img)
 
    capture.release()
    cv2.destroyWindow("camera")

