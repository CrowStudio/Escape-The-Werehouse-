from pickle import FALSE
import sys
import logging
import pygame
import subprocess
# from game_board.maps import game_maps, tutorial_maps
from game_board import BoardElements, TileType, TILE_SIZE
from sound import AudioManager
from high_scores import ScoreManager
from start_screen import StartMenu

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize PyGame and audio
try:
    pygame.mixer.pre_init(44100, -16, 1, 2048)
    pygame.init()

    # Create font objects
    tutorial_font = pygame.font.SysFont('Lucida Console', 12)  # Font for tutorial text
    font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
    dead_font = pygame.font.SysFont('Arial Black', 72)  # Biggest font for GAME OVER
except pygame.error as e:
    logger.error(f"Failed to initialize PyGame: {e}")
    sys.exit(1)

# Game constants
FPS = 120
DISTANCE = TILE_SIZE
MOVEMENT_DELAY = 10  # Controls movement speed (higher = slower)
ARROW_KEYS = {pygame.K_UP:    {'direction': 'up',    'travel': 1, 'search': 1},
              pygame.K_DOWN:  {'direction': 'down',  'travel': 2, 'search': 2},
              pygame.K_LEFT:  {'direction': 'left',  'travel': 3, 'search': 3},
              pygame.K_RIGHT: {'direction': 'right', 'travel': 4, 'search': 4}}

# # Creates a list of maps from tutorial_maps and game_maps
# level_map = [tutorial_maps.tutorial_map]
# level_map.append(game_maps.level_map)


class GameState:
    def __init__(self):
        self.game = False  # False == no of initial tutorial levels, True == no of game levels
        self.is_playing = True
        self.new_level = True

        self.current_level = 0
        self.moves = 0
        self.total_moves = 0
        self.lives = 3

        self.debounce_timer = 0  # To avoid unwanted movements
        self.a_key_pressed = False

        self.normal_movement = True
        self.travel = 0  # Only keep track of direction
        self.direction = None
        self.facing_direction = 'up'  # New attribute to track facing direction
        self.is_pulling = False
        self.player_in_pit = False

        self.lights_out = False  # New attribute for lights checkbox
        self.is_searching = False
        self.search = 0
        self.search_speed = 0.4

def check_level_complete(board, game_state):
    # Check if player is on exit tile
    for element in board.elements:
        if element[0] == TileType.EXIT:
            if (board.px, board.py) == element[1]:  # Player position matches exit position
                game_state.travel = 0
                return True

    return False

def handle_input(keys, board, game_state, audio):
    """
    Handle keyboard input for player movement and actions.
    """
    # Reset movement variables for this frame to ensure no residual state affects the current frame
    reset_movement_variables(game_state)

    # Handle pulling action, which is instantaneous and triggered by the spacebar
    game_state.is_pulling = keys[pygame.K_SPACE]

    # Handle searching with WASD keys, which controls the searchlight direction independently of movement
    handle_searching(keys, game_state)

    # Store the current player position to allow rollback if the move is invalid or dangerous
    prev_x, prev_y = board.px, board.py

    # Process arrow key inputs for player movement and direction changes
    if process_arrow_keys(keys, game_state, board):
        # Attempt to move the player and boxes; if successful, increment the move count
        if move_player_and_boxes(board, audio, game_state):
            # Only increment the move count if the player's position has changed
            if (board.px, board.py) != (prev_x, prev_y):
                game_state.moves += 1
                # Add moves to total_moves for high scores
                game_state.total_moves += 1
            return True
        else:
            # Reset player position if the move was invalid or the player fell into a pit
            board.px, board.py = prev_x, prev_y

    return False

def reset_movement_variables(game_state):
    """
    Reset the game state variables related to movement at the start of each frame.
    """
    game_state.direction = None  # Reset the movement direction
    game_state.travel = 0  # Reset the travel distance

def handle_searching(keys, game_state):
    """
    Handle the searching action using WASD keys, which controls the searchlight direction.
    """
    # Check each WASD key and set the search direction accordingly
    if keys[pygame.K_w]:
        set_search_direction(game_state, 1)  # Search up
    elif keys[pygame.K_s]:
        set_search_direction(game_state, 2)  # Search down
    elif keys[pygame.K_a]:
        set_search_direction(game_state, 3)  # Search left
    elif keys[pygame.K_d]:
        set_search_direction(game_state, 4)  # Search right
    else:
        game_state.search_speed = 0.4
        game_state.is_searching = False  # No searching if no WASD key is pressed

def set_search_direction(game_state, direction):
    """
    Set the search direction and activate searching mode.
    """
    game_state.search_speed = 0.1
    game_state.search = direction  # Set the search direction
    game_state.is_searching = True  # Activate searching mode

def process_arrow_keys(keys, game_state, board):
    """
    Process arrow key inputs for player movement and direction changes.
    """
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

def handle_movement(game_state, movement):
    """
    Handle the movement logic based on the current game state and movement input.
    """
    if game_state.normal_movement:
        # Handle normal movement when the player is allowed to move up
        handle_normal_movement(game_state, movement)
    else:
        # Handle alternative movement, such as rotating or moving in the facing direction
        handle_alternative_movement(game_state, movement)

def handle_normal_movement(game_state, movement):
    """
    Handle normal movement when the player is moving up.
    """
    if game_state.lights_out and not game_state.is_pulling:
        # Handle movement when the lights are out, affecting visibility and direction
        handle_lights_out_movement(game_state, movement)
    elif game_state.is_pulling:
        # If pulling, set the movement direction
        set_movement_direction(game_state, movement)
    else:
        # Normal movement without pulling or lights out
        set_movement_direction(game_state, movement)

def handle_lights_out_movement(game_state, movement):
    """
    Handle movement logic when the lights are out, affecting visibility.
    """
    if game_state.facing_direction == movement['direction']:
        # Move in the facing direction if already aligned
        set_movement_direction(game_state, movement)
    else:
        # Update the facing direction and set searching properties if not aligned
        update_facing_direction(game_state, movement)

def set_movement_direction(game_state, movement):
    """
    Set the movement direction and travel distance based on the movement input.
    """
    game_state.direction = movement['direction']  # Set the movement direction
    game_state.travel = movement['travel']  # Set the travel distance

def update_facing_direction(game_state, movement):
    """
    Update the player's facing direction and set searching properties.
    """
    game_state.facing_direction = movement['direction']  # Update the facing direction
    game_state.search = movement['search']  # Set the search direction
    game_state.is_searching = True  # Activate searching mode

def handle_alternative_movement(game_state, movement):
    """
    Handle alternative movement logic, such as rotating or moving in the facing direction.
    """
    if movement['direction'] == 'left':
        # Rotate the facing direction counter-clockwise
        rotate_facing_direction(game_state, counter_clockwise=True)
    elif movement['direction'] == 'right':
        # Rotate the facing direction clockwise
        rotate_facing_direction(game_state, counter_clockwise=False)
    elif movement['direction'] in ['up', 'down']:
        # Move in the current facing direction
        move_in_facing_direction(game_state, movement)

def rotate_facing_direction(game_state, counter_clockwise):
    """
    Rotate the player's facing direction clockwise or counter-clockwise.
    """
    directions = ['up', 'right', 'down', 'left']  # List of possible directions
    current_index = directions.index(game_state.facing_direction)  # Find the current direction index
    if counter_clockwise:
        current_index = (current_index - 1) % 4  # Rotate counter-clockwise
    else:
        current_index = (current_index + 1) % 4  # Rotate clockwise
    game_state.facing_direction = directions[current_index]  # Update the facing direction

def move_in_facing_direction(game_state, movement):
    """
    Move the player in the current facing direction based on the movement input.
    """
    # Map the movement direction to the facing direction
    direction_map = {
        'up': {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'},
        'down': {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    }
    game_state.direction = direction_map[movement['direction']][game_state.facing_direction]  # Set the movement direction
    game_state.travel = movement['travel']  # Set the travel distance

# Handle actions when a level is completed
def handle_level_complete(board, game_board, game_state, screen, high_scores):
    # Render one last frame with player on exit
    screen.fill((30, 30, 30))
    board.blit_level(screen)
    board.blit_box_1(screen, 0, 0)
    board.blit_box_2(screen, 0, 0)
    board.blit_box_3(screen, 0, 0)
    board.blit_box_4(screen, 0, 0)
    board.blit_player(screen, game_state, 0)

    # Show score for completed level
    if game_state.game:
        pygame.display.set_caption(f'Escape the Werehouse!')

        # Draw the status bar at the top
        bar_rect = pygame.Rect(0, board.offset_y - board.offset_y, screen.get_width(), board.offset_y)
        pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar

        # Render the text inside the bar
        moves_text = font.render(f'Moves: {game_state.moves}', True, (255, 255, 255))
        total_moves_text = font.render(f'Total Moves: {game_state.total_moves}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {game_state.lives}', True, (255, 255, 255))
        game_board.blit(moves_text, (10, 10))
        game_board.blit(total_moves_text, (200, 10))
        game_board.blit(lives_text, (480, 10))

        # Blit stars
        board.blit_stars(screen, game_state)

    pygame.display.flip()
    pygame.time.wait(300)

    # Increment level counter
    game_state.current_level += 1
    game_state.moves = 0
    game_state.new_level = True

    # Handle mode transitions
    if game_state.game == False and game_state.current_level >= 4:
        # Debug statement
        print('Well done, you finished the Tutorials! Now try to Escape the Werehouse!')
        # Set game states
        game_state.game = True
        game_state.current_level = 0
        game_state.moves = 0
        game_state.total_moves = 0
        game_state.lives = 3
    elif game_state.game == True and game_state.current_level >= board.no_of_levels[1]:
        # Debug statements
        print('Congratulations! You finished the last level!')
        print(f'Your have made a total of {game_state.total_moves} successful moves!')
        # End game
        game_state.is_playing = False
        if high_scores.is_high_score(game_state.total_moves):
            initials = high_scores.get_initials(pygame.display.get_surface())
            high_scores.add_score(game_state.total_moves, initials)

        print("Displaying high scores...")  # Debug statement
        high_scores.display_scores(pygame.display.get_surface())

# Handle movement of player and associated boxes
def move_player_and_boxes(board, audio, game_state):
    # Get current position
    x = board.px
    y = board.py
    new_x, new_y = x, y

    # Calculate target position (exactly one tile)
    if game_state.direction == 'up':
        new_y = y - 100  # Move exactly one tile up
    elif game_state.direction == 'down':
        new_y = y + 100  # Move exactly one tile down
    elif game_state.direction == 'left':
        new_x = x - 100  # Move exactly one tile left
    elif game_state.direction == 'right':
        new_x = x + 100  # Move exactly one tile right

    # First check if the move is valid
    if not is_valid_move(board, new_x, new_y, game_state):
        return False  # Don't move if invalid

    # Handle box movement
    if game_state.is_pulling:
        # Calculate position behind player
        behind_x = x + (x - new_x)
        behind_y = y + (y - new_y)

        # Check for box behind player and move it to current player position first
        if (behind_x, behind_y) == (board.b1x, board.b1y) and board.box1:
            board.b1x, board.b1y = x, y  # Move box to current player position
            check_box_in_pit(board, 1, x, y)
            audio.play_sound('move')
        elif (behind_x, behind_y) == (board.b2x, board.b2y) and board.box2:
            board.b2x, board.b2y = x, y  # Move box to current player position
            check_box_in_pit(board, 2, x, y)
            audio.play_sound('move')
        elif (behind_x, behind_y) == (board.b3x, board.b3y) and board.box3:
            board.b3x, board.b3y = x, y  # Move box to current player position
            check_box_in_pit(board, 3, x, y)
            audio.play_sound('move')
        elif (behind_x, behind_y) == (board.b4x, board.b4y) and board.box4:
            board.b4x, board.b4y = x, y  # Move box to current player position
            check_box_in_pit(board, 4, x, y)
            audio.play_sound('move')
    else:
        # Handle pushing boxes
        if (new_x, new_y) == (board.b1x, board.b1y) and board.box1:
            board.b1x = new_x + (new_x - x)
            board.b1y = new_y + (new_y - y)
            if check_box_in_pit(board, 1, board.b1x, board.b1y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')
        elif (new_x, new_y) == (board.b2x, board.b2y) and board.box2:
            board.b2x = new_x + (new_x - x)
            board.b2y = new_y + (new_y - y)
            if check_box_in_pit(board, 2, board.b2x, board.b2y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')
        elif (new_x, new_y) == (board.b3x, board.b3y) and board.box3:
            board.b3x = new_x + (new_x - x)
            board.b3y = new_y + (new_y - y)
            if check_box_in_pit(board, 3, board.b3x, board.b3y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')
        elif (new_x, new_y) == (board.b4x, board.b4y) and board.box4:
            board.b4x = new_x + (new_x - x)
            board.b4y = new_y + (new_y - y)
            if check_box_in_pit(board, 4, board.b4x, board.b4y):
                audio.play_sound('fall')
            else:
                audio.play_sound('move')

    # Check if player falls into pit
    if check_player_in_pit(board, game_state, new_x, new_y, audio):
        return False  # Movement was valid but player fell

    # Move player to new position
    board.px = new_x
    board.py = new_y

    return True

# Check if a box has fallen into a pit and update states accordingly
def check_box_in_pit(board, box_num, x, y):
    # Mapping of pit types to their corresponding attributes
    pit_mapping = {
        TileType.PIT1: ('pit1', 'in_pit1'),
        TileType.PIT2: ('pit2', 'in_pit2'),
        TileType.PIT3: ('pit3', 'in_pit3'),
        TileType.PIT4: ('pit4', 'in_pit4'),
    }

    # Iterate over the elements on the board
    for element in board.elements:
        position, pit_type = element[1], element[0]

        # Check if the current element is a pit and matches the given coordinates
        if position == (x, y) and pit_type in pit_mapping:
            pit_attr, in_pit_attr = pit_mapping[pit_type]

            # Only proceed if the pit is active
            if getattr(board, pit_attr):
                # Deactivate the pit and set the box number in the pit
                setattr(board, pit_attr, False)
                setattr(board, in_pit_attr, box_num)
                print(f"Box {box_num} fell into pit {pit_type}")  # Debug statement

                if box_num == 1:
                    board.box1 = False
                elif box_num == 2:
                    board.box2 = False
                elif box_num == 3:
                    board.box3 = False
                elif box_num == 4:
                    board.box4 = False
                return True

            return False

# Check if move is valid
def is_valid_move(board, new_x, new_y, game_state):
    if new_x < 0 or new_x >= 600 or new_y < 0 or new_y >= 600:
        return False

    # Check if the target position contains a valid tile
    valid_move = False
    for element in board.elements:
        if element[1] == (new_x, new_y):
            # Check for valid tiles including EXIT and PITS
            if element[0] == TileType.EXIT and board.exit:  # Allow exit only if active
                valid_move = True
                break
            elif element[0] == TileType.START or element[0] == TileType.FLOOR:
                valid_move = True
                break
            elif element[0] == TileType.PIT1 and (not board.pit1 or not game_state.is_pulling):
                valid_move = True  # Allow movement onto pit if not pulling  or pit is filled
                break
            elif element[0] == TileType.PIT2 and (not board.pit2 or not game_state.is_pulling):
                valid_move = True
                break
            elif element[0] == TileType.PIT3 and (not board.pit3 or not game_state.is_pulling):
                valid_move = True
                break
            elif element[0] == TileType.PIT4 and (not board.pit4 or not game_state.is_pulling):
                valid_move = True
                break
            elif element[0] in [TileType.WALL, TileType.PIT_WALL]:
                return False

    if not valid_move:
        return False

    # Get active box positions
    box_positions = []
    if board.box1: box_positions.append((board.b1x, board.b1y))
    if board.box2: box_positions.append((board.b2x, board.b2y))
    if board.box3: box_positions.append((board.b3x, board.b3y))
    if board.box4: box_positions.append((board.b4x, board.b4y))

    # Calculate position behind player
    behind_x = board.px + (board.px - new_x)
    behind_y = board.py + (board.py - new_y)

    if game_state.is_pulling:
        # Check for box behind player
        box_behind = False
        for box_pos in box_positions:
            if box_pos == (behind_x, behind_y):
                box_behind = True
                break

        # If no box behind when pulling, check if we're trying to walk over a box
        if not box_behind:
            for box_pos in box_positions:
                if box_pos == (new_x, new_y):
                    return False  # Can't walk over box while holding space
            return True

        # Check if target position is blocked by another box
        for box_pos in box_positions:
            if box_pos == (new_x, new_y):
                return False
    else:
        # Handle pushing boxes
        box_at_target = False
        for box_pos in box_positions:
            if box_pos == (new_x, new_y):
                box_at_target = True
                break

        if box_at_target:
            # Rest of pushing validation...
            push_x = new_x + (new_x - board.px)
            push_y = new_y + (new_y - board.py)

            # Check if push position is valid
            push_valid = False
            for element in board.elements:
                if element[1] == (push_x, push_y):
                    if element[0] in [TileType.START, TileType.FLOOR, TileType.EXIT,
                                    TileType.PIT1, TileType.PIT2, TileType.PIT3, TileType.PIT4]:
                        push_valid = True
                    elif element[0] in [TileType.WALL, TileType.PIT_WALL]:
                        return False

            if not push_valid:
                return False

            # Check if pushing into another box
            for box_pos in box_positions:
                if box_pos == (push_x, push_y):
                    return False

    return True

def check_player_in_pit(board, game_state, x, y, audio):
    if game_state.player_in_pit:
        return False

    for element in board.elements:
        if element[1] == (x, y):
            if element[0] in [TileType.PIT1, TileType.PIT2, TileType.PIT3, TileType.PIT4]:
                # Check if pit is not filled (active)
                if ((element[0] == TileType.PIT1 and board.pit1) or
                    (element[0] == TileType.PIT2 and board.pit2) or
                    (element[0] == TileType.PIT3 and board.pit3) or
                    (element[0] == TileType.PIT4 and board.pit4)):
                    # Player fell in pit
                    audio.play_sound('fall')
                    game_state.lives -= 1
                    game_state.player_in_pit = True

                    # Update player position to the pit
                    board.px, board.py = x, y

                    # Blit the game board and boxes
                    screen = pygame.display.get_surface()
                    screen.fill((30, 30, 30))
                    board.blit_level(screen)
                    board.blit_box_1(screen, 0, 0)
                    board.blit_box_2(screen, 0, 0)
                    board.blit_box_3(screen, 0, 0)
                    board.blit_box_4(screen, 0, 0)

                    # Debug statement to check player position
                    print(f"Blitting player at pit position: ({board.px}, {board.py})")

                    # Reset player movement
                    game_state.travel = 0

                    # Blit the player on the pit tile
                    board.blit_player(screen, game_state, 0)
                    pygame.display.flip()

                    # Fade out effect
                    board.fade_out(game_state, screen, board.game_board_x, (board.game_board_y + board.offset_y))

                    if game_state.lives <= 0:
                        display_game_over(game_state)
                        game_state.is_playing = False
                    else:
                        # Reset level
                        game_state.new_level = True
                        game_state.total_moves += game_state.moves
                        game_state.moves = 0

                        return False

                    return True
    return False

# Show GAME OVER screen when out of lives
def display_game_over(game_state):
    screen = pygame.display.get_surface()
    # Clear the screen
    screen.fill((10, 10, 10))
    pygame.display.set_caption('GAME OVER')
    # Render "GAME OVER" text
    game_over_text = dead_font.render('GAME OVER', True, (220, 0, 10))
    game_over_center = game_over_text.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(game_over_text, game_over_center)

    # Update the display
    pygame.display.flip()

    # Wait for a few seconds before returning to the start screen
    pygame.time.wait(3000)

def main():
    # Initialize game components
    game_state = GameState()
    board = BoardElements()
    audio = AudioManager()
    high_scores = ScoreManager()
    screen = pygame.display.set_mode((600, 640))  # Set the screen size to 600x640
    start_menu = StartMenu(screen, game_state, high_scores, board)

    clock = pygame.time.Clock()
    show_start_screen = True

    # # Update the game board size based on the current level
    # mode_index = 0 if game_state.game == False else 1
    # board.update_game_board_size(level_map[mode_index][game_state.current_level])

    while True:
        if show_start_screen:
            start_menu.draw()
            action = start_menu.handle_events()
            if action == 'start_game':
                show_start_screen = False
            elif action == 'show_high_scores':
                # Set to True to enable Back button
                high_scores.from_start_screen = True
                high_scores.display_scores(screen)
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
            # Set up game board
            game_board = pygame.display.set_mode((board.game_board_x, board.game_board_y + board.offset_y))  # Adjust the height
            game_state.new_level = True  # Reset level to start from the selected one


            # Main game loop
            while game_state.is_playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_state.is_playing = False
                        show_start_screen = True

                # Generate new level if needed
                if game_state.new_level:
                    board.lv = game_state.current_level
                    mode_index = 0 if game_state.game == False else 1
                    game_state.new_level = board.generate_level(game_board, game_state, True, mode_index)

                    game_board.fill((30, 30, 30))
                    # Fade in effect after resetting the level
                    board.fade_in(screen, board.game_board_x, (board.game_board_y + board.offset_y), board, game_state)

                    # Apply flickering effect if lights are off
                    if game_state.lights_out:
                        board.flicker_effect(game_board, game_state, board, screen)

                    game_state.player_in_pit = False

                # Handle input only if not in movement cooldown
                if game_state.debounce_timer == 0:
                    keys = pygame.key.get_pressed()
                    if handle_input(keys, board, game_state, audio):
                        game_state.debounce_timer = MOVEMENT_DELAY

                else:
                    game_state.debounce_timer -= 1

                # Check level completion
                if check_level_complete(board, game_state):
                    handle_level_complete(board, game_board, game_state, screen, high_scores)
                    if not game_state.is_playing:
                        high_scores.from_start_screen = False  # Set the flag to False
                        high_scores.display_scores(screen)
                        show_start_screen = True

                    # Fade out effect
                    board.fade_out(game_state, screen, board.game_board_x, (board.game_board_y + board.offset_y))

                if not game_state.player_in_pit and not check_level_complete(board, game_state):
                    # Set background color
                    game_board.fill((30, 30, 30))

                    # Render the rest of the game elements
                    board.blit_level(game_board)
                    board.blit_box_1(game_board, 0, 0)
                    board.blit_box_2(game_board, 0, 0)
                    board.blit_box_3(game_board, 0, 0)
                    board.blit_box_4(game_board, 0, 0)

                    # Render player with direction
                    if game_state.travel in [1, 2]:
                        board.blit_player(game_board, game_state, board.py)
                    elif game_state.travel in [3, 4]:
                        board.blit_player(game_board, game_state, board.px)
                    else:
                        board.blit_player(game_board, game_state, 0)

                    # Apply blackout effect
                    board.apply_blackout(game_board, game_state)

                    # Draw the status bar at the top
                    bar_rect = pygame.Rect(0, board.offset_y - board.offset_y, screen.get_width(), board.offset_y)
                    pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar

                    # Set caption and render the text inside the status bar
                    if game_state.game and game_state.is_playing:
                        # Set window caption
                        pygame.display.set_caption(f'Escape the Werehouse! - {board.map_title[1][game_state.current_level]}')
                        # Set status bar
                        moves_text = font.render(f'Moves: {game_state.moves}', True, (255, 255, 255))
                        total_moves_text = font.render(f'Total Moves: {game_state.total_moves}', True, (255, 255, 255))
                        lives_text = font.render(f'Lives: {game_state.lives}', True, (255, 255, 255))
                        # Render status bar
                        game_board.blit(moves_text, (10, 10))
                        game_board.blit(total_moves_text, (200, 10))
                        game_board.blit(lives_text, (480, 10))
                    elif game_state.is_playing:
                        # Set window caption
                        pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {game_state.current_level + 1}')
                        # Set status bar
                        tutorial_text = tutorial_font.render(f'{board.map_title[0][game_state.current_level]}', True, (255, 255, 255))
                        # Render status bar
                        game_board.blit(tutorial_text, (15, 15))

                    pygame.display.flip()
                    # Cap frame rate
                    clock.tick(FPS)

            # Ensure the start screen is shown after game over
            show_start_screen = True
            game_state.is_playing = True

    pygame.quit()

if __name__ == '__main__':
    main()
