import sys
from time import sleep
import pygame
from settins import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Aliens
from button import Button
from scoreboard import Scoreboard


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
        /
        在创建屏幕窗口后，定义诸如飞船等其他窗口前 创建一个GameStats实例
        """
        # 创建一个用于存储游戏统计信息的实例 如剩下飞船数量
        self.stats = GameStats(self)

        # Ship(self) self指向当前AlienInvasion实例，目的为了访问对象如screen
        self.ship = Ship(self)
        # self.backgroud = Backgroud()
        # 给发射出去的子弹编组方便管理
        self.bullets = pygame.sprite.Group()
        # 给外星人编组
        self.aliens = pygame.sprite.Group()
        # 创建外星人函数
        self._create_fleet()

        # 实例化按钮
        self.play_button = Button(self, "Play")
        # 实例化记分牌
        self.sb = Scoreboard(self)


    def _create_fleet(self):
        """创建外星人群"""
        # 创建一群外星人并计算一行可以容纳多少个外星人
        # 外星人间的间距为一个外星人的宽度
        # 程序等待一秒
        # time.sleep(1)
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
        for number_alien in range(numbers_aliens_y):
            for alien_number in range(numbers_aliens_x):
                self._create_alien(alien_number, number_alien)
        # self._create_alien(1, 1)

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
        # print(len(self.aliens))

    # 按键发射子弹
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        # 设置屏幕上只能同时出现三发子弹，但是可以无限射击
        if len(self.bullets) < self.settings.bullets_allowed:
            # 传递参数self使用自身，self指向当前AlienInvasion实例，目的为了访问对象如screen
            new_bullet = Bullet(self)
            # 将子弹编组
            self.bullets.add(new_bullet)

    def _start_game(self):
        """按p键开始游戏"""
        if not self.stats.game_active:
            # 游戏运行中隐藏鼠标光标 因为他碍眼 但是游戏结束后鼠标又不显示了 需要 再次设置
            pygame.mouse.set_visible(False)
            # 重置游戏信息 比如飞船个数,游戏运行状态,
            self.stats.reset_status()
            self.stats.game_active = True

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人 并且让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 开始新游戏 重置 元素速度
            self.settings.initialize_dynamic_settings()
            # 再次开始新游戏时 需要重置得分 不然刚开始上面显示的上一局的得分
            self.sb.prep_score()
            # 再次开始新游戏时 需要重新绘制 剩余飞船
            self.sb.prep_ships()
            # 更新最高得分并且 将其绘制成 surface 此处不需要 只需要加在子弹碰撞检测处即可
            # if self.stats.score > self.stats.high_score:
            #     self.stats.high_score = self.stats.score
            # self.sb.prep_high_score()

            # 开始新游戏前 重置level 等级重置包含在 函数中了不需要在单独 添加了
            # self.stats.level = 1
            self.sb.prep_level()


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
        # 按p键开始游戏
        elif event.key == pygame.K_p:
            self._start_game()
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

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        # collidepoint检查鼠标点击时位置是否在按钮区域内 且 游戏运行状态为False时 才会响应游戏点击
        # 为什么要加上 两个判断条件？ 第一个是为了 实现 play按钮控制
        # 第二个是为了防止 游戏处于运行中，用户不小心点击 按钮位置 导致游戏一直重置
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # 游戏运行中隐藏鼠标光标 因为他碍眼 但是游戏结束后鼠标又不显示了 需要 再次设置
            pygame.mouse.set_visible(False)
            # 重置游戏信息 比如飞船个数,游戏运行状态,
            self.stats.reset_status()
            self.stats.game_active = True

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人 并且让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            # 开始新游戏 重置元素速度
            self.settings.initialize_dynamic_settings()
            # 再次开始新游戏时 需要重置得分 不然刚开始上面显示的上一局的得分
            self.sb.prep_score()
            # 再次开始新游戏时 需要重新绘制 剩余飞船
            self.sb.prep_ships()
            # 更新最高得分并且 将其绘制成 surface 此处不需要 只需要加在子弹碰撞检测处即可
            # if self.stats.score > self.stats.high_score:
            #     self.stats.high_score = self.stats.score
            # self.sb.prep_high_score()
            # 开始新游戏前 重置level
            # self.stats.level = 1
            self.sb.prep_level()


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
            # 检测到鼠标事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get_pos() 返回一个元组其中包含了点击鼠标时的x轴和y轴
                mouse_pos = pygame.mouse.get_pos()
                # 检查返回的x，y轴是否在 button按钮中
                self._check_play_button(mouse_pos)

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞，删除发生碰撞的子弹和外星人"""
        # 检查是否有子弹击中外星人
        #   如果是，就删除相应的子弹和外星人
        # sprite.groupcollide() 将一个编组里每个元素的rect 与另一个编组里的每个元素的rect进行比较
        # 这里是将每个子弹rect与每个外星人rect进行比较返回一个 key=碰撞的子弹，value=碰撞的外星人 的字典
        #   两个实参True 让pygame删除发生碰撞的子弹（第一个true）和外星人（第二个True）
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 这种方法虽然也可以计算得分 但是如果子弹很大同时打到多个外星人也只会记一个人的得分，或者两个子弹打到同一个外星人
        # 因此需要对得分的方法 进行优化 思路是：collisions是一个字典，key是子弹 value是外星人或者是外星人列表 (即可能是一个或多个)
        #                                因此 可以计算每一个value的长度 来确定 一颗子弹打到了 多少外星人
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
                # 数值发生了变化 需要重新生成一个surface 来覆盖 /////////////重要！！！！！
                # 游戏结束了但是 得分数值没有重新绘制 刚开始会不变
                self.sb.prep_score()
                # 更新最高得分并且 将其绘制成 surface 可以这样写 我们可以将其集成到 scoreboard 类中
                # if self.stats.score > self.stats.high_score:
                #     self.stats.high_score = self.stats.score
                # self.sb.prep_high_score()
                self.sb.check_high_score()

        # 为了保证外星人足够的多，需要在 self.aliens 为空时 再次生成外星人 self.aliens 为布尔类型
        # if len(self.aliens) == 0:
        # 让程序等待 1s 后再执行
        if not self.aliens:
            # time.sleep(1)
            # 清空剩余子弹
            self.bullets.empty()
            # 新建外星人群
            self._create_fleet()
            # 增加游戏元素移动速度
            # 需要注意清空玩一波外星人后 提升了 元素速度 但是 再次点击一次 play按钮时 这些元素速度并没有被重置 需要手动重置
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            # print(self.settings.alien_speed)

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

        # 响应子弹和外星人碰撞，删除发生碰撞的子弹和外星人
        self._check_bullet_alien_collisions()

    def _change_fleet_direction(self):
        """将外星人整体下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            # 外星人达到屏幕边缘后下移一段距离
            alien.rect.y += self.settings.fleet_drop_speed
        # 当外星人全部下移后 改变其移动方向 至于为什么用 *= 而不是直接让其为 -1 因为存在 从左到右的情况（-1~1）
        self.settings.fleet_direction = self.settings.fleet_direction * (-1)
        # print(self.settings.fleet_direction)

    def _check_fleet_edges(self):
        """有外星人到达屏幕边缘时采取相应措施"""
        # print(len(self.aliens))
        for alien in self.aliens.sprites():
            # 如果到达屏幕边缘返回True, 切记函数后面要带上()代表引用
            if alien.check_edges():
                # 修改移动方向
                self._change_fleet_direction()
                # ??????????? 跳出本次while循环 到达屏幕左右侧了 不继续移动 即跳过转向那一次的移动
                break

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的底部"""
        # 获取屏幕所在 矩形
        screen_rect = self.screen.get_rect()
        # 遍历外星人组
        for alien in self.aliens.sprites():
            # 如果存在外星人的底部 大于等于 屏幕的底部
            if alien.rect.bottom >= screen_rect.bottom:
                # 重新开始游戏
                self._ship_hit()
                # 只要找到一个就行了 不用再继续找下去了
                break
                # print("已到达屏幕底边")

    def _ship_hit(self):
        """
        响应飞船被外星人撞到
        1、飞船数量 -1 且 飞船数量大于0时重置
        2、清空剩下飞船和子弹
        3、创建新的外星人和飞船
        4、暂停程序以 给 玩家反映时间
        """
        if self.stats.ship_left > 0:
            # 将剩余飞船数量 -1
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            # 清空外星人和子弹
            self.bullets.empty()
            self.aliens.empty()
            # 创建一群新的外星人和飞船
            self._create_fleet()
            # 创建新的飞船不能用这种方法 self.ship.blitme() 这个是重新绘制飞船图形 目标是让其重置 归位到屏幕最低端中央部位
            # self.ship.blitme()
            self.ship.center_ship()
            # 暂停 1s
            sleep(1)
        else:
            # 改变游戏运行状态
            self.stats.game_active = False
            # 游戏结束设置 鼠标箭头非隐藏
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """更新外星人的移动位置"""
        # 检查外星人的位置
        self._check_fleet_edges()
        self.aliens.update()

        # 检查飞船和外星人间的碰撞
        # sprite.spritecollideany() 检查一个精灵和精灵组的碰撞，并在找到碰撞对象后停止遍历 精灵组
        # 此处代码就行 遍历外星人组找到第一个和 飞船发生碰撞的 外星人 如果没找到就 返回 None ,如果找到了就返回那个碰撞的外星人
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship Hit !!!")
            self._ship_hit()
            # print(self.stats.ship_left)
        # 检查是否有外星人到达屏幕底部
        self._check_aliens_bottom()

    def _update_screen(self):
        """更屏幕刷新函数"""
        # 设置窗口图标
        self.screen.fill(self.settings.bg_color)
        # 每次执行while 都会重绘一个新的屏幕窗口和飞船
        pygame.display.set_icon(self.settings.logo)
        # 绘制飞船
        self.ship.blitme()

        # 绘制子弹
        # self.screen.blit(self.backgroud.backgroud, (350, 150))
        # self.bullets.sprites()返回一个列表，为编组里的所有精灵
        # 需要验证为什么，换成for bullet in self.bullets: 也没问题
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 把外星人画出来
        self.aliens.draw(self.screen)

        # 将得分显示出来 / 最高得分/等级/飞船
        self.sb.show_score()

        # 如果游戏处于非运行状态 就绘制Play按钮
        # 放在这不会被 背景 外星人等覆盖
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 显示屏幕
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            """
            1、游戏需要一直响应_check_events，用来判断用户是否 按压 q 退出游戏
            2、游戏需要一直刷新屏幕以便等待玩家是否选择开始新游戏时修改屏幕
            3、现在在飞船用完后 屏幕就不会再发生变化了
            """
            self._check_events()
            if self.stats.game_active:
                # 更新飞船位置
                self.ship.update_move()
                # 发射/更新子弹
                self._update_bullets()
                self._update_aliens()
            # 下面注释掉的代码也可以实现游戏结束时 鼠标箭头再次显示出来
            # else:
            #     pygame.mouse.set_visible(True)
            # 更新屏幕
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并允许游戏
    ai = AlienInvasion()
    ai.run_game()
