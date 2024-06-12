import pygame
from client.UIObjects.button import Scene_change_button
from client.characters.PlayableChar import PlayableChar

pygame.init()
screen = pygame.display.set_mode((640,480))

scene = "start"


def change_scene(new_scene):
    global scene
    scene = new_scene


start_button = Scene_change_button("Start", 100, 0, "play")
home_button = Scene_change_button("Home", 100, 0, "start")
me = PlayableChar(0, 0, 0.3, 100, 200)


def redraw_window():
    Scene_change_button.mouse_x, Scene_change_button.mouse_y = pygame.mouse.get_pos()
    Scene_change_button.current_scene = scene
    screen.fill((255, 255, 255))


def main():
    global scene
    run = True

    while run:

        redraw_window()

        if scene == "start":
            scene = start_button.display(screen)
        elif scene == "play":
            scene = home_button.display(screen)
            me.display(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Scene_change_button.mouse_clicked = True
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main()