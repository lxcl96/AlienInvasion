# @Time : 2021-03-29 21:50
# @Author : ly
# @Project : alien_invasion
# @GitHub : https://github.com/lxcl96
import pygame.font


class Button:
    """由于pygame没有内置按钮的方法，我们需要借助font将其渲染成surface对象来自定义一个按钮"""
    def __init__(self, ai_game, msg):
        # 初始化按钮的属性  msg为要显示的文本内容
        # 获取屏幕信息
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # 指定什么字体来渲染文本 参数none代表使用默认字体，48为字号
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象初始位置（0，0）初始长宽 ，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需要创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上"""
        # render 将文本转化为surface对象，第一个参数为要显示的内容 第二个参数为是否消除锯齿
        #   第三个参数为文本的颜色，第四个参数为背景的颜色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # 初始化此surface对象 位置
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        # 显示 按钮颜色 大小
        self.screen.fill(self.button_color, self.rect)
        # 显示文本 surface 大小
        self.screen.blit(self.msg_image, self.msg_image_rect)