# @Time : 2021-03-28 11:41
# @Author : ly
# @Project : alien_invasion
# @GitHub : https://github.com/lxcl96
class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        # 重置飞船 初始实例时 飞船数量等于settings中 飞船数量
        self.reset_status()
        # 设置游戏运行标志 初始设为false
        self.game_active = False


    def reset_status(self):
        """初始化在游戏运行期间可能变化 的统计信息"""
        # 此处统计剩下飞船数量
        self.ship_left = self.settings.ship_limit