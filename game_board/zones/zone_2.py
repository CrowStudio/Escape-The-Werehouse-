import pygame
import json
import os
from game_board.basic_blitting import BasicBoardElements
from game_board.elements.sprites import Sprite
from game_board.zones.zone_2_tiles import Zone2Tiles

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ZONE_2_PATH = os.path.join(DIR_PATH, 'level_maps', 'zone_2_maps.json')

# Load the game maps
with open(ZONE_2_PATH, 'r') as file:
    ZONE_DATA = json.load(file)

class ZoneTwo(BasicBoardElements):
    '''zone 2'''
    def __init__(self):
        super().__init__(ZONE_DATA)

    def check_zone_element_state(self, element, game_state, player_pos=None, boxes_pos=None):
        '''Check if a zone element is valid based on its type and game state.'''
        element_type = element[0]
        element_pos = element[1]

        if element_type in Zone2Tiles.state_mapping:   # Look up the element in the mapping
            entry = Zone2Tiles.state_mapping[element_type]
            print('Element typ: ', entry)

            if isinstance(entry, tuple) and len(entry) == 4:  # Latching or momentary switches
                switch_state, door_state, element_info, switch_type = entry
                if 'latching' in switch_type:
                    print('Switch type is: Latching')
                    latching = True
                else:
                    print('Switch type is: Momentary')
                    latching = False

                if latching:  # Wall switches (latching)
                    # Invert switch state
                    switch_value = getattr(game_state, switch_state)
                    setattr(game_state, switch_state, not switch_value)
                    print(f'Activating {element_info}' if getattr(game_state, switch_state) else f'Deactivating {element_info}')

                    # Invert door state
                    door_value = getattr(game_state, door_state)
                    setattr(game_state, door_state, not door_value)
                    # Sliding doors output
                    if 'closed' in door_state and not switch_value:
                        print('Opening sliding door')
                    elif 'closed' in door_state and not door_value:
                        print('Closing sliding door')
                    if 'open' in door_state and switch_value:
                        print('Opening sliding door')
                    elif 'open' in door_state and not door_value:
                        print('Closing sliding door')

                    return True

                ##############################################################
                # Need to refactor code to be able to update this each frame #
                ##############################################################

                else:  # Floor switches (momentary)
                    print('Player pos: ', player_pos)
                    print('Boxes pos: ', boxes_pos)
                    print('Element pos: ', element_pos)


                    activated = (player_pos == element_pos) or (boxes_pos and element_pos in boxes_pos)

                    if activated:
                        print('Engaging', element_info)
                        # Invert switch state
                        setattr(game_state, switch_state, activated)
                        switch_value = getattr(game_state, switch_state)
                        print(switch_value)

                        # Invert door state
                        setattr(game_state, door_state, activated)
                        door_value = getattr(game_state, door_state)
                        print(door_value)

                    else:
                        print('Disengaging', element_info)
                        # Invert switch state
                        setattr(game_state, switch_state, activated)
                        switch_value = getattr(game_state, switch_state)
                        print(switch_value)

                        # Invert door state
                        setattr(game_state, door_state, activated)
                        door_value = getattr(game_state, door_state)
                        print(door_value)

                    # Trap doors output
                    if 'closed' in door_state and activated:
                        print('Opening trap door')
                    elif 'closed' in door_state and not activated:
                        print('Closing trap door')
                    if 'open' in door_state and activated:
                        print('Opening trap door')
                    elif 'open' in door_state and not activated:
                        print('Closing trap door')
                    return True

            # Basic tiles are OK
            elif element_type in self.basic_tile:
                return True

            else:  # Check sliding door, or trap door status
                door_state, element_info = entry
                active = getattr(game_state, door_state)
                if 'SD' in door_state:  # Sliding doors status
                    if active:
                        print(f'The {element_info} is closed!')
                        return False
                    else:
                        print(f'Passing {element_info}')
                        return True

                else:  # Trap doors status
                    if active:
                        print(f'The {element_info} is open!')
                        return False
                    else:
                        print(f'Passing {element_info}')
                        return True

        # Default case: Element not in mapping
        print(f"Warning: Unknown element {element_type} in check_zone_element_state")
        return False


    def blit_zone_element(self, element, pos, i, game_state):
        # Blit the floor tile
        self.game_board.blit(Sprite.FLOOR[i], pos)
        # Look up the element in the sprite mapping
        if element in Zone2Tiles.sprite_mapping:
            sprite_tuple, state_attr = Zone2Tiles.sprite_mapping[element]
            # Get the state of the element from game_state
            element_state = getattr(game_state, state_attr)

            # Select the appropriate sprite based on the element state
            if isinstance(sprite_tuple, tuple) and len(sprite_tuple) == 2:
                # Use the first sprite if element_state is True, else use the second sprite
                sprite = sprite_tuple[0] if element_state == False else sprite_tuple[1]
            else:
                # Fallback: Use the sprite directly if it's not a tuple
                sprite = sprite_tuple

            # Blit the selected sprite
            self.game_board.blit(sprite, pos)

    def blit_level(self, game_state):
        super().blit_basic_elements(game_state, blit_zone_element = self.blit_zone_element)

    def validate_move(self, new_x, new_y, game_state):
        return super().validate_move(new_x, new_y, game_state, check_zone_element_state=self.check_zone_element_state)

    def validate_push(self, push_x, push_y, game_state):
        return super().validate_push(push_x, push_y, game_state, check_zone_element_state=self.check_zone_element_state)