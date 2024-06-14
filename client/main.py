import pygame
from client.UIObjects.button import Scene_change_button
from client.characters.PlayableChar import PlayableChar
from random import randint
from client.environment.tree import Tree
from client.UIObjects.CameraGroup import camera_group

pygame.init()
screen_x, screen_y = 1280, 720
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()

camera_group = camera_group()

scene = "play"

def change_scene(new_scene):
    global scene
    scene = new_scene


start_button = Scene_change_button("Start", 100, 0, "play")
home_button = Scene_change_button("Home", 100, 0, "start")
me = PlayableChar(0, 0, camera_group)


for i in range(20):
    rand_x = randint(0, 1000)
    rand_y = randint(0, 1000)
    Tree((rand_x, rand_y), camera_group)


def redraw_window():
    Scene_change_button.mouse_x, Scene_change_button.mouse_y = pygame.mouse.get_pos()
    Scene_change_button.current_scene = scene
    screen.fill('#a9d0db')
    camera_group.set_offset(-me.rect.x + screen_x/2 - me.rect.width/2, -me.rect.y + screen_y/2 - me.rect.height/2)



def main():
    global scene
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Scene_change_button.mouse_clicked = True
            if event.type == pygame.QUIT:
                run = False

        redraw_window()

        if scene == "start":
            scene = start_button.display(screen)
        elif scene == "play":
            # scene = home_button.display(screen)
            camera_group.custom_draw()

        camera_group.update()
        pygame.display.update()

    pygame.quit()

main()