import sys
import pygame
from settins import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化背景设置
        pygame.init()
        self.settings = Settings()
        # 创建一个宽1200px，高800px的窗口先显示图案
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_heigth))
        # 设置弹出窗口的标题
        pygame.display.set_caption("Alien Invasion")
        """
        需注意此处飞船调用必须要在__init__函数末端，因为ship模块中使用到了screen属性，如果在前面实例化ship则会报错提示：screen属性不存在
        """
        # Ship(self) self指向当前AlienInvasion实例，目的为了访问对象如screen
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # pygame.event.get()获取键盘或鼠标的操作，通过event来记录每一个操作
            # 此处为一个事件循环，侦听事件并作出相应的操作
            for event in pygame.event.get():
                # 如果玩家点击了右上角的 x 事件
                if event.type == pygame.QUIT:
                    # 退出游戏
                    sys.exit()
            # 每次执行while 都会重绘一个新的屏幕窗口和飞船
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # 展示窗口
            pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并允许游戏
    ai = AlienInvasion()
    ai.run_game()
