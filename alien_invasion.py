import sys
import pygame
from settins import Settings
from ship import Ship
from picture import Backgroud


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化背景设置
        pygame.init()
        self.settings = Settings()
        # 创建一个宽1200px，高800px的窗口先显示图案
        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_heigth))
        # 创建一个全屏屏幕
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # 获取全屏屏幕的长和宽复制到settings文件中
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # 设置弹出窗口的标题
        pygame.display.set_caption("Alien Invasion")
        """
        需注意此处飞船调用必须要在__init__函数末端，因为ship模块中使用到了screen属性，如果在前面实例化ship则会报错提示：screen属性不存在
        """
        # Ship(self) self指向当前AlienInvasion实例，目的为了访问对象如screen
        self.ship = Ship(self)
        self.backgroud = Backgroud()

    # 此处为按压方向键（KEYDOWN）
    def __check_keydown_events(self, event):
        # 获取事件值为，右方向键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 获取事件值为，左方向键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #test--------------------------
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # 按q键 退出游戏
        elif event.key == pygame.K_q:
            sys.exit()

    # 此处为松开右方向键（KEYUP）
    def _check_keyup_events(self, event):
        # 松开右方向键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # 松开左方向键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        # test------------------------------
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_events(self):
        """响应按键和鼠标事件函数"""
        # pygame.event.get()获取键盘或鼠标的操作，通过event来记录每一个操作
        # 此处为一个事件循环，侦听事件并作出相应的操作
        for event in pygame.event.get():
            # 如果玩家点击了右上角的 x 事件
            if event.type == pygame.QUIT:
                # 退出游戏
                sys.exit()
            # 检测屏幕输入KEYDOWN (按下按键)事件
            elif event.type == pygame.KEYDOWN:
                self.__check_keydown_events(event)
            # 此处为松开右方向键（KEYUP）
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)



    def _update_screen(self):
        """更屏幕刷新函数"""
        # 设置窗口图标
        self.screen.fill(self.settings.bg_color)
        # 每次执行while 都会重绘一个新的屏幕窗口和飞船
        pygame.display.set_icon(self.settings.logo)
        self.ship.blitme()

        # 展示窗口
        self.screen.blit(self.backgroud.backgroud, (350, 150))
        pygame.display.flip()


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update_move()
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并允许游戏
    ai = AlienInvasion()
    ai.run_game()
