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

#### 环境

本项目环境为 Windows11，软件版本如下：

~~~
Python 3.9.12
go version go1.18.1 windows/amd64
~~~



#### 目录

本项目主体文件目录如下：

~~~
├── examples
    ├── greeter_client            // python 客户端
    │   ├── greeter_client.py         // 客户端主程序
    │   ├── helloworld_pb2.py         // python 编译后的 proto 文件
    │   ├── helloworld_pb2_grpc.py    // python 编译后的 proto 文件
    │   ├── sunset.jpg                // 待操作的图片
    │   ├── background.png            // 背景图片
    ├── greeter_server            // go 服务端
    │   ├── main.go                   // 服务端主程序
    ├── helloworld                // 存放 proto 文件及 go 编译后的文件
    │   ├── helloworld.proto          // proto 文件
    │   ├── helloworld.pb.go          // go 编译后的 proto 文件
    │   ├── helloworld_grpc.pb.go     // go 编译后的 proto 文件
    ├── redis                      // go 通过 redis 获取的图片
    │   ├── sub_img_0.jpg
    │   ├── ......
    │   ├── sub_img_99.jpg
    ├── subimages                  // python 分割为 100 份后的图片
    │   ├── sub_img_0.jpg
    │   ├── ......
    │   ├── sub_img_99.jpg
    ├──────────────────────
~~~

> 注：本项目父目录中的文件皆不能删除，含 go 运行所必要的环境，除非你有能力自己配置它们



#### 下载

使用下列命令将文件下载到本地：

~~~
git clone https://github.com/roomdestroyer/grpc_game.git
~~~

假设你的工作路径为 `D:\00000`，下一步打开主目录文件：

~~~
cd D:\00000\grpc-go\examples\helloworld
~~~

下载 go 依赖：

~~~
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
~~~

下载 python 依赖：

> 运行过程中缺什么就用 pip 下什么

下载 redis：

进入官网 `https://github.com/MicrosoftArchive/redis/releases`，选择 `.zip` 文件下载，下载好后解压到任意一个目录，解压后可以看到服务、客户端等，选择服务**redis-server.exe**双击开启：

![image-20220430223942725](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220430223942725.png)



#### 编译

通过 go 编译 proto 文件：

~~~
protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative helloworld/helloworld.proto
~~~

通过 python3 编译 proto 文件：

~~~
python3 -m grpc_tools.protoc -I./helloworld --python_out=. --grpc_python_out=. helloworld/helloworld.proto
~~~

编译好的文件需将其手动移动到 `./greeter_client` 下。



#### 运行

启动两个 windows shell，其中一个运行服务端，另一个运行客户端。

首先进入工作目录：

~~~
cd D:\00000\grpc-go\examples\helloworld
~~~

Shell1 运行服务端：

~~~
go run greeter_server/main.go
~~~

Shell2 运行客户端：

~~~
python3 greeter_client/greeter_client.py
~~~

当然也可以使用 pycharm 运行客户端，运行成功后显示一个窗口，通过该窗口即可完成特定的功能。

