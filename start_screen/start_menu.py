import pygame
import sys
import subprocess

class StartMenu:
    def __init__(self, level, game_state):
        # Initialize the start screen with necessary attributes
        self.level = level
        self.screen = level.game_board
        self.game_state = game_state
        self.tutorial_checked = False  # Checkbox state for tutorial
        self.selected_level = 0  # Currently selected level
        self.show_high_scores = False  # Flag to show high scores
        self.dropdown_open = False  # Flag to indicate if level dropdown is open
        self.options_dropdown_open = False  # Flag to indicate if options dropdown is open
        self.lights_off_checked = False  # Checkbox state for lights off option
        self.arrow_up_up_checked = True  # Checkbox state for arrow up move option, default is True
        self.arrow_up_facing_checked = False  # Checkbox state for arrow up facing move option
        self.dropdown_font = pygame.font.SysFont('Lucida Console', 20)  # Smaller font for dropdown
        self.menu_font = pygame.font.SysFont('Arial Black', 42)  # Even bigger font for START MENU
        self.font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
        self.dropdown_options = ["Lights OFF", "Arrow Up = Move Up", "Arrow Up = Move Facing Direction"]


    def draw(self):
        # Draw the start screen UI
        self.screen.fill((30, 30, 30))  # Fill the screen with a dark background
        pygame.display.set_caption('Escape the Werehouse! - START MENU')  # Set the window caption

        # Title
        title_text = self.menu_font.render('Escape the Werehouse!', True, (255, 215, 115))
        title_center = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_center)

        # Store the position of the letter "E" in the title
        self.e_position = (title_center.x + 10, title_center.y)  # Adjust the x offset as needed

        # Tutorial checkbox
        tutorial_text = self.font.render('Tutorial', True, (255, 255, 255))
        tutorial_check = pygame.Rect(350, 116, 25, 25)
        pygame.draw.rect(self.screen, (255, 255, 255), tutorial_check, 2)
        if self.tutorial_checked:
            pygame.draw.line(self.screen, (255, 255, 255), (355, 120), (369, 135), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (369, 120), (355, 135), 2)
        tutorial_text_center = tutorial_text.get_rect(center=(280, 130))
        self.screen.blit(tutorial_text, tutorial_text_center)

        # Level selection dropdown
        level_text = self.font.render('Select Level:', True, (255, 255, 255))
        level_text_center = level_text.get_rect(center=(self.screen.get_width() // 2, 170))
        self.screen.blit(level_text, level_text_center)
        dropdown_button = pygame.Rect(200, 190, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), dropdown_button, 2)

        # Display the selected level
        if self.tutorial_checked:
            selected_level_text = self.dropdown_font.render(f'Tutorial {self.selected_level + 1}', True, (255, 255, 255))
        else:
            selected_level_text = self.dropdown_font.render(f'Level {self.selected_level + 1}', True, (255, 255, 255))
        selected_level_text_center = selected_level_text.get_rect(center=(self.screen.get_width() // 2, 210))
        self.screen.blit(selected_level_text, selected_level_text_center)

        # Start Game button
        start_button = pygame.Rect(200, 240, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), start_button, 2)
        start_text = self.font.render('Start Game', True, (255, 255, 255))
        start_text_center = start_text.get_rect(center=(self.screen.get_width() // 2, 260))
        self.screen.blit(start_text, start_text_center)

        # Options dropdown
        options_dropdown_button = pygame.Rect(200, 450, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), options_dropdown_button, 2)

        # Display the selected options
        selected_options_text = self.dropdown_font.render('Options', True, (255, 255, 255))
        selected_options_text_center = selected_options_text.get_rect(center=(self.screen.get_width() // 2, 470))
        self.screen.blit(selected_options_text, selected_options_text_center)

        # High Scores button
        high_scores_button = pygame.Rect(200, 500, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), high_scores_button, 2)
        high_scores_text = self.font.render('High Scores', True, (255, 255, 255))
        high_scores_text_center = high_scores_text.get_rect(center=(self.screen.get_width() // 2, 520))
        self.screen.blit(high_scores_text, high_scores_text_center)

        # Quit button
        quit_button = pygame.Rect(200, 550, 200, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), quit_button, 2)
        quit_text = self.font.render('Quit', True, (255, 255, 255))
        quit_text_center = quit_text.get_rect(center=(self.screen.get_width() // 2, 570))
        self.screen.blit(quit_text, quit_text_center)

        # Draw the level dropdown menu if it is open
        if self.dropdown_open:
            # Determine which set of titles to use based on tutorial mode
            if self.tutorial_checked:
                titles = self.level.zone_data.map_title[0]
            else:
                titles = self.level.zone_data.map_title[1]

            dropdown_levels = []  # Initialize a list to hold the level text lines for the dropdown
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
                level_words = title_text.split()  # Split the title text into level_words
                current_line = ""  # Initialize the current line of text

                # Build the lines of text for the dropdown
                for word in level_words:
                    test_line = current_line + word + " "  # Test adding the next word to the current line
                    if self.dropdown_font.size(test_line)[0] > max_line_width:  # If the line is too wide, finalize the current line
                        dropdown_levels.append(current_line)
                        current_line = word + " "  # Start a new line with the current word
                    else:
                        current_line = test_line  # Continue building the current line

                if current_line:  # If there's any remaining text, add it as a new line
                    dropdown_levels.append(current_line.strip())

            # Calculate the size and position of the dropdown box
            dropdown_width = max(self.dropdown_font.size(line)[0] for line in dropdown_levels) + 40
            text_height = len(dropdown_levels) * 32
            dropdown_y = 235
            bottom_padding = 16
            dropdown_height = text_height + bottom_padding
            dropdown_x = self.screen.get_width() // 2 - dropdown_width // 2
            dropdown_box = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            pygame.draw.rect(self.screen, (50, 50, 50), dropdown_box)  # Draw the dropdown background

            # Render and display each line of text in the dropdown
            for i, line in enumerate(dropdown_levels):
                level_text = self.dropdown_font.render(line, True, (255, 255, 255))
                level_text_rect = level_text.get_rect()
                level_text_rect.topleft = (dropdown_x + 20, dropdown_y + 16 + i * 32)
                self.screen.blit(level_text, level_text_rect)

        # Draw the options dropdown menu if it is open
        if self.options_dropdown_open:
            max_line_width = self.screen.get_width() - 50

            # Calculate the size and position of the options dropdown box
            dropdown_width = max(self.dropdown_font.size(line)[0] for line in self.dropdown_options) + 80
            text_height = len(self.dropdown_options) * 32
            dropdown_y = 495
            bottom_padding = 16
            dropdown_height = text_height + bottom_padding
            dropdown_x = self.screen.get_width() // 2 - dropdown_width // 2
            dropdown_box = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            pygame.draw.rect(self.screen, (50, 50, 50), dropdown_box)  # Draw the options dropdown background

            # Render and display each option in the dropdown
            for i, line in enumerate(self.dropdown_options):
                option_text = self.dropdown_font.render(line, True, (255, 255, 255))
                option_text_rect = option_text.get_rect()
                option_text_rect.topleft = (dropdown_x + 20, dropdown_y + 16 + i * 32)
                self.screen.blit(option_text, option_text_rect)

                # Calculate checkbox position
                checkbox_x = dropdown_x + dropdown_width - 40
                checkbox_rect = pygame.Rect(checkbox_x, dropdown_y + 16 + i * 29, 25, 25)
                pygame.draw.rect(self.screen, (255, 255, 255), checkbox_rect, 2)

                # Draw the checkmark if the option is checked
                if i == 0 and self.lights_off_checked:
                    pygame.draw.line(self.screen, (255, 255, 255), \
                                    (checkbox_x + 5, dropdown_y + 20 + i * 32), \
                                    (checkbox_x + 19, dropdown_y + 35 + i * 32), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), \
                                    (checkbox_x + 19, dropdown_y + 20 + i * 32), \
                                    (checkbox_x + 5, dropdown_y + 35 + i * 32), 2)
                elif i == 1 and self.arrow_up_up_checked:
                    pygame.draw.line(self.screen, (255, 255, 255), \
                                    (checkbox_x + 5, dropdown_y + 18 + i * 32), \
                                    (checkbox_x + 19, dropdown_y + 33 + i * 32), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), \
                                    (checkbox_x + 19, dropdown_y + 18 + i * 32), \
                                    (checkbox_x + 5, dropdown_y + 32 + i * 32), 2)
                elif i == 2 and self.arrow_up_facing_checked:
                    pygame.draw.line(self.screen, (255, 255, 255), \
                                    (checkbox_x + 5, dropdown_y + 15 + i * 32), \
                                    (checkbox_x + 19, dropdown_y + 30 + i * 32), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), \
                                    (checkbox_x + 19, dropdown_y + 15 + i * 32), \
                                    (checkbox_x + 5, dropdown_y + 30 + i * 32), 2)

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
                    levels = self.level.no_of_levels[0] if self.tutorial_checked else self.level.no_of_levels[1]
                    if level_index < levels:
                        self.selected_level = level_index
                        self.dropdown_open = False

                # Check if the options dropdown button is clicked
                elif 200 <= mouse_pos[0] <= 400 and 450 <= mouse_pos[1] <= 490:
                    self.options_dropdown_open = not self.options_dropdown_open
                    self.dropdown_open = False

                # Check if an option in the options dropdown is clicked
                elif self.options_dropdown_open:
                    dropdown_x = self.screen.get_width() // 2 - (max(self.dropdown_font.size(line)[0] \
                                    for line in self.dropdown_options) + 80) // 2
                    dropdown_y = 495

                    # Check if the "Lights OFF" option is clicked
                    if dropdown_x <= mouse_pos[0] <= dropdown_x + max(self.dropdown_font.size(line)[0] \
                                    for line in self.dropdown_options) + 80 \
                                    and dropdown_y + 13 <= mouse_pos[1] <= dropdown_y + 38:
                        self.lights_off_checked = not self.lights_off_checked
                        self.game_state.lights_out = self.lights_off_checked
                        self.level.blackout = self.game_state.lights_out
                        print(f"Light toggled: {'OFF' if self.level.blackout else 'ON'}")
                        self.draw()

                    # Check if the "Arrow Up = Move Up" option is clicked
                    elif dropdown_x <= mouse_pos[0] <= dropdown_x + max(self.dropdown_font.size(line)[0] \
                                    for line in self.dropdown_options) + 80 \
                                    and dropdown_y + 43 <= mouse_pos[1] <= dropdown_y + 68:
                        self.arrow_up_up_checked = True
                        self.arrow_up_facing_checked = False
                        self.game_state.normal_movement = True
                        self.draw()

                    # Check if the "Arrow Up = Move Facing Direction" option is clicked
                    elif dropdown_x <= mouse_pos[0] <= dropdown_x + max(self.dropdown_font.size(line)[0] \
                                    for line in self.dropdown_options) + 80 \
                                    and dropdown_y + 73 <= mouse_pos[1] <= dropdown_y + 98:
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
                    dropdown_x = self.screen.get_width() // 2 - (max(self.dropdown_font.size(line)[0] \
                                for line in self.dropdown_options) + 80) // 2
                    dropdown_y = 235
                    dropdown_width = max(self.dropdown_font.size(line)[0] for line in self.dropdown_options) + 80
                    dropdown_height = len(self.dropdown_options) * 32 + 16
                    if not (dropdown_x <= mouse_pos[0] <= dropdown_x + dropdown_width \
                            and dropdown_y <= mouse_pos[1] <= dropdown_y + dropdown_height):
                        if not (200 <= mouse_pos[0] <= 400 and 190 <= mouse_pos[1] <= 230):
                            self.dropdown_open = False

                if self.options_dropdown_open:
                    dropdown_x = self.screen.get_width() // 2 - (max(self.dropdown_font.size(line)[0] \
                                for line in self.dropdown_options) + 80) // 2
                    dropdown_y = 495
                    dropdown_width = max(self.dropdown_font.size(line)[0] for line in self.dropdown_options) + 80
                    dropdown_height = len(self.dropdown_options) * 32 + 16
                    if not (dropdown_x <= mouse_pos[0] <= dropdown_x + dropdown_width \
                            and dropdown_y <= mouse_pos[1] <= dropdown_y + dropdown_height):
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