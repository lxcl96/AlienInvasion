import pygame


class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置 宽度/高度/背景
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.logo = pygame.image.load('images/ship.bmp')

        # 飞船设置
        self.ship_speed = 0.5

        # 子弹设置:速度1px，宽度3px，长度15px 颜色为
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 限制子弹数量
        self.bullets_allowed = 3
