# @Time : 2021-03-15 19:41
# @Author : ly
# @File : picture.py.py
# @Software : PyCharm
import pygame


class Backgroud:
    """设置背景为图案"""
    def __init__(self):
        self.backgroud = pygame.image.load('images/bg.bmp')