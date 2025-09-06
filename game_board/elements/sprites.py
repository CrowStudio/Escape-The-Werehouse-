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
    # Used for random PIT
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

    ACTIVATE_EXIT = [
        pygame.image.load(os.path.join(graphics_dir, 'exit_switch_DISENGAGED.png')),
        pygame.image.load(os.path.join(graphics_dir, 'exit_switch_ACTIVE.png'))
    ]

    EXIT = [
        pygame.image.load(os.path.join(graphics_dir, 'exit_disengaged.png')),
        pygame.image.load(os.path.join(graphics_dir, 'exit_active.png'))
    ]

    # Wall switches ON:
    # UP
    WALL_SWITCH_UP_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_up.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_up.png'))
    ]
    WALL_SWITCH_UP_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_up.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_up.png'))
    ]
    # DOWN
    WALL_SWITCH_DOWN_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_down.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_down.png'))
    ]
    WALL_SWITCH_DOWN_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_down.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_down.png'))
    ]
    # LEFT
    WALL_SWITCH_LEFT_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_left.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_left.png'))
    ]
    WALL_SWITCH_LEFT_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_left.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_left.png'))
    ]
    # RIGHT
    WALL_SWITCH_RIGHT_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_right.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_right.png'))
    ]
    WALL_SWITCH_RIGHT_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_right.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_ON_right.png'))
    ]

    # Wall switches OFF:
    # UP
    WALL_SWITCH_UP_1_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_up.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_up.png'))
    ]
    WALL_SWITCH_UP_2_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_up.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_up.png'))
    ]
    # DOWN
    WALL_SWITCH_DOWN_1_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_down.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_down.png'))
    ]
    WALL_SWITCH_DOWN_2_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_down.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_down.png'))
    ]
    # LEFT
    WALL_SWITCH_LEFT_1_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_left.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_left.png'))
    ]
    WALL_SWITCH_LEFT_2_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_left.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_left.png'))
    ]
    # RIGHT
    WALL_SWITCH_RIGHT_1_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_right.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_right.png'))
    ]
    WALL_SWITCH_RIGHT_2_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_DISENGAGED_right.png')),
        pygame.image.load(os.path.join(graphics_dir, 'wall_switch_OFF_right.png'))
    ]

    # Sliding doors OPEN (NO):
    # HORIZONTAL
    SLIDING_DOOR_HORIZONTAL_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_horizontal.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_horizontal.png'))
    ]
    SLIDING_DOOR_HORIZONTAL_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_horizontal.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_horizontal.png'))
    ]
    # VERTICAL
    SLIDING_DOOR_VERTICAL_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_vertical.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_vertical.png'))
    ]
    SLIDING_DOOR_VERTICAL_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_vertical.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_vertical.png'))
    ]

    # Sliding doors CLOSED (NC):
    # HORIZONTAL
    SLIDING_DOOR_HORIZONTAL_1_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_horizontal.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_horizontal.png'))
    ]
    SLIDING_DOOR_HORIZONTAL_2_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_horizontal.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_horizontal.png'))
    ]
    # VERTICAL
    SLIDING_DOOR_VERTICAL_1_0 = [
            pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_vertical.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_vertical.png'))
    ]
    SLIDING_DOOR_VERTICAL_2_0 = [
            pygame.image.load(os.path.join(graphics_dir, 'sliding_door_OPEN_vertical.png')),
        pygame.image.load(os.path.join(graphics_dir, 'sliding_door_CLOSED_vertical.png'))
    ]

    # Floor switches ON:
    FLOOR_SWITCH_1_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_ON_DISENGAGED.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_ON.png'))
    ]
    FLOOR_SWITCH_2_1 = [
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_ON_DISENGAGED.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_ON.png'))
    ]

    # Floor switches OFF:
    FLOOR_SWITCH_1_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_OFF_DISENGAGED.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_OFF.png'))
    ]
    FLOOR_SWITCH_2_0 = [
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_OFF_DISENGAGED.png')),
        pygame.image.load(os.path.join(graphics_dir, 'floor_switch_OFF.png'))
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
