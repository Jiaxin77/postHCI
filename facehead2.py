# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json
""" 
  人脸特征分析年龄WebAPI接口调用示例接口文档(必看)：https://doc.xfyun.cn/rest_api/%E4%BA%BA%E8%84%B8%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90-%E5%B9%B4%E9%BE%84.html
  图片属性：png、jpg、jpeg、bmp、tif图片大小不超过800k
  (Very Important)创建完webapi应用添加服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
  错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
  @author iflytek
"""
# 人脸特征分析年龄webapi接口地址
URL = "http://tupapi.xfyun.cn/v1/age"
# 应用ID  (必须为webapi类型应用，并人脸特征分析服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = "5d946330"
# 接口密钥(webapi类型应用开通人脸特征分析服务后，控制台--我的应用---人脸特征分析---服务的apikey)
API_KEY = "325b026d5a151cd93b806bb45bc7c10f"
ImageName = "sad2.jpg"
#ImageUrl = "http://hbimg.b0.upaiyun.com/a09289289df694cd6157f997ffa017cc44d4ca9e288fb-OehMYA_fw658"
# 图片数据可以通过两种方式上传，第一种在请求头设置image_url参数，第二种将图片二进制数据写入请求体中。若同时设置，以第一种为准。
# 此demo使用第一种方式进行上传图片地址，如果想使用第二种方式，将图片二进制数据写入请求体即可。
FilePath = r"/Users/jiaxin/Documents/研一/人机交互/camera/frames_1.jpg"


def getHeader(image_name, image_url=None):
    curTime = str(int(time.time()))
    param = "{\"image_name\":\"" + image_name + "\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))
    tmp = str(paramBase64)

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + tmp).encode('utf-8'))
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header

# def getHeader(image_name, data):
#     curTime = str(int(time.time()))
#     param = str(data)
#     #param = "{\"image_name\":\"" + image_name + "\",\"image_url\":\"" + str(data) + "\"}"
#     #param = "{\"image_name\":\"" + image_name + "\",\"image_url\":"+data+"\"}"
#     #print(param)
#     paramBase64 = base64.b64encode(param.encode('utf-8'))
#     tmp = str(paramBase64, 'utf-8')

#     m2 = hashlib.md5()
#     m2.update((API_KEY + curTime + tmp).encode('utf-8'))
#     checkSum = m2.hexdigest()

#     header = {
#         'X-CurTime': curTime,
#         'X-Param': paramBase64,
#         'X-Appid': APPID,
#         'X-CheckSum': checkSum,
#     }
#     return header    


def getBody(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    #print(data)

    #image_base64 = str(base64.b64encode(data), encoding='utf-8')
    
    return data


def myswitch(dic_label):
    
  if dic_label == 0:
      age = 1
  elif dic_label == 1:
      age = 3
  elif dic_label == 2:
      age = 7
  elif dic_label == 3:
      age = 13
  elif dic_label == 4:
      age = 18
  elif dic_label == 5:
      age = 23
  elif dic_label == 6:
      age = 35
  elif dic_label == 7:
      age = 45
  elif dic_label == 8:
      age = 55
  elif dic_label == 9:
      age = 70
  elif dic_label == 10:
      age = 90
  elif dic_label == 12:
      age = 27
  return age


#r = requests.post(URL, headers = getHeader(ImageName,getBody(FilePath)))
#print(getHeader(ImageName, ImageUrl))
r = requests.post(URL, getBody(FilePath),headers=getHeader(ImageName))
print(r.content)
print(type(r.content))

dict_str = json.loads(r.text) #转换为json格式
dic_label = dict_str["data"]["fileList"][0]["label"]
print(dic_label)#当前判断的年龄码
print(type(dic_label))
dic_list=[]
dic_list = dict_str["data"]["fileList"][0]["labels"]
print(dic_list)#当前判断的可能性
print(type(dic_list[0]))

if(dic_label == 11):#如果为其他，则选择第二选项
  dic_label = dic_list[1]

result_age = myswitch(dic_label)


print("用户年龄为"+str(result_age))


#if(dic_label)
#怎么获取其中的值！判断年龄-输出年龄
#resultLabel= r.get("data").get("fileList")
#print(resultLabel)
