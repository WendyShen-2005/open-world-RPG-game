import pygame
from client.UIObjects.button import Scene_change_button
from client.characters.PlayableChar import PlayableChar
from random import randint
from client.environment.tree import Tree
from client.UIObjects.CameraGroup import camera_group
from server.network import Network

# initialize variables
pygame.init()
screen_x, screen_y = 720, 720
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()

camera_group = camera_group()

scene = "play"


def change_scene(new_scene):
    global scene
    scene = new_scene

obstacles = []

# for i in range(20):
#     rand_x = randint(0, 1000)
#     rand_y = randint(0, 1000)
#     Tree((rand_x, rand_y), camera_group)
#     obstacles.append(Tree((rand_x, rand_y), camera_group))


def redraw_window():
    global scene

    Scene_change_button.mouse_x, Scene_change_button.mouse_y = pygame.mouse.get_pos()
    Scene_change_button.current_scene = scene
    screen.fill('#a9d0db')
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
me = PlayableChar(0, 0, camera_group)


def update_players(new_positions, players):
    print("new pos: " + str(new_positions) + ", players: " + str(players))

    try:
        new_positions.index(",")
        new_positions = new_positions[:-1]
    except ValueError as e:
        pass

    new_pos = new_positions.split(",")
    print("new positions " + str(new_pos))
    for i in range(len(players)):
        pos = new_pos[i].split("/")
        print(str(pos) + " " + str(i) + " " + str(len(players) - 1))
        x = int(pos[0])
        y = int(pos[1])
        players[i].set_pos(x, y)
    return players


def read_obstacles(obst_pos, cam_group):
    obstacles_list = []
    new_obstacles = obst_pos.split(",")
    print(obst_pos)
    print(str(new_obstacles) + " yes")
    for pos in new_obstacles:
        p = pos.split("/")
        print(str(p))
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
                Scene_change_button.mouse_clicked = True
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)

        num_players = int(n.send("num players"))
        if num_players != len(others) + 1:
            others.append(PlayableChar(0, 0, camera_group))
            print("num players: " + str(num_players))

        # other players position gets updated here

        new_pos = n.send(str(me.rect.centerx) + "/" + str(me.rect.centery))

        if new_pos != "N/A":
            others = update_players(new_pos, others)
        # ^^ sending our player pos to server, server sends player 2s data back
        # me2.set_pos(p2Pos[0], p2Pos[1])

        redraw_window()

        camera_group.update()
        pygame.display.update()

    pygame.quit()


main()