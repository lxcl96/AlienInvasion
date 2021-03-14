import pygame
# 将图像当作rect（矩形来处理）
class Ship:
    """管理飞船的类"""
    def __init__(self, ai_game):    # ai_game就是ai
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen    # 获取主程序中的屏幕大小（ai.screen）
        # get_rect()是一个处理矩形图像的方法，返回值包含矩形的居中属性，用点表示面location1
        self.screen_rect = ai_game.screen.get_rect() # 获取主程序中屏幕的中心位置即x轴，目的是保证飞船中心和屏幕中心一致

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')   # 上传飞船图片
        self.rect = self.image.get_rect()   # 获取飞船的中心位置即x轴，用点表示面location2
        # location1 要和location2 一致 飞船屏幕中心左右一致
        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom    # 把屏幕底部位置给飞船

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect) # 使用图片，位置来绘制飞船self.rect矩形对象，self.rect.midbottom 矩形位置