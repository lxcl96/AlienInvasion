import sys
import pygame
from settins import Settings
from ship import Ship
from bullet import Bullet
from alien import Aliens


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化背景设置
        pygame.init()
        self.settings = Settings()
        # 创建一个宽1200px，高800px的窗口先显示图案
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 创建一个全屏屏幕
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # 获取全屏屏幕的长和宽复制到settings文件中
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # 设置弹出窗口的标题
        pygame.display.set_caption("Alien Invasion")
        """
        需注意此处飞船调用必须要在__init__函数末端，因为ship模块中使用到了screen属性，如果在前面实例化ship则会报错提示：screen属性不存在
        """
        # Ship(self) self指向当前AlienInvasion实例，目的为了访问对象如screen
        self.ship = Ship(self)
        # self.backgroud = Backgroud()
        # 给发射出去的子弹编组方便管理
        self.bullets = pygame.sprite.Group()
        # 给外星人编组
        self.aliens = pygame.sprite.Group()
        # 创建外星人函数
        self._create_fleet()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一群外星人并计算一行可以容纳多少个外星人
        # 外星人间的间距为一个外星人的宽度
        alien = Aliens(self)
        # 标记外星人宽度, 高度
        alien_width, alien_height = alien.rect.size
        # alien_width = alien.rect.width
        # alien_height = alien.rect.height
        # 计算屏幕可用宽度，两边各留空一个外星人的位置
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # 计算容纳多少个外星人
        numbers_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可以容纳多少行外星人
        # 统计飞船高度 也可以用self.ship.rect.height
        ship_height = self.ship.image.get_height()
        # 计算可以行距 减去第一行外星人的高度，及行间距为一个外星人 和最后外星人和飞船间空的一个一个外星人高度
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        # 计算可以利用 行数即可以容纳多少行外星人
        numbers_aliens_y = available_space_y // (2 * alien_height)
        # 创建多行外星人
        for number_alien in range(numbers_aliens_y + 1):
            for alien_number in range(numbers_aliens_x + 1):
                self._create_alien(alien_number, number_alien)

    def _create_alien(self, alien_number, number_alien):
        """创建多行外星人并将其放在当前行"""
        # 设置当前外星人的位置
        # 少了这一步不会循环创建外星人
        alien = Aliens(self)
        alien_width, alien_height = alien.rect.size
        # 算法难点?????????????????????? 展示单行外星人数
        alien.x = alien_width + 2 * alien_width * alien_number
        # 将外星人x轴位置 坐标更新 相应 外星人坐标x轴也被更新了
        alien.rect.x = alien.x
        # 更新y轴才会多行显示 不然就是一行显示了
        alien.rect.y = alien_height + 2 * alien_height * number_alien
        self.aliens.add(alien)

    # 按键发射子弹
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        # 设置屏幕上只能同时出现三发子弹，但是可以无限射击
        if len(self.bullets) < self.settings.bullets_allowed:
            # 传递参数self使用自身，self指向当前AlienInvasion实例，目的为了访问对象如screen
            new_bullet = Bullet(self)
            # 将子弹编组
            self.bullets.add(new_bullet)

    # 此处为按压方向键（KEYDOWN）
    def __check_keydown_events(self, event):
        # 获取事件值为，右方向键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 获取事件值为，左方向键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # test--------------------------
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # 按q键 退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            # 以下方法只能发射三发子弹
            '''
            # 如果子弹存量大于0
            if self.settings.bullets_allowed > 0:
                # 射击
                self._fire_bullet()
                # 子弹数量-1
                self.settings.bullets_allowed -= 1
            '''

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

    def _update_bullets(self):
        # 更新子弹位置，为pygame.sprite.group()函数
        # 对编组调用update（）时，编组自动对组里的每一个精灵调用update（）
        # 调用的是精灵组里的 update，但是update（）已经在Bullet组里被重写了，所有调用的就是类里的update
        self.bullets.update()
        # 删除消失的子弹，因为子弹还在运行会继续消耗内存
        # for bullet in self.bullets.copy() 和for bullet in self.sprite()好像是一样的哦？
        for bullet in self.bullets.sprites():
            # 使用bullet.rect.bottom比较准确，因为这个是子弹的底部而bullet.rect.y描述不准确因为有上下y
            if bullet.rect.bottom <= 0:
                # 删掉精灵组里的过界子弹
                self.bullets.remove(bullet)
        # 打印精灵组的子弹
        # print(len(self.bullets))

    def _update_screen(self):
        """更屏幕刷新函数"""
        # 设置窗口图标
        self.screen.fill(self.settings.bg_color)
        # 每次执行while 都会重绘一个新的屏幕窗口和飞船
        pygame.display.set_icon(self.settings.logo)
        self.ship.blitme()

        # 展示窗口
        # self.screen.blit(self.backgroud.backgroud, (350, 150))
        # self.bullets.sprites()返回一个列表，为编组里的所有精灵
        # 需要验证为什么，换成for bullet in self.bullets: 也没问题
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 把外星人画出来
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            # 更新飞船位置
            self.ship.update_move()
            # 发射/更新子弹
            self._update_bullets()
            # 更新屏幕
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并允许游戏
    ai = AlienInvasion()
    ai.run_game()
