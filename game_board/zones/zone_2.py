import pygame
import json
import os
from game_board.blitter import Blitter
from game_board.elements.sprites import Sprite
from game_board.zones.zone_2_tile import Zone2Tile
from game_board.basic_tile import BasicTile

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ZONE_2_PATH = os.path.join(DIR_PATH, 'level_maps', 'zone_2_maps.json')

# Load the game maps
with open(ZONE_2_PATH, 'r') as file:
    ZONE_DATA = json.load(file)

class ZoneTwo(Blitter):
    '''zone 2'''
    def __init__(self):
        super().__init__(ZONE_DATA, Zone2Tile)
        self.basic_tile = BasicTile

    def check_zone_element_state(self, element, game_state, player_pos=None, boxes_pos=None):
        '''Check if a zone element is valid based on its type and game state.'''
        element_type = element[0]

        if element_type in Zone2Tile.state_mapping:   # Look up the element in the mapping
            entry = Zone2Tile.state_mapping[element_type]
            print('Element type: ', entry)

            if isinstance(entry, tuple) and len(entry) == 4:  # Latching or momentary switches
                switch_state, door_state, element_info, switch_type = entry

                if 'latching' in switch_type:  # Wall switches (latching)
                    # Invert switch state
                    switch_value = getattr(game_state, switch_state)
                    setattr(game_state, switch_state, not switch_value)
                    new_switch_value = not switch_value

                    # Print activation/deactivation with the requested format
                    if new_switch_value:
                        print(f'Switch type is: Latching - Activating {element_info}')
                    else:
                        print(f'Switch type is: Latching - Deactivating {element_info}')

                    # Invert door state
                    door_value = getattr(game_state, door_state)
                    setattr(game_state, door_state, not door_value)
                    # Sliding doors output

                    # Sliding doors output
                    if 'closed' in door_state:
                        if not switch_value:
                            print('Opening sliding door')
                        else:
                            print('Closing sliding door')
                    elif 'open' in door_state:
                        if switch_value:
                            print('Opening sliding door')
                        else:
                            print('Closing sliding door')

                    return True

                else:  # Floor switches (momentary) - state updates in main game loop
                    return True

            else:  # Check sliding door, or trap door status
                door_state, element_info = entry
                active = getattr(game_state, door_state)
                if 'SD' in door_state:  # Sliding door status
                    if active:
                        print(f'The {element_info} is closed!')
                        return False
                    else:
                        print(f'Passing {element_info}')
                        return True

                elif 'TD' in door_state:  # Trap door status
                    if active:
                        print(f'The {element_info} is open!')
                        return False
                    else:
                        print(f'Passing {element_info}')
                        return True


        # Check for basic tiles
        if element_type in self.basic_tile.mapping:
            # Check if Exit is inactive
            if element_type == self.basic_tile.mapping[8] and not game_state.exit:
                return False
            else:
                return True

        # Default case: Element not in mapping
        print(f"Warning: Unknown element {element_type} in check_zone_element_state")
        return False


    def blit_zone_element(self, element, pos, i, game_state):
        # Blit the floor tile
        self.game_board.blit(Sprite.FLOOR[i], pos)
        # Look up the element in the sprite mapping
        if element in Zone2Tile.sprite_mapping:
            sprite_tuple, state_attr = Zone2Tile.sprite_mapping[element]
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


    def blit_level_elements(self, game_state):
        super().blit_level_elements(game_state, blit_zone_element = self.blit_zone_element)

    def blit_status_bar(self, game_state):
        super().blit_status_bar(game_state)

    def validate_move(self, new_x, new_y):
        return super().validate_move(new_x, new_y, check_zone_element_state=self.check_zone_element_state)

    def validate_push(self, push_x, push_y):
        return super().validate_push(push_x, push_y, check_zone_element_state=self.check_zone_element_state)