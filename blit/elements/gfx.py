import pygame

# Set images for blitting
start = pygame.image.load('graphics/start.png')

floor = [pygame.image.load('graphics/floor1.png'), pygame.image.load('graphics/floor2.png'),
        pygame.image.load('graphics/floor3.png'), pygame.image.load('graphics/floor4.png'),
        pygame.image.load('graphics/floor5.png'),pygame.image.load('graphics/floor6.png'),
        pygame.image.load('graphics/floor7.png'), pygame.image.load('graphics/floor8.png'),
        pygame.image.load('graphics/floor9.png'), pygame.image.load('graphics/floor10.png'),
        pygame.image.load('graphics/floor11.png'), pygame.image.load('graphics/floor12.png'),
        pygame.image.load('graphics/floor13.png'), pygame.image.load('graphics/floor14.png'),
        pygame.image.load('graphics/floor15.png'),pygame.image.load('graphics/floor16.png'),
        pygame.image.load('graphics/floor17.png'), pygame.image.load('graphics/floor18.png'),
        pygame.image.load('graphics/floor19.png'), pygame.image.load('graphics/floor20.png'),
        pygame.image.load('graphics/floor21.png'), pygame.image.load('graphics/floor22.png'),
        pygame.image.load('graphics/floor23.png'), pygame.image.load('graphics/floor24.png'),
        pygame.image.load('graphics/floor25.png'),pygame.image.load('graphics/floor26.png'),
        pygame.image.load('graphics/floor27.png'), pygame.image.load('graphics/floor28.png'),
        pygame.image.load('graphics/floor29.png'), pygame.image.load('graphics/floor30.png'),
        pygame.image.load('graphics/floor31.png'), pygame.image.load('graphics/floor32.png'),
        pygame.image.load('graphics/floor33.png'), pygame.image.load('graphics/floor34.png'),
        pygame.image.load('graphics/floor35.png'),pygame.image.load('graphics/floor36.png'),
        pygame.image.load('graphics/floor37.png'), pygame.image.load('graphics/floor38.png'),
        pygame.image.load('graphics/floor39.png'), pygame.image.load('graphics/floor40.png')]

wall = pygame.image.load('graphics/wall.png')

pit = pygame.image.load('graphics/pit.png')
pit_evil = [pygame.image.load('graphics/pit_evil1.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_evil2.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_evil3.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_evil4.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_evil5.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png')]
pit_crazy = [pygame.image.load('graphics/pit_crazy1.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_crazy2.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_crazy3.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_crazy4.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit_crazy5.png'), pygame.image.load('graphics/pit.png'),
            pygame.image.load('graphics/pit.png'), pygame.image.load('graphics/pit.png')]

exit = pygame.image.load('graphics/exit.png')
no_exit = pygame.image.load('graphics/exit_inactive.png')

boxes = [pygame.image.load('graphics/box_in_pit.png'), pygame.image.load('graphics/box.png'),
        pygame.image.load('graphics/box_in_pit_return_.png'), pygame.image.load('graphics/box_return.png'),
        pygame.image.load('graphics/box_in_pit_fragile.png'), pygame.image.load('graphics/box_fragile.png'),
        pygame.image.load('graphics/box_in_pit_biohazard.png'), pygame.image.load('graphics/box_biohazard.png')]

player = pygame.image.load('graphics/player.png')
player_up = pygame.image.load('graphics/player_up.png')
player_down = pygame.image.load('graphics/player_down.png')
player_left = pygame.image.load('graphics/player_left.png')
player_right = pygame.image.load('graphics/player_right.png')

stars = [pygame.image.load('graphics/0_stars.png'), pygame.image.load('graphics/1_stars.png'),
        pygame.image.load('graphics/2_stars.png'), pygame.image.load('graphics/3_stars.png')]