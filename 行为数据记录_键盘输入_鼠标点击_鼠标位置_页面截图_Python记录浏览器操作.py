# ! /usr/bin/env python
# coding:utf-8
# python interpreter:3.6.2
# author: admin_maxin
# from turtle import *
# import time
# python实时获取鼠标在屏幕中停留位置的坐标 + url
# 先下载pyautogui库，pip install pyautogui
# 要确保活动页面在最右 tab

# ===========================================声明============================================== #
# 如若商用，或者用于发表论文，请注明程序来源：南开大学商学院 网络社会治理研究中心 papers_mx@163.com             #
# ============================================================================================ #
import os
import time
import pyautogui as pag
from selenium import webdriver


def record(start_url, f, img_store_path):
    """
    记录用户在浏览器中的操作
    :param start_url:
    :param f:
    :param img_store_path:
    :return:
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    # driver.implicitly_wait(3)
    driver.get(start_url)

    flg = 1
    text = ""
    text2 = ""
    result = ""

    try:
        while True:
            # 切换到活动标签页
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])

            # 记录活动页面的url
            url = driver.current_url
            driver.get_screenshot_as_file(img_store_path.format(flg))

            # 记录鼠标所在的坐标
            x, y = pag.position()
            position = str(x).rjust(4) + ',' + str(y).rjust(4)

            # 获取用户的输入内容(仅记录第一次输入的内容)
            # https://blog.csdn.net/u012941152/article/details/83011110
            try:
                text2 = driver.find_element_by_xpath("//div[@class='t4_search t4_sub_search']//p//input").get_attribute("value")
            except Exception as e:
                print(text)

            # 将 [tab页, url, 鼠标位置, 用户检索词, 截图名称] 存储到本地文件
            if text2 != text:
                result = handles[-1] + "," + url + "," + position + "," + str(text2) + "," + str(flg)
                text = text2
            else:
                result = handles[-1] + "," + url + "," + position + "," + "" + "," + str(flg)
            f.write(result + "\n")
            f.flush()

            # 每一行耗时0.2s
            print("record:", result)
            flg = flg + 1

    except KeyboardInterrupt:
        f.close()
        print('end....')


if "__main__" == __name__:

    f = open("./experiment_position.txt", "a")
    f.write("windows,url,x,y,text,img_No" + "\n")

    start_url = "https://opendata.sz.gov.cn/"
    img_store_path = "./pictures/{}.png"

    record(start_url, f, img_store_path)