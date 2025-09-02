import pygame
import os

class Sprite:
    # Define the base directory for graphics
    graphics_dir = os.path.join('graphics')

    # Set images for blitting
    START = pygame.image.load(os.path.join(graphics_dir, 'start.png'))

    FLOOR = [
        pygame.image.load(os.path.join(graphics_dir, 'floor1.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor2.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor3.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor4.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor5.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor6.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor7.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor8.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor9.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor10.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor11.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor12.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor13.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor14.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor15.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor16.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor17.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor18.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor19.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor20.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor21.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor22.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor23.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor24.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor25.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor26.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor27.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor28.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor29.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor30.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor31.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor32.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor33.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor34.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor35.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor36.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor37.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor38.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor39.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor40.png'))
    ]
    WALL = pygame.image.load(os.path.join(graphics_dir, 'wall.png'))

    PIT = pygame.image.load(os.path.join(graphics_dir, 'pit.png'))
    PIT_EVIL = [
        pygame.image.load(os.path.join(graphics_dir, 'pit_evil1.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_evil2.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_evil3.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_evil4.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_evil5.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png'))
    ]
    PIT_CRAZY = [
        pygame.image.load(os.path.join(graphics_dir, 'pit_crazy1.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_crazy2.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_crazy3.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_crazy4.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit_crazy5.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'pit.png'))
    ]

    EXIT = pygame.image.load(os.path.join(graphics_dir, 'exit.png'))
    NO_EXIT = pygame.image.load(os.path.join(graphics_dir, 'exit_inactive.png'))

    WALL_SWITCH_UP_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_up.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_up.png'))
    ]
    WALL_SWITCH_DOWN_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_down.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_down.png'))
    ]
    WALL_SWITCH_LEFT_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_left.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_left.png'))
    ]
    WALL_SWITCH_RIGHT_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_right.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_right.png'))
    ]

    SLIDING_DOOR_HORIZONTAL_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_horizontal.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_horizontal.png'))
    ]
    SLIDING_DOOR_VERTICAL_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_vertical.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_vertical.png'))
    ]

    BOXES = [
        pygame.image.load(os.path.join(graphics_dir, 'box_in_pit.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box_in_pit_return_.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box_return.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box_in_pit_fragile.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box_fragile.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box_in_pit_biohazard.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box_biohazard.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box1.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box2.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box3.png')),
        pygame.image.load(os.path.join(graphics_dir, 'box4.png'))
    ]

    PLAYER = pygame.image.load(os.path.join(graphics_dir, 'player.png'))
    PLAYER_UP = pygame.image.load(os.path.join(graphics_dir, 'player_up.png'))
    PLAYER_DOWN = pygame.image.load(os.path.join(graphics_dir, 'player_down.png'))
    PLAYER_LEFT = pygame.image.load(os.path.join(graphics_dir, 'player_left.png'))
    PLAYER_RIGHT = pygame.image.load(os.path.join(graphics_dir, 'player_right.png'))

    STARS = [
        pygame.image.load(os.path.join(graphics_dir, '0_stars.png')),
        pygame.image.load(os.path.join(graphics_dir, '1_stars.png')),
        pygame.image.load(os.path.join(graphics_dir, '2_stars.png')),
        pygame.image.load(os.path.join(graphics_dir, '3_stars.png'))
    ]
