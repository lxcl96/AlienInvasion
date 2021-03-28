import pygame
# 将图像当作rect（矩形来处理）
class Ship:
    """管理飞船的类"""
    def __init__(self, ai_game):    # ai_game就是ai
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen    # 获取主程序中的屏幕大小（ai.screen）
        self.settings = ai_game.settings
        # get_rect()是一个处理矩形图像的方法，返回值包含矩形的居中属性，用点表示面location1
        self.screen_rect = ai_game.screen.get_rect() # 获取主程序中屏幕的中心位置即x轴，目的是保证飞船中心和屏幕中心一致

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')   # 上传飞船图片
        self.rect = self.image.get_rect()   # 获取飞船的中心位置即x,y轴，用点表示面location2
        # location1 要和location2 一致 飞船屏幕中心左右一致
        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom    # 把屏幕底部位置给飞船

        # 在飞船的属性x中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    # 实现持续移动
    def update_move(self):
        """根据移动标志持续调整飞船位置向右"""
        # 更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:  # 限定飞船左右移动范围
            self.x += self.settings.ship_speed
        """根据移动标志持续调整飞船位置向左"""
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        """根据移动标志持续调整飞船位置向上"""
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        """根据移动标志持续调整飞船位置向下"""
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制飞船"""
        # 使用图片，位置来绘制飞船self.rect矩形对象，self.rect.midbottom 矩形位置
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船处于屏幕低端中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        # 更新了飞船的位置 需要重新指定 飞船x轴y轴 为了其可以继续进行 满足小数位 移动
        self.x = float(self.rect.x)
        # 重置用于跟踪飞船确切位置的 x，y
        self.y = float(self.rect.y)