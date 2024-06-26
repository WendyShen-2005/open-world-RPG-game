import pygame
from client.UIObjects.button import SceneChangeButton
from client.characters.PlayableChar import PlayableChar
from client.environment.tree import Tree
from client.UIObjects.CameraGroup import CameraGroup
from server.network import Network
from client.characters.Projectiles import Projectile
from client.UIObjects.MouseAttributes import MouseAttributes

# initialize variables
pygame.init()
screen_x, screen_y = 720, 720
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()

camera_group = CameraGroup()

scene = "play"


def change_scene(new_scene):
    global scene
    scene = new_scene


obstacles = []

def redraw_window():
    global scene

    MouseAttributes.set_offset(camera_group.offset)

    # Projectile.mouse_pos = pygame.mouse.get_pos() - camera_group.offset
    SceneChangeButton.mouse_x, SceneChangeButton.mouse_y = pygame.mouse.get_pos()
    SceneChangeButton.current_scene = scene

    camera_group.set_offset(-me.rect.x + screen_x/2 - me.rect.width/2, -me.rect.y + screen_y/2 - me.rect.height/2)

    me.check_collision(obstacles)

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


others = []

# start_button = Scene_change_button("Start", 100, 0, "play")
# home_button = Scene_change_button("Home", 100, 0, "start")
me = PlayableChar(0, 0, camera_group, True, [])


def update_players(new_positions, players):

    new_pos = new_positions.split(",")
    for i in range(len(players)):
        pos = new_pos[i].split("/")
        x = int(pos[0])
        y = int(pos[1])
        players[i].set_pos(x, y)
    return players


def read_obstacles(obst_pos, cam_group):
    obstacles_list = []
    new_obstacles = obst_pos.split(",")
    for pos in new_obstacles:
        p = pos.split("/")
        new_obst = Tree((int(p[0]), int(p[1])), cam_group)
        obstacles_list.append(new_obst)

    return obstacles_list


def main():
    global scene, others, camera_group, obstacles
    run = True

    # start connected to server
    n = Network()

    obstacles = read_obstacles(n.send("get obstacles"), camera_group)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not MouseAttributes.get_mouse_hold():
                    MouseAttributes.set_mouse_hold(True)
                    MouseAttributes.set_mouse_click(False)
                else:
                    MouseAttributes.set_mouse_hold(False)
                    MouseAttributes.set_mouse_click(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                MouseAttributes.set_mouse_hold(False)
                MouseAttributes.set_mouse_click(False)
            elif event.type == pygame.QUIT:
                run = False

        clock.tick(60)

        # other players position gets updated here
        for o in others:
            for p in o.projectiles:
                p.kill()
            o.kill()

        others = []
        new_other_players_list = n.send(me.my_data())

        print("NEW LOOP")
        for new in new_other_players_list:
            new_player = PlayableChar(new[0][0], new[0][1], camera_group, False, new[1])
            others.append(new_player)
            for pro in new_player.projectiles:
                print(str(pro.rect.center))

        print("MY LOOP")
        for p in me.projectiles:
            print(str(p.rect.center))
        redraw_window()
        camera_group.update()
        pygame.display.update()

    pygame.quit()


main()