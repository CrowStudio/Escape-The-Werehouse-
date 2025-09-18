import pygame
import json
import os
import glob
import sys
from game_board.basic_tile import BasicTile

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
LEVEL_MAPS_PATH = os.path.join(DIR_PATH, '..', 'game_board', 'zones', 'level_maps')

# Set path for the high_scores.py file
HIGH_SCORE_PATH = os.path.join(DIR_PATH, 'high_scores.py')

class ScoreManager:
    def __init__(self):
        # Initialize game board size to zone values
        self.game_board = pygame.display.set_mode((BasicTile.BOARD_WIDTH, BasicTile.BOARD_HEIGHT))  # Set the screen size to zone width x zone height

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

    def is_high_score(self, score):
        # If there are fewer than 3 high scores, the score qualifies automatically
        if len(self.scores) < 3:
            return True

        # The list is sorted in ascending order (lower is better)
        third_place = self.scores[-1][0]

        # If the new score is strictly better than (i.e., less than) the third place, it's a high score.
        if score < third_place:
            return True

        # If the new score equals any of the existing high scores, and not equals third place it should qualify
        for existing_score, _ in self.scores:
            if score == existing_score and not score == third_place:
                return True

        # Otherwise, it doesn't qualify as a high score.
        return False


    def load_scores(self):
        # Dynamically detect all zone files
        zone_files = glob.glob(os.path.join(LEVEL_MAPS_PATH, 'zone_*_maps.json'))
        total_score = 0

        # Sum all level scores across all zones
        for zone_file in zone_files:
            with open(zone_file, 'r') as maps_file:
                zone_data = json.load(maps_file)
                total_score += sum(level['score'] for level in zone_data['levels'])

        # Apply adjustments to the total score
        adjusted_scores = [
            (total_score + 1, 'who'),  # Total score + 1
            (total_score + 3, 'are'),  # Total score + 3 (one inccorect move +1)
            (total_score + 5, 'you')   # Total score + 5 (two inccorect moves +1)
        ]

        if not os.path.exists(HIGH_SCORE_PATH):
            with open(HIGH_SCORE_PATH, 'w') as file:
                file.write(f'SCORES = {adjusted_scores}')

        try:
            with open(HIGH_SCORE_PATH, 'r') as file:
                content = file.read()
                scores = eval(content.split('=')[1])
                return scores
        except Exception as e:
            print(f"Error loading scores: {e}")
            return adjusted_scores


    # Save the current scores to a file
    def save_scores(self):

        with open(HIGH_SCORE_PATH, 'w') as file:
            file.write(f'SCORES = {self.scores}')

    def display_scores(self):
        # Fill background with dark color
        self.game_board.fill((30, 30, 30))

        # Set window caption
        pygame.display.set_caption('High Scores')

        # Render the title at the top center
        title_text = self.hig_score_font.render('High Scores', True, (255, 215, 115))
        title_rect = title_text.get_rect(center=(BasicTile.BOARD_WIDTH // 2, 120))
        self.game_board.blit(title_text, title_rect)

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
        left_x = (BasicTile.BOARD_WIDTH - total_group_width) // 2

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
                self.game_board.blit(index_shadow, (index_x + offset, y_pos + offset))
                self.game_board.blit(initials_shadow, (initials_x + offset, y_pos + offset))
                self.game_board.blit(score_shadow, (score_x + offset, y_pos + offset))

            # Blit the main texts in white.
            self.game_board.blit(row["index_surface"], (index_x, y_pos))
            self.game_board.blit(row["initials_surface"], (initials_x, y_pos))
            self.game_board.blit(row["score_surface"], (score_x, y_pos))

        # Optionally, display a 'Back' button if coming from the start screen
        if self.from_start_screen:
            back_button = pygame.Rect(200, 500, 200, 40)  # Adjusted back button position
            pygame.draw.rect(self.game_board, (255, 255, 255), back_button, 2)
            back_text = self.font.render('Back', True, (255, 255, 255))
            back_text_center = back_text.get_rect(center=(BasicTile.BOARD_WIDTH // 2, 520))
            self.game_board.blit(back_text, back_text_center)
            pygame.display.flip()
        else:
            pygame.display.flip()
            # Wait for a bit so the display stays visible (or you can handle events for interactive behavior)
            pygame.time.wait(3000)


    # Input box for entering initials after achieving a high score
    def get_initials(self):
        input_box = pygame.Rect(0, 0, 140, 32)
        input_box.center = (BasicTile.BOARD_WIDTH // 2, 120)
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

            self.game_board.fill((30, 30, 30))
            # Show celebration text
            celebration_text = self.font.render('Congratulations!', True, (255, 255, 255))
            celebration_center = celebration_text.get_rect(center=(BasicTile.BOARD_WIDTH // 2, 30))
            self.game_board.blit(celebration_text, celebration_center)
            three_text = self.font.render('You made it to the top three!', True, (255, 255, 255))
            three_center = three_text.get_rect(center=(BasicTile.BOARD_WIDTH // 2, 60))
            self.game_board.blit(three_text, three_center)

            # Show prompt text
            prompt_text = self.font.render('Enter your initials:', True, (255, 255, 255))
            prompt_center = prompt_text.get_rect(center=(BasicTile.BOARD_WIDTH // 2, 90))
            self.game_board.blit(prompt_text, prompt_center)

            # Blit input text
            txt_surface = self.font.render(text, True, color)
            text_center = txt_surface.get_rect(center=input_box.center)
            self.game_board.blit(txt_surface, text_center)

            pygame.display.flip()

        return text
