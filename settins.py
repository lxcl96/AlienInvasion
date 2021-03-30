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
        self.ship_limit = 3

        # 子弹设置:速度1px，宽度3px，长度15px 颜色为
        self.bullet_speed = 1.5
        self.bullet_width = 300
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
        """
        更新settings文件 将游戏划分为动态和静态两组，对游戏进行而变化并在开始新游戏时重置信息
        """
        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        # __init__()定义静态设置，下面进行动态设置
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.0
        self.bullet_speed = 3.0
        self.alien_speed = 0.3

        # fleet_direction 为1代表向右 -1代表向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置 在整群外星人被消灭时 调用 加快游戏进度"""
        # 需要注意清空玩一波外星人后 提升了 元素速度 但是 再次点击一次 play按钮时 这些元素速度并没有被重置 需要手动重置
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale