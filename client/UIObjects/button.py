import pygame


class Scene_change_button:

    mouse_x, mouse_y = -100, -100
    mouse_clicked = False
    current_scene = "start"

    def __init__(self, name, x, y, new_scene):
        self.name = name
        self.x = x
        self.y = y
        self.new_scene = new_scene

    def display_font(self, screen):
        pygame.font.init()
        my_font = pygame.font.SysFont(self.name, 30)
        text_surface = my_font.render(self.name, False, (255, 255, 255))
        screen.blit(text_surface, (self.x, self.y))

    def hover_display(self, screen):
        if Scene_change_button.mouse_clicked:
            Scene_change_button.mouse_clicked = False
            return self.new_scene

        pygame.draw.rect(screen, "#000000", (self.x - 5, self.y - 5, 110, 110))
        self.display_font(screen)
        return Scene_change_button.current_scene

    def not_hover_display(self, screen):
        pygame.draw.rect(screen, "#000000", (self.x, self.y, 100, 100))
        self.display_font(screen)

    def display(self, screen):
        if (self.x <= Scene_change_button.mouse_x <= self.x + 100) and (self.y <= Scene_change_button.mouse_y <= self.y + 100):
            return self.hover_display(screen)
        else:
            self.not_hover_display(screen)
            return Scene_change_button.current_scene



