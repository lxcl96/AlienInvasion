# @Time : 2021-03-31 21:47
# @Author : ly
# @Project : alien_invasion
# @GitHub : https://github.com/lxcl96
import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""
    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()
        # 绘制最高得分
        self.prep_high_score()

        # 绘制当前等级
        self.prep_level()
        # 绘制剩余 可用飞船数
        self.prep_ships()

    def prep_score(self):
        """将得分选染成一个surface"""
        # 对数字得分进行格式设置
        # round四舍五入 -1代表舍弃个位 到十位
        rounded_score = round(self.stats.score, -1)
        # 使用了字符串格式设置指令， 将数值转成str类型并且在其中插入逗号 例如：1000000 变成 1,000,000
        score_str = "{:,}".format(rounded_score)
        # score_str = str(self.stats.score)
        self.score_image = self.font.render("Score " + score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右侧显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def prep_high_score(self):
        """将最高的得分渲染成 surface"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("High Score " + high_score_str, True, self.text_color, self.settings.bg_color)

        # 将最高得分放在屏幕的中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    # 更新系统当前的最大分数
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
        self.prep_high_score()

    def prep_level(self):
        """将等级绘制成 surface"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render("Level " + level_str, True, self.text_color, self.settings.bg_color)
        # 将等级放置到得分的下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩下多少艘飞船"""
        # 将剩下飞船编组
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            # 实例化飞船
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            # 将飞船加组
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示实时分数  和最高得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)