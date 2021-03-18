# @Time : 2021-03-16 22:17
# @Author : ly
# @File : bullet.py.py
# @Software : PyCharm
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()  # super后要加（）代表调用
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # 在（0，0）处创建一个表示子弹(长宽)的矩形，再设置正确位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # 子弹为飞船打出来的 自然要和飞船对齐
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储小数表示子弹位置
        self.y = float(self.rect.y)

    # sprite精灵组调用update需要自己在定义
    # 对精灵组中的每一个精灵依次调用update()方法，并且update()方法需要自己在自己定义的精灵类中去实现
    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制出子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)