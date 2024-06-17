import pygame
from client.UIObjects.button import Scene_change_button
from client.characters.PlayableChar import PlayableChar
from random import randint
from client.environment.tree import Tree
from client.UIObjects.CameraGroup import camera_group
from server.network import Network

# initialize variables
pygame.init()
screen_x, screen_y = 1280, 720
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()

camera_group = camera_group()

scene = "play"


def change_scene(new_scene):
    global scene
    scene = new_scene


# start_button = Scene_change_button("Start", 100, 0, "play")
# home_button = Scene_change_button("Home", 100, 0, "start")
me = PlayableChar(0, 0, camera_group)
me2 = PlayableChar(0, 0, camera_group)


for i in range(20):
    rand_x = randint(0, 1000)
    rand_y = randint(0, 1000)
    Tree((rand_x, rand_y), camera_group)


def redraw_window():
    global scene

    Scene_change_button.mouse_x, Scene_change_button.mouse_y = pygame.mouse.get_pos()
    Scene_change_button.current_scene = scene
    screen.fill('#a9d0db')
    camera_group.set_offset(-me.rect.x + screen_x/2 - me.rect.width/2, -me.rect.y + screen_y/2 - me.rect.height/2)

    if scene == "start":
        print("start")
        # scene = start_button.display(screen)
    elif scene == "play":
        # scene = home_button.display(screen)
        camera_group.zoom_control()
        camera_group.custom_draw()


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(x, y):
    return str(x) + "," + str(y)

def main():
    global scene
    run = True

    n = Network()

    # only need to set our starting position
    mePos = read_pos(n.get_pos())
    me.set_pos(mePos[0], mePos[1])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Scene_change_button.mouse_clicked = True
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)

        # other players starting position gets updated here
        p2Pos = read_pos(n.send(make_pos(me.rect.centerx, me.rect.centery)))
        me2.set_pos(p2Pos[0], p2Pos[1])

        redraw_window()

        camera_group.update()
        pygame.display.update()

    pygame.quit()

main()