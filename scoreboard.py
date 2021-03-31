# @Time : 2021-03-31 21:47
# @Author : ly
# @Project : alien_invasion
# @GitHub : https://github.com/lxcl96
import pygame.font


class Scoreboard:
    """显示得分信息的类"""
    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()

    def prep_score(self):
        """将得分选染成一个surface"""
        # 对数字得分进行格式设置
        # round四舍五入 -1代表舍弃个位 到十位
        rounded_score = round(self.stats.score, -1)
        # 使用了字符串格式设置指令， 将数值转成str类型并且在其中插入逗号 例如：1000000 变成 1,000,000
        score_str = "{:,}".format(rounded_score)
        # score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右侧显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示实时分数"""
        self.screen.blit(self.score_image, self.score_rect)