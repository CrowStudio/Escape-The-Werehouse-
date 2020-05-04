import pygame
from maps import levels

# Initiate PyGame Mixer to avoid delay of sound playback 
pygame.mixer.pre_init(44100, -16, 1, 1024)
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
ANIMATE = 10


# CLASS for Player and Box movements
class Movements():
    '''Movements'''

    def __init__(self):
        '''__init__'''
        # Keep track of PLayer's moves to get score (scores not yet added)
        self.moves = 0
        self.total_moves = 0

    # Checks for wall when moving up
    def move_player_up(self):
        '''move_player_up'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Player's coordinates matches coordinates of Wall
            # - Add movement from Player's direction coordinate and Player's moves
            if (pos_o == (board.px, board.py) and tile == W):
                board.py += DIFF
                self.moves -= 1
                break


    # Checks for wall when moving down
    def move_player_down(self):
        '''move_player_down'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Player's coordinates matches coordinates of Wall
            # - Subtract movement from Player's direction coordinate and Player's moves
            if (pos_o == (board.px, board.py) and tile == W):
                board.py -= DIFF
                self.moves -= 1
                break


    # Checks for wall when moving left
    def move_player_left(self):
        '''move_player_left'''
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


    # Checks for wall when moving right
    def move_player_right(self):
        '''move_player_right'''
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
                ch3.stop()
                ch2.play(fall_in_pit)
                ch2.fadeout(400)
                ch1.play(moving)
                ch1.fadeout(100)
                break

            # If box_n's coordinates matches coordinates of pit2
            # - Set pit2 equals False to fill pit, box_active to False to inactivate box_n,
            #   and set in_pit2 equals to box_n's box_in_pit sprite fill pit, then break foor loop
            elif pos_o == (x, y) and tile == P2 and board.pit2:
                board.pit2 = False
                box_active = False
                board.in_pit2 = board.pit_box[box_n]
                # Fade out moving sound and play fall_in_pit sound if Box fell in pit
                ch3.stop()
                ch2.play(fall_in_pit)
                ch2.fadeout(400)
                ch1.play(moving)
                ch1.fadeout(100)
                break

            else:
                # Play moving sound
                if not ch3.get_busy():
                    ch1.stop()
                    ch3.play(moving)
                    # Fade out moving sound
                    ch3.play(moving)
                    ch3.fadeout(750)

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
    def __detect_wall_up__(self, x, y):
        '''__detect_wall_up__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Adds movement to Box and Player's direction coordinate, then break for loop
            if (pos_o == (x, y) and tile == W) or y < 0:
                y += DIFF
                board.py += DIFF
                # Stop sound of moving box if hit Wall
                ch1.stop()
                ch3.stop()
                break


        # Returns direction coordinate of Box
        return y


    # Detect other box when moving up 
    def __detect_box_up__(self, x, y, box_n):
        '''__detect_box_up__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, y)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Adds movement to Box and Player's direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            # Stop sound of moving box if other box is blocking
            ch1.stop()
            ch3.stop()
            y += DIFF
            board.py += DIFF  

        # Returns direction coordinate of Box
        return y


    def move_box_up(self):
        '''move_box_up'''         
        
        # If Player's coorinates matches coordinates of box1, and dragging Box up (space + up key)
        if board.px == board.b1x and board.py + (DIFF + 100) == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box1
            board.b1y -= DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        # If Player's coorinates matches coordinates of box1, moving up and box1 is active
        if board.px == board.b1x and board.py == board.b1y and key[pygame.K_UP] and board.box1:
            # Update direction coordinate of box1
            board.b1y -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

            # Checks for Pits when box1 is moved, and set state of box1
            board.box1 = self.__detect_pit__(board.b1x, board.b1y, board.box1, 0)
            
            # If box1 still active
            if board.box1:
                # Check for Walls, and refresh direction coordinates for box1
                board.b1y = self.__detect_wall_up__(board.b1x, board.b1y)
                # Check if other box is blocking, and refresh direction coordinates for box1
                board.b1y = self.__detect_box_up__(board.b1x, board.b1y, 0)


        # If Player's coorinates matches coordinates of box2, and dragging Box up (space + up key)
        if board.px == board.b2x and board.py + (DIFF + 100) == board.b2y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box2
            board.b2y -= DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        if board.px == board.b2x and board.py == board.b2y and key[pygame.K_UP] and board.box2:
            # Update direction coordinate of box2
            board.b2y -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

            # Checks for Pits when box2 is moved, and set state of box2
            board.box2 = self.__detect_pit__(board.b2x, board.b2y, board.box2, 1)
            
            # If box2 still active
            if board.box2:
                # Check for Walls, and refresh direction coordinates for box2
                board.b2y = self.__detect_wall_up__(board.b2x, board.b2y)
                # Check if other box is blocking, and refresh direction coordinates for box2
                board.b2y = self.__detect_box_up__(board.b2x, board.b2y, 1)

        # If Player's coorinates matches coordinates of box3, and dragging Box up (space + up key)
        if board.px == board.b3x and board.py + (DIFF + 100) == board.b3y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box3
            board.b3y -= DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        if board.px == board.b3x and board.py == board.b3y and key[pygame.K_UP] and board.box3:
            # Update direction coordinate of box3
            board.b3y -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

            # Checks for Pits when box3 is moved, and set state of box3
            board.box3 = self.__detect_pit__(board.b3x, board.b3y, board.box3, 2)
            
            # If box3 still active
            if board.box3:
                # Check for Walls, and refresh direction coordinates for box3
                board.b3y = self.__detect_wall_up__(board.b3x, board.b3y)
                # Check if other box is blocking, and refresh direction coordinates for box3
                board.b3y = self.__detect_box_up__(board.b3x, board.b3y, 2)

        # If Player's coorinates matches coordinates of box4, and dragging Box up (space + up key)
        if board.px == board.b4x and board.py + (DIFF + 100) == board.b4y\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box4
            board.b4y -= DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)
                
        if board.px == board.b4x and board.py == board.b4y and key[pygame.K_UP] and board.box4:
            # Update direction coordinate of box4
            board.b4y -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

            # Checks for Pits when box4 is moved, and set state of box4
            board.box4 = self.__detect_pit__(board.b4x, board.b4y, board.box4, 3)
            
            # If box4 still active
            if board.box4:
                # Check for Walls, and refresh direction coordinates for box4
                board.b4y = self.__detect_wall_up__(board.b4x, board.b4y)
                # Check if other box is blocking, and refresh direction coordinates for box4
                board.b4y = self.__detect_box_up__(board.b4x, board.b4y, 3)


    # Detect Wall when moving up 
    def __detect_wall_down__(self, x, y):
        '''__detect_wall_down__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Subtract movement from Box and Player's direction coordinate, then break for loop
            if (pos_o == (x, y) and tile == W) or y > board.game_board_y - DIFF:
                y -= DIFF
                board.py -= DIFF
                # Stop sound of moving box if hit Wall
                ch1.stop()
                ch3.stop()
                break


        # Returns direction coordinate of Box
        return y


    # Detect other box when moving down
    def __detect_box_down__(self, x, y, box_n):
        '''__detect_box_down__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, y)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Subtracts movement from Box and Player's direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            # Stop sound of moving box if other box is blocking
            ch1.stop()
            ch3.stop()
            y -= DIFF
            board.py -= DIFF

        # Returns direction coordinate of Box
        return y


    def move_box_down(self):
        '''move_box_down'''
        # If Player's coorinates matches coordinates of box1, and dragging Box down (space + down key)
        if board.px == board.b1x and board.py - (DIFF + 100) == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box1
            board.b1y += DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)            

        # If Player's coorinates matches coordinates of box1, moving down and box1 is active
        if board.px == board.b1x and board.py == board.b1y and key[pygame.K_DOWN] and board.box1:
            # Update direction coordinate of box1
            board.b1y += DIFF
            
            # Checks for Pits when box1 is moved, and set state of box1           
            board.box1 = self.__detect_pit__(board.b1x, board.b1y, board.box1, 0)

            # If box1 still active
            if board.box1:
                # Check for Walls, and refresh direction coordinates for box1
                board.b1y = self.__detect_wall_down__(board.b1x, board.b1y)
                # Check if other box is blocking, and refresh direction coordinates for box1
                board.b1y = self.__detect_box_down__(board.b1x, board.b1y, 0)

        # If Player's coorinates matches coordinates of box2, and dragging Box down (space + down key)
        if board.px == board.b2x and board.py - (DIFF + 100) == board.b2y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box2
            board.b2y += DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        # If Player's coorinates matches coordinates of box2, moving down and box2 is active
        if board.px == board.b2x and board.py == board.b2y and key[pygame.K_DOWN] and board.box2:
            # Update direction coordinate of box2
            board.b2y += DIFF

            # Checks for Pits when box2 is moved, and set state of box2          
            board.box2 = self.__detect_pit__(board.b2x, board.b2y, board.box2, 1)

            # If box2 still active
            if board.box2:
                # Check for Walls, and refresh direction coordinates for box2
                board.b2y = self.__detect_wall_down__(board.b2x, board.b2y)
                # Check if other box is blocking, and refresh direction coordinates for box2
                board.b2y = self.__detect_box_down__(board.b2x, board.b2y, 1)

        # If Player's coorinates matches coordinates of box3, and dragging Box down (space + down key)
        if board.px == board.b3x and board.py - (DIFF + 100) == board.b3y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box3
            board.b3y += DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        # If Player's coorinates matches coordinates of box3, moving down and box3 is active
        if board.px == board.b3x and board.py == board.b3y and key[pygame.K_DOWN] and board.box3:
            # Update direction coordinate of box3
            board.b3y += DIFF

            # Checks for Pits when box3 is moved, and set state of box3      
            board.box3 = self.__detect_pit__(board.b3x, board.b3y, board.box3, 2)

            # If box3 still active
            if board.box3:
                # Check for Walls, and refresh direction coordinates for box3
                board.b3y = self.__detect_wall_down__(board.b3x, board.b3y)
                # Check if other box is blocking, and refresh direction coordinates for box3
                board.b3y = self.__detect_box_down__(board.b3x, board.b3y, 2)

        # If Player's coorinates matches coordinates of box4, and dragging Box down (space + down key)
        if board.px == board.b4x and board.py - (DIFF + 100) == board.b4y\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box4
            board.b4y += DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)
           
        # If Player's coorinates matches coordinates of box4, moving down and box4 is active     
        if board.px == board.b4x and board.py == board.b4y and key[pygame.K_DOWN] and board.box4:
            # Update direction coordinate of box4
            board.b4y += DIFF

            # Checks for Pits when box4 is moved, and set state of box4            
            board.box4 = self.__detect_pit__(board.b4x, board.b4y, board.box4, 3)

            # If box4 still active
            if board.box4:
                # Check for Walls, and refresh direction coordinates for box4
                board.b4y = self.__detect_wall_down__(board.b4x, board.b4y)
                # Check if other box is blocking, and refresh direction coordinates for box4
                board.b4y = self.__detect_box_down__(board.b4x, board.b4y, 3)


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
                # Stop sound of moving box if hit Wall
                ch1.stop()
                ch3.stop()
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
            # Stop sound of moving box if other box is blocking
            ch1.stop()
            ch3.stop()
            x += DIFF
            board.px += DIFF

        # Returns direction coordinate of Box
        return x


    def move_box_left(self):
        '''move_box_left'''
        # If Player's coorinates matches coordinates of box1, and dragging Box left (space + left key)
        if board.px  + (DIFF + 100) == board.b1x and board.py == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_LEFT]:
            # Update direction coordinate of box1
            board.b1x -= DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        # If Player's coorinates matches coordinates of box1, moving left and box1 is active
        if board.px == board.b1x and board.py == board.b1y and key[pygame.K_LEFT] and board.box1:
            # Update direction coordinate of box1
            board.b1x -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

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
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        if board.px == board.b2x and board.py == board.b2y and key[pygame.K_LEFT] and board.box2:
            # Update direction coordinate of box2
            board.b2x -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

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
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        if board.px == board.b3x and board.py == board.b3y and key[pygame.K_LEFT] and board.box3:
            # Update direction coordinate of box3
            board.b3x -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

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
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

        if board.px == board.b4x and board.py == board.b4y and key[pygame.K_LEFT] and board.box4:
            # Update direction coordinate of box4
            board.b4x -= DIFF

            if not ch3.get_busy():
                ch3.play(moving)
                ch3.fadeout(750)

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
                # Stop sound of moving box if hit Wall
                ch1.stop()
                ch3.stop()
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
            # Stop sound of moving box if other box is blocking
            ch1.stop()
            ch3.stop()
            x -= DIFF
            board.px -= DIFF

        # Returns direction coordinate of Box
        return x


    def move_box_right(self):
        '''move_box_right'''
        # If Player's coorinates matches coordinates of box1, and dragging Box right (space + right key)
        if board.px - (DIFF + 100) == board.b1x and board.py == board.b1y\
        and key[pygame.K_SPACE] and key[pygame.K_RIGHT]:
            # Update direction coordinate of box1
            board.b1x += DIFF
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

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
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

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
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

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
            if not ch1.get_busy():
                ch1.play(moving)
                ch1.fadeout(750)

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


# Initiate clock for frame rate 
clock = pygame.time.Clock()

# Initiate Movements object
movements = Movements()

# Initiate game_on
game_on = True
# Initiate new_level
new_level = True
# Initiate move - used for debouncing key press
move = 0
# Initiate mobile - used for animation
mobile = 0

#MAIN LOOP
while game_on:
    # Set frame rate to 20 frames per second
    clock.tick(20)

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
        board.py -= DIFF
        movements.moves += 1
        move = 1
        movements.move_player_up()
        movements.move_box_up()            

    # If arrow-down key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.py < (board.game_board_y - DIFF) and (key[pygame.K_DOWN] or key[pygame.K_DOWN] and key[pygame.K_SPACE]):
        board.py += DIFF
        movements.moves += 1
        move = 1
        movements.move_player_down()
        movements.move_box_down()
    
    # If arrow-left key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.px > 0 and (key[pygame.K_LEFT] or key[pygame.K_LEFT] and key[pygame.K_SPACE]):
        board.px -= DIFF
        movements.moves += 1
        move = 1
        movements.move_player_left()
        movements.move_box_left()

    # If arrow-right key is pressed and Player's coordinate is within game_board
    # - Refresh direction coordinate, +1 to moves, increase debounce varibale, move Player and Box
    if move == 0 and board.px < (board.game_board_x - DIFF) and (key[pygame.K_RIGHT] or key[pygame.K_RIGHT] and key[pygame.K_SPACE]):
        board.px += DIFF
        movements.moves += 1
        move = 1
        movements.move_player_right()
        movements.move_box_right()

    # Check for Exit or Pit tiles, refresh state of game_on and new_level
    game_on, new_level = movements.player_detect_exit_or_pit(new_level)
    
    # Blit current level
    board.blit_level(game_board)
    # Blit position of Boxes
    board.blit_box_1(game_board)
    board.blit_box_2(game_board)
    board.blit_box_3(game_board)
    board.blit_box_4(game_board)
    # Blit direction of Player's marker
    board.blit_player(game_board, new_level, key)
    
    # Set caption for window
    pygame.display.set_caption(f'Escape the Werehouse!                 Moves: {movements.moves}')

    # Update all changes to display
    pygame.display.update()

pygame.mixer.quit()
pygame.quit()
exit()