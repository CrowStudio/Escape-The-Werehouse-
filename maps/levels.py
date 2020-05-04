import pygame
from random import randrange

start = pygame.image.load('start.png')
floor = [pygame.image.load('floor1.png'), pygame.image.load('floor2.png'),\
        pygame.image.load('floor3.png'), pygame.image.load('floor4.png'),\
        pygame.image.load('floor5.png'),pygame.image.load('floor6.png'),\
        pygame.image.load('floor7.png'), pygame.image.load('floor8.png'),\
        pygame.image.load('floor9.png'), pygame.image.load('floor10.png'),
        pygame.image.load('floor11.png'), pygame.image.load('floor12.png'),\
        pygame.image.load('floor13.png'), pygame.image.load('floor14.png'),\
        pygame.image.load('floor15.png'),pygame.image.load('floor16.png'),\
        pygame.image.load('floor17.png'), pygame.image.load('floor18.png'),\
        pygame.image.load('floor19.png'), pygame.image.load('floor20.png'),\
        pygame.image.load('floor21.png'), pygame.image.load('floor22.png'),\
        pygame.image.load('floor23.png'), pygame.image.load('floor24.png'),\
        pygame.image.load('floor25.png'),pygame.image.load('floor26.png'),\
        pygame.image.load('floor27.png'), pygame.image.load('floor28.png'),\
        pygame.image.load('floor29.png'), pygame.image.load('floor30.png'),\
        pygame.image.load('floor31.png'), pygame.image.load('floor32.png'),\
        pygame.image.load('floor33.png'), pygame.image.load('floor34.png'),\
        pygame.image.load('floor35.png'),pygame.image.load('floor36.png'),\
        pygame.image.load('floor37.png'), pygame.image.load('floor38.png'),\
        pygame.image.load('floor39.png'), pygame.image.load('floor40.png')]
wall = pygame.image.load('wall.png')
pit = pygame.image.load('pit.png')
box_in_pit = pygame.image.load('box_in_pit.png')
exit = pygame.image.load('exit.png')
exit = pygame.image.load('exit.png')

player = pygame.image.load('player.png')
player_up = pygame.image.load('player_up.png')
player_down = pygame.image.load('player_down.png')
player_left = pygame.image.load('player_left.png')
player_right = pygame.image.load('player_right.png')

boxes = [pygame.image.load('box_in_pit.png'), pygame.image.load('box.png'),\
        pygame.image.load('box_in_pit_return_.png'), pygame.image.load('box_return.png'),\
        pygame.image.load('box_in_pit_fragile.png'), pygame.image.load('box_fragile.png'),\
        pygame.image.load('box_in_pit_biohazard.png'), pygame.image.load('box_biohazard.png')]

x1 = 0
x2 = 100
x3 = 200
x4 = 300
x5 = 400
#y6 = 500
y1 = 0
y2 = 100
y3 = 200
y4 = 300
y5 = 400
#y6 = 500

t1r1 = (x1, y1)
t2r1 = (x2, y1)
t3r1 = (x3, y1)
t4r1 = (x4, y1)
t5r1 = (x5, y1)
#t6r1 = (x6, y1)
t1r2 = (x1, y2)
t2r2 = (x2, y2)
t3r2 = (x3, y2)
t4r2 = (x4, y2)
t5r2 = (x5, y2)
#t6r2 = (x6, y2)
t1r3 = (x1, y3)
t2r3 = (x2, y3)
t3r3 = (x3, y3)
t4r3 = (x4, y3)
t5r3 = (x5, y3)
#t6r3 = (x6, y3)
t1r4 = (x1, y4)
t2r4 = (x2, y4)
t3r4 = (x3, y4)
t4r4 = (x4, y4)
t5r4 = (x5, y4)
#t6r4 = (x6, y4)
t1r5 = (x1, y5)
t2r5 = (x2, y5)
t3r5 = (x3, y5)
t4r5 = (x4, y5)
t5r5 = (x5, y5)
#t6r5 = (x6, y5)
#t1r6 = (x1, y6)
#t2r6 = (x2, y6)
#t3r6 = (x3, y6)
#t4r6 = (x4, y6)
#t5r6 = (x5, y6)
#t6r6 = (x6, y6)

S = 0
F = 1
W = 2
P1 = 3
P2 = 4
E = 5

tiles = (t1r1, t2r1, t3r1, t4r1, t5r1,\
        t1r2, t2r2, t3r2, t4r2, t5r2,\
        t1r3, t2r3, t3r3, t4r3, t5r3,\
        t1r4, t2r4, t3r4, t4r4, t5r4,\
        t1r5, t2r5, t3r5, t4r5, t5r5)

# tiles = (t1r1, t2r1, t3r1, t4r1, t5r1, t6r1,\
#         t1r2, t2r2, t3r2, t4r2, t5r2, t6r2,\
#         t1r3, t2r3, t3r3, t4r3, t5r3, t6r3,\
#         t1r4, t2r4, t3r4, t4r4, t5r4, t6r4,\
#         t1r5, t2r5, t3r5, t4r5, t5r5, t6r5,\
#         t1r6, t2r6, t3r6, t4r6, t5r6, t6r6,)

level_map = [[E, W, W, F, W,\
             F, F, F, F, P1,\
             W, P2 ,W, W, F,\
             F, F, F, F, F,\
             S, F, W, F, F]]

# level_map = [E, W, F, F, W, F,\
#             F, F, F, F, P1, F,\
#             W, P2 ,F, F, F, F,\
#             F, F, F, F, F, F,\
#             W, F, W, F, F, F,
#             S, F, W, F, F, F]

active_boxes = [[True, True, True, False]]
positions = [[t1r2, t2r4, t3r4, t2r2]]

player_start = [t1r5]

level_map.append([W, W, W, F, W,\
             F, P1, E, F, F,\
             W, F ,W, W, W,\
             F, P2, F, S, F,\
             F, F, W, F, F])


active_boxes.append([True, True, False, False])
positions.append([t2r3, t3r4, t1r4, t2r3])

player_start.append(t4r4)



class BoardElements():
    '''BoardElements'''
    def __init__(self):
        '''__init__'''
        self.game_board_x = 500
        self.game_board_y = 500

        self.no_of_levels = sum(type(i) == type([]) for i in level_map)

        self.play = True

        self.pit1 = 1
        self.pit2 = 1

        self.elements = []
        self.box = []
        self.pit_box = []

        self.in_pit1 = 0
        self.in_pit2 = 0

        self.lv = 0


    def __start__(self, game_board,pos):
        '''__start__'''
        game_board.blit(start, (pos))


    def __floor__(self, game_board, pos, i):
        '''__floor__'''
        game_board.blit(floor[i], (pos))


    def __wall__(self, game_board, pos):
        '''__wall__'''
        game_board.blit(wall, (pos))

    def __pit_1__(self, game_board, pos, box):
        '''__pit_1__'''
        if self.pit1:
            game_board.blit(pit, (pos))

        elif not self.pit1:
            game_board.blit(boxes[box], (pos))


    def __pit_2__(self, game_board, pos, box):
        '''__pit_2__'''
        if self.pit2:
            game_board.blit(pit, (pos))

        elif not self.pit2:
            game_board.blit(boxes[box], (pos))


    def __exit___(self, game_board, pos):
        '''__exit___'''        
        game_board.blit(exit, (pos))


    def __create_level__(self, game_board, level_map):
        '''__create_level__'''

        for i in range(len(level_map)):
            rand = randrange(0, 39)

            if level_map[i] == 0:
                self.__start__(game_board, tiles[i])

            elif level_map[i] == 1:
                self.__floor__(game_board, tiles[i], rand)

            elif level_map[i] == 2:
                self.__wall__(game_board, tiles[i])

            elif level_map[i] == 3:
                self.__pit_1__(game_board, tiles[i], self.in_pit1)

            elif level_map[i] == 4:
                self.__pit_2__(game_board, tiles[i], self.in_pit2)

            elif level_map[i] == 5:
                self.__exit___(game_board, tiles[i])
            
            self.elements.append([level_map[i], tiles[i], rand])


    def __create_boxes__(self, level_boxes):
        '''__create_boxes__'''
        rand = randrange(1, 8, 2)
        rand_box = [rand, level_boxes[rand]]
        rand_pit_box = (rand - 1)
        self.pit_box.append(rand_pit_box)
        self.box.append(rand_box)

        r = 1

        while r < 4:
            rand = randrange(1, 8, 2)
            rand_box = [rand, level_boxes[rand]]
            rand_pit_box = (rand - 1)
            
            if rand_box not in self.box:
                self.box.append(rand_box)
                self.pit_box.append(rand_pit_box)

                r += 1


    def __place_boxes_and_player__(self, active_boxes, positions, player_start):
        '''__place_boxes_and_player__'''
        self.px, self.py = player_start

        self.box1 = active_boxes[0]
        self.b1x, self.b1y = positions[0]

        self.box2 = active_boxes[1]
        self.b2x, self.b2y = positions[1]
        
        self.box3 = active_boxes[2]
        self.b3x, self.b3y = positions[2]
        
        self.box4 = active_boxes[3]
        self.b4x, self.b4y = positions[3]

        self.pit1 = 1
        self.pit2 = 1


    def blit_level(self, game_board):
        '''blit_level'''
        for el in self.elements:
            if el[0] == 0:
                self.__start__(game_board, el[1])

            elif el[0] == 1:
                self.__floor__(game_board, el[1], el[2])

            elif el[0] == 2:
                self.__wall__(game_board, el[1])

            elif el[0] == 3:
                self.__pit_1__(game_board, el[1], self.in_pit1)

            elif el[0] == 4:
                self.__pit_2__(game_board, el[1], self.in_pit2)

            elif el[0] == 5:
                self.__exit___(game_board, el[1])


    def generate_level(self, game_board, new_level):
        if new_level:
            self.elements = []
            self.__create_level__(game_board, level_map[self.lv])

            self.box = []
            self.pit_box = []
            self.__create_boxes__(boxes)
            self.__place_boxes_and_player__(active_boxes[self.lv], positions[self.lv], player_start[self.lv])
            
            self.lv += 1

            return False


    def blit_box_1(self, game_board):
        '''blit_box_1'''
        if self.box1:
            game_board.blit(self.box[0][1], (self.b1x, self.b1y))


    def blit_box_2(self, game_board):
        '''blit_box2'''
        if self.box2: 
            game_board.blit(self.box[1][1], (self.b2x, self.b2y))


    def blit_box_3(self, game_board):
        '''blit_box3'''
        if self.box3:
            game_board.blit(self.box[2][1], (self.b3x, self.b3y))


    def blit_box_4(self, game_board):
        '''blit_box4'''    
        if self.box4:
            game_board.blit(self.box[3][1], (self.b4x, self.b4y))

        
    def blit_player(self, game_board, new_level, key):
        '''blit_player'''

        if self.play and not new_level:
            if key[pygame.K_UP]:
                game_board.blit(player_up, (self.px, self.py))

            elif key[pygame.K_DOWN]:
                game_board.blit(player_down, (self.px, self.py))

            elif key[pygame.K_LEFT]:
                game_board.blit(player_left, (self.px, self.py))

            elif key[pygame.K_RIGHT]:
                game_board.blit(player_right, (self.px, self.py))
            else:
                game_board.blit(player, (self.px, self.py))

        else:
            game_board.blit(player, (self.px, self.py))
