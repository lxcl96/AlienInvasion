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

        # 飞船设置 速度为1.5 数量限制为 3
        self.ship_speed = 0.5
        self.ship_limit = 1

        # 子弹设置:速度1px，宽度3px，长度15px 颜色为
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 限制子弹数量
        self.bullets_allowed = 3

        # 外星人移动速度设置
        self.alien_speed = 0.2
        # 此速度指的是外星人撞到屏幕边缘时，外星人向下移动的速度
        self.fleet_drop_speed = 40.0
        # self.fleet_direction为 1 代表右移 ，为 -1 代表左移
        self.fleet_direction = 1


