# 化整为零，化零为整

### 一、需求

开发一个简单的完整应用，涉及到python, 可视化（pygame, opencv)，go, grpc, shell等基础知识，锻炼一下实操能力，为后续的研发打下基础。

![image-20220430212407893](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220430212407893.png)

##### 1. 整体应用的效果

点击UI画面不同位置，点击后所在的格子中出现图片局部的内容（总共10\*10个格子），显示了10\*10个位置后，可以显示出一张完整的图片。

> 点击链接查看演示效果：
>
> https://bucket02.obs.cn-north-4.myhuaweicloud.com:443/demo.mp4?AccessKeyId=EPMCKIK9NRITQHB3EEVR&Expires=1682429221&Signature=%2BLNoKjgwcukLD3HODHzTQ2rU0us%3D



##### 2. Redis

功能1：将一张720\*1280的图片，拆成10\*10, 共100张图片(可以采用python的opencv来拆分和落文件)，每张图片大小为72\*128，自己定义key, value格式；

功能2：采用redis的shell工具，将100张图片set到redis数据库。

### 

##### 3. UI：开发语言Python

功能1：用pygame组件写一个可视化的应用。应用的窗口大小为720*1280

功能2：画面渲染，拉起一张图片，在应用窗口中显示 

功能3：点击事件，点击窗口的某一位置，将位置发给内容服务，返回是一张图片的内容，显示在应用窗口中

功能4：向内容服务请求，使用python grpc client接口



##### 4. 内容服务：开发语言go；MQ框架grpc

功能1：收到UI发送过来的请求，通过坐标, 计算对应的的图片id

功能2：根据图片id，向redis请求，拉取对应的图片内容，再转发回UI



---

### 二、快速使用





