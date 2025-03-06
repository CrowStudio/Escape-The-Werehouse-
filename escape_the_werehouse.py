from ast import If
import sys
import os
import logging
import pygame
# from game_board.maps import game_maps, tutorial_maps
from game_board import BoardElements, TileType, TILE_SIZE

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize PyGame and audio
try:
    pygame.mixer.pre_init(44100, -16, 1, 2048)
    pygame.init()
    # Create a font object using a system font
    font = pygame.font.SysFont('Lucida Console', 36)  # Used for High Scores

except pygame.error as e:
    logger.error(f"Failed to initialize PyGame: {e}")
    sys.exit(1)

# Game constants
ANIMATION_SPEED = 17
DISTANCE = TILE_SIZE
MOVEMENT_DELAY = 10  # Controls movement speed (higher = slower)

# # Creates a list of maps from tutorial_maps and game_maps
# level_map = [tutorial_maps.tutorial_map]
# level_map.append(game_maps.level_map)

# Audio setup
class AudioManager:
    def __init__(self):
        try:
            self.channels = {
                'movement': pygame.mixer.Channel(0),
                'effects': pygame.mixer.Channel(1),
                'ambient1': pygame.mixer.Channel(2),
                'ambient2': pygame.mixer.Channel(3)
            }
            self.sounds = {
                'move': pygame.mixer.Sound('sound/moving.wav'),
                'fall': pygame.mixer.Sound('sound/fall_in_pit.wav')
            }
        except (pygame.error, FileNotFoundError) as e:
            logger.error(f"Failed to load audio: {e}")
            self.sounds = {}
            self.channels = {}

    def play_sound(self, sound_name):
        if not self.sounds or not self.channels:
            return
            
        try:
            channel = self.channels['effects']
            if sound_name == 'move':
                channel = self.channels['movement']
                
            channel.play(self.sounds[sound_name])
            channel.set_volume(1.0)
            channel.fadeout(450)

        except (KeyError, pygame.error) as e:
            logger.warning(f"Failed to play sound {sound_name}: {e}")

class HighScores:
    def __init__(self):
        self.scores = self.load_scores()

    def add_score(self, score, initials):
        self.scores.append((score, initials))
        self.scores = sorted(self.scores, key=lambda x: x[0])[:3]  # Keep only top 3
        self.save_scores()

    def is_high_score(self, score):
        return score <= max(self.scores)[0]

    def display_scores(self, screen):
        screen.fill((30, 30, 30))

        # Render the title
        title_text = font.render('High Scores', True, (255, 255, 255))
        title_center = title_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_text, title_center)

        # Determine the maximum score length for alignment
        max_score_length = max(len(str(score)) for score, _ in self.scores)

        # Render each score entry with alignment
        for i, (score, initials) in enumerate(self.scores, start=1):
            score_str = f'{i}. {str(score).rjust(max_score_length)} {initials}'
            score_text = font.render(score_str, True, (255, 255, 255))
            score_center = score_text.get_rect(center=(screen.get_width() // 2, 50 + i * 50))
            screen.blit(score_text, score_center)

        pygame.display.flip()

    def get_initials(self, screen):
        input_box = pygame.Rect(0, 0, 140, 32)
        input_box.center = (screen.get_width() // 2, 100)
        color = pygame.Color('white')
        active = True
        text = ''
        done = False

        prompt_text = font.render('Enter your initials:', True, (255, 255, 255))
        prompt_center = prompt_text.get_rect(center=(screen.get_width() // 2, 50))

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if len(text) < 3:
                                text += event.unicode.upper()

            screen.fill((30, 30, 30))
            screen.blit(prompt_text, prompt_center)
            txt_surface = font.render(text, True, color)
            text_center = txt_surface.get_rect(center=input_box.center)
            screen.blit(txt_surface, text_center)

            pygame.display.flip()

        return text


    def load_scores(self):
        try:
            if os.path.exists('high_scores.py'):
                with open('high_scores.py', 'r') as file:
                    content = file.read()
                    # Extract scores from the file content
                    scores = eval(content.split('=')[1])
                    return scores
        except Exception as e:
            print(f"Error loading scores: {e}")

        # Return default scores if loading fails
        return [(float('inf'), 'AAA')] * 3

    def save_scores(self):
        with open('high_scores.py', 'w') as file:
            file.write(f'SCORES = {self.scores}')


class GameState:
    def __init__(self):
        self.game = False  # False == 4 initial tutorial levels, True = 5 game levels

        self.current_level = 0
        self.moves = 0
        self.retries = 3

        self.is_playing = True
        self.new_level = True
        self.total_moves = 0

        self.debounce_timer = 0 # To avoid unvanted movements
        self.travel = 0  # Only keep track of direction

def main():
    # Initialize game components
    game_state = GameState()
    board = BoardElements()
    audio = AudioManager()
    high_scores = HighScores()

    # # Update the game board size based on the current level
    # mode_index = 0 if game_state.game == False else 1
    # board.update_game_board_size(level_map[mode_index][game_state.current_level])

    # Set up game board
    game_board = pygame.display.set_mode((board.game_board_x, board.game_board_y))

    # Main game loop
    clock = pygame.time.Clock()
    while game_state.is_playing:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.is_playing = False

        # Generate new level if needed
        if game_state.new_level:
            board.lv = game_state.current_level  # Set level index before generating
            mode_index = 0 if game_state.game == False else 1
            game_state.new_level = board.generate_level(game_board, True, mode_index)

        # Handle input only if not in movement cooldown
        if game_state.debounce_timer == 0:
            keys = pygame.key.get_pressed()
            if handle_input(keys, board, game_state, audio):
                game_state.debounce_timer = MOVEMENT_DELAY
        else:
            game_state.debounce_timer -= 1

        # Check level completion
        if check_level_complete(board, game_state):
            handle_level_complete(board, game_state, high_scores)

        # Set background color
        game_board.fill((30, 30, 30))

        # Render current level
        board.blit_level(game_board)

        # Render boxes
        board.blit_box_1(game_board, 0, 0)
        board.blit_box_2(game_board, 0, 0)
        board.blit_box_3(game_board, 0, 0)
        board.blit_box_4(game_board, 0, 0)

        # Render player with direction
        if game_state.travel in [1, 2]:  # Up or Down
            board.blit_player(game_board, game_state.travel, board.py)
        elif game_state.travel in [3, 4]:  # Left or Right
            board.blit_player(game_board, game_state.travel, board.px)
        else:
            board.blit_player(game_board, 0, 0)  # No movement

        if game_state.game:
            pygame.display.set_caption(f'Escape the Werehouse!                 Moves: {game_state.moves}                 Retries: {game_state.retries}     ')

        else:
            pygame.display.set_caption(f'{board.titel[game_state.current_level]}')

        pygame.display.flip()

        # Cap frame rate
        clock.tick(60)

    pygame.quit()

def check_level_complete(board, game_state):
    """Check if current level is complete"""
    # Check if exit is active
    if not board.exit:
        return False

    # Check if player is on exit tile
    for element in board.elements:
        if element[0] == TileType.EXIT:  # Exit tile
            if (board.px, board.py) == element[1]:  # Player position matches exit position
                # Render one last frame with player on exit
                pygame.display.get_surface().fill((30, 30, 30))
                board.blit_level(pygame.display.get_surface())
                board.blit_box_1(pygame.display.get_surface(), 0, 0)
                board.blit_box_2(pygame.display.get_surface(), 0, 0)
                board.blit_box_3(pygame.display.get_surface(), 0, 0)
                board.blit_box_4(pygame.display.get_surface(), 0, 0)
                board.blit_player(pygame.display.get_surface(), 0, 0)  # Show player on exit

                # Show score for completed level
                if game_state.game:
                    pygame.display.set_caption(f'Escape the Werehouse!                 Moves: {game_state.moves}                 Retries: {game_state.retries}     ')
                    board.blit_stars(pygame.display.get_surface(), game_state.moves)
                    # Add moves to total_moves for high scores
                    game_state.total_moves += game_state.moves

                pygame.display.flip()
                pygame.time.wait(500)  # Wait half a second to show player on exit

                return True

    return False

def handle_input(keys, board, game_state, audio):
    """Handles keyboard input"""
    direction = None
    is_dragging = keys[pygame.K_SPACE]

    # Store previous position for validation
    prev_x = board.px
    prev_y = board.py

    if keys[pygame.K_UP]:
        direction = 'up'
        game_state.travel = 1
    elif keys[pygame.K_DOWN]:
        direction = 'down'
        game_state.travel = 2
    elif keys[pygame.K_LEFT]:
        direction = 'left'
        game_state.travel = 3
    elif keys[pygame.K_RIGHT]:
        direction = 'right'
        game_state.travel = 4
    else:
        game_state.travel = 0

    if direction:
        if move_player_and_boxes(board, direction, game_state.travel, is_dragging, audio, game_state):
            game_state.moves += 1
            return True
        else:
            # Reset position if move was invalid or player fell
            board.px = prev_x
            board.py = prev_y
    return False


def handle_level_complete(board, game_state, high_scores):
    """Handles level completion"""
    game_state.moves = 0
    game_state.new_level = True

    # Increment level counter
    game_state.current_level += 1

    # Handle mode transitions
    if game_state.game == False and game_state.current_level >= 4:
        game_state.game = True
        game_state.current_level = 0
        print('Well done, you finished the Tutorials! Now try to Escape the Werehouse!') # Debug statement
    elif game_state.game == True and game_state.current_level >= 5:
        game_state.is_playing = False
        print('Congratulations! You finished the last level!')  # Debug statement

        if high_scores.is_high_score(game_state.total_moves):
            initials = high_scores.get_initials(pygame.display.get_surface())
            high_scores.add_score(game_state.total_moves, initials)

        print("Displaying high scores...")  # Debug statement
        high_scores.display_scores(pygame.display.get_surface())
        pygame.time.wait(5000)  # Display high scores for 5 seconds


def move_player_and_boxes(board, direction, travel, is_dragging, audio, game_state):
    """Handles movement of player and associated boxes"""
    # Get current position
    x = board.px
    y = board.py
    new_x, new_y = x, y

    # Calculate target position (exactly one tile)
    if direction == 'up':
        new_y = y - 100  # Move exactly one tile up
    elif direction == 'down':
        new_y = y + 100  # Move exactly one tile down
    elif direction == 'left':
        new_x = x - 100  # Move exactly one tile left
    elif direction == 'right':
        new_x = x + 100  # Move exactly one tile right

    # First check if the move is valid
    if not is_valid_move(board, new_x, new_y, direction, is_dragging):
        return False  # Don't move if invalid

    # Handle box movement
    if is_dragging:
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

    # Move player to new position
    board.px = new_x
    board.py = new_y

    # Check if player falls into pit
    if check_player_in_pit(board, game_state, new_x, new_y, audio):
        return False  # Movement was valid but player fell

    return True

def check_box_in_pit(board, box_num, x, y):
    """Check if a box has fallen into a pit and update states accordingly."""
    # Mapping of pit types to board attribute names
    pit_mapping = {
        TileType.PIT1: ('pit1', 'in_pit1'),
        TileType.PIT2: ('pit2', 'in_pit2'),
        TileType.PIT3: ('pit3', 'in_pit3'),
        TileType.PIT4: ('pit4', 'in_pit4'),
    }

    for element in board.elements:
        if element[1] == (x, y):
            pit_type = element[0]
            if pit_type in pit_mapping:
                pit_attr, in_pit_attr = pit_mapping[pit_type]
                # Only proceed if the pit is active
                if getattr(board, pit_attr):
                    setattr(board, pit_attr, False)       # Deactivate pit
                    setattr(board, in_pit_attr, box_num)  # Store box number

                    # Set the corresponding box status to False
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

def is_valid_move(board, new_x, new_y, direction, is_dragging):
    """Check if move is valid"""
    # Check board boundaries
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
            elif element[0] == TileType.PIT1 and (not board.pit1 or not is_dragging):
                valid_move = True  # Allow movement onto pit if not dragging or pit is filled
                break
            elif element[0] == TileType.PIT2 and (not board.pit2 or not is_dragging):
                valid_move = True
                break
            elif element[0] == TileType.PIT3 and (not board.pit3 or not is_dragging):
                valid_move = True
                break
            elif element[0] == TileType.PIT4 and (not board.pit4 or not is_dragging):
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

    if is_dragging:
        # Check for box behind player
        box_behind = False
        for box_pos in box_positions:
            if box_pos == (behind_x, behind_y):
                box_behind = True
                break

        # If no box behind to drag, check if we're trying to walk over a box
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
    """Check if player has fallen into a pit"""
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
                    game_state.retries -= 1
                    if game_state.retries <= 0:
                        game_state.is_playing = False
                    else:
                        # Reset level
                        game_state.new_level = True
                        game_state.moves = 0
                    return True
    return False

if __name__ == '__main__':
    main()