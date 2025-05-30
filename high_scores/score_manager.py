import os
import sys
import json
import pygame

class ScoreManager:
    def __init__(self):
        self.scores = self.load_scores()
        self.latest_score = None  # Track the latest added score
        self.from_start_screen = False  # Initialize the flag
        self.hig_score_font = pygame.font.SysFont('Arial Black', 32)  # Bigger font for High Scores
        self.font = pygame.font.SysFont('Lucida Console', 24)  # Define the font variable

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

    def load_scores(self):
        # Get the directory of the current file
        dir_path = os.path.dirname(os.path.abspath(__file__))

        # Navigate one level up and into the game_board/maps directory
        game_maps_path = os.path.join(dir_path, '..', 'game_board', 'maps', 'game_maps.json')

        # Load the game maps to calculate the total score
        with open(game_maps_path, 'r') as maps_file:
            game_maps = json.load(maps_file)

        # Calculate the adjusted scores for each level
        adjusted_scores = [
            sum(level['score'] + 1 for level in game_maps['levels']),
            sum(level['score'] + 2 for level in game_maps['levels']),
            sum(level['score'] + 3 for level in game_maps['levels'])
        ]

        # Define the default scores with adjusted values
        default_scores = [
            (adjusted_scores[0], 'who'),
            (adjusted_scores[1], 'are'),
            (adjusted_scores[2], 'you')
        ]

        # Construct the full path for the high_scores.py file
        file_path = os.path.join(dir_path, 'high_scores.py')

        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(f'SCORES = {default_scores}')

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                # Extract scores from the file content
                scores = eval(content.split('=')[1])
                return scores
        except Exception as e:
            print(f"Error loading scores: {e}")

        # Return default scores if loading fails
        return default_scores

    # Save the current scores to a file
    def save_scores(self):
        # Get the directory of the current file
        dir_path = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path for the high_scores.py file
        file_path = os.path.join(dir_path, 'high_scores.py')

        with open(file_path, 'w') as file:
            file.write(f'SCORES = {self.scores}')

    def display_scores(self, screen):
        # Fill background with dark color
        screen.fill((30, 30, 30))

        # Set window caption
        pygame.display.set_caption('High Scores')

        # Render the title at the top center
        title_text = self.hig_score_font.render('High Scores', True, (255, 215, 115))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 120))
        screen.blit(title_text, title_rect)

        # Define spacing between columns
        spacing = 20

        # Precompute maximum widths for each column so that all rows line up
        max_index_width = 0
        max_initials_width = 0
        max_score_width = 0

        # We'll also store rendered surfaces for each row for efficiency.
        rendered_rows = []

        for i, (score, initials) in enumerate(self.scores, start=1):
            index_str = f"{i}."
            score_str = str(score)
            initials_str = initials  # The text for the second column

            index_surface = self.hig_score_font.render(index_str, True, (255, 255, 255))
            initials_surface = self.hig_score_font.render(initials_str, True, (255, 255, 255))
            score_surface = self.hig_score_font.render(score_str, True, (255, 255, 255))

            max_index_width = max(max_index_width, index_surface.get_width())
            max_initials_width = max(max_initials_width, initials_surface.get_width())
            max_score_width = max(max_score_width, score_surface.get_width())

            # Also store the surfaces along with texts for later use.
            rendered_rows.append({
                "index_str": index_str,
                "score_str": score_str,
                "initials_str": initials_str,
                "index_surface": index_surface,
                "initials_surface": initials_surface,
                "score_surface": score_surface,
                "score": score,  # raw number for highlight matching
                "initials": initials
            })

        # Calculate total width of the 3 columns (with spacing)
        total_group_width = max_index_width + spacing + max_initials_width + spacing + max_score_width

        # Left position to center the group horizontally
        left_x = (screen.get_width() - total_group_width) // 2

        # Now calculate the fixed x positions for each column:
        index_x = left_x
        initials_x = index_x + max_index_width + spacing
        score_x = initials_x + max_initials_width + spacing

        # Loop again over each row to blit them.
        # We'll start rendering rows at a given y position.
        start_y = 100
        row_spacing_y = 50

        for i, row in enumerate(rendered_rows):
            y_pos = start_y + (i + 1) * row_spacing_y

            # Determine if this row should be highlighted (using latest_score)
            highlight = (self.latest_score is not None) and (self.latest_score == (row["score"], row["initials"]))
            offset = 1 if highlight else 0

            if highlight:
                # Render shadow texts in gold with a 1-pixel offset.
                index_shadow = self.hig_score_font.render(row["index_str"], True, (255, 215, 0))
                initials_shadow = self.hig_score_font.render(row["initials_str"], True, (255, 215, 0))
                score_shadow = self.hig_score_font.render(row["score_str"], True, (255, 215, 0))
                screen.blit(index_shadow, (index_x + offset, y_pos + offset))
                screen.blit(initials_shadow, (initials_x + offset, y_pos + offset))
                screen.blit(score_shadow, (score_x + offset, y_pos + offset))

            # Blit the main texts in white.
            screen.blit(row["index_surface"], (index_x, y_pos))
            screen.blit(row["initials_surface"], (initials_x, y_pos))
            screen.blit(row["score_surface"], (score_x, y_pos))

        # Optionally, display a 'Back' button if coming from the start screen
        if self.from_start_screen:
            back_button = pygame.Rect(200, 500, 200, 40)  # Adjusted back button position
            pygame.draw.rect(screen, (255, 255, 255), back_button, 2)
            back_text = self.font.render('Back', True, (255, 255, 255))
            back_text_center = back_text.get_rect(center=(screen.get_width() // 2, 520))
            screen.blit(back_text, back_text_center)
            pygame.display.flip()
        else:
            pygame.display.flip()
            # Wait for a bit so the display stays visible (or you can handle events for interactive behavior)
            pygame.time.wait(3000)


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
            celebration_text = self.font.render('Congratulations!', True, (255, 255, 255))
            celebration_center = celebration_text.get_rect(center=(screen.get_width() // 2, 30))
            screen.blit(celebration_text, celebration_center)
            three_text = self.font.render('You made it to the top three!', True, (255, 255, 255))
            three_center = three_text.get_rect(center=(screen.get_width() // 2, 60))
            screen.blit(three_text, three_center)

            # Show prompt text
            prompt_text = self.font.render('Enter your initials:', True, (255, 255, 255))
            prompt_center = prompt_text.get_rect(center=(screen.get_width() // 2, 90))
            screen.blit(prompt_text, prompt_center)

            # Blit input text
            txt_surface = self.font.render(text, True, color)
            text_center = txt_surface.get_rect(center=input_box.center)
            screen.blit(txt_surface, text_center)

            pygame.display.flip()

        return text