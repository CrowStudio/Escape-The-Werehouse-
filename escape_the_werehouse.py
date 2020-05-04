import pygame
from maps import levels

# Initiate PyGame Mixer to avoid delay of sound playback 
pygame.mixer.pre_init(44100, -16, 1, 2048)
# Initiate PyGame
pygame.init()

# Create BoardElements objekt
board = levels.BoardElements()      

# Set size of game board surface with a color depth of 24-bit 
game_board = pygame.display.set_mode((board.game_board_x,board.game_board_y), 0, 24)
# Set background color - this will be the color of the fill between the tiles and the color of the walls
game_board.fill((30, 30, 30))

ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)

moving = pygame.mixer.Sound('moving.wav')
fall_in_pit = pygame.mixer.Sound('fall_in_pit.wav')



# Value of game board elements 
S = 0
F = 1
W = 2
P1 = 3
P2 = 4
E = 5

# Movement coefficient
DIFF = 100
ANIMATE = 17


# CLASS for Player and Box movements
class Movements():
    '''Movements'''

    def __init__(self):
        '''__init__'''
        # Keep track of PLayer's moves to get score (scores not yet added)
        self.moves = 0
        self.total_moves = 0

        self.p_travel = False
        self.p_dest = 0
        self.p_move = 0

        self.b_sound = False

        self.b1_travel = False
        self.b1_dest = 0
        self.b1_move = 0

        self.b2_travel = False
        self.b2_dest = 0
        self.b2_move = 0

        self.b3_travel = False
        self.b3_dest = 0
        self.b3_move = 0

        self.b4_travel = False
        self.b4_dest = 0
        self.b4_move = 0


    


    # Checks for Pits when box_n is moved
    def __detect_pit__(self, x, y, box_active, box_n):
        '''__detect_pit__''' 
        # Checks for Pit tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If box_n's coordinates matches coordinates of pit1
            # - Set pit1 equals False to fill pit, box_active to False to inactivate box_n,
            #   and set in_pit1 equals to box_n's box_in_pit sprite fill pit, then break foor loop
            if pos_o == (x, y) and tile == P1 and board.pit1:
                board.pit1 = False
                box_active = False
                board.in_pit1 = board.pit_box[box_n]
                # Fade out moving sound and play fall_in_pit sound if Box fell in pit
                ch2.play(fall_in_pit)
                ch2.fadeout(350)
                break

            # If box_n's coordinates matches coordinates of pit2
            # - Set pit2 equals False to fill pit, box_active to False to inactivate box_n,
            #   and set in_pit2 equals to box_n's box_in_pit sprite fill pit, then break foor loop
            elif pos_o == (x, y) and tile == P2 and board.pit2:
                board.pit2 = False
                box_active = False
                board.in_pit2 = board.pit_box[box_n]
                # Fade out moving sound and play fall_in_pit sound if Box fell in pit
                ch2.play(fall_in_pit)
                ch2.fadeout(350)
                break

        # Returns state of active_box
        return box_active


    # Logic for Box detection used in private methods __detect_box_* 
    def __detect_other_box__(self, x, y):
        '''__detect_other_box__'''
        # List of logic to detect if other box is blocking active Box
        self.box_pos = [x == board.b1x and y == board.b1y and board.box1,\
                        x == board.b2x and y == board.b2y and board.box2,\
                        x == board.b3x and y == board.b3y and board.box3,\
                        x == board.b4x and y == board.b4y and board.box4]


    # Detect Wall when moving up         
    def __detect_wall_up__(self, x, y, travel, dest, move):
        '''__detect_wall_up__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Adds movement to Box and Player's direction coordinate, then break for loop
            if (pos_o == (x, dest) and tile == W) or dest < 0:
                self.p_travel = False
                self.p_move -= board.py
                self.p_dest = board.py + DIFF

                travel = False
                move -= y
                dest = y + DIFF
                break

        # Returns direction coordinate of Box
        return y, travel, dest, move


    # Detect other box when moving up 
    def __detect_box_up__(self, x, y, travel, dest, move, box_n):
        '''__detect_box_up__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, dest)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Adds movement to Box and Player's direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            self.p_travel = False
            self.p_move -= board.py
            self.p_dest = board.py + DIFF

            travel = False
            move -= y
            dest = y + DIFF

        # Returns direction coordinate of Box
        return y, travel, dest, move

            
    def __start_animate_up__(self, y, travel, dest, move):
        '''__start_animate_up__'''
        travel = 1
        dest = y - DIFF
        move = y
        if not ch1.get_busy() and self.b_sound:
            ch1.play(moving)
            ch1.fadeout(350)
            self.b_sound = False

        return travel, dest, move


    def __animate_up__(self, y, travel, dest, move):
        '''__animate_up__'''
        if move < dest:
            y = int(round(move,-2))
            travel = False
        else: 
            move -= ANIMATE

        return y, travel, move


    # Checks for wall when moving üp
    def move_player_up(self):
        '''move_player_up'''
        if not self.p_travel:
            self.p_travel, self.p_dest, self.p_move = \
            self.__start_animate_up__(board.py, self.p_travel, self.p_dest, self.p_move)

        elif self.p_travel:
            board.py, self.p_travel, self.p_move = \
            self.__animate_up__(board.py, self.p_travel, self.p_dest, self.p_move)


        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Player's coordinates matches coordinates of Wall
            # - Add movement from Player's direction coordinate and Player's moves
            if (pos_o == (board.px, self.p_dest) and tile == W):
                self.p_travel = False
                self.b1_travel, self.b2_travel, self.b3_travel, self.b4_travel = False, False, False, False
                self.p_move -= board.py
                self.p_dest = board.py + DIFF
                self.moves -= 1
                break


    def move_box_up(self):
        '''move_box_up'''         
        # If Player's coorinates matches coordinates of box1, and dragging Box up (space + up key)
        if board.px == board.b1x and self.p_dest + (DIFF * 2)  == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box1
            if not self.b1_travel:
                self.b_sound = True
                self.b1_travel, self.b1_dest, self.b1_move = \
                self.__start_animate_up__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)
            
            elif self.b1_travel:
                board.b1y, self.b1_travel, self.b1_move = \
                self.__animate_up__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)

        # If Player's coorinates matches coordinates of box1, moving up and box1 is active
        if board.px == board.b1x and self.p_dest == board.b1y and key[pygame.K_UP] and board.box1:
            # Update direction coordinate of box1
            if not self.b1_travel:
                self.b_sound = True
                self.b1_travel, self.b1_dest, self.b1_move = \
                self.__start_animate_up__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)
            
            elif self.b1_travel:
                board.b1y, self.b1_travel, self.b1_move = \
                self.__animate_up__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)

            # Checks for Pits when box1 is moved, and set state of box1
            board.box1 = self.__detect_pit__(board.b1x, board.b1y, board.box1, 0)
            
            # If box1 still active
            if board.box1:
                # Check for Walls, and refresh direction coordinates for box1
                board.b1y, self.b1_travel, self.b1_dest, self.b1_move = \
                self.__detect_wall_up__(board.b1x, board.b1y, self.b1_travel, self.b1_dest, self.b1_move)
                # Check if other box is blocking, and refresh direction coordinates for box1
                board.b1y, self.b1_travel, self.b1_dest, self.b1_move = \
                self.__detect_box_up__(board.b1x, board.b1y, self.b1_travel, self.b1_dest, self.b1_move, 0)



        # If Player's coorinates matches coordinates of box2, and dragging Box up (space + up key)
        if board.px == board.b2x and self.p_dest + (DIFF * 2) == board.b2y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box2
            if not self.b2_travel:
                self.b_sound = True
                self.b2_travel, self.b2_dest, self.b2_move = \
                self.__start_animate_up__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)
            
            elif self.b2_travel:
                board.b2y, self.b2_travel, self.b2_move = \
                self.__animate_up__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)

        if board.px == board.b2x and self.p_dest == board.b2y and key[pygame.K_UP] and board.box2:
            # Update direction coordinate of box2
            if not self.b2_travel:
                self.b_sound = True
                self.b2_travel, self.b2_dest, self.b2_move = \
                self.__start_animate_up__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)
            
        
            elif self.b2_travel:
                board.b2y, self.b2_travel, self.b2_move = \
                self.__animate_up__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)

            # Checks for Pits when box2 is moved, and set state of box2
            board.box2 = self.__detect_pit__(board.b2x, board.b2y, board.box2, 1)
            
            # If box2 still active
            if board.box2:
                board.b2y, self.b2_travel, self.b2_dest, self.b2_move = \
                self.__detect_wall_up__(board.b2x, board.b2y, self.b2_travel, self.b2_dest, self.b2_move)
                # Check if other box is blocking, and refresh direction coordinates for box2
                board.b2y, self.b2_travel, self.b2_dest, self.b2_move = \
                self.__detect_box_up__(board.b2x, board.b2y, self.b2_travel, self.b2_dest, self.b2_move, 1)


        # If Player's coorinates matches coordinates of box3, and dragging Box up (space + up key)
        if board.px == board.b3x and self.p_dest + (DIFF * 2) == board.b3y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box3
            if not self.b3_travel:
                self.b_sound = True
                self.b3_travel, self.b3_dest, self.b3_move = \
                self.__start_animate_up__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)
            
            elif self.b3_travel:
                board.b3y, self.b3_travel, self.b3_move = \
                self.__animate_up__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)

        if board.px == board.b3x and self.p_dest == board.b3y and key[pygame.K_UP] and board.box3:
            # Update direction coordinate of box3
            if not self.b3_travel:
                self.b_sound = True
                self.b3_travel, self.b3_dest, self.b3_move = \
                self.__start_animate_up__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)
            
        
            elif self.b3_travel:
                board.b3y, self.b3_travel, self.b3_move = \
                self.__animate_up__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)

            # Checks for Pits when box3 is moved, and set state of box3
            board.box3 = self.__detect_pit__(board.b3x, board.b3y, board.box3, 2)
            
            # If box3 still active
            if board.box3:
                board.b3y, self.b3_travel, self.b3_dest, self.b3_move = \
                self.__detect_wall_up__(board.b3x, board.b3y, self.b3_travel, self.b3_dest, self.b3_move)
                # Check if other box is blocking, and refresh direction coordinates for box3
                board.b3y, self.b3_travel, self.b3_dest, self.b3_move = \
                self.__detect_box_up__(board.b3x, board.b3y, self.b3_travel, self.b3_dest, self.b3_move, 2)

        # If Player's coorinates matches coordinates of box4, and dragging Box up (space + up key)
        if board.px == board.b4x and self.p_dest + (DIFF * 2) == board.b4y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box4
            if not self.b4_travel:
                self.b_sound = True
                self.b4_travel, self.b4_dest, self.b4_move = \
                self.__start_animate_up__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)
            
            elif self.b4_travel:
                board.b4y, self.b4_travel, self.b4_move = \
                self.__animate_up__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)

        if board.px == board.b4x and self.p_dest == board.b4y and key[pygame.K_UP] and board.box4:
            # Update direction coordinate of box4
            if not self.b4_travel:
                self.b_sound = True
                self.b4_travel, self.b4_dest, self.b4_move = \
                self.__start_animate_up__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)
            
        
            elif self.b4_travel:
                board.b4y, self.b4_travel, self.b4_move = \
                self.__animate_up__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)

            # Checks for Pits when box4 is moved, and set state of box4
            board.box4 = self.__detect_pit__(board.b4x, board.b4y, board.box4, 3)
            
            # If box4 still active
            if board.box4:
                board.b4y, self.b4_travel, self.b4_dest, self.b4_move = \
                self.__detect_wall_up__(board.b4x, board.b4y, self.b4_travel, self.b4_dest, self.b4_move)
                # Check if other box is blocking, and refresh direction coordinates for box4
                board.b4y, self.b4_travel, self.b4_dest, self.b4_move = \
                self.__detect_box_up__(board.b4x, board.b4y, self.b4_travel, self.b4_dest, self.b4_move, 3)


    # Detect Wall when moving up 
    def __detect_wall_down__(self, x, y, b_dest, b_travel):
        '''__detect_wall_down__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Subtract movement from Box and Player's direction coordinate, then break for loop
            if (pos_o == (x, b_dest) and tile == W) or b_dest > board.game_board_y - DIFF:
                self.p_travel = False
                self.p_move += board.py
                self.p_dest = board.py - DIFF

                b_travel = False
                self.b1_move += 0
                self.b1_dest = y - DIFF
                break

        # Returns direction coordinate of Box
        return y, b_travel


    # Detect other box when moving down
    def __detect_box_down__(self, x, y, b_dest, b_travel, box_n):
        '''__detect_box_down__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, b_dest)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Subtracts movement from Box and Player's direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            self.p_travel = False
            self.p_move += board.py
            self.p_dest = board.py - DIFF

            b_travel = False
            self.b1_move += 0
            self.b1_dest = y - DIFF

        # Returns direction coordinate of Box
        return y, b_travel


    def __start_animate_down__(self, y, travel, dest, move):
        '''__start_animate_down__'''
        travel = 2
        dest = y + DIFF
        move = y
        if not ch1.get_busy() and self.b_sound:
            ch1.play(moving)
            ch1.fadeout(350)
            self.b_sound = False

        return travel, dest, move


    def __animate_down__(self, y, travel, dest, move):
        '''__animate_down__'''
        if move > dest:
            y = int(round(move,-2))
            travel = False
        else: 
            move += ANIMATE

        return y, travel, move


    # Checks for wall when moving üp
    def move_player_down(self):
        '''move_player_down'''
        if not self.p_travel:
            self.p_travel, self.p_dest, self.p_move = \
            self.__start_animate_down__(board.py, self.p_travel, self.p_dest, self.p_move)

        elif self.p_travel:
            board.py, self.p_travel, self.p_move = \
            self.__animate_down__(board.py, self.p_travel, self.p_dest, self.p_move)


        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Player's coordinates matches coordinates of Wall
            # - Add movement from Player's direction coordinate and Player's moves
            if (pos_o == (board.px, board.py) and tile == W):
                board.py -= DIFF
                self.moves -= 1
                self.p_travel = False
                break


    def move_box_down(self):
        '''move_box_down'''
        # If Player's coorinates matches coordinates of box1, and dragging Box down (space + down key)
        if board.px == board.b1x and self.p_dest - (DIFF * 2)  == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box1
            if not self.b1_travel:
                self.b_sound = True
                self.b1_travel, self.b1_dest, self.b1_move = \
                self.__start_animate_down__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)
            
            elif self.b1_travel:
                board.b1y, self.b1_travel, self.b1_move = \
                self.__animate_down__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)

        # If Player's coorinates matches coordinates of box1, moving down and box1 is active
        if board.px == board.b1x and self.p_dest == board.b1y and key[pygame.K_DOWN] and board.box1:
            # Update direction coordinate of box1
            if not self.b1_travel:
                self.b_sound = True
                self.b1_travel, self.b1_dest, self.b1_move = \
                self.__start_animate_down__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)

            elif self.b1_travel:
                board.b1y, self.b1_travel, self.b1_move = \
                self.__animate_down__(board.b1y, self.b1_travel, self.b1_dest, self.b1_move)
            
            # Checks for Pits when box1 is moved, and set state of box1
            board.box1 = self.__detect_pit__(board.b1x, board.b1y, board.box1, 0)
            
            # If box1 still active
            if board.box1:
                # Check for Walls, and refresh direction coordinates for box1
                board.b1y, self.b1_travel = self.__detect_wall_down__(board.b1x, board.b1y, self.b1_dest, self.b1_travel)
                # Check if other box is blocking, and refresh direction coordinates for box1
                board.b1y, self.b1_travel = self.__detect_box_down__(board.b1x, board.b1y, self.b1_dest, self.b1_travel, 0)


        # If Player's coorinates matches coordinates of box2, and dragging Box down (space + down key)
        if board.px == board.b2x and self.p_dest - (DIFF * 2) == board.b2y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box2
            if not self.b2_travel:
                self.b_sound = True
                self.b2_travel, self.b2_dest, self.b2_move = \
                self.__start_animate_down__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)
            
            elif self.b2_travel:
                board.b2y, self.b2_travel, self.b2_move = \
                self.__animate_down__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)

        # If Player's coorinates matches coordinates of box2, moving down and box2 is active
        if board.px == board.b2x and self.p_dest == board.b2y and key[pygame.K_DOWN] and board.box2:
            # Update direction coordinate of box2
            if not self.b2_travel:
                self.b_sound = True
                self.b2_travel, self.b2_dest, self.b2_move = \
                self.__start_animate_down__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)            

            elif self.b2_travel:
                board.b2y, self.b2_travel, self.b2_move = \
                self.__animate_down__(board.b2y, self.b2_travel, self.b2_dest, self.b2_move)

            # Checks for Pits when box2 is moved, and set state of box2
            board.box2 = self.__detect_pit__(board.b2x, board.b2y, board.box2, 1)
            
            # If box2 still active
            if board.box2:
                # Check for Walls, and refresh direction coordinates for box2
                board.b2y, self.b2_travel = self.__detect_wall_down__(board.b2x, board.b2y, self.b2_dest, self.b2_travel)
                # Check if other box is blocking, and refresh direction coordinates for box2
                board.b2y, self.b2_travel = self.__detect_box_down__(board.b2x, board.b2y, self.b2_dest, self.b2_travel, 1)

        # If Player's coorinates matches coordinates of box3, and dragging Box down (space + down key)
        if board.px == board.b3x and self.p_dest - (DIFF * 2) == board.b3y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box3
            if not self.b3_travel:
                self.b_sound = True
                self.b3_travel, self.b3_dest, self.b3_move = \
                self.__start_animate_down__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)
            
            elif self.b3_travel:
                board.b3y, self.b3_travel, self.b3_move = \
                self.__animate_down__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)

        # If Player's coorinates matches coordinates of box3, moving down and box3 is active
        if board.px == board.b3x and self.p_dest == board.b3y and key[pygame.K_DOWN] and board.box3:
            # Update direction coordinate of box3
            if not self.b3_travel:
                self.b_sound = True
                self.b3_travel, self.b3_dest, self.b3_move = \
                self.__start_animate_down__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)            

            elif self.b3_travel:
                board.b3y, self.b3_travel, self.b3_move = \
                self.__animate_down__(board.b3y, self.b3_travel, self.b3_dest, self.b3_move)

            # Checks for Pits when box3 is moved, and set state of box3
            board.box3 = self.__detect_pit__(board.b3x, board.b3y, board.box3, 2)
            
            # If box3 still active
            if board.box3:
                # Check for Walls, and refresh direction coordinates for box3
                board.b3y, self.b3_travel = self.__detect_wall_down__(board.b3x, board.b3y, self.b3_dest, self.b3_travel)
                # Check if other box is blocking, and refresh direction coordinates for box3
                board.b3y, self.b3_travel = self.__detect_box_down__(board.b3x, board.b3y, self.b3_dest, self.b3_travel, 2)

        # If Player's coorinates matches coordinates of box4, and dragging Box down (space + down key)
        if board.px == board.b4x and self.p_dest - (DIFF * 2) == board.b4y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box4
            if not self.b4_travel:
                self.b_sound = True
                self.b4_travel, self.b4_dest, self.b4_move = \
                self.__start_animate_down__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)
            
            elif self.b4_travel:
                board.b4y, self.b4_travel, self.b4_move = \
                self.__animate_down__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)

        # If Player's coorinates matches coordinates of box4, moving down and box4 is active
        if board.px == board.b4x and self.p_dest == board.b4y and key[pygame.K_DOWN] and board.box4:
            # Update direction coordinate of box4
            if not self.b4_travel:
                self.b_sound = True
                self.b4_travel, self.b4_dest, self.b4_move = \
                self.__start_animate_down__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)            

            elif self.b4_travel:
                board.b4y, self.b4_travel, self.b4_move = \
                self.__animate_down__(board.b4y, self.b4_travel, self.b4_dest, self.b4_move)

            # Checks for Pits when box4 is moved, and set state of box4
            board.box4 = self.__detect_pit__(board.b4x, board.b4y, board.box4, 3)
            
            # If box4 still active
            if board.box4:
                # Check for Walls, and refresh direction coordinates for box4
                board.b4y, self.b4_travel = self.__detect_wall_down__(board.b4x, board.b4y, self.b4_dest, self.b4_travel)
                # Check if other box is blocking, and refresh direction coordinates for box4
                board.b4y, self.b4_travel = self.__detect_box_down__(board.b4x, board.b4y, self.b4_dest, self.b4_travel, 3)


    # Detect Wall when moving up 
    def __detect_wall_left__(self, x, y):
        '''__detect_wall_left__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Adds movement to Box and Player's direction coordinate, then break for loop
            if (pos_o == (x, y) and tile == W) or x < 0:
                x += DIFF
                board.px += DIFF
                break


        # Returns direction coordinate of Box
        return x


    # Detect other box when moving left
    def __detect_box_left__(self, x, y, box_n):
        '''__detect_box_left__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, y)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Adds movement to Box and Player's direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            x += DIFF
            board.px += DIFF

        # Returns direction coordinate of Box
        return x


    # Checks for wall when moving left
    def move_player_left(self):
        '''move_player_left'''
        if self.p_travel:
            if self.p_move > self.p_dest: 
                self.p_move -= ANIMATE
            else:
                board.px = int(round(self.p_move,-2))
                self.p_travel = False

        elif not self.p_travel: 
            self.p_move = board.px
            self.p_dest = board.px - DIFF
            self.p_travel = 3
            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(350)

        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Player's coordinates matches coordinates of Wall
            # - Add movement from Player's direction coordinate and Player's moves
            if (pos_o == (board.px, board.py) and tile == W):
                board.px += DIFF
                self.moves -= 1
                break


    def move_box_left(self):
        '''move_box_left'''
        # If Player's coorinates matches coordinates of box1, and dragging Box left (space + left key)
        if board.px  + (DIFF + 100) == board.b1x and board.py == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_LEFT]:
            # Update direction coordinate of box1
            board.b1x -= DIFF

        # If Player's coorinates matches coordinates of box1, moving left and box1 is active
        if board.px == board.b1x and board.py == board.b1y and key[pygame.K_LEFT] and board.box1:
            # Update direction coordinate of box1
            board.b1x -= DIFF

            # Checks for Pits when box1 is moved, and set state of box1   
            board.box1 = self.__detect_pit__(board.b1x, board.b1y, board.box1, 0)
            
            # If box1 still active
            if board.box1:
                # Check for Walls, and refresh direction coordinates for box1
                board.b1x = self.__detect_wall_left__(board.b1x, board.b1y)
                # Check if other box is blocking, and refresh direction coordinates for box1
                board.b1x = self.__detect_box_left__(board.b1x, board.b1y, 0)


        # If Player's coorinates matches coordinates of box2, and dragging Box left (space + left key)
        if board.px  + (DIFF + 100) == board.b2x and board.py == board.b2y\
        and key[pygame.K_SPACE] and key[pygame.K_LEFT]:
            # Update direction coordinate of box2
            board.b2x -= DIFF

        if board.px == board.b2x and board.py == board.b2y and key[pygame.K_LEFT] and board.box2:
            # Update direction coordinate of box2
            board.b2x -= DIFF

            # Checks for Pits when box2 is moved, and set state of box2 
            board.box2 = self.__detect_pit__(board.b2x, board.b2y, board.box2, 1)
            
            # If box2 still active
            if board.box2:
                # Check for Walls, and refresh direction coordinates for box2
                board.b2x = self.__detect_wall_left__(board.b2x, board.b2y)
                # Check if other box is blocking, and refresh direction coordinates for box2
                board.b2x = self.__detect_box_left__(board.b2x, board.b2y, 1)

        # If Player's coorinates matches coordinates of box3, and dragging Box left (space + left key)
        if board.px  + (DIFF + 100) == board.b3x and board.py == board.b3y\
        and key[pygame.K_SPACE] and key[pygame.K_LEFT]:
            # Update direction coordinate of box3
            board.b3x -= DIFF

        if board.px == board.b3x and board.py == board.b3y and key[pygame.K_LEFT] and board.box3:
            # Update direction coordinate of box3
            board.b3x -= DIFF

            # Checks for Pits when box3 is moved, and set state of box3  
            board.box3 = self.__detect_pit__(board.b3x, board.b3y, board.box3, 2)
            
            # If box3 still active
            if board.box3:
                # Check for Walls, and refresh direction coordinates for box3
                board.b3x = self.__detect_wall_left__(board.b3x, board.b3y)
                # Check if other box is blocking, and refresh direction coordinates for box3
                board.b3x = self.__detect_box_left__(board.b3x, board.b3y, 2)

        # If Player's coorinates matches coordinates of box4, and dragging Box left (space + left key)
        if board.px  + (DIFF + 100) == board.b4x and board.py == board.b4y\
        and key[pygame.K_SPACE] and key[pygame.K_LEFT]:
            # Update direction coordinate of box4
            board.b4x -= DIFF

        if board.px == board.b4x and board.py == board.b4y and key[pygame.K_LEFT] and board.box4:
            # Update direction coordinate of box4
            board.b4x -= DIFF

            # Checks for Pits when box4 is moved, and set state of box4 
            board.box4 = self.__detect_pit__(board.b4x, board.b4y, board.box4, 3)
            
            # If box4 still active
            if board.box4:
                # Check for Walls, and refresh direction coordinates for box4
                board.b4x = self.__detect_wall_left__(board.b4x, board.b4y)
                # Check if other box is blocking, and refresh direction coordinates for box4
                board.b4x = self.__detect_box_left__(board.b4x, board.b4y, 3)


    # Detect Wall when moving up 
    def __detect_wall_right__(self, x, y):
        '''__detect_wall_right__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Subtract movement from Box and Player's direction coordinate, then break for loop
            if (pos_o == (x, y) and tile == W) or x > board.game_board_x - DIFF:
                x -= DIFF
                board.px -= DIFF
                break


        # Returns direction coordinate of Box
        return x


    # Detect other box when moving right
    def __detect_box_right__(self, x, y, box_n):
        '''__detect_box_right__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, y)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Subtracts movement from Box and Player's direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            x -= DIFF
            board.px -= DIFF

        # Returns direction coordinate of Box
        return x


    # Checks for wall when moving right
    def move_player_right(self):
        '''move_player_right'''
        if self.p_travel:
            if self.p_move < self.p_dest:
                self.p_move += ANIMATE
            else:
                board.px = int(round(self.p_move,-2))
                self.p_travel = False

        elif not self.p_travel: 
            self.p_move = board.px
            self.p_dest = board.px + DIFF
            self.p_travel = 4
            if not ch4.get_busy():
                ch4.play(moving)
                ch4.fadeout(350)

        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Player's coordinates matches coordinates of Wall
            # - Subtract movement from Player's direction coordinate and Player's moves
            if (pos_o == (board.px, board.py) and tile == W):
                board.px -= DIFF
                self.moves -= 1
                break


    def move_box_right(self):
        '''move_box_right'''
        # If Player's coorinates matches coordinates of box1, and dragging Box right (space + right key)
        if board.px - (DIFF + 100) == board.b1x and board.py == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_RIGHT]:
            # Update direction coordinate of box1
            board.b1x += DIFF

        # If Player's coorinates matches coordinates of box1, moving right and box1 is active
        if board.px == board.b1x and board.py == board.b1y and key[pygame.K_RIGHT] and board.box1:
            # Update direction coordinate of box1
            board.b1x += DIFF

            # Checks for Pits when box1 is moved, and set state of box1   
            board.box1 = self.__detect_pit__(board.b1x, board.b1y, board.box1, 0)
            
            # If box1 still active
            if board.box1:
                # Check for Walls, and refresh direction coordinates for box1
                board.b1x = self.__detect_wall_right__(board.b1x, board.b1y)
                # Check if other box is blocking, and refresh direction coordinates for box1
                board.b1x = self.__detect_box_right__(board.b1x, board.b1y, 0)

        # If Player's coorinates matches coordinates of box2, and dragging Box right (space + right key)
        if board.px - (DIFF + 100) == board.b2x and board.py == board.b2y\
        and key[pygame.K_SPACE] and key[pygame.K_RIGHT]:
            # Update direction coordinate of box2
            board.b2x += DIFF

        if board.px == board.b2x and board.py == board.b2y and key[pygame.K_RIGHT] and board.box2:
            # Update direction coordinate of box2
            board.b2x += DIFF
            # Checks for Pits when box2 is moved, and set state of box2 
            board.box2 = self.__detect_pit__(board.b2x, board.b2y, board.box2, 1)
            
            # If box2 still active
            if board.box2:
                # Check for Walls, and refresh direction coordinates for box2
                board.b2x = self.__detect_wall_right__(board.b2x, board.b2y)
                # Check if other box is blocking, and refresh direction coordinates for box2
                board.b2x = self.__detect_box_right__(board.b2x, board.b2y, 1)

        # If Player's coorinates matches coordinates of box3, and dragging Box right (space + right key)
        if board.px - (DIFF + 100) == board.b3x and board.py == board.b3y\
        and key[pygame.K_SPACE] and key[pygame.K_RIGHT]:
            # Update direction coordinate of box3
            board.b3x += DIFF

        if board.px == board.b3x and board.py == board.b3y and key[pygame.K_RIGHT] and board.box3:
            # Update direction coordinate of box3
            board.b3x += DIFF

            # Checks for Pits when box3 is moved, and set state of box3  
            board.box3 = self.__detect_pit__(board.b3x, board.b3y, board.box3, 2)
            
            # If box3 still active
            if board.box3:
                # Check for Walls, and refresh direction coordinates for box3
                board.b3x = self.__detect_wall_right__(board.b3x, board.b3y)
                # Check if other box is blocking, and refresh direction coordinates for box3
                board.b3x = self.__detect_box_right__(board.b3x, board.b3y, 2)

        # If Player's coorinates matches coordinates of box4, and dragging Box right (space + right key)
        if board.px - (DIFF + 100) == board.b4x and board.py == board.b4y\
        and key[pygame.K_SPACE] and key[pygame.K_RIGHT]:
            # Update direction coordinate of box4
            board.b4x += DIFF

        if board.px == board.b4x and board.py == board.b4y and key[pygame.K_RIGHT] and board.box4:
            # Update direction coordinate of box4
            board.b4x += DIFF

            # Checks for Pits when box4 is moved, and set state of box4 
            board.box4 = self.__detect_pit__(board.b4x, board.b4y, board.box4, 3)
            
            # If box4 still active
            if board.box4:
                # Check for Walls, and refresh direction coordinates for box4
                board.b4x = self.__detect_wall_right__(board.b4x, board.b4y)
                # Check if other box is blocking, and refresh direction coordinates for box4
                board.b4x = self.__detect_box_right__(board.b4x, board.b4y, 3)


    # Method to decide if Player 
    def player_detect_exit_or_pit(self, new_level):
        '''player_detect_exit_or_pit'''
        # Check for Exit or Pit tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Player's coordinates matches coordinates of Pit
            # - Set play and new_level to False
            if pos_o == (board.px, board.py) and tile == P1 and board.pit1\
            or pos_o == (board.px, board.py) and tile == P2 and board.pit2:
                board.play = False
                new_level = False
                break
            
            # If Player's coordinates matches coordinates of Exit, and there is more levels
            # - Add moves to total_moves, set moves to 0, and set new_level to True
            elif pos_o == (board.px, board.py) and tile == E and board.lv < board.no_of_levels:
                self.total_moves += self.moves
                self.moves = 0
                new_level = True
                break

            # If Player's coordinates matches coordinates of Exit, and there is no more levels
            # - Set play to False and new_level to True 
            elif pos_o == (board.px, board.py) and tile == E and board.lv >= board.no_of_levels:
                board.play = False
                new_level = True

        # Player has not yet finished the level
        if board.play and not new_level:
            # Returns state for game_on and new_level
            return True, False

        # Player has finished the level
        elif board.play and new_level:
            # Returns state for game_on and new_level
            return True, True

        # Player has finished the last level
        elif not board.play and new_level:
            print('Congratulations! You finished the last level!')
            print(f'Your have made a total of {self.total_moves} moves!')
            # Returns state for game_on and new_level
            return False, False

        # Player fell into a Pit and it is Game Over
        else:       
            print('Game Over!')
            # Returns state for game_on and new_level
            return False, False


# Initiate clock for frame rate 
clock = pygame.time.Clock()

# Initiate Movements object
movements = Movements()


def blit(): 
    game_board.fill((30, 30, 30))
    # Blit current level
    board.blit_level(game_board)
    # Blit position of Boxes
    board.blit_box_1(game_board, movements.b1_travel, movements.b1_move)
    board.blit_box_2(game_board, movements.b2_travel, movements.b2_move)
    board.blit_box_3(game_board, movements.b3_travel, movements.b3_move)
    board.blit_box_4(game_board, movements.b4_travel, movements.b4_move)
    # Blit direction of Player's marker
    board.blit_player(game_board, movements.p_travel, movements.p_move)
    
    # Set caption for window
    pygame.display.set_caption(f'Escape the Werehouse!                 Moves: {movements.moves}')

    # Update all changes to display
    pygame.display.update()


# Initiate game_on
game_on = True
# Initiate new_level
new_level = True
# Initiate move - used for debouncing key press
move = 0

#MAIN LOOP
while game_on:
    # Set frame rate to 20 frames per second
    clock.tick(24)

    # Blit new level if new_level equals True, refresh state of new_level
    new_level = board.generate_level(game_board, new_level)

    # Check for pygame.QUIT event (close window button)
    for event in pygame.event.get():
            # If window is closed
            # - Quite PyGame and Exit program
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                exit()

    # Log state of pressed keys
    key = pygame.key.get_pressed()

    # Movement Debouncing
    if move > 0:
        move += 1
    if move > 3:
        move = 0

    # If arrow-up key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.py > 0 and (key[pygame.K_UP] or key[pygame.K_UP] and key[pygame.K_SPACE]):
        movements.moves += 1
        move = 1
        movements.move_player_up()
        movements.move_box_up() 
        while movements.p_travel == 1:
            clock.tick(24)
            blit()
            movements.move_player_up()
            movements.move_box_up()       

    # If arrow-down key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.py < (board.game_board_y - DIFF) and (key[pygame.K_DOWN] or key[pygame.K_DOWN] and key[pygame.K_SPACE]):
        movements.moves += 1
        move = 1
        movements.move_player_down()
        movements.move_box_down()
        while movements.p_travel == 2:
            clock.tick(24)
            blit()
            movements.move_player_down()
            movements.move_box_down() 
    
    # If arrow-left key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.px > 0 and (key[pygame.K_LEFT] or key[pygame.K_LEFT] and key[pygame.K_SPACE]):
        movements.moves += 1
        move = 1
        movements.move_player_left()
        movements.move_box_left()
        while movements.p_travel == 3:
            clock.tick(24)
            blit()
            movements.move_player_left()
            movements.move_box_down()

    # If arrow-right key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.px < (board.game_board_x - DIFF) and (key[pygame.K_RIGHT] or key[pygame.K_RIGHT] and key[pygame.K_SPACE]):
        movements.moves += 1
        move = 1
        movements.move_player_right()
        movements.move_box_right()
        while movements.p_travel == 4:
            clock.tick(24)
            blit()
            movements.move_player_right()
            movements.move_box_down()

    game_on, new_level = movements.player_detect_exit_or_pit(new_level)
    blit()

pygame.mixer.quit()
pygame.quit()
exit()
