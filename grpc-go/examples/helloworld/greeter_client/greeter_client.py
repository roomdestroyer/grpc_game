# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import os
import shutil
import pygame
import grpc
import base64
import redis
import cv2
import helloworld_pb2
import helloworld_pb2_grpc
from PIL import Image


# -----------------------------------对象定义---------------------------------
# ------------------------------加载基本的窗口和时钟----------------------------
# 使用pygame之前必须初始化
pygame.init()
# 设置标题
pygame.display.set_caption("MyGame")
# 设置用于显示的窗口，单位为像素
screen_width, screen_height = 720, 1280
sub_image_num = 10
save_path = "../subimages/"

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # 设置时钟
# -------------------------------- 加载对象 ----------------------------------
# 加载图片
bg_img = pygame.image.load("background.png").convert()  # 背景图片


def cut():

    src = cv2.imread("./sunset.jpg", -1)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    else:
        shutil.rmtree(save_path)
        os.mkdir(save_path)

    sub_images = []
    src_height, src_width = src.shape[0], src.shape[1]
    sub_height = src_height // sub_image_num
    sub_width = src_width // sub_image_num
    for j in range(sub_image_num):
        for i in range(sub_image_num):
            if j < sub_image_num - 1 and i < sub_image_num - 1:
                image_roi = src[j * sub_height: (j + 1) * sub_height, i * sub_width: (i + 1) * sub_width, :]
            elif j < sub_image_num - 1:
                image_roi = src[j * sub_height: (j + 1) * sub_height, i * sub_width:, :]
            elif i < sub_image_num - 1:
                image_roi = src[j * sub_height:, i * sub_width: (i + 1) * sub_width, :]
            else:
                image_roi = src[j * sub_height:, i * sub_width:, :]
            sub_images.append(image_roi)
    for i, img in enumerate(sub_images):
        im_file = save_path + 'sub_img_' + str(i) + '.png'
        cv2.imwrite(im_file, img)

        im = Image.open(im_file)
        out = im.resize((72, 128), Image.ANTIALIAS)
        out.save(im_file)


def save():
    for i in range(sub_image_num * sub_image_num):
        img = save_path + 'sub_img_' + str(i) + '.png'
        with open(img, "rb") as f:
            base64_data = base64.b64encode(f.read())
            r = redis.Redis(host='127.0.0.1', port=6379)
            save_name = 'sub_img_' + str(i)
            r.set(save_name, base64_data)

            var = r.get(save_name)
            data = base64.b64decode(var)  # 把二进制文件解码，并复制给data
            im_file = "../redis/" + 'sub_img_' + str(i) + '.jpg'
            with open(im_file, "wb") as q:  # 写入生成一个jd.png
                q.write(data)
            im = Image.open(im_file)
            out = im.resize((72, 128), Image.ANTIALIAS)
            out.save(im_file)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    if not os.path.exists("../redis/"):
        os.mkdir("../redis/")
    else:
        shutil.rmtree("../redis/")
        os.mkdir("../redis/")
    cut()
    save()
    logging.basicConfig()
    # ------------------------------- 游戏主循环 ---------------------------------
    run = True
    while run:
        clock.tick(60)
        # -------------------------------- 渲染对象 -------------------------------
        # 渲染图片
        screen.blit(bg_img, (720, 1280))  # 绘制背景
        # ------------------------ 事件检测及状态更新 ------------------------------
        for event in pygame.event.get():  # 循环获取事件
            if event.type == pygame.QUIT:  # 若检测到事件类型为退出，则退出系统
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 按下按键
                # print("[MOUSEBUTTONDOWN]", event.pos, event.button)
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = helloworld_pb2_grpc.GreeterStub(channel)
                    response = stub.SayHello(helloworld_pb2.HelloRequest(point_x=event.pos[0], point_y=event.pos[1]))
                    index = response.index
                    message = response.message
                    data = base64.b64decode(message)  # 把二进制文件解码，并复制给data
                    img_name = "../redis/" + 'sub_img_' + str(index) + '.png'
                    with open(img_name, "wb") as q:  # 写入生成一个jd.png
                        q.write(data)

                    item = pygame.image.load(img_name).convert_alpha()

                    pygame.display.update()
                    left_index = int(index / 10)
                    top_index = int(index % 10)
                    left = top_index * 72
                    top = left_index * 128
                    print("index = ", index, "left_index = ", left, "top = ", top)
                    screen.blit(item, (left, top))

                # print(event.pos)
        # -------------------------- 窗口更新并绘制 -------------------------------
        pygame.display.update()  # 更新屏幕内容
    pygame.quit()


    # run()
