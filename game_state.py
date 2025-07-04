import pygame
from game_board.basic_tile import BasicTile

class GameState:
    def __init__(self, level):
        self.level = level

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
        self.prev_x = 0
        self.prev_y = 0

        self.lights_out = False  # New attribute for lights checkbox
        self.is_searching = False
        self.search = 0
        self.search_speed = 0.4

        # Create font objects
        self.font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
        self.tutorial_font = pygame.font.SysFont('Lucida Console', 12)  # Font for tutorial text
        self.font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
        self.dead_font = pygame.font.SysFont('Arial Black', 72)  # Biggest font for GAME OVER

    def draw_status_bar(self):
        # Draw the status bar at the top
        bar_rect = pygame.Rect(0, 0, BasicTile.BOARD_WIDTH, BasicTile.HEIGHT_OFFSET)
        pygame.draw.rect(self.level.game_board, (50, 50, 50), bar_rect)  # Dark gray color for the bar

        # Set caption and render the text inside the status bar
        if self.game and self.is_playing:
            # Set window caption
            pygame.display.set_caption(f'Escape the Werehouse! - {self.level.map_title[1][self.current_level]}')
            # Set status bar
            moves_text = self.font.render(f'Moves: {self.moves}', True, (255, 255, 255))
            total_moves_text = self.font.render(f'Total Moves: {self.total_moves}', True, (255, 255, 255))
            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            # Render status bar
            self.level.game_board.blit(moves_text, (10, 10))
            self.level.game_board.blit(total_moves_text, (200, 10))
            self.level.game_board.blit(lives_text, (480, 10))
        elif self.is_playing:
            # Set window caption
            pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {self.current_level + 1}')
            # Set status bar
            tutorial_text = self.tutorial_font.render(f'{self.level.map_title[0][self.current_level]}', True, (255, 255, 255))
            # Render status bar
            self.level.game_board.blit(tutorial_text, (15, 15))

    def check_level_complete(self):
        # Check if player is on exit tile
        for element in self.level.elements:
            if element[0] == BasicTile.EXIT:
                if (self.level.px, self.level.py) == element[1]:  # Player position matches exit position
                    self.travel = 0
                    return True

        return False

    # Handle actions when a level is completed
    def handle_level_complete(self, high_scores):
        # Render one last frame with player on exit
        self.__blit_level_elements__()

        # Show score for completed level
        if self.game:
            pygame.display.set_caption(f'Escape the Werehouse!')

            # Draw the status bar at the top
            bar_rect = pygame.Rect(0, 0, BasicTile.BOARD_WIDTH, BasicTile.HEIGHT_OFFSET)
            pygame.draw.rect(self.level.game_board, (50, 50, 50), bar_rect)  # Dark gray color for the bar

            # Render the text inside the bar
            moves_text = self.font.render(f'Moves: {self.moves}', True, (255, 255, 255))
            total_moves_text = self.font.render(f'Total Moves: {self.total_moves}', True, (255, 255, 255))
            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.level.game_board.blit(moves_text, (10, 10))
            self.level.game_board.blit(total_moves_text, (200, 10))
            self.level.game_board.blit(lives_text, (480, 10))

            # Blit stars
            self.level.blit_stars(self)

        pygame.display.flip()
        pygame.time.wait(300)

        # Increment level counter
        self.current_level += 1
        self.moves = 0
        self.new_level = True

        # Handle mode transitions
        if self.game == False and self.current_level >= 4:
            # Debug statement
            print('Well done, you finished the Tutorials! Now try to Escape the Werehouse!')
            # Set game states
            self.game = True
            self.current_level = 0
            self.moves = 0
            self.total_moves = 0
            self.lives = 3
        elif self.game == True and self.current_level >= self.level.no_of_levels[1]:
            # Debug statements
            print('Congratulations! You finished the last level!')
            print(f'Your have made a total of {self.total_moves} successful moves!')
            # End game
            self.is_playing = False
            if high_scores.is_high_score(self.total_moves):
                initials = high_scores.get_initials()
                high_scores.add_score(self.total_moves, initials)

            print("Displaying high scores...")  # Debug statement
            high_scores.display_scores()

    def reset_movement_variables(self):
        """
        Reset the game state variables related to movement at the start of each frame.
        """
        self.direction = None  # Reset the movement direction
        self.travel = 0  # Reset the travel distance

    def set_search_direction(self, direction):
        """
        Set the search direction and activate searching mode.
        """
        self.search_speed = 0.1
        self.search = direction  # Set the search direction
        self.is_searching = True  # Activate searching mode

    def set_movement_direction(self, movement):
        """
        Set the movement direction and travel distance based on the movement input.
        """
        self.direction = movement['direction']  # Set the movement direction
        self.travel = movement['travel']  # Set the travel distance

    def update_facing_direction(self, movement):
        """
        Update the player's facing direction and set searching properties.
        """
        self.facing_direction = movement['direction']  # Update the facing direction
        self.search = movement['search']  # Set the search direction
        self.is_searching = True  # Activate searching mode

    # Check if a box has fallen into a pit and update states accordingly
    def check_box_in_pit(self, box_num, bx, by):
        # Mapping of pit types to their corresponding attributes
        pit_mapping = {
            BasicTile.PIT1: ('pit1', 'in_pit1'),
            BasicTile.PIT2: ('pit2', 'in_pit2'),
            BasicTile.PIT3: ('pit3', 'in_pit3'),
            BasicTile.PIT4: ('pit4', 'in_pit4'),
        }

        # Iterate over the elements of the level
        for element in self.level.elements:
            position, pit_type = element[1], element[0]

            # Check if the current element is a pit and matches the given coordinates
            if position == (bx, by) and pit_type in pit_mapping:
                pit_attr, in_pit_attr = pit_mapping[pit_type]

                # Only proceed if the pit is active
                if getattr(self.level, pit_attr):
                    # Deactivate the pit and set the box number in the pit
                    setattr(self.level, pit_attr, False)
                    setattr(self.level, in_pit_attr, box_num)
                    print(f"Box {box_num} fell into pit {pit_type}")  # Debug statement

                    if box_num == 1:
                        self.level.box1 = False
                    elif box_num == 2:
                        self.level.box2 = False
                    elif box_num == 3:
                        self.level.box3 = False
                    elif box_num == 4:
                        self.level.box4 = False
                    return True

                return False

    def check_player_in_pit(self, x, y, audio):
        if self.player_in_pit:
            return False

        for element in self.level.elements:
            if element[1] == (x, y):
                if element[0] in [BasicTile.PIT1, BasicTile.PIT2, BasicTile.PIT3, BasicTile.PIT4]:
                    # Check if pit is not filled (active)
                    if ((element[0] == BasicTile.PIT1 and self.level.pit1) or
                        (element[0] == BasicTile.PIT2 and self.level.pit2) or
                        (element[0] == BasicTile.PIT3 and self.level.pit3) or
                        (element[0] == BasicTile.PIT4 and self.level.pit4)):
                        # Player fell in pit
                        audio.play_sound('fall')
                        self.lives -= 1
                        self.player_in_pit = True
                        # Reset player movement
                        self.travel = 0

                        # Update player position to the pit
                        self.level.px, self.level.py = x, y

                        self.__blit_level_elements__()

                        # Debug statement to check player position
                        print(f"Blitting player at pit position: ({self.level.px}, {self.level.py})")

                        pygame.display.flip()

                        # Fade out effect
                        self.level.fade_out(self)

                        if self.lives <= 0:
                            self.__display_game_over__()
                            self.is_playing = False
                        else:
                            # Reset level
                            self.new_level = True
                            self.total_moves += 1
                            self.moves = 0
                            self.prev_x, self.prev_y = self.level.px, self.level.py

                            return False

                        return True

    # Blit the level and boxes
    def __blit_level_elements__(self):
        self.level.game_board.fill((30, 30, 30))
        self.level.blit_level()
        self.level.blit_box_1(0, 0)
        self.level.blit_box_2(0, 0)
        self.level.blit_box_3(0, 0)
        self.level.blit_box_4(0, 0)
        self.level.blit_player(self, 0)
        # Draw the status bar at the top
        bar_rect = pygame.Rect(0, 0, BasicTile.BOARD_WIDTH, BasicTile.HEIGHT_OFFSET)
        pygame.draw.rect(self.level.game_board, (50, 50, 50), bar_rect)  # Dark gray color for the bar

    # Show GAME OVER screen when out of lives
    def __display_game_over__(self):
        # Clear the screen
        self.level.game_board.fill((10, 10, 10))
        pygame.display.set_caption('GAME OVER')
        # Render "GAME OVER" text
        game_over_text = self.dead_font.render('GAME OVER', True, (220, 0, 10))
        game_over_center = game_over_text.get_rect(center=(self.level.game_board.get_width() // 2, 200))
        self.level.game_board.blit(game_over_text, game_over_center)

        # Update the display
        pygame.display.flip()

        # Wait for a few seconds before returning to the start screen
        pygame.time.wait(3000)
