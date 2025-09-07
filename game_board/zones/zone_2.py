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

    def check_zone_element_state(self, element, game_state):
        '''Check if a zone element is valid based on its type and game state.'''
        element_type = element[0]

        # Look up the element in the mapping
        if element_type in Zone2Tiles.state_mapping:
            entry = Zone2Tiles.state_mapping[element_type]

            # Wall switches:
            if isinstance(entry, tuple) and len(entry) == 3:
                switch_state, door_state, message = entry
                # Invert the state of switch
                switch_value = getattr(game_state, switch_state)
                setattr(game_state, switch_state, not switch_value)
                print('Activating' if getattr(game_state, switch_state) else 'Disengaging')

                door_value = getattr(game_state, door_state)
                setattr(game_state, door_state, not door_value)  # Set door state to match switch state
                # Sliding doors
                if 'SD' in door_state:
                    # For normally closed doors
                    if 'closed' in door_state and not switch_value:
                        print('Opening sliding door')
                    elif 'closed' in door_state and not door_value:
                        print('Closing sliding door')
                    # For normally open doors
                    if 'open' in door_state and switch_value:
                        print('Opening sliding door')
                    elif 'open' in door_state and not door_value:
                        print('Closing sliding door')
                # Trap doors
                else:
                    # For normally closed doors
                    if 'closed' in door_state and not switch_value:
                        print('Opening trap door')
                    elif 'closed' in door_state and not door_value:
                        print('Closing trap door')
                    # For normally open doors
                    if 'open' in door_state and switch_value:
                        print('Opening trap door')
                    elif 'open' in door_state and not door_value:
                        print('Closing trap door')

                return True

            else:  # Sliding doors:
                door_state, door = entry
                active = getattr(game_state, door_state)
                # Sliding doors
                if 'SD' in door_state:
                    if active:
                        print('The', door, 'is closed!')
                        return False
                    else:
                        print('Passing', door)
                        return True
                # Trap doors
                else:
                    if active:
                        print('The', door, 'is open!')
                        return False
                    else:
                        print('Passing', door)
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

    def validate_push(self, box_data, push_x, push_y, game_state):
        return super().validate_push(box_data, push_x, push_y, game_state, check_zone_element_state=self.check_zone_element_state)