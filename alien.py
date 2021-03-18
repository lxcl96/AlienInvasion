# @Time : 2021-03-17 22:20
# @Author : ly
# @File : alien.py.py
# @Software : PyCharm
import pygame
from pygame.sprite import Sprite

class Aliens(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        # 继承Sprite类
        super().__init__()
        # 获取主程序中屏幕大小
        self.screen = ai_game.screen
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        # 从加载的图像中获取外星人矩形大小
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕左上角附近 ???? 没看懂
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 存储每个外星人的准确位置
        self.x = float(self.rect.x)