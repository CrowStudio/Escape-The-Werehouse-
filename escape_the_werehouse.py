import pygame
import logging
import sys
from game_board.basic_tile import BasicTile
from game_board.zone_level_wrapper import ZoneLevelWrapper
from sound import AudioManager
from high_scores import ScoreManager
from start_screen import StartMenu
from game_state import GameState

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize PyGame and audio
try:
    pygame.mixer.pre_init(44100, -16, 1, 2048)
    pygame.init()
except pygame.error as e:
    logger.error(f"Failed to initialize PyGame: {e}")
    sys.exit(1)

# Game constants
FPS = 120
MOVEMENT_DELAY = 6  # Controls movement speed (higher = slower)
ARROW_KEYS = {pygame.K_UP:    {'direction': 'up',    'travel': 1, 'search': 1},
              pygame.K_DOWN:  {'direction': 'down',  'travel': 2, 'search': 2},
              pygame.K_LEFT:  {'direction': 'left',  'travel': 3, 'search': 3},
              pygame.K_RIGHT: {'direction': 'right', 'travel': 4, 'search': 4}}

# # Creates a list of maps from tutorial_maps and game_maps
# level_map = [tutorial_maps.tutorial_map]
# level_map.append(game_maps.level_map)


# Handle keyboard input for player movement and actions.
def handle_input(keys, level, game_state, audio):
    # Reset movement variables for this frame to ensure no residual state affects the current frame
    game_state.reset_movement_variables()

    # Handle pulling action, which is triggered by the spacebar + any arrow key while standing close to box
    game_state.is_pulling = keys[pygame.K_SPACE]

    # Handle searching with WASD keys, which controls the searchlight direction independently of movement when lights out
    handle_searching(keys, game_state)

    # Store the current player position to allow rollback if the move is invalid or dangerous
    game_state.prev_x, game_state.prev_y = game_state.px, game_state.py

    # Process arrow key inputs for player movement and direction changes
    if process_arrow_keys(keys, game_state):
        # Attempt to move the player and boxes; if successful, increment the move count
        if move_player_and_boxes(level, audio, game_state):
            # Only increment the move count if the player's position has changed
            if (game_state.px, game_state.py) != (game_state.prev_x, game_state.prev_y):
                game_state.moves += 1
                # Add moves to total_moves for high scores
                game_state.total_moves += 1
            return True
        else:
            # Reset player position if the move was invalid or the player fell into a pit
            game_state.px, game_state.py = game_state.prev_x, game_state.prev_y

    return False


# Process arrow key inputs for player movement and direction changes.
def process_arrow_keys(keys, game_state):
    # Iterate over each arrow key and its corresponding movement data
    for key, movement in ARROW_KEYS.items():
        if keys[key] and not game_state.key_locked:
            # Handle the movement based on the arrow key pressed
            handle_movement(game_state, movement)
            game_state.key_locked = True  # Lock the key to prevent repeated actions from a single press
            return True  # Only process one arrow key per frame

    # Unlock the key if no arrow key is pressed this frame, allowing future input
    if not any(keys[k] for k in ARROW_KEYS):
        game_state.key_locked = False

    return False


# Handle the searching action using WASD keys, which controls the searchlight direction.
def handle_searching(keys, game_state):
    # Check each WASD key and set the search direction accordingly
    if keys[pygame.K_w]:
        game_state.set_search_direction(1)  # Search up
    elif keys[pygame.K_s]:
        game_state.set_search_direction(2)  # Search down
    elif keys[pygame.K_a]:
        game_state.set_search_direction(3)  # Search left
    elif keys[pygame.K_d]:
        game_state.set_search_direction(4)  # Search right
    else:
        game_state.search_speed = 0.4
        game_state.is_searching = False  # No searching if no WASD key is pressed


# Handle the movement logic based on the current game state and movement input.
def handle_movement(game_state, movement):
    if game_state.normal_movement:
        # Handle normal movement when the player is allowed to move up
        handle_normal_movement(game_state, movement)
    else:
        # Handle alternative movement, such as rotating or moving in the facing direction
        handle_alternative_movement(game_state, movement)


# Handle normal movement when the player is moving up.
def handle_normal_movement(game_state, movement):
    if game_state.lights_out and not game_state.is_pulling:
        # Handle movement when the lights are out, affecting visibility and direction
        handle_lights_out_movement(game_state, movement)
    elif game_state.is_pulling:
        # If pulling, set the movement direction
        game_state.set_movement_direction(movement)
    else:
        # Normal movement without pulling or lights out
        game_state.set_movement_direction(movement)


# Handle movement logic when the lights are out, affecting visibility.
def handle_lights_out_movement(game_state, movement):

    if game_state.facing_direction == movement['direction']:
        # Move in the facing direction if already aligned
        game_state.set_movement_direction(movement)
    else:
        # Update the facing direction and set searching properties if not aligned
        game_state.update_facing_direction(movement)


# Handle alternative movement logic, such as rotating or moving in the facing direction.
def handle_alternative_movement(game_state, movement):
    if movement['direction'] == 'left':
        # Rotate the facing direction counter-clockwise
        rotate_facing_direction(game_state, counter_clockwise=True)
    elif movement['direction'] == 'right':
        # Rotate the facing direction clockwise
        rotate_facing_direction(game_state, counter_clockwise=False)
    elif movement['direction'] in ['up', 'down']:
        # Move in the current facing direction
        move_in_facing_direction(game_state, movement)


# Rotate the player's facing direction clockwise or counter-clockwise.
def rotate_facing_direction(game_state, counter_clockwise):
    directions = ['up', 'right', 'down', 'left']  # List of possible directions
    current_index = directions.index(game_state.facing_direction)  # Find the current direction index
    if counter_clockwise:
        current_index = (current_index - 1) % 4  # Rotate counter-clockwise
    else:
        current_index = (current_index + 1) % 4  # Rotate clockwise
    game_state.facing_direction = directions[current_index]  # Update the facing direction


# Move the player in the current facing direction based on the movement input.
def move_in_facing_direction(game_state, movement):
    # Map the movement direction to the facing direction
    direction_map = {
        'up': {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'},
        'down': {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    }
    game_state.direction = direction_map[movement['direction']][game_state.facing_direction]  # Set the movement direction
    game_state.travel = movement['travel']  # Set the travel distance


# Check if move is valid
def is_valid_move(level, new_x, new_y, game_state):
    # Check if the target position contains a valid tile
    valid_move = game_state.validate_move(level, new_x, new_y, check_zone_element_state=level.check_zone_element_state)
    if not valid_move:
        return False
    return True


def is_push_valid(level, new_x, new_y, game_state):
    if not game_state.is_box_within_game_board(new_x, new_y):
        print(f"Push ({new_x}, {new_y}) outside the board is not valid!")
        return False

    # Get active box positions
    box_positions = []
    if level.box1: box_positions.append([[1], (game_state.b1x, game_state.b1y)])
    if level.box2: box_positions.append([[2], (game_state.b2x, game_state.b2y)])
    if level.box3: box_positions.append([[3], (game_state.b3x, game_state.b3y)])
    if level.box4: box_positions.append([[4], (game_state.b4x, game_state.b4y)])

    # Calculate position behind player
    behind_x = game_state.px + (game_state.px - new_x)
    behind_y = game_state.py + (game_state.py - new_y)
    if game_state.is_pulling:
        # Check for box behind player
        box_behind = False
        for box_pos in box_positions:
            if box_pos[1] == (behind_x, behind_y):
                box_behind = True
                break

        # If no box behind when pulling, check if we're trying to walk over a box
        if not box_behind:
            for box_pos in box_positions:
                if box_pos[1] == (new_x, new_y):
                    return False  # Can't walk over box while holding space
            return True

        # Check if target position is blocked by another box
        for box_pos in box_positions:
            if box_pos[1] == (new_x, new_y):
                return False
    else:
        # Handle pushing boxes
        box_at_target = False
        for box_pos in box_positions:
            if box_pos[1] == (new_x, new_y):
                box_at_target = True
                # box_data = [box_pos[0], box_pos[1]]
                break

        if box_at_target:
            # Rest of pushing validation...
            push_x = new_x + (new_x - game_state.px)
            push_y = new_y + (new_y - game_state.py)

            # Check if push position is valid
            push_valid = game_state.validate_push(level, push_x, push_y, game_state)
            if not push_valid:
                return False

            # Check if pushing into another box
            for box_pos in box_positions:
                if box_pos == (push_x, push_y):
                    return False

    return True


# Handle movement of player and associated boxes
def move_player_and_boxes(level, audio, game_state):
    # Get current position
    x = game_state.px
    y = game_state.py
    new_x, new_y = x, y

    # Calculate target position (exactly one tile)
    if game_state.direction == 'up':
        new_y = y - BasicTile.SIZE  # Move exactly one tile up
    elif game_state.direction == 'down':
        new_y = y + BasicTile.SIZE  # Move exactly one tile down
    elif game_state.direction == 'left':
        new_x = x - BasicTile.SIZE  # Move exactly one tile left
    elif game_state.direction == 'right':
        new_x = x + BasicTile.SIZE  # Move exactly one tile right

    # Check if the push is valid
    if not is_push_valid(level, new_x, new_y, game_state):
        print('Cannot move in that direction!')
        return False  # Don't push if invalid

    # Check if the move is valid
    if not is_valid_move(level, new_x, new_y, game_state):
        print('Cannot move in that direction!')
        return False  # Don't move if invalid

    # Check if player falls into pit
    if game_state.check_player_in_pit(new_x, new_y, audio):
        return False  # Movement was valid but player fell

    # Handle box movement
    if game_state.is_pulling:
        # Calculate position behind player
        behind_x = x + (x - new_x)
        behind_y = y + (y - new_y)

        # Check for box behind player and move it to current player position first
        if (behind_x, behind_y) == (game_state.b1x, game_state.b1y) and level.box1:
            game_state.b1x, game_state.b1y = x, y  # Move box to current player position
            game_state.check_box_in_pit(1, x, y)
            audio.play_sound('move')
        elif (behind_x, behind_y) == (game_state.b2x, game_state.b2y) and level.box2:
            game_state.b2x, game_state.b2y = x, y  # Move box to current player position
            game_state.check_box_in_pit(2, x, y)
            audio.play_sound('move')
        elif (behind_x, behind_y) == (game_state.b3x, game_state.b3y) and level.box3:
            game_state.b3x, game_state.b3y = x, y  # Move box to current player position
            game_state.check_box_in_pit(3, x, y)
            audio.play_sound('move')
        elif (behind_x, behind_y) == (game_state.b4x, game_state.b4y) and level.box4:
            game_state.b4x, game_state.b4y = x, y  # Move box to current player position
            game_state.check_box_in_pit(4, x, y)
            audio.play_sound('move')
    else:
        # Handle pushing boxes
        if (new_x, new_y) == (game_state.b1x, game_state.b1y) and level.box1:
            game_state.b1x = new_x + (new_x - x)
            game_state.b1y = new_y + (new_y - y)
            if game_state.check_box_in_pit(1, game_state.b1x, game_state.b1y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')
        elif (new_x, new_y) == (game_state.b2x, game_state.b2y) and level.box2:
            game_state.b2x = new_x + (new_x - x)
            game_state.b2y = new_y + (new_y - y)
            if game_state.check_box_in_pit(2, game_state.b2x, game_state.b2y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')
        elif (new_x, new_y) == (game_state.b3x, game_state.b3y) and level.box3:
            game_state.b3x = new_x + (new_x - x)
            game_state.b3y = new_y + (new_y - y)
            if game_state.check_box_in_pit(3, game_state.b3x, game_state.b3y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')
        elif (new_x, new_y) == (game_state.b4x, game_state.b4y) and level.box4:
            game_state.b4x = new_x + (new_x - x)
            game_state.b4y = new_y + (new_y - y)
            if game_state.check_box_in_pit(4, game_state.b4x, game_state.b4y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')

    # Move player to new position
    print('Moving')
    game_state.px = new_x
    game_state.py = new_y

    return True


def main():
    # Initialize game components
    audio = AudioManager()
    high_scores = ScoreManager()
    zone = ZoneLevelWrapper()
    game_state = GameState(zone)
    start_menu = StartMenu(zone, game_state)

    clock = pygame.time.Clock()
    show_start_screen = True

    while True:
        # Show start screen
        if show_start_screen:
            start_menu.draw()
            action = start_menu.handle_events()
            # Start game
            if action == 'start_game':
                show_start_screen = False
            # Show High Scores
            elif action == 'show_high_scores':
                high_scores.from_start_screen = True  # Set to True to enable Back button
                high_scores.display_scores()
                while start_menu.show_high_scores:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        # Back to start screen
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if 200 <= mouse_pos[0] <= 400 and 500 <= mouse_pos[1] <= 540:
                                start_menu.show_high_scores = False
                                start_menu.draw()
        else:
            game_state.new_level = True  # Reset level to start from the selected one

            # Main game loop
            while game_state.is_playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_state.is_playing = False
                        show_start_screen = True

                # Prepare new level
                if game_state.new_level:
                    zone.current_level_set.level_index = game_state.current_level
                    mode_index = 0 if game_state.game == False else 1  # Check if it is tutorial level or game level
                    game_state.initialize_zone_elements()
                    zone.current_level_set.game_board.fill((30, 30, 30))
                    game_state.new_level = zone.current_level_set.generate_level(game_state, True, mode_index)
                    game_state.player_in_pit = False # Reset player

                    # Initialize momentary_elements AFTER level generation
                    game_state.momentary_elements = [
                        (element, pos)
                        for element, pos, _, _ in zone.current_level_set.elements
                        if element in game_state.zone_tile.state_mapping
                        and isinstance(game_state.zone_tile.state_mapping[element], tuple)
                        and len(game_state.zone_tile.state_mapping[element]) == 4
                        and 'latching' not in game_state.zone_tile.state_mapping[element][3]
                    ]

                    # Fade in effect after resetting the level
                    zone.current_level_set.fade_in(game_state)

                    # Apply flickering effect if lights are out
                    if game_state.lights_out:
                        zone.current_level_set.flicker_effect(game_state)

                # Handle input only if NOT in movement cooldown
                if game_state.debounce_timer == 0:
                    keys = pygame.key.get_pressed()
                    if handle_input(keys, zone.current_level_set, game_state, audio):
                        game_state.debounce_timer = MOVEMENT_DELAY

                else:
                    game_state.debounce_timer -= 1

                # Check level completion
                level_complete = game_state.check_level_complete()

                # Handle level completion
                if level_complete:
                    previous_zone = zone.current_zone_index
                    active_zone = game_state.handle_level_complete(high_scores)

                    # Update the zone reference for the start_menu object when zone.current_zone_index changes
                    if active_zone != previous_zone:
                        start_menu = StartMenu(zone, game_state)

                    if not game_state.is_playing:
                        high_scores.from_start_screen = False  # Set the flag to False
                        high_scores.display_scores()
                        show_start_screen = True

                    # Fade out effect
                    zone.current_level_set.fade_out(game_state)

                if not game_state.player_in_pit and not level_complete:
                    # Set background color
                    zone.current_level_set.game_board.fill((30, 30, 30))

                    game_state.check_momentary_switches()

                    # Render the the game elements
                    zone.current_level_set.blit_level_elements(game_state)
                    zone.current_level_set.blit_box_1(game_state, 0, 0)
                    zone.current_level_set.blit_box_2(game_state, 0, 0)
                    zone.current_level_set.blit_box_3(game_state, 0, 0)
                    zone.current_level_set.blit_box_4(game_state, 0, 0)


                    # Render player with direction
                    if game_state.travel in [1, 2]:
                        zone.current_level_set.blit_player(game_state, game_state.py)
                    elif game_state.travel in [3, 4]:
                        zone.current_level_set.blit_player(game_state, game_state.px)
                    else:
                        zone.current_level_set.blit_player(game_state, 0)

                    # Apply blackout effect if lights are out
                    if game_state.lights_out:
                        zone.current_level_set.apply_blackout(game_state)

                    zone.current_level_set.blit_status_bar(game_state)

                    # Update the display
                    pygame.display.flip()
                    # Cap frame rate
                    clock.tick(FPS)

            # Ensure the start screen is shown after game over
            show_start_screen = True
            game_state.is_playing = True

    pygame.quit()

if __name__ == '__main__':
    main()
