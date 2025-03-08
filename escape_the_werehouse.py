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
    # Create font objects
    font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
    dropdown_font = pygame.font.SysFont('Lucida Console', 20)  # Smaller font for dropdown
    hig_score_font = pygame.font.SysFont('Arial Black', 32)  # Bigger font for High Scores
    menu_font = pygame.font.SysFont('Arial Black', 42)  # Even bigger font for START MENU
    dead_font = pygame.font.SysFont('Arial Black', 72)  # Biggest font for GAME OVER
except pygame.error as e:
    logger.error(f"Failed to initialize PyGame: {e}")
    sys.exit(1)

# Game constants
ANIMATION_SPEED = 17
DISTANCE = TILE_SIZE
MOVEMENT_DELAY = 10 # Controls movement speed (higher = slower)

# # Creates a list of maps from tutorial_maps and game_maps
# level_map = [tutorial_maps.tutorial_map]
# level_map.append(game_maps.level_map)

# Audio setup
class AudioManager:
    def __init__(self):
        try:
            # Initialize audio channels and sounds
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

    # Play the specified sound if channels and sounds are available
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
        self.latest_score = None  # Track the latest added score
        self.from_start_screen = False  # Initialize the flag

    # Add a new score to the list and sort
    def add_score(self, score, initials):
        self.scores.append((score, initials))
        self.scores = sorted(self.scores, key=lambda x: x[0])[:3]  # Keep only top 3
        self.latest_score = (score, initials)  # Update the latest score
        self.save_scores()

    # Check if the score is a high score
    def is_high_score(self, score):
        return score <= max(self.scores)[0]

    # Display the high scores on the screen
    def display_scores(self, screen):
        screen.fill((30, 30, 30))

        # Render the title
        pygame.display.set_caption(f'High Scores')
        title_text = hig_score_font.render('High Scores', True, (255, 215, 115))
        title_center = title_text.get_rect(center=(screen.get_width() // 2, 120))
        screen.blit(title_text, title_center)

        # Determine the maximum score length for alignment
        max_score_length = max(len(str(score)) for score, _ in self.scores)

        # Render each score entry with alignment
        for i, (score, initials) in enumerate(self.scores, start=1):
            score_str = f'{i}. {str(score).rjust(max_score_length)} {initials}'

            # Highlight the latest added score by rendering text twice with an offset
            if self.latest_score and self.latest_score == (score, initials):
                bold_text = font.render(score_str, True, (255, 215, 0))  # Gold color for highlight
                bold_center = bold_text.get_rect(center=(screen.get_width() // 2 + 1, 120 + i * 50 + 1))
                screen.blit(bold_text, bold_center)

            score_text = font.render(score_str, True, (255, 255, 255))
            score_center = score_text.get_rect(center=(screen.get_width() // 2, 120 + i * 50))
            screen.blit(score_text, score_center)

        # Only show Back button if comming from start screen
        if self.from_start_screen:
            back_button = pygame.Rect(200, 540, 200, 40)  # Adjusted back button position
            pygame.draw.rect(screen, (255, 255, 255), back_button, 2)
            back_text = font.render('Back', True, (255, 255, 255))
            back_text_center = back_text.get_rect(center=(screen.get_width() // 2, 560))
            screen.blit(back_text, back_text_center)

        pygame.display.flip()


    # Input box for entering initials after achieving a high score
    def get_initials(self, screen):
        input_box = pygame.Rect(0, 0, 140, 32)
        input_box.center = (screen.get_width() // 2, 120)
        color = pygame.Color('gold')
        active = True
        text = ''
        done = False

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
            # Show celebration text
            celebration_text = font.render('Congratulations!', True, (255, 255, 255))
            celebration_center = celebration_text.get_rect(center=(screen.get_width() // 2, 30))
            screen.blit(celebration_text, celebration_center)
            three_text = font.render('You made it to the top three!', True, (255, 255, 255))
            three_center = three_text.get_rect(center=(screen.get_width() // 2, 60))
            screen.blit(three_text, three_center)

            # Show prompt text
            prompt_text = font.render('Enter your initials:', True, (255, 255, 255))
            prompt_center = prompt_text.get_rect(center=(screen.get_width() // 2, 90))
            screen.blit(prompt_text, prompt_center)

            # Blit input text
            txt_surface = font.render(text, True, color)
            text_center = txt_surface.get_rect(center=input_box.center)
            screen.blit(txt_surface, text_center)

            pygame.display.flip()

        return text

    # Load scores from a file, create the file if it doesn't exist
    def load_scores(self):
        if not os.path.exists('high_scores.py'):
            with open('high_scores.py', 'w') as file:
                file.write('SCORES = [(100, \'who\'), (200, \'are\'), (300, \'you\')]')

        try:
            with open('high_scores.py', 'r') as file:
                content = file.read()
                # Extract scores from the file content
                scores = eval(content.split('=')[1])
                return scores
        except Exception as e:
            print(f"Error loading scores: {e}")

        # Return default scores if loading fails
        return [(100, 'who'), (200, 'are'), (300, 'you')]

    # Save the current scores to a file
    def save_scores(self):
        with open('high_scores.py', 'w') as file:
            file.write(f'SCORES = {self.scores}')

class GameState:
    def __init__(self):
        self.game = False  # False == 4 initial tutorial levels, True == 5 game levels

        self.current_level = 0
        self.moves = 0
        self.lives = 3

        self.is_playing = True
        self.new_level = True
        self.total_moves = 0

        self.debounce_timer = 0  # To avoid unwanted movements
        self.reset_cooldown = 0  # Cooldown timer after level reset
        self.travel = 0  # Only keep track of direction

class StartScreen:
    def __init__(self, screen, game_state, high_scores):
        self.screen = screen
        self.game_state = game_state
        self.high_scores = high_scores
        self.tutorial_checked = False
        self.selected_level = 0
        self.show_high_scores = False
        self.dropdown_open = False

    def draw(self):
        # Draw the start screen UI
        self.screen.fill((30, 30, 30))
        pygame.display.set_caption(f'Escape the Werehouse! - START MENU')
        title_text = menu_font.render('Escape the Werehouse!', True, (255, 215, 115))
        title_center = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_center)

        # Tutorial checkbox
        tutorial_text = font.render('Tutorial', True, (255, 255, 255))
        tutorial_check = pygame.Rect(350, 116, 25, 25)  # Adjusted checkbox position
        pygame.draw.rect(self.screen, (255, 255, 255), tutorial_check, 2)
        if self.tutorial_checked:
            # Draw the "X" mark inside the checkbox
            pygame.draw.line(self.screen, (255, 255, 255), (355, 120), (369, 135), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (369, 120), (355, 135), 2)
        tutorial_text_center = tutorial_text.get_rect(center=(280, 130))
        self.screen.blit(tutorial_text, tutorial_text_center)

        # Level selection dropdown
        level_text = font.render('Select Level:', True, (255, 255, 255))
        level_text_center = level_text.get_rect(center=(self.screen.get_width() // 2, 170))
        self.screen.blit(level_text, level_text_center)
        dropdown_button = pygame.Rect(200, 190, 200, 40)  # Adjusted dropdown button position
        pygame.draw.rect(self.screen, (255, 255, 255), dropdown_button, 2)

        # Draw the dropdown menu as a single frame/box
        if self.dropdown_open:
            levels = ['Tutorial 1', 'Tutorial 2', 'Tutorial 3', 'Tutorial 4'] if self.tutorial_checked else ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']
            dropdown_box = pygame.Rect(200, 250, 200, len(levels) * 32)
            pygame.draw.rect(self.screen, (50, 50, 50), dropdown_box)  # Darker background for dropdown
            for i, level in enumerate(levels):
                level_text = dropdown_font.render(level, True, (255, 255, 255))
                self.screen.blit(level_text, (210, 260 + i * 30))

        # Display the selected level when dropdown is closed
        if not self.dropdown_open:
            if self.tutorial_checked:
                selected_level_text = dropdown_font.render(f'Tutorial {self.selected_level + 1}', True, (255, 255, 255))
                selected_level_text_center = selected_level_text.get_rect(center=(self.screen.get_width() // 2, 210))
                self.screen.blit(selected_level_text, selected_level_text_center)
            else:
                selected_level_text = dropdown_font.render(f'Level {self.selected_level + 1}', True, (255, 255, 255))
                selected_level_text_center = selected_level_text.get_rect(center=(self.screen.get_width() // 2, 210))
                self.screen.blit(selected_level_text, selected_level_text_center)

        # Start Game button
        start_button = pygame.Rect(200, 440, 200, 40)  # Adjusted start button position
        pygame.draw.rect(self.screen, (255, 255, 255), start_button, 2)
        start_text = font.render('Start Game', True, (255, 255, 255))
        start_text_center = start_text.get_rect(center=(self.screen.get_width() // 2, 460))
        self.screen.blit(start_text, start_text_center)

        # High Scores button
        high_scores_button = pygame.Rect(200, 490, 200, 40)  # Adjusted high scores button position
        pygame.draw.rect(self.screen, (255, 255, 255), high_scores_button, 2)
        high_scores_text = font.render('High Scores', True, (255, 255, 255))
        high_scores_text_center = high_scores_text.get_rect(center=(self.screen.get_width() // 2, 510))
        self.screen.blit(high_scores_text, high_scores_text_center)

        # Quit button
        quit_button = pygame.Rect(200, 540, 200, 40)  # Adjusted quit button position
        pygame.draw.rect(self.screen, (255, 255, 255), quit_button, 2)
        quit_text = font.render('Quit', True, (255, 255, 255))
        quit_text_center = quit_text.get_rect(center=(self.screen.get_width() // 2, 560))
        self.screen.blit(quit_text, quit_text_center)

        pygame.display.flip()

    def handle_events(self):
        # Handle user interactions on the start screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Toggle tutorial checkbox
                if 350 <= mouse_pos[0] <= 375 and 116 <= mouse_pos[1] <= 141:
                    self.tutorial_checked = not self.tutorial_checked
                    self.selected_level = 0  # Reset level selection
                # Toggle dropdown menu
                elif 200 <= mouse_pos[0] <= 400 and 200 <= mouse_pos[1] <= 240:
                    self.dropdown_open = not self.dropdown_open
                # Select a level from the dropdown
                elif self.dropdown_open and 200 <= mouse_pos[0] <= 400 and 250 <= mouse_pos[1] <= 490:
                    level_index = (mouse_pos[1] - 250) // 30
                    levels = 4 if self.tutorial_checked else 5
                    if level_index < levels:
                        self.selected_level = level_index
                        self.dropdown_open = False
                # Start the game
                elif 200 <= mouse_pos[0] <= 400 and 450 <= mouse_pos[1] <= 490:
                    self.game_state.game = not self.tutorial_checked
                    self.game_state.current_level = self.selected_level
                    self.game_state.is_playing = True
                    # Reset game_state
                    self.game_state.moves = 0
                    self.game_state.total_moves = 0
                    self.game_state.lives = 3
                    return 'start_game'
                # Show high scores
                elif 200 <= mouse_pos[0] <= 400 and 500 <= mouse_pos[1] <= 540:
                    self.show_high_scores = True
                    return 'show_high_scores'
                # Quit the game
                elif 200 <= mouse_pos[0] <= 400 and 550 <= mouse_pos[1] <= 590:
                    pygame.quit()
                    sys.exit()
        return None

def check_level_complete(board, game_state):
    # Check if the current level is complete
    if not board.exit:
        return False

    # Check if player is on exit tile
    for element in board.elements:
        if element[0] == TileType.EXIT:
            if (board.px, board.py) == element[1]: # Player position matches exit position
                # Render one last frame with player on exit
                pygame.display.get_surface().fill((30, 30, 30))
                board.blit_level(pygame.display.get_surface())
                board.blit_box_1(pygame.display.get_surface(), 0, 0)
                board.blit_box_2(pygame.display.get_surface(), 0, 0)
                board.blit_box_3(pygame.display.get_surface(), 0, 0)
                board.blit_box_4(pygame.display.get_surface(), 0, 0)
                board.blit_player(pygame.display.get_surface(), 0, 0)

                # Show score for completed level
                if game_state.game:
                    # Add moves to total_moves for high scores
                    game_state.total_moves += game_state.moves

                    pygame.display.set_caption(f'Escape the Werehouse!          Moves: {game_state.moves}          Total Moves: {game_state.total_moves}          Lives: {game_state.lives}     ')
                    board.blit_stars(pygame.display.get_surface(), game_state.moves)

                pygame.display.flip()
                pygame.time.wait(500)

                return True

    return False

# Handle keyboard input for player movement
def handle_input(keys, board, game_state, audio):
     # Check for cooldown period
    if game_state.reset_cooldown > 0:
        game_state.reset_cooldown -= 1
        return False

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

# Handle actions when a level is completed
def handle_level_complete(board, game_state, high_scores):
    game_state.moves = 0
    game_state.new_level = True

    # Increment level counter
    game_state.current_level += 1

    # Handle mode transitions
    if game_state.game == False and game_state.current_level >= 4:
        game_state.game = True
        game_state.current_level = 0
        # Debug statement
        print('Well done, you finished the Tutorials! Now try to Escape the Werehouse!')
    elif game_state.game == True and game_state.current_level >= 5:
        game_state.is_playing = False
        # Debug statements
        print('Congratulations! You finished the last level!')
        print(f'Your have made a total of {game_state.total_moves} successful moves!')

        if high_scores.is_high_score(game_state.total_moves):
            initials = high_scores.get_initials(pygame.display.get_surface())
            high_scores.add_score(game_state.total_moves, initials)

        print("Displaying high scores...") # Debug statement
        high_scores.display_scores(pygame.display.get_surface())

# Handle movement of player and associated boxes
def move_player_and_boxes(board, direction, travel, is_dragging, audio, game_state):
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

     # Check if player falls into pit
    if check_player_in_pit(board, game_state, new_x, new_y, audio):
        return False  # Movement was valid but player fell

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

    return True

# Check if a box has fallen into a pit and update states accordingly
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
def is_valid_move(board, new_x, new_y, direction, is_dragging):
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

# Check if player has fallen into a pit
def check_player_in_pit(board, game_state, x, y, audio):
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
                    if game_state.lives <= 0:
                        display_game_over(game_state)
                        game_state.is_playing = False
                        return True

                    else:
                        # Reset level
                        game_state.new_level = True
                        game_state.total_moves += game_state.moves
                        game_state.moves = 0
                        game_state.reset_cooldown = 30  # Set cooldown period (e.g. 30 = 0.5 seconds at 60 FPS)
                    return True
    return False

# Show GAME OVER screen when out of lives
def display_game_over(game_state):
    screen = pygame.display.get_surface()
    # Clear the screen
    screen.fill((30, 30, 30))
    pygame.display.set_caption('GAME OVER')
    # Render "GAME OVER" text
    game_over_text = dead_font.render('GAME OVER', True, (255, 0, 10))
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
    high_scores = HighScores()
    screen = pygame.display.set_mode((600, 600))
    start_screen = StartScreen(screen, game_state, high_scores)

    clock = pygame.time.Clock()
    show_start_screen = True

    # # Update the game board size based on the current level
    # mode_index = 0 if game_state.game == False else 1
    # board.update_game_board_size(level_map[mode_index][game_state.current_level])

    while True:
        if show_start_screen:
            start_screen.draw()
            action = start_screen.handle_events()
            if action == 'start_game':
                show_start_screen = False
            elif action == 'show_high_scores':
                # Set to True to enable Back buttonn
                high_scores.from_start_screen = True
                high_scores.display_scores(screen)
                while start_screen.show_high_scores:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        # Back to start screen
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if 150 <= mouse_pos[0] <= 350 and 550 <= mouse_pos[1] <= 590:
                                start_screen.show_high_scores = False
                                start_screen.draw()
        else:
            # Set up game board
            game_board = pygame.display.set_mode((board.game_board_x, board.game_board_y))
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
                    if not game_state.is_playing:
                        high_scores.from_start_screen = False  # Set the flag to False
                        high_scores.display_scores(screen)
                        pygame.time.wait(3000)
                        show_start_screen = True

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
                if game_state.travel in [1, 2]:
                    board.blit_player(game_board, game_state.travel, board.py)
                elif game_state.travel in [3, 4]:
                    board.blit_player(game_board, game_state.travel, board.px)
                else:
                    board.blit_player(game_board, 0, 0)

                # Apply blackout effect
                board.apply_blackout(game_board, game_state)

                if game_state.game:
                    pygame.display.set_caption(f'Escape the Werehouse!          Moves: {game_state.moves}          Total Moves: {game_state.total_moves}          Lives: {game_state.lives}     ')
                else:
                    pygame.display.set_caption(f'{board.titel[game_state.current_level]}')

                pygame.display.flip()
                # Cap frame rate
                clock.tick(60)

            # Ensure the start screen is shown after game over
            show_start_screen = True
            game_state.is_playing = True

    pygame.quit()

if __name__ == '__main__':
    main()