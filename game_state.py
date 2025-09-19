import pygame
from game_board.basic_tile import BasicTile

class GameState:
    def __init__(self, zone):
        # Variable for ZoneLevelWrapper instance
        self.zone = zone
        self.zone_level = self.zone.current_level_set
        self.zone_tile = self.zone_level.zone_tile

        # Variables for game lavels
        self.game = False  # False == tutorial levels, True == zone levels
        self.current_level = 0
        self.is_playing = True
        self.new_level = True

        # Varibales for game stats
        self.moves = 0
        self.total_moves = 0
        self.lives = 3

        # Variables for movements
        self.debounce_timer = 0  # To avoid unwanted movements
        self.a_key_pressed = False
        self.normal_movement = True
        self.travel = 0
        self.direction = None  # Only keep track of direction
        self.prev_x = 0
        self.prev_y = 0

        # Variables for the player
        self.facing_direction = 'up'  # Variable to track facing direction of the player
        self.px = 0
        self.py = 0
        self.is_pulling = False
        self.player_in_pit = False

        # Box positions
        # Box 1
        self.b1x = 0
        self.b1y = 0
        # Box 2
        self.b2x = 0
        self.b2y = 0
        # Box 3
        self.b3x = 0
        self.b3y = 0
        # Box 4
        self.b4x = 0
        self.b4y = 0

        # Variables for active/inactive Pit
        self.pit1 = True
        self.pit2 = True
        self.pit3 = True
        self.pit4 = True

        # Variables for Box to fill Pit with
        self.in_pit1 = False
        self.in_pit2 = False
        self.in_pit3 = False
        self.in_pit4 = False

        # Variables for active/inactive Exit
        self.exit = False

        # Variables for game options
        self.lights_out = False
        self.is_searching = False
        self.search = 0
        self.search_speed = 0.4

        self.initialize_zone_elements()


    def initialize_zone_elements(self):
        # Variable for Exit switch
        self.activate_exit = False

        # Variables for wall switches ON:
        # UP
        self.WS_U1_on = False
        self.WS_U2_on = False
        # DOWN
        self.WS_D1_on = False
        self.WS_D2_on = False
        # LEFT
        self.WS_L1_on = False
        self.WS_L2_on = False
        # RIGTH
        self.WS_R1_on = False
        self.WS_R2_on = False

        # Variables for wall switches OFF:
        # UP
        self.WS_U1_off = False
        self.WS_U2_off = False
        # DOWN
        self.WS_D1_off = False
        self.WS_D2_off = False
        # LEFT
        self.WS_L1_off = False
        self.WS_L2_off = False
        # RIGTH
        self.WS_R1_off = False
        self.WS_R2_off = False

        # Variables for sliding doors OPEN (NO):
        # HORIZONTAL
        self.SD_H1_1_normally_open = False
        self.SD_H2_1_normally_open = False
        self.SD_H3_1_normally_open = False
        self.SD_H4_1_normally_open = False
        # VERTICAL
        self.SD_V1_1_normally_open = False
        self.SD_V2_1_normally_open = False
        self.SD_V3_1_normally_open = False
        self.SD_V4_1_normally_open = False

        # Variables for sliding doors CLOSED (NC):
        # HORIZONTAL
        self.SD_H1_0_normally_closed = True
        self.SD_H2_0_normally_closed = True
        self.SD_H3_0_normally_closed = True
        self.SD_H4_0_normally_closed = True
        # VERTICAL
        self.SD_V1_0_normally_closed = True
        self.SD_V2_0_normally_closed = True
        self.SD_V3_0_normally_closed = True
        self.SD_V4_0_normally_closed = True

        # To keep track of momentary elements
        self.momentary_elements = []
        # To keep track of momentary switch states
        self.previous_switch_states = {}

        # Variables for floor switch ON:
        self.FS1_on = False
        self.FS2_on = False
        self.FS3_on = False
        self.FS4_on = False

        # Variables for floor switch OFF:
        self.FS1_off = False
        self.FS2_off = False
        self.FS3_off = False
        self.FS4_off = False


        # Variables for trap doors OPEN (NO):
        # UP
        self.TD_U1_1_normally_open = True
        # DOWN
        self.TD_D1_1_normally_open = True
        # LEFT
        self.TD_L1_1_normally_open = True
        # RIGHT
        self.TD_R1_1_normally_open = True

        # Variables for trap doors CLOSED (NC):
        # UP
        self.TD_U1_0_normally_closed = False
        # DOWN
        self.TD_D1_0_normally_closed = False
        # LEFT
        self.TD_L1_0_normally_closed = False
        # RIGHT
        self.TD_R1_0_normally_closed = False

    def update_zone_tiles(self):
        self.zone_level = self.zone.current_level_set
        self.zone_tile = self.zone_level.zone_tile
        self.initialize_zone_elements()

    # Check if player has reach Exit
    def check_level_complete(self):
        # Check if player is on exit tile
        for element in self.zone_level.elements:
            if element[0] == BasicTile.EXIT:
                if (self.px, self.py) == element[1]:  # Player position matches exit position
                    self.travel = 0
                    return True

        return False


    # Handle actions when a level is completed
    def handle_level_complete(self, high_scores):
        # Render one last frame with player on exit
        self.zone_level.blit_level(self)

        # Show score for completed level
        if self.game:
            # Blit status bar
            self.zone_level.blit_status_bar(self)
            # Blit stars
            self.zone_level.blit_stars(self)
            pygame.time.wait(300)

        # Increment level counter
        self.current_level += 1
        self.moves = 0
        self.new_level = True

        # Handle mode transitions
        if self.game == False and self.current_level >= self.zone_level.no_of_tutorial_levels:
            # Debug statement
            print('Well done, you finished the Tutorials! Now try to Escape the Werehouse!')
            # Set game states
            self.game = True
            self.current_level = 0
            self.moves = 0
            self.total_moves = 0
            self.lives = 3

            return self.zone.current_zone_index

        elif self.game == True and self.current_level >= self.zone_level.no_of_zone_levels and self.zone.current_zone_index < self.zone.no_of_zones:
            self.current_level = 0
            self.moves = 0
            self.zone.switch_to_next_zone()
            self.update_zone_tiles()

            return self.zone.current_zone_index

        elif self.game == True and self.current_level >= self.zone_level.no_of_zone_levels and self.zone.current_zone_index >= self.zone.no_of_zones:
            # Debug statements
            print('Congratulations! You finished the last level!')
            print(f'Your have made a total of {self.total_moves} successful moves!')
            # End game
            self.is_playing = False
            if high_scores.is_high_score(self.total_moves):
                initials = high_scores.get_initials()
                high_scores.add_score(self.total_moves, initials)

            print("Displaying high scores...")  # Debug statement
            high_scores.display_scores()

            return self.zone.current_zone_index


    # Reset the game state variables related to movement at the start of each frame.
    def reset_movement_variables(self):
        self.direction = None  # Reset the movement direction
        self.travel = 0  # Reset the travel distance


    # Set the search direction and activate searching mode.
    def set_search_direction(self, direction):
        self.search_speed = 0.1
        self.search = direction  # Set the search direction
        self.is_searching = True  # Activate searching mode


    # Set the movement direction and travel distance based on the movement input.
    def set_movement_direction(self, movement):
        self.direction = movement['direction']  # Set the movement direction
        self.travel = movement['travel']  # Set the travel distance


    # Update the player's facing direction and set searching properties.
    def update_facing_direction(self, movement):
        self.facing_direction = movement['direction']  # Update the facing direction
        self.search = movement['search']  # Set the search direction
        self.is_searching = True  # Activate searching mode


    # Move within game board
    def is_player_within_game_board(self, new_x, new_y):
        if (new_x < 0 or new_x > self.zone_level.width) or (new_y < 0 or new_y > self.zone_level.height):
            return False
        else:
            return True


    # Move within game board
    def is_box_within_game_board(self, new_x, new_y):
        if (new_x < 0 or new_x > self.zone_level.width-100) or (new_y < 0 or new_y > self.zone_level.height-100):
            return False
        else:
            return True


    # Validate movement
    def validate_move(self, level, new_x, new_y, check_zone_element_state=None):
        if not self.is_player_within_game_board(new_x, new_y):
            print(f"Move ({new_x}, {new_y}) outside the board is not valid!")
            return False

        for element in level.elements:
            if element[1] == (new_x, new_y):
                # Check for valid tiles including EXIT and PITS
                if element[0] == BasicTile.EXIT and self.exit:  # Allow exit only if active
                    return True
                elif element[0] == BasicTile.START or element[0] == BasicTile.FLOOR:
                    return True
                elif element[0] == BasicTile.PIT1 and (not self.pit1 or not self.is_pulling):
                    return True
                elif element[0] == BasicTile.PIT2 and (not self.pit2 or not self.is_pulling):
                    return True
                elif element[0] == BasicTile.PIT3 and (not self.pit3 or not self.is_pulling):
                    return True
                elif element[0] == BasicTile.PIT4 and (not self.pit4 or not self.is_pulling):
                    return True
                elif element[0] == BasicTile.BOTTOMLESS_PIT:
                    return True
                elif element[0] == BasicTile.WALL:
                    return False
                else:
                    return level.check_zone_element_state(element, game_state=self, player_pos=(new_x, new_y))


    # Check if another box is in the way of psuhing box
    def __check_for_obstructing_boxes__(self, level, push_x, push_y):
        # Get active box positions
        box_positions = []
        if level.box1:
            if (self.b1x, self.b1y) == (push_x, push_y):
                print(f'Box 1 (C:{int(self.b1x/100+1)}, R:{int(self.b1y/100+1)}) infront of pushing box!')
            box_positions.append((self.b1x, self.b1y))
        if level. box2:
            if (self.b2x, self.b2y) == (push_x, push_y):
                print(f'Box 2 (C:{int(self.b2x/100+1)}, R:{int(self.b2y/100+1)}) infront of pushing box!')
            box_positions.append((self.b2x, self.b2y))
        if level.box3:
            if (self.b3x, self.b3y) == (push_x, push_y):
                print(f'Box 3 (C:{int(self.b3x/100+1)}, R:{int(self.b3y/100+1)}) infront of pushing box!')
            box_positions.append((self.b3x, self.b3y))
        if level.box4:
            if (self.b4x, self.b4y) == (push_x, push_y):
                print(f'Box 4 (C:{int(self.b4x/100+1)}, R:{int(self.b4y/100+1)}) infront of pushing box!')
            box_positions.append((self.b4x, self.b4y))

        # Check if pushing into another box
        for box_pos in box_positions:
            if box_pos == (push_x, push_y):
                return False

        print('Pushing box')
        return True


    # Validate push
    def validate_push(self, level, push_x, push_y, check_zone_element_state=None):
        if not self.is_box_within_game_board(push_x, push_y):
            print(f"Push ({push_x}, {push_y}) outside the board is not valid!")
            return False

        for element in level.elements:
            if element[1] == (push_x, push_y):
                if element[0] in [BasicTile.START, BasicTile.FLOOR, BasicTile.EXIT,
                                BasicTile.PIT1, BasicTile.PIT2, BasicTile.PIT3, BasicTile.PIT4, BasicTile.BOTTOMLESS_PIT]:
                    return self.__check_for_obstructing_boxes__(level, push_x, push_y)
                elif element[0] == BasicTile.WALL:
                    return False
                else:
                    # Check for obstructing boxes
                    no_boxes = self.__check_for_obstructing_boxes__(level, push_x, push_y)
                    if no_boxes:
                        return level.check_zone_element_state(element, game_state=self, boxes_pos=level.zone_data.positions[1][level.level_index][0])
                    else:
                        return False
        return True


    # Check if a box has fallen into a pit and update states accordingly
    def check_box_in_pit(self, box_num, bx, by):
        # Mapping of pit types to their corresponding attributes
        pit_mapping = {
            BasicTile.PIT1: ('pit1', 'in_pit1'),
            BasicTile.PIT2: ('pit2', 'in_pit2'),
            BasicTile.PIT3: ('pit3', 'in_pit3'),
            BasicTile.PIT4: ('pit4', 'in_pit4'),
            BasicTile.BOTTOMLESS_PIT: ('bottomless_pit')
        }

        # Look for pit element
        for element in self.zone_level.elements:
            position, pit_type = element[1], element[0]

            # Check if the current element is a bottomless pit and matches the given coordinates
            if position == (bx, by) and pit_mapping.get(pit_type) == 'bottomless_pit':
                if box_num == 1:
                    self.zone_level.box1 = False
                elif box_num == 2:
                    self.zone_level.box2 = False
                elif box_num == 3:
                    self.zone_level.box3 = False
                elif box_num == 4:
                    self.zone_level.box4 = False
                return True

            # Check if the current element is pit1-pit4 and matches the given coordinates
            elif position == (bx, by) and pit_type in pit_mapping and not pit_mapping == 'bottomless_pit':
                pit_state, in_pit = pit_mapping[pit_type]
                pit_active = getattr(self, pit_state)

                # Only proceed if the pit is active
                if pit_active:
                    # Deactivate the pit and set the box number in the pit
                    setattr(self, pit_state, False)
                    setattr(self, in_pit, box_num)
                    print(f"Box {box_num} fell into pit {pit_type} (C:{int(bx/100+1)}, R:{int(by/100+1)})")  # Debug statement

                    if box_num == 1:
                        self.zone_level.box1 = False
                    elif box_num == 2:
                        self.zone_level.box2 = False
                    elif box_num == 3:
                        self.zone_level.box3 = False
                    elif box_num == 4:
                        self.zone_level.box4 = False
                    return True

                return False


    # Check if player fell into a pit
    def check_player_in_pit(self, px, py, audio):
        if self.player_in_pit:
            return False

        # Mapping of pit types to their corresponding attributes
        pit_mapping = {
            BasicTile.PIT1: ('pit1'),
            BasicTile.PIT2: ('pit2'),
            BasicTile.PIT3: ('pit3'),
            BasicTile.PIT4: ('pit4'),
            BasicTile.BOTTOMLESS_PIT: ('bottomless_pit')
        }

        # Look for pit element
        for element in self.zone_level.elements:
            position, pit_type = element[1], element[0]

            # Check if the current element is a pit and matches the given coordinates
            if position == (px, py) and pit_type in pit_mapping:
                pit_state = pit_mapping[pit_type]
                if not element[0] == BasicTile.BOTTOMLESS_PIT:
                    pit_active = getattr(self, pit_state)
                else:
                    pit_active = True

                # Only proceed if the pit is active
                if pit_active:
                    # Player fell in pit
                    audio.play_sound('fall')
                    self.lives -= 1
                    self.player_in_pit = True
                    # Reset player movement
                    self.travel = 0

                    # Update player position to the pit
                    self.px, self.py = px, py

                    self.zone_level.blit_level(self)
                    # Update the display
                    pygame.display.flip()

                    # Debug statement to check player position
                    print(f"Oh no! You fell into a pit {pit_type} (C:{int(px/100+1)}, R:{int(py/100+1)})")

                    # Fade out effect
                    self.zone_level.fade_out(self)

                    # Reset level
                    if self.lives > 0:
                        self.new_level = True
                        self.total_moves += 1
                        self.moves = 0
                        self.prev_x, self.prev_y = self.px, self.py
                        return False
                    # Game Over
                    else:
                        self.zone_level.display_game_over()
                        self.is_playing = False
                        return True


    def check_momentary_switches(self):
        '''Check all momentary switches (e.g., floor plates) every frame.'''
        # Collect box positions
        box_positions = [
            (getattr(self, f'b{i}x'), getattr(self, f'b{i}y'))
            for i in range(1, 5)
            if getattr(self.zone_level, f'box{i}')
        ]

        for element, element_pos in self.momentary_elements:
            entry = self.zone_tile.state_mapping[element]
            switch_state, door_state, switch_name, _ = entry

            # Check if player or box is at the element position
            activated = (
                (self.px, self.py) == element_pos
                or any(box_pos == element_pos for box_pos in box_positions)
            )

            # Update switch state
            setattr(self, switch_state, activated)

            # Always update door state to match switch state
            if 'closed' in door_state:
                setattr(self, door_state, activated)
            elif 'open' in door_state:
                setattr(self, door_state, not activated)
            else:
                setattr(self, door_state, activated)

            # Only print if state changed
            previous_state = self.previous_switch_states.get(element, False)
            if activated != previous_state:
                # Print player position if player on element position
                if (self.px, self.py) == element_pos:
                    print('Player position: ', (self.px, self.py))
                    print('Element pos: ', element_pos)
                elif any(box_pos == element_pos for box_pos in box_positions):
                    # Print box position if box on element position
                    for box_pos in box_positions:
                        if box_pos == element_pos:
                            print('Box position:', box_pos)
                            print('Element pos: ', element_pos)

                if activated:
                    print(f'Switch type is: Momentary - Engaging {switch_name} ')
                    if 'closed' in door_state:
                        print('Opening trap door')
                    elif 'open' in door_state:
                        print('Closing trap door')
                    else:
                        print('Exit activated!')
                else:
                    print(f'Switch type is: Momentary - Disengaging {switch_name} ')
                    if 'closed' in door_state:
                        print('Closing trap door')
                    elif 'open' in door_state:
                        print('Opening trap door')
                    else:
                        print('Exit deactivated!')

            # Update previous switch state
            self.previous_switch_states[element] = activated