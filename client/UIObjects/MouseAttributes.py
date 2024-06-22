import pygame.mouse


class MouseAttributes:
    __hold_time_threshold = 500
    __mouse_click = False
    __mouse_hold = False
    __offset = (0, 0)

    @staticmethod
    def get_offset():
        return MouseAttributes.__offset

    @staticmethod
    def set_offset(offset):
        MouseAttributes.__offset = offset

    @staticmethod
    def get_mouse_pos():
        return pygame.mouse.get_pos()

    @staticmethod
    def get_mouse_click():
        return MouseAttributes.__mouse_click

    @staticmethod
    def get_mouse_hold():
        return MouseAttributes.__mouse_hold

    @staticmethod
    def set_mouse_hold(hold):
        MouseAttributes.__mouse_hold = hold

    @staticmethod
    def set_mouse_click(click):
        MouseAttributes.__mouse_click = click