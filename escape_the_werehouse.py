from pickle import FALSE
import sys
import os
import logging
import pygame
import subprocess
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
    tutorial_font = pygame.font.SysFont('Lucida Console', 12)  # Font for tutorial text
    font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
    dropdown_font = pygame.font.SysFont('Lucida Console', 20)  # Smaller font for dropdown
    hig_score_font = pygame.font.SysFont('Arial Black', 32)  # Bigger font for High Scores
    menu_font = pygame.font.SysFont('Arial Black', 42)  # Even bigger font for START MENU
    dead_font = pygame.font.SysFont('Arial Black', 72)  # Biggest font for GAME OVER
except pygame.error as e:
    logger.error(f"Failed to initialize PyGame: {e}")
    sys.exit(1)

# Game constants
FPS = 70
DISTANCE = TILE_SIZE
MOVEMENT_DELAY = 10  # Controls movement speed (higher = slower)
ARROW_KEYS = {pygame.K_UP:    {'direction': 'up',    'travel': 1, 'search': 1},
              pygame.K_DOWN:  {'direction': 'down',  'travel': 2, 'search': 2},
              pygame.K_LEFT:  {'direction': 'left',  'travel': 3, 'search': 3},
              pygame.K_RIGHT: {'direction': 'right', 'travel': 4, 'search': 4}}

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
        # If there are fewer than 3 high scores, the score qualifies automatically
        if len(self.scores) < 3:
            return True

        # The list is sorted in ascending order (lower is better)
        third_place = self.scores[-1][0]

        # If the new score is strictly better than (i.e. less than) the third place, it's a high score.
        if score < third_place:
            return True

        # If the new score equals the third place score, only allow it if
        # it also matches one of the top two scores that are strictly better.
        # In other words, at least one of the top two scores must be strictly less than the new score.
        elif score == third_place:
            # Check for at least one score among the top two that's strictly less than the new score
            if self.scores[0][0] < score or self.scores[1][0] < score:
                return True

        # Otherwise, it doesn't qualify as a high score.
        return False

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

        # Only show Back button if coming from start screen
        if self.from_start_screen:
            back_button = pygame.Rect(200, 500, 200, 40)  # Adjusted back button position
            pygame.draw.rect(screen, (255, 255, 255), back_button, 2)
            back_text = font.render('Back', True, (255, 255, 255))
            back_text_center = back_text.get_rect(center=(screen.get_width() // 2, 520))
            screen.blit(back_text, back_text_center)

        pygame.display.flip()
        pygame.time.wait(300)

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

class StartScreen:
    def __init__(self, screen, game_state, high_scores, board):
        # Initialize the start screen with necessary attributes
        self.screen = screen
        self.game_state = game_state
        self.high_scores = high_scores
        self.board = board
        self.tutorial_checked = False  # Checkbox state for tutorial
        self.selected_level = 0  # Currently selected level
        self.show_high_scores = False  # Flag to show high scores
        self.dropdown_open = False  # Flag to indicate if level dropdown is open
        self.options_dropdown_open = False  # Flag to indicate if options dropdown is open
        self.lights_off_checked = False  # Checkbox state for lights off option
        self.arrow_up_up_checked = True  # Checkbox state for arrow up move option, default is True
        self.arrow_up_facing_checked = False  # Checkbox state for arrow up facing move option

    def draw(self):
        # Draw the start screen UI
        self.screen.fill((30, 30, 30))  # Fill the screen with a dark background
        pygame.display.set_caption('Escape the Werehouse! - START MENU')  # Set the window caption

        # Title
        title_text = menu_font.render('Escape the Werehouse!', True, (255, 215, 115))
        title_center = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_center)

        # Store the position of the letter "E" in the title
        self.e_position = (title_center.x + 10, title_center.y)  # Adjust the x offset as needed

        # Tutorial checkbox
        tutorial_text = font.render('Tutorial', True, (255, 255, 255))
        tutorial_check = pygame.Rect(350, 116, 25, 25)
        pygame.draw.rect(self.screen, (255, 255, 255), tutorial_check, 2)
        if self.tutorial_checked:
            pygame.draw.line(self.screen, (255, 255, 255), (355, 120), (369, 135), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (369, 120), (355, 135), 2)
        tutorial_text_center = tutorial_text.get_rect(center=(280, 130))
        self.screen.blit(tutorial_text, tutorial_text_center)

        # Level selection dropdown
        level_text = font.render('Select Level:', True, (255, 255, 255))
        level_text_center = level_text.get_rect(center=(self.screen.get_width() // 2, 170))
        self.screen.blit(level_text, level_text_center)
        dropdown_button = pygame.Rect(200, 190, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), dropdown_button, 2)

        # Display the selected level
        if self.tutorial_checked:
            selected_level_text = dropdown_font.render(f'Tutorial {self.selected_level + 1}', True, (255, 255, 255))
        else:
            selected_level_text = dropdown_font.render(f'Level {self.selected_level + 1}', True, (255, 255, 255))
        selected_level_text_center = selected_level_text.get_rect(center=(self.screen.get_width() // 2, 210))
        self.screen.blit(selected_level_text, selected_level_text_center)

        # Start Game button
        start_button = pygame.Rect(200, 240, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), start_button, 2)
        start_text = font.render('Start Game', True, (255, 255, 255))
        start_text_center = start_text.get_rect(center=(self.screen.get_width() // 2, 260))
        self.screen.blit(start_text, start_text_center)

        # Options dropdown
        options_dropdown_button = pygame.Rect(200, 450, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), options_dropdown_button, 2)

        # Display the selected options
        selected_options_text = dropdown_font.render('Options', True, (255, 255, 255))
        selected_options_text_center = selected_options_text.get_rect(center=(self.screen.get_width() // 2, 470))
        self.screen.blit(selected_options_text, selected_options_text_center)

        # High Scores button
        high_scores_button = pygame.Rect(200, 500, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), high_scores_button, 2)
        high_scores_text = font.render('High Scores', True, (255, 255, 255))
        high_scores_text_center = high_scores_text.get_rect(center=(self.screen.get_width() // 2, 520))
        self.screen.blit(high_scores_text, high_scores_text_center)

        # Quit button
        quit_button = pygame.Rect(200, 550, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), quit_button, 2)
        quit_text = font.render('Quit', True, (255, 255, 255))
        quit_text_center = quit_text.get_rect(center=(self.screen.get_width() // 2, 570))
        self.screen.blit(quit_text, quit_text_center)

        # Draw the level dropdown menu if it is open
        if self.dropdown_open:
            # Determine which set of titles to use based on tutorial mode
            if self.tutorial_checked:
                titles = self.board.map_title[0]
            else:
                titles = self.board.map_title[1]

            lines = []  # Initialize a list to hold the lines of text for the dropdown
            max_line_width = self.screen.get_width() - 50  # Maximum width for a line of text

            # Process each title to format it for the dropdown
            for i, title in enumerate(titles, start=1):
                # Handle titles with special characters
                if '!' in title:
                    trimmed_title = title.split('!')[0] + '!'
                else:
                    trimmed_title = title
                trimmed_title = trimmed_title.split(',')[0]  # Remove any additional info after a comma
                title_text = f"{i}: {trimmed_title}"  # Format the title text with its index
                words = title_text.split()  # Split the title text into words
                current_line = ""  # Initialize the current line of text

                # Build the lines of text for the dropdown
                for word in words:
                    test_line = current_line + word + " "  # Test adding the next word to the current line
                    if dropdown_font.size(test_line)[0] > max_line_width:  # If the line is too wide, finalize the current line
                        lines.append(current_line)
                        current_line = word + " "  # Start a new line with the current word
                    else:
                        current_line = test_line  # Continue building the current line

                if current_line:  # If there's any remaining text, add it as a new line
                    lines.append(current_line.strip())

            # Calculate the size and position of the dropdown box
            dropdown_width = max(dropdown_font.size(line)[0] for line in lines) + 40
            text_height = len(lines) * 32
            dropdown_y = 235
            bottom_padding = 16
            dropdown_height = text_height + bottom_padding
            dropdown_x = self.screen.get_width() // 2 - dropdown_width // 2
            dropdown_box = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            pygame.draw.rect(self.screen, (50, 50, 50), dropdown_box)  # Draw the dropdown background

            # Render and display each line of text in the dropdown
            for i, line in enumerate(lines):
                level_text = dropdown_font.render(line, True, (255, 255, 255))
                level_text_rect = level_text.get_rect()
                level_text_rect.topleft = (dropdown_x + 20, dropdown_y + 16 + i * 32)
                self.screen.blit(level_text, level_text_rect)

        # Draw the options dropdown menu if it is open
        if self.options_dropdown_open:
            lines = ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]
            max_line_width = self.screen.get_width() - 50

            # Calculate the size and position of the options dropdown box
            dropdown_width = max(dropdown_font.size(line)[0] for line in lines) + 80
            text_height = len(lines) * 32
            dropdown_y = 495
            bottom_padding = 16
            dropdown_height = text_height + bottom_padding
            dropdown_x = self.screen.get_width() // 2 - dropdown_width // 2
            dropdown_box = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            pygame.draw.rect(self.screen, (50, 50, 50), dropdown_box)  # Draw the options dropdown background

            # Render and display each option in the dropdown
            for i, line in enumerate(lines):
                option_text = dropdown_font.render(line, True, (255, 255, 255))
                option_text_rect = option_text.get_rect()
                option_text_rect.topleft = (dropdown_x + 20, dropdown_y + 16 + i * 32)
                self.screen.blit(option_text, option_text_rect)

                # Calculate checkbox position
                checkbox_x = dropdown_x + dropdown_width - 40
                checkbox_rect = pygame.Rect(checkbox_x, dropdown_y + 16 + i * 29, 25, 25)
                pygame.draw.rect(self.screen, (255, 255, 255), checkbox_rect, 2)

                # Draw the checkmark if the option is checked
                if i == 0 and self.lights_off_checked:
                    pygame.draw.line(self.screen, (255, 255, 255), (checkbox_x + 5, dropdown_y + 20 + i * 32), (checkbox_x + 19, dropdown_y + 35 + i * 32), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), (checkbox_x + 19, dropdown_y + 20 + i * 32), (checkbox_x + 5, dropdown_y + 35 + i * 32), 2)
                elif i == 1 and self.arrow_up_up_checked:
                    pygame.draw.line(self.screen, (255, 255, 255), (checkbox_x + 5, dropdown_y + 18 + i * 32), (checkbox_x + 19, dropdown_y + 33 + i * 32), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), (checkbox_x + 19, dropdown_y + 18 + i * 32), (checkbox_x + 5, dropdown_y + 32 + i * 32), 2)
                elif i == 2 and self.arrow_up_facing_checked:
                    pygame.draw.line(self.screen, (255, 255, 255), (checkbox_x + 5, dropdown_y + 15 + i * 32), (checkbox_x + 19, dropdown_y + 30 + i * 32), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), (checkbox_x + 19, dropdown_y + 15 + i * 32), (checkbox_x + 5, dropdown_y + 30 + i * 32), 2)

        # Update the display
        pygame.display.flip()

    def handle_events(self):
        # Handle user events such as mouse clicks and key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle the quit event
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse button down events
                mouse_pos = pygame.mouse.get_pos()

                # Check if the letter "E" in the title is clicked
                if self.is_e_clicked(mouse_pos):
                    self.launch_level_editor()

                # Check if the tutorial checkbox is clicked
                if 350 <= mouse_pos[0] <= 375 and 116 <= mouse_pos[1] <= 141:
                    self.tutorial_checked = not self.tutorial_checked
                    self.selected_level = 0
                    return  # Exit the method to prevent closing the dropdown

                # Check if the level dropdown button is clicked
                elif 200 <= mouse_pos[0] <= 400 and 190 <= mouse_pos[1] <= 230:
                    self.dropdown_open = not self.dropdown_open
                    self.options_dropdown_open = False

                # Check if a level is selected from the dropdown
                elif self.dropdown_open and 200 <= mouse_pos[0] <= 400 and 235 <= mouse_pos[1] <= 475:
                    level_index = (mouse_pos[1] - 235) // 32
                    levels = self.board.no_of_levels[0] if self.tutorial_checked else self.board.no_of_levels[1]
                    if level_index < levels:
                        self.selected_level = level_index
                        self.dropdown_open = False

                # Check if the options dropdown button is clicked
                elif 200 <= mouse_pos[0] <= 400 and 450 <= mouse_pos[1] <= 490:
                    self.options_dropdown_open = not self.options_dropdown_open
                    self.dropdown_open = False

                # Check if an option in the options dropdown is clicked
                elif self.options_dropdown_open:
                    dropdown_x = self.screen.get_width() // 2 - (max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80) // 2
                    dropdown_y = 495

                    # Check if the "Lights OFF" option is clicked
                    if dropdown_x <= mouse_pos[0] <= dropdown_x + max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80 and dropdown_y + 13 <= mouse_pos[1] <= dropdown_y + 38:
                        self.lights_off_checked = not self.lights_off_checked
                        self.game_state.lights_out = self.lights_off_checked
                        self.board.blackout = self.game_state.lights_out
                        print(f"Light toggled: {'OFF' if self.board.blackout else 'ON'}")
                        self.draw()

                    # Check if the "Arrow Up = Move Up" option is clicked
                    elif dropdown_x <= mouse_pos[0] <= dropdown_x + max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80 and dropdown_y + 43 <= mouse_pos[1] <= dropdown_y + 68:
                        self.arrow_up_up_checked = True
                        self.arrow_up_facing_checked = False
                        self.game_state.normal_movement = True
                        self.draw()

                    # Check if the "Arrow Up = Move Facing Direction" option is clicked
                    elif dropdown_x <= mouse_pos[0] <= dropdown_x + max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80 and dropdown_y + 73 <= mouse_pos[1] <= dropdown_y + 98:
                        self.arrow_up_up_checked = False
                        self.arrow_up_facing_checked = True
                        self.game_state.normal_movement = False
                        self.draw()

                # Check if the "Start Game" button is clicked
                elif 200 <= mouse_pos[0] <= 400 and 240 <= mouse_pos[1] <= 280:
                    self.game_state.game = not self.tutorial_checked
                    self.game_state.current_level = self.selected_level
                    self.game_state.is_playing = True
                    self.game_state.moves = 0
                    self.game_state.total_moves = 0
                    self.game_state.lives = 3
                    return 'start_game'

                # Check if the "High Scores" button is clicked
                elif 200 <= mouse_pos[0] <= 400 and 500 <= mouse_pos[1] <= 540:
                    self.show_high_scores = True
                    return 'show_high_scores'

                # Check if the "Quit" button is clicked
                elif 200 <= mouse_pos[0] <= 400 and 550 <= mouse_pos[1] <= 590:
                    pygame.quit()
                    sys.exit()

                # Close dropdowns if clicking outside their respective areas
                if self.dropdown_open:
                    dropdown_x = self.screen.get_width() // 2 - (max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80) // 2
                    dropdown_y = 235
                    dropdown_width = max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80
                    dropdown_height = len(["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) * 32 + 16
                    if not (dropdown_x <= mouse_pos[0] <= dropdown_x + dropdown_width and dropdown_y <= mouse_pos[1] <= dropdown_y + dropdown_height):
                        if not (200 <= mouse_pos[0] <= 400 and 190 <= mouse_pos[1] <= 230):
                            self.dropdown_open = False

                if self.options_dropdown_open:
                    dropdown_x = self.screen.get_width() // 2 - (max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80) // 2
                    dropdown_y = 495
                    dropdown_width = max(dropdown_font.size(line)[0] for line in ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) + 80
                    dropdown_height = len(["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]) * 32 + 16
                    if not (dropdown_x <= mouse_pos[0] <= dropdown_x + dropdown_width and dropdown_y <= mouse_pos[1] <= dropdown_y + dropdown_height):
                        if not (200 <= mouse_pos[0] <= 400 and 450 <= mouse_pos[1] <= 490):
                            self.options_dropdown_open = False

        return None

    def is_e_clicked(self, mouse_pos):
        # Define the area around the letter "E"
        e_rect = pygame.Rect(self.e_position[0], self.e_position[1], 20, 40)  # Adjust the width and height as needed
        return e_rect.collidepoint(mouse_pos)

    def launch_level_editor(self):
        # Launch the level editor script
        subprocess.Popen([sys.executable, "level_editor.py"])

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
    high_scores = HighScores()
    screen = pygame.display.set_mode((600, 640))  # Set the screen size to 600x640
    start_screen = StartScreen(screen, game_state, high_scores, board)

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
                # Set to True to enable Back button
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
                            if 200 <= mouse_pos[0] <= 400 and 500 <= mouse_pos[1] <= 540:
                                start_screen.show_high_scores = False
                                start_screen.draw()
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
