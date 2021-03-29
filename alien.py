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
        # !!!!!!! 切记 此处的settings 一定要从主程序出获取 不然会出现 设定值一直不变的情况如 飞船移动方向
        self.settings = ai_game.settings

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False

    def update(self):
        """向右/左移动外星人"""
        # 设置外星人移动位置 为 其速度和 方向的成绩（可正可负） 实现其左右移动
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        # if self.settings.fleet_direction == -1:
        #     print(self.settings.fleet_direction)
        self.rect.x = self.x