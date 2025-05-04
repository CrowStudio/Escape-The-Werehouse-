import pygame
from game_board.elements import gfx
import random
from collections import deque
import os
import tkinter as tk
from tkinter import filedialog
import json

# Constants for tile types and their properties
TILE_TYPES = {
    'START': 'Start',
    'EXIT': 'Exit',
    'FLOOR': 'Floor',
    'PIT_WALL': 'Pit',
    'WALL': 'Wall',
    'PIT1': 'Pit1',
    'PIT2': 'Pit2',
    'PIT3': 'Pit3',
    'PIT4': 'Pit4',
    'BOX1': 'Box1',
    'BOX2': 'Box2',
    'BOX3': 'Box3',
    'BOX4': 'Box4'
}

TILE_IMAGES = {
    'START': gfx.start,
    'FLOOR': None,  # Will be randomly chosen when drawn
    'WALL': gfx.wall,
    'PIT1': gfx.pit,
    'PIT2': gfx.pit,
    'PIT3': gfx.pit,
    'PIT4': gfx.pit,
    'PIT_WALL': gfx.pit,
    'EXIT': gfx.exit,
    'BOX1': gfx.boxes[8],
    'BOX2': gfx.boxes[9],
    'BOX3': gfx.boxes[10],
    'BOX4': gfx.boxes[11]
}

TILE_BUTTON_COLORS = {
    'START': (255, 255, 255),
    'FLOOR': (211, 211, 211),
    'WALL': (0, 0, 0),
    'PIT1': (0, 0, 255),
    'PIT2': (0, 0, 255),
    'PIT3': (0, 0, 255),
    'PIT4': (0, 0, 255),
    'PIT_WALL': (0, 0, 139),
    'EXIT': (64, 224, 208),
    'BOX1': (165, 42, 42),
    'BOX2': (165, 42, 42),
    'BOX3': (165, 42, 42),
    'BOX4': (165, 42, 42)
}

class LevelEditor:
    def __init__(self, screen, level_map):
        self.screen = screen
        self.level_map = level_map
        self.rows = len(level_map)
        self.cols = len(level_map[0])
        self.current_tile = 'FLOOR'
        self.placed_tiles = self.initialize_placed_tiles()
        self.cell_size = 600 // max(self.rows, self.cols)
        self.file_path = os.path.join(os.path.dirname(__file__), 'game_board', 'maps', 'game_maps.json')
        self.initialize_pygame()
        self.initialize_floor_indices()
        self.initialize_under_tiles()
        self.loaded_levels = []
        self.current_level_index = None
        self.running = True
        self.active_menu = None
        self.menu_items = {
            'File': ['Load Level', 'Save Level'],
            'Edit': ['Set Level Path'],
            'Randomize Map': ['Regenerate']
        }
        self.dropdown_active = False
        self.dropdown_index = 0
        self.save_dialog_active = False
        self.level_selection_active = False
        self.path_popup_active = False
        self.active_input = None
        self.last_clicked_button = self.tile_buttons['FLOOR']['rect']
        self.cursor_visible = True

    def initialize_placed_tiles(self):
        return {tile: False for tile in ['PIT1', 'PIT2', 'PIT3', 'PIT4', 'BOX1', 'BOX2', 'BOX3', 'BOX4', 'START', 'EXIT']}

    def initialize_pygame(self):
        pygame.init()
        self.pit_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.header_font = pygame.font.SysFont('Lucida Console', 18)
        self.path_font = pygame.font.SysFont('Lucida Console', 10)
        self.button_font = pygame.font.SysFont('Lucida Console', 12)
        self.input_font = pygame.font.SysFont('Arial', 24)
        self.menu_font = pygame.font.SysFont('Arial', 20)
        self.tile_buttons = self.create_tile_buttons()

    def create_tile_buttons(self):
        tile_buttons = {}
        button_width, button_height = 40, 15
        button_margin = 5
        x, y = button_margin, 669 + button_margin
        for tile_type, tile_name in TILE_TYPES.items():
            bg_color = TILE_BUTTON_COLORS[tile_type]
            fg_color = 'white' if sum(bg_color) < 384 else 'black'
            button_rect = pygame.Rect(x, y, button_width, button_height)
            tile_buttons[tile_type] = {
                'rect': button_rect,
                'color': bg_color,
                'text': tile_name,
                'text_color': fg_color,
                'action': lambda t=tile_type: self.set_current_tile(t)
            }
            x += button_width + button_margin
            if tile_name in ['Exit', 'Pit as Wall', 'Pit4']:
                x += button_margin
        return tile_buttons

    def initialize_floor_indices(self):
        self.floor_indices = [[random.randint(0, len(gfx.floor) - 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def initialize_under_tiles(self):
        self.under_tiles = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def start_rendering_loop(self):
        self.running = True
        while self.running:
            self.draw_screen()
            self.handle_pygame_events()
            pygame.display.flip()

    def handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.save_dialog_active:
                    save_dialog_rect = pygame.Rect(100, 150, 400, 350)
                    if not save_dialog_rect.collidepoint(event.pos):
                        self.save_dialog_active = False
                        return
                if self.level_selection_active:
                    level_selection_rect = pygame.Rect(100, 150, 400, 200)
                    if not level_selection_rect.collidepoint(event.pos):
                        self.level_selection_active = False
                        return
                if self.path_popup_active:
                    path_popup_rect = pygame.Rect(100, 150, 400, 150)
                    if not path_popup_rect.collidepoint(event.pos):
                        self.path_popup_active = False
                        return
                if event.pos[1] > 665:
                    self.handle_button_click(event.pos)
                elif event.pos[1] > 0 and event.pos[1] < 30:
                    self.handle_menu_click(event.pos)
                elif self.active_menu:
                    menu_items = self.menu_items[self.active_menu]
                    menu_height = len(menu_items) * 30
                    menu_y_start = 30
                    menu_y_end = 30 + menu_height
                    if menu_y_start <= event.pos[1] <= menu_y_end:
                        self.handle_menu_click(event.pos)
                    else:
                        self.active_menu = None
                else:
                    self.on_tile_click(event.pos)

    def handle_button_click(self, pos):
        for tile_type, button in self.tile_buttons.items():
            if button['rect'].collidepoint(pos):
                button['action']()
                if tile_type in self.placed_tiles:
                    self.update_button_appearance(tile_type)
                self.last_clicked_button = button['rect']

    def handle_menu_click(self, pos):
        menu_rects = [
            pygame.Rect(0, 0, 100, 30),
            pygame.Rect(100, 0, 100, 30),
            pygame.Rect(200, 0, 150, 30)
        ]
        menus = ['File', 'Edit', 'Randomize Map']
        for rect, menu in zip(menu_rects, menus):
            if rect.collidepoint(pos):
                if self.active_menu == menu:
                    self.active_menu = None
                else:
                    self.active_menu = menu
                break
        if self.active_menu:
            menu_items = self.menu_items[self.active_menu]
            for i, item in enumerate(menu_items):
                item_rect = pygame.Rect(menu_rects[menus.index(self.active_menu)].x, 30 + i * 30, 150, 30)
                if item_rect.collidepoint(pos):
                    self.handle_menu_item_click(item)
                    self.active_menu = None
                    break

    def handle_menu_item_click(self, item):
        if item == 'Load Level':
            self.show_level_selection_dialog()
        elif item == 'Save Level':
            if not self.are_start_and_exit_tiles_placed():
                self.show_message("Save Error", "Both the Start and Exit tiles must be placed to save the level.")
                return
            self.show_save_dialog()
        elif item == 'Set Level Path':
            self.show_path_popup()
        elif item == 'Regenerate':
            self.regenerate_map()

    def show_level_selection_dialog(self):
        self.load_levels_from_json()
        self.level_selection_active = True
        self.current_level_index = 0
        while self.level_selection_active:
            self.draw_level_selection_dialog()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level_selection_active = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_level_selection_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_level_index = (self.current_level_index - 1) % len(self.loaded_levels)
                    elif event.key == pygame.K_DOWN:
                        self.current_level_index = (self.current_level_index + 1) % len(self.loaded_levels)
                    elif event.key == pygame.K_RETURN:
                        self.load_selected_level()

    def draw_level_selection_dialog(self):
        dialog_surface = pygame.Surface((400, 300))
        dialog_surface.fill((50, 50, 50))
        pygame.draw.rect(dialog_surface, (255, 255, 255), dialog_surface.get_rect().inflate(-10, -10), 2)

        title_text = self.header_font.render("Select Level", True, (255, 255, 255))
        dialog_surface.blit(title_text, (20, 20))

        for i, level in enumerate(self.loaded_levels):
            level_text = self.input_font.render(level['title'], True, (255, 255, 255))
            dialog_surface.blit(level_text, (20, 56 + i * 30))
            if i == self.current_level_index:
                pygame.draw.rect(dialog_surface, (255, 255, 255), (10, 55 + i * 30, 380, 30), 2)

        cancel_button_rect = pygame.Rect(260, 250, 100, 40)
        pygame.draw.rect(dialog_surface, (200, 0, 0), cancel_button_rect)
        cancel_button_text = self.button_font.render("Cancel", True, (255, 255, 255))
        dialog_surface.blit(cancel_button_text, cancel_button_text.get_rect(center=cancel_button_rect.center))

        self.screen.blit(dialog_surface, (100, 150))

    def handle_level_selection_click(self, pos):
        adjusted_pos = (pos[0] - 100, pos[1] - 150)

        for i in range(len(self.loaded_levels)):
            level_rect = pygame.Rect(10, 55 + i * 30, 380, 30)
            if level_rect.collidepoint(adjusted_pos):
                self.current_level_index = i
                self.load_selected_level()
                return

        cancel_button_rect = pygame.Rect(260, 250, 100, 40)
        if cancel_button_rect.collidepoint(adjusted_pos):
            self.level_selection_active = False

    def load_selected_level(self):
        if self.current_level_index is None:
            print("No level selected.")
            return

        if 0 <= self.current_level_index < len(self.loaded_levels):
            selected_level = self.loaded_levels[self.current_level_index]

            # Extract data from the selected level
            self.level_map = selected_level['map']
            self.active_boxes = selected_level['active_boxes']
            self.positions = selected_level['box_positions']
            self.player_start = selected_level['player_start']
            self.player_direction = selected_level['player_direction']
            self.active_exit = selected_level['exit_active']

            # Check if 'score' exists in the selected level
            self.level_score = selected_level.get('score', None)

            # Initialize other necessary attributes if needed
            self.initialize_floor_indices()
            self.initialize_under_tiles()

            # Reset placed tiles and update button appearances
            self.reset_placed_tiles()
            for tile_type, is_active in self.placed_tiles.items():
                if is_active:
                    self.update_button_appearance(tile_type)

            # Place the boxes based on their positions and active status
            for i, (position, active) in enumerate(zip(self.positions, self.active_boxes)):
                if active:
                    # Convert tuple position to string format if necessary
                    if isinstance(position, tuple):
                        position = f"t{position[0]//100+1}r{position[1]//100+1}"

                    # Convert position string to row and column indices
                    col, row = self.convert_position_to_indices(position)
                    if col is None or row is None:
                        continue
                    self.level_map[row][col] = f"BOX{i+1}"
                    self.placed_tiles[f"BOX{i+1}"] = True

                    # Place a FLOOR tile under the BOX
                    self.under_tiles[row][col] = 'FLOOR'

            # Update button appearances based on placed tiles
            for tile_type, is_placed in self.placed_tiles.items():
                self.update_button_appearance(tile_type)

            self.rows = len(self.level_map)
            self.cols = len(self.level_map[0])
            self.cell_size = 600 // max(self.rows, self.cols)

            self.draw_grid()

        self.level_selection_active = False

    def convert_position_to_indices(self, position):
        try:
            if isinstance(position, str):  # Handle string format "t1r1"
                if 't' not in position or 'r' not in position:
                    raise ValueError(f"Unexpected position format: {position}")
                col = int(position[position.index('t') + 1:position.index('r')]) - 1
                row = int(position[position.index('r') + 1:]) - 1
            elif isinstance(position, list) and len(position) == 2:  # Handle list format [0, 3]
                col, row = position
            else:
                raise ValueError(f"Unexpected position format: {position}")

            return col, row
        except ValueError as e:
            print(f"Error converting position to indices: {e}")
            return None, None

    def draw_button_frame(self, button_rect, color):
        if color:
            pygame.draw.rect(self.screen, color, button_rect.inflate(2, 2), 1)

    def update_button_appearance(self, tile_type):
        button = self.tile_buttons[tile_type]
        if self.placed_tiles[tile_type]:
            button['color'] = (100, 100, 100)
            button['text_color'] = (60, 60, 60)
        else:
            button['color'] = TILE_BUTTON_COLORS[tile_type]
            button['text_color'] = 'white' if sum(TILE_BUTTON_COLORS[tile_type]) < 384 else 'black'

    def draw_screen(self):
        self.screen.fill((30, 30, 30))
        self.draw_menu_field()
        self.draw_info_field()
        self.draw_button_field()
        self.draw_buttons()
        self.draw_grid()
        self.draw_active_menu()
        if self.path_popup_active:
            self.draw_path_popup()

    def draw_menu_field(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, 600, 30))
        menu_items = ['File', 'Edit', 'Randomize Map']
        for i, item in enumerate(menu_items):
            text = self.menu_font.render(item, True, (0, 0, 0))
            self.screen.blit(text, (10 + i * 100, 5))

    def draw_info_field(self):
        pygame.draw.rect(self.screen, (50, 50, 50), pygame.Rect(0, 30, 600, 40))
        header = self.header_font.render('Add Elements or Edit map!', True, (255, 255, 255))
        self.screen.blit(header, (10, 42))

    def draw_button_field(self):
        for button in self.tile_buttons.values():
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            text_surface = self.button_font.render(button['text'], True, button['text_color'])
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_tile(row, col)

    def draw_tile(self, row, col):
        x0, y0 = col * self.cell_size, row * self.cell_size + 70
        tile_type = self.level_map[row][col]
        self.draw_under_tile(row, col, x0, y0)
        self.draw_top_tile(tile_type, x0, y0)

    def draw_under_tile(self, row, col, x0, y0):
        tile_type = self.level_map[row][col]
        if "BOX" in tile_type and self.under_tiles[row][col]:
            under_type = self.under_tiles[row][col]
            if under_type == 'FLOOR':
                floor_image = gfx.floor[self.floor_indices[row][col]]
                self.screen.blit(floor_image, (x0, y0))
            else:
                self.screen.blit(TILE_IMAGES[under_type], (x0, y0))
        elif tile_type == 'FLOOR':
            floor_image = gfx.floor[self.floor_indices[row][col]]
            self.screen.blit(floor_image, (x0, y0))

    def draw_top_tile(self, tile_type, x0, y0):
        if "BOX" in tile_type:
            self.screen.blit(TILE_IMAGES[tile_type], (x0, y0))
        elif tile_type != 'FLOOR':
            self.screen.blit(TILE_IMAGES[tile_type], (x0, y0))
        if tile_type in ['PIT1', 'PIT2', 'PIT3', 'PIT4']:
            self.add_pit_number(tile_type, x0, y0)

    def draw_buttons(self):
        for button in self.tile_buttons.values():
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            text_surface = self.button_font.render(button['text'], True, button['text_color'])
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
            if button['rect'] == self.last_clicked_button:
                self.draw_button_frame(button['rect'], (255, 102, 102))

    def draw_active_menu(self):
        if self.active_menu:
            menu_items = self.menu_items[self.active_menu]
            menu_width = 150
            menu_height = len(menu_items) * 30

            if self.active_menu == 'File':
                menu_x = 0
            elif self.active_menu == 'Edit':
                menu_x = 100
            elif self.active_menu == 'Randomize Map':
                menu_x = 200

            menu_y = 30
            menu_surface = pygame.Surface((menu_width, menu_height))
            menu_surface.fill((150, 150, 150))
            for i, item in enumerate(menu_items):
                text = self.menu_font.render(item, True, (0, 0, 0))
                menu_surface.blit(text, (10, 3 + i * 30))
            self.screen.blit(menu_surface, (menu_x, menu_y))

    def on_tile_click(self, pos):
        if pos[0] >= 600 or pos[1] >= 670:
            return
        col, row = pos[0] // self.cell_size, (pos[1] - 70) // self.cell_size
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        self.update_tile(row, col)

    def update_tile(self, row, col):
        previous_tile = self.level_map[row][col]
        if previous_tile in self.placed_tiles and self.placed_tiles[previous_tile]:
            self.placed_tiles[previous_tile] = False
            if previous_tile in self.placed_tiles:
                self.update_button_appearance(previous_tile)

        if self.is_unique_tile(self.current_tile):
            self.handle_unique_tile_placement(row, col, previous_tile)
        else:
            self.handle_repeatable_tile_placement(row, col)

        self.draw_tile(row, col)

        if self.current_tile in self.placed_tiles:
            self.update_button_appearance(self.current_tile)

    def is_unique_tile(self, tile_type):
        return "BOX" in tile_type or tile_type.startswith("PIT") or tile_type in ['START', 'EXIT']

    def handle_unique_tile_placement(self, row, col, previous_tile):
        if not self.under_tiles[row][col]:
            self.under_tiles[row][col] = previous_tile

        if self.current_tile in self.placed_tiles and self.placed_tiles[self.current_tile]:
            return

        self.level_map[row][col] = self.current_tile
        if self.current_tile in self.placed_tiles:
            self.placed_tiles[self.current_tile] = True

    def handle_repeatable_tile_placement(self, row, col):
        self.level_map[row][col] = self.current_tile
        if self.current_tile == 'FLOOR':
            self.floor_indices[row][col] = random.randint(0, len(gfx.floor) - 1)

    def add_pit_number(self, tile_type, x0, y0):
        number = tile_type[-1]
        text = self.pit_font.render(number, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x0 + self.cell_size // 2, y0 + self.cell_size // 2))
        self.screen.blit(text, text_rect)

    def set_current_tile(self, tile_type):
        self.current_tile = tile_type

    def save_level(self):
        if not self.are_start_and_exit_tiles_placed():
            self.show_message("Save Error", "Both the Start and Exit tiles must be placed to save the level.")
            return
        self.show_save_dialog()

    def are_start_and_exit_tiles_placed(self):
        start_tile_placed = any(tile == 'START' for row in self.level_map for tile in row)
        exit_tile_placed = any(tile == 'EXIT' for row in self.level_map for tile in row)
        return start_tile_placed and exit_tile_placed

    def show_message(self, title, message):
        dialog = pygame.Surface((500, 150))
        dialog.fill((50, 50, 50))
        pygame.draw.rect(dialog, (255, 255, 255), dialog.get_rect().inflate(-10, -10), 2)
        title_text = self.header_font.render(title, True, (255, 255, 255))
        message_text = self.path_font.render(message, True, (255, 255, 255))
        dialog.blit(title_text, (20, 20))
        dialog.blit(message_text, (20, 60))
        self.screen.blit(dialog, (50, 150))
        pygame.display.flip()
        pygame.time.wait(2000)

    def show_save_dialog(self):
        self.save_dialog_active = True
        if self.current_level_index is not None:
            selected_level = self.loaded_levels[self.current_level_index]
            self.save_dialog_inputs = {
                'level_number': str(selected_level['level']),
                'level_name': selected_level['title'],
                'player_direction': selected_level['player_direction'],
                'moves_for_3_stars': str(selected_level.get('score', ''))
            }
        else:
            self.save_dialog_inputs = {
                'level_number': '',
                'level_name': '',
                'player_direction': 'up',
                'moves_for_3_stars': ''
            }
        while self.save_dialog_active:
            self.draw_save_dialog()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_dialog_active = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_save_dialog_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_save_dialog_keydown(event)

    def draw_save_dialog(self):
        dialog_surface = pygame.Surface((400, 360))
        dialog_surface.fill((50, 50, 50))
        pygame.draw.rect(dialog_surface, (255, 255, 255), dialog_surface.get_rect().inflate(-10, -10), 2)

        title_text = self.header_font.render("Save Level", True, (255, 255, 255))
        dialog_surface.blit(title_text, (20, 20))

        self.draw_input_field(dialog_surface, "Level Number:", 60, self.save_dialog_inputs['level_number'], 'level_number')
        self.draw_input_field(dialog_surface, "Level Name:", 100, self.save_dialog_inputs['level_name'], 'level_name')
        self.draw_dropdown(dialog_surface, "Player Direction:", 140, self.save_dialog_inputs['player_direction'], ['up', 'down', 'left', 'right'], self.dropdown_active)
        self.draw_input_field(dialog_surface, "Moves for 3 Stars:", 180, self.save_dialog_inputs['moves_for_3_stars'], 'moves_for_3_stars')

        save_button_rect = pygame.Rect(150, 300, 100, 40)
        pygame.draw.rect(dialog_surface, (0, 200, 0), save_button_rect)
        save_button_text = self.button_font.render("Save", True, (255, 255, 255))
        dialog_surface.blit(save_button_text, save_button_text.get_rect(center=save_button_rect.center))

        cancel_button_rect = pygame.Rect(260, 300, 100, 40)
        pygame.draw.rect(dialog_surface, (200, 0, 0), cancel_button_rect)
        cancel_button_text = self.button_font.render("Cancel", True, (255, 255, 255))
        dialog_surface.blit(cancel_button_text, cancel_button_text.get_rect(center=cancel_button_rect.center))

        if self.dropdown_active:
            for i, option in enumerate(self.save_dialog_inputs['player_direction_options']):
                option_rect = pygame.Rect(180, 170 + i * 30, 200, 30)
                pygame.draw.rect(dialog_surface, (80, 80, 80), option_rect)
                option_text = self.input_font.render(option, True, (255, 255, 255))
                dialog_surface.blit(option_text, (option_rect.x + 5, option_rect.y))
                if option == self.save_dialog_inputs['player_direction']:
                    pygame.draw.rect(dialog_surface, (255, 255, 255), option_rect, 2)

        # Draw the cursor if an input field is active
        if self.active_input:
            input_rect = self.save_dialog_inputs[f'{self.active_input}_rect']
            cursor_x = input_rect.x + 5 + self.input_font.size(self.save_dialog_inputs[self.active_input])[0]
            cursor = pygame.Rect(cursor_x, input_rect.y + 2, 2, input_rect.height - 4)
            pygame.draw.rect(dialog_surface, (255, 255, 255), cursor)

        self.screen.blit(dialog_surface, (100, 150))

    def handle_save_dialog_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self.save_level_data()
        elif event.key == pygame.K_BACKSPACE:
            if self.active_input in self.save_dialog_inputs:
                self.save_dialog_inputs[self.active_input] = self.save_dialog_inputs[self.active_input][:-1]
        else:
            if self.active_input in self.save_dialog_inputs:
                self.save_dialog_inputs[self.active_input] += event.unicode

    def handle_save_dialog_click(self, pos):
        adjusted_pos = (pos[0] - 100, pos[1] - 150)
        if self.save_dialog_inputs['level_number_rect'].collidepoint(adjusted_pos):
            self.active_input = 'level_number'
        elif self.save_dialog_inputs['level_name_rect'].collidepoint(adjusted_pos):
            self.active_input = 'level_name'
        elif self.save_dialog_inputs['moves_for_3_stars_rect'].collidepoint(adjusted_pos):
            self.active_input = 'moves_for_3_stars'
        elif self.save_dialog_inputs['player_direction_rect'].collidepoint(adjusted_pos):
            self.toggle_dropdown()
        elif self.dropdown_active and self.save_dialog_inputs['player_direction_options']:
            for i, option in enumerate(self.save_dialog_inputs['player_direction_options']):
                option_rect = pygame.Rect(180, 170 + i * 30, 200, 30)
                if option_rect.collidepoint(adjusted_pos):
                    self.save_dialog_inputs['player_direction'] = option
                    self.dropdown_active = False
                    break
        elif pygame.Rect(150, 290, 100, 40).collidepoint(adjusted_pos):
            self.save_level_data()
        elif pygame.Rect(260, 290, 100, 40).collidepoint(adjusted_pos):
            self.save_dialog_active = False

    def draw_input_field(self, surface, label, y, value, key):
        label_text = self.input_font.render(label, True, (255, 255, 255))
        surface.blit(label_text, (20, y))
        input_rect = pygame.Rect(180, y, 200, 30)
        pygame.draw.rect(surface, (255, 255, 255), input_rect, 2)
        input_text = self.input_font.render(value, True, (255, 255, 255))
        surface.blit(input_text, (input_rect.x + 5, input_rect.y + 1))
        self.save_dialog_inputs[key + '_rect'] = input_rect

    def draw_dropdown(self, surface, label, y, value, options, is_active=False):
        label_text = self.input_font.render(label, True, (255, 255, 255))
        surface.blit(label_text, (20, y))
        dropdown_rect = pygame.Rect(180, y, 200, 30)
        pygame.draw.rect(surface, (50, 50, 50), dropdown_rect)
        dropdown_text = self.input_font.render(value, True, (255, 255, 255))
        surface.blit(dropdown_text, (dropdown_rect.x + 5, dropdown_rect.y))
        self.save_dialog_inputs['player_direction_rect'] = dropdown_rect
        self.save_dialog_inputs['player_direction_options'] = options

    def handle_dropdown_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_dialog_inputs['player_direction_rect'].collidepoint(event.pos):
                self.toggle_dropdown()
            elif self.dropdown_active:
                for i, option in enumerate(self.save_dialog_inputs['player_direction_options']):
                    option_rect = pygame.Rect(180, 170 + i * 30, 200, 30)
                    if option_rect.collidepoint(event.pos):
                        self.save_dialog_inputs['player_direction'] = option
                        self.dropdown_active = False
                        break

    def handle_save_dialog_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self.save_level_data()
        elif event.key == pygame.K_BACKSPACE:
            if self.active_input in self.save_dialog_inputs:
                self.save_dialog_inputs[self.active_input] = self.save_dialog_inputs[self.active_input][:-1]
        else:
            if self.active_input in self.save_dialog_inputs:
                self.save_dialog_inputs[self.active_input] += event.unicode

    def toggle_dropdown(self):
        self.dropdown_active = not self.dropdown_active

    def save_level_data(self):
        level_number = self.save_dialog_inputs['level_number']
        level_name = self.save_dialog_inputs['level_name']
        player_direction = self.save_dialog_inputs['player_direction']
        moves_for_3_stars = self.save_dialog_inputs['moves_for_3_stars']

        if not level_number or not level_name or not moves_for_3_stars:
            self.show_message("Input Error", "All fields must be filled.")
            return

        file_path = self.file_path

        # Format the level data
        formatted_level_data = self.format_level_data_for_saving(level_number, level_name, player_direction, moves_for_3_stars)

        self.write_level_to_file(file_path, formatted_level_data)
        self.show_message("Level Saved", f"The level '{level_name}' has been appended to the JSON file.")
        self.regenerate_map()
        self.save_dialog_active = False

    def are_start_and_exit_tiles_placed(self):
        start_tile_placed = any(tile == 'START' for row in self.level_map for tile in row)
        exit_tile_placed = any(tile == 'EXIT' for row in self.level_map for tile in row)
        return start_tile_placed and exit_tile_placed

    def format_level_data_for_saving(self, level_number, level_name, player_direction, moves_for_3_stars):
        # Construct the level_map without the box tiles
        saved_level_map = [
            [self.under_tiles[row_idx][col_idx] if self.level_map[row_idx][col_idx] in ["BOX1", "BOX2", "BOX3", "BOX4"] else tile
             for col_idx, tile in enumerate(row)]
            for row_idx, row in enumerate(self.level_map)
        ]

        return {
            "level_number": int(level_number),
            "level_name": level_name,
            "player_direction": player_direction,
            "moves_for_3_stars": int(moves_for_3_stars),
            "map": saved_level_map,
            "active_boxes": self.get_active_boxes(),
            "box_positions": self.get_box_positions(),
            "player_start": self.get_player_start_position(),
        }

    def get_active_boxes(self):
        # Determine the active state of each box
        return [any(tile == f"BOX{i+1}" for row in self.level_map for tile in row) for i in range(4)]

    def get_box_positions(self):
        box_positions = [[0, 0], [0, 0], [0, 0], [0, 0]]
        for row_idx, row in enumerate(self.level_map):
            for col_idx, tile in enumerate(row):
                if tile == "BOX1":
                    box_positions[0] = [col_idx, row_idx]
                    self.under_tiles[row_idx][col_idx] = 'FLOOR'  # Save the element under the box
                elif tile == "BOX2":
                    box_positions[1] = [col_idx, row_idx]
                    self.under_tiles[row_idx][col_idx] = 'FLOOR'  # Save the element under the box
                elif tile == "BOX3":
                    box_positions[2] = [col_idx, row_idx]
                    self.under_tiles[row_idx][col_idx] = 'FLOOR'  # Save the element under the box
                elif tile == "BOX4":
                    box_positions[3] = [col_idx, row_idx]
                    self.under_tiles[row_idx][col_idx] = 'FLOOR'  # Save the element under the box
        return box_positions

    def get_player_start_position(self):
        for row_idx, row in enumerate(self.level_map):
            for col_idx, tile in enumerate(row):
                if tile == 'START':
                    return [col_idx, row_idx]
        return None

    def show_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialdir=os.path.dirname(self.file_path),
            initialfile='game_maps.json',
            title="Select Level Path"
        )
        root.destroy()
        return file_path

    def write_level_to_file(self, file_path, formatted_level_data):
        with open(file_path, 'r') as file:
            data = json.load(file)

        new_level = {
            "level": formatted_level_data['level_number'],
            "title": formatted_level_data['level_name'],
            "map": formatted_level_data['map'],
            "active_boxes": formatted_level_data['active_boxes'],
            "box_positions": formatted_level_data['box_positions'],
            "player_start": formatted_level_data['player_start'],
            "player_direction": formatted_level_data['player_direction'],
            "exit_active": True,
            "score": formatted_level_data['moves_for_3_stars'] if 'moves_for_3_stars' in formatted_level_data else None
        }

        data['levels'].append(new_level)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def format_level_map(self):
        level_map_str = ""
        for row_idx, row in enumerate(self.level_map):
            row_str = ','.join(['FLOOR' if tile in ['BOX1', 'BOX2', 'BOX3', 'BOX4'] else tile for tile in row])
            if row_idx == 0:
                level_map_str += f"    {row_str},\\n"
            elif row_idx == len(self.level_map) - 1:
                level_map_str += f"    {row_str}\\n"
            else:
                level_map_str += f"    {row_str},\\n"
        return level_map_str

    def find_unoccupied_floor_tile(self, box_positions):
        modified_map = [['WALL' if tile in ['BOX1', 'BOX2', 'BOX3', 'BOX4'] else tile for tile in row] for row in self.level_map]
        for row_idx, row in enumerate(modified_map):
            for col_idx, tile in enumerate(row):
                if tile == 'WALL' and f"t{col_idx+1}r{row_idx+1}" not in box_positions.values():
                    return f"t{col_idx+1}r{row_idx+1}"
        return None

    def set_level_path(self):
        self.show_path_popup()

    def show_path_popup(self):
        self.path_popup_active = True
        while self.path_popup_active:
            self.draw_path_popup()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.path_popup_active = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_path_popup_click(event.pos)

    def draw_path_popup(self):
        dialog_surface = pygame.Surface((550, 150))
        dialog_surface.fill((50, 50, 50))
        pygame.draw.rect(dialog_surface, (255, 255, 255), dialog_surface.get_rect().inflate(-10, -10), 2)
        title_text = self.header_font.render("Current Level Path:", True, (255, 255, 255))
        dialog_surface.blit(title_text, (20, 20))
        path_text = self.path_font.render(self.file_path if self.file_path else "No path set", True, (255, 255, 255))
        dialog_surface.blit(path_text, (20, 60))
        update_button_rect = pygame.Rect(50, 100, 120, 40)
        pygame.draw.rect(dialog_surface, (0, 200, 0), update_button_rect)
        update_button_text = self.button_font.render("Update Path", True, (255, 255, 255))
        dialog_surface.blit(update_button_text, update_button_text.get_rect(center=update_button_rect.center))
        close_button_rect = pygame.Rect(230, 100, 120, 40)
        pygame.draw.rect(dialog_surface, (200, 0, 0), close_button_rect)
        close_button_text = self.button_font.render("Close", True, (255, 255, 255))
        dialog_surface.blit(close_button_text, close_button_text.get_rect(center=close_button_rect.center))
        self.screen.blit(dialog_surface, (25, 150))

    def handle_path_popup_click(self, pos):
        adjusted_pos = (pos[0] - 100, pos[1] - 150)
        if pygame.Rect(50, 100, 120, 40).collidepoint(adjusted_pos):
            self.update_level_path()
        elif pygame.Rect(230, 100, 120, 40).collidepoint(adjusted_pos):
            self.path_popup_active = False

    def update_level_path(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialdir=os.path.dirname(self.file_path),
            initialfile='game_maps.json',
            title="Select Level Path"
        )
        root.destroy()
        if file_path:
            self.file_path = file_path
            self.load_levels_from_json()

    def load_levels_from_json(self):
        try:
            with open(self.file_path, 'r') as file:
                level_data = json.load(file)

            if 'levels' not in level_data:
                print("Error: Missing key 'levels' in JSON data")
                return

            self.loaded_levels = level_data['levels']

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e.msg} at line {e.lineno} column {e.colno}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def reset_placed_tiles(self):
        self.placed_tiles = {tile: False for tile in self.placed_tiles}

        for row in self.level_map:
            for tile in row:
                if tile in self.placed_tiles and not self.placed_tiles[tile]:
                    self.placed_tiles[tile] = True

    def regenerate_map(self):
        self.level_map, self.floor_indices = generate_random_map(self.rows, self.cols)
        self.draw_grid()
        self.reset_placed_tiles()

        # Clear save dialog fields
        self.save_dialog_inputs = {
            'level_number': '',
            'level_name': '',
            'player_direction': 'up',
            'moves_for_3_stars': ''
        }

        # Reset button appearances
        for tile_type in self.placed_tiles:
            self.update_button_appearance(tile_type)

        # Reset the current level index
        self.current_level_index = None

def generate_random_map(rows, cols, max_attempts=1000):
    def is_connected(level_map):
        def bfs(start):
            queue = deque([start])
            visited = set()
            while queue:
                x, y = queue.popleft()
                if (x, y) in visited:
                    continue
                visited.add((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and level_map[nx][ny] == 'FLOOR':
                        queue.append((nx, ny))
            return visited

        start_floors = [(i, j) for i in range(rows) for j in range(cols) if level_map[i][j] == 'FLOOR']
        if not start_floors:
            return False

        visited_floors = bfs(start_floors[0])
        return len(visited_floors) == len(start_floors)

    for attempt in range(max_attempts):
        level_map = [['WALL' for _ in range(cols)] for _ in range(rows)]
        start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1)
        level_map[start_x][start_y] = 'FLOOR'
        queue = deque([(start_x, start_y)])

        while queue:
            x, y = queue.popleft()
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and level_map[nx][ny] == 'WALL':
                    level_map[nx][ny] = 'FLOOR'
                    queue.append((nx, ny))
                    if len(queue) >= rows * cols // 3:
                        break

        floor_tiles = [(i, j) for i in range(rows) for j in range(cols) if level_map[i][j] == 'FLOOR']
        random.shuffle(floor_tiles)
        for i, j in floor_tiles:
            if random.random() < 0.3:
                level_map[i][j] = 'WALL'
                if not is_connected(level_map):
                    level_map[i][j] = 'FLOOR'

        if is_connected(level_map):
            floor_indices = [[random.randint(0, len(gfx.floor) - 1) for _ in range(cols)] for _ in range(rows)]
            return level_map, floor_indices

    level_map = [['WALL' for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows-1 or j == 0 or j == cols-1:
                level_map[i][j] = 'WALL'
            else:
                level_map[i][j] = 'FLOOR'
    floor_indices = [[random.randint(0, len(gfx.floor) - 1) for _ in range(cols)] for _ in range(rows)]
    return level_map, floor_indices

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 695))
    pygame.display.set_caption("Level Editor")

    level_map, floor_indices = generate_random_map(6, 6)
    editor = LevelEditor(screen, level_map)

    editor.start_rendering_loop()

    pygame.quit()

if __name__ == "__main__":
    main()
