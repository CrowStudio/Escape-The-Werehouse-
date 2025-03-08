import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
from collections import deque

# Define tile types and colors for visualization
TILE_TYPES = {
    'START': 'Start',
    'EXIT': 'Exit',
    'FLOOR': 'Floor',
    'WALL': 'Wall',
    'PIT_WALL': 'Pit as Wall',
    'PIT1': 'Pit1',
    'PIT2': 'Pit2',
    'PIT3': 'Pit3',
    'PIT4': 'Pit4',
    'BOX1': 'Box1',
    'BOX2': 'Box2',
    'BOX3': 'Box3',
    'BOX4': 'Box4'
}

TILE_COLORS = {
    'START': 'white',
    'FLOOR': 'light grey',
    'WALL': 'black',
    'PIT1': 'blue',
    'PIT2': 'blue',
    'PIT3': 'blue',
    'PIT4': 'blue',
    'PIT_WALL': 'dark blue',
    'EXIT': 'turquoise',
    'BOX1': 'brown',
    'BOX2': 'brown',
    'BOX3': 'brown',
    'BOX4': 'brown'
}

class LevelEditor:
    def __init__(self, root, level_map):
        """
        Initialize the LevelEditor with a root window and a level map.
        """
        self.root = root
        self.level_map = level_map
        self.rows = len(level_map)
        self.cols = len(level_map[0])
        self.current_tile = 'FLOOR'
        self.placed_tiles = {'PIT1': False, 'PIT2': False, 'PIT3': False, 'PIT4': False,
                             'BOX1': False, 'BOX2': False, 'BOX3': False, 'BOX4': False}

        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        self.draw_grid()
        self.bind_events()

        # Create a frame for controls
        controls_frame = tk.Frame(root)
        controls_frame.pack()

        # Add tile selection buttons
        self.tile_buttons = {}
        for tile_type, tile_name in TILE_TYPES.items():
            bg_color = TILE_COLORS[tile_type]
            fg_color = 'white' if bg_color in ['black', 'dark blue', 'blue', 'brown'] else 'black'
            button = tk.Button(controls_frame, text=tile_name, bg=bg_color, fg=fg_color, command=lambda t=tile_type: self.set_current_tile(t))
            button.pack(side=tk.LEFT)
            self.tile_buttons[tile_type] = button

            # Add space between EXIT and FLOOR, and PIT_WALL and PIT1
            if tile_name == 'Exit':
                spacer = tk.Label(controls_frame, text="     ")  # Add a single space after EXIT
                spacer.pack(side=tk.LEFT)
            elif tile_name == 'Pit as Wall':
                spacer = tk.Label(controls_frame, text="     ")  # Add a single space after PIT_WALL
                spacer.pack(side=tk.LEFT)

        # Add a spacer label to create space between tile buttons and save button
        spacer = tk.Label(controls_frame, text="     ")  # Reduced number of spaces
        spacer.pack(side=tk.LEFT)

        # Add save button
        save_button = tk.Button(controls_frame, text="Save Level", bg='dark green', fg='white', command=self.save_level)
        save_button.pack(side=tk.LEFT)

    def draw_grid(self):
        """
        Draw the grid on the canvas based on the level map.
        """
        cell_size = 600 // max(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                tile_type = self.level_map[row][col]
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=TILE_COLORS[tile_type], outline='black')
                self.add_tile_number(tile_type, x0, y0, x1, y1)

    def bind_events(self):
        """
        Bind mouse click events to the canvas.
        """
        self.canvas.bind('<Button-1>', self.on_tile_click)

    def on_tile_click(self, event):
        """
        Handle tile click events to update the tile type.
        """
        cell_size = 600 // max(self.rows, self.cols)
        col = event.x // cell_size
        row = event.y // cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            previous_tile = self.level_map[row][col]
            if previous_tile in self.placed_tiles and self.placed_tiles[previous_tile]:
                self.placed_tiles[previous_tile] = False
                self.tile_buttons[previous_tile].config(state=tk.NORMAL)

            if self.current_tile not in ['FLOOR', 'WALL', 'PIT_WALL'] and not self.placed_tiles.get(self.current_tile, False):
                self.level_map[row][col] = self.current_tile
                self.placed_tiles[self.current_tile] = True
                self.tile_buttons[self.current_tile].config(state=tk.DISABLED)
                self.update_tile(row, col)
            elif self.current_tile in ['FLOOR', 'WALL', 'PIT_WALL']:
                self.level_map[row][col] = self.current_tile
                self.update_tile(row, col)

    def update_tile(self, row, col):
        """
        Update the tile display on the canvas.
        """
        cell_size = 600 // max(self.rows, self.cols)
        x0, y0 = col * cell_size, row * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=TILE_COLORS[self.current_tile], outline='black')
        self.add_tile_number(self.current_tile, x0, y0, x1, y1)

    def add_tile_number(self, tile_type, x0, y0, x1, y1):
        """
        Add tile numbers or letters to the canvas for special tiles.
        """
        if tile_type in ['PIT1', 'PIT2', 'PIT3', 'PIT4']:
            number = tile_type[-1]  # Extract the last character, which is the number
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text='P' + number, font=('Arial', 24), fill='black')
        elif tile_type in ['BOX1', 'BOX2', 'BOX3', 'BOX4']:
            number = tile_type[-1]  # Extract the last character, which is the number
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text='B' + number, font=('Arial', 24), fill='black')
        elif tile_type == 'EXIT':
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text='EXIT', font=('Arial', 24), fill='black')
        elif tile_type == 'START':
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text='START', font=('Arial', 24), fill='black')

    def set_current_tile(self, tile_type):
        """
        Set the current tile type for placement.
        """
        self.current_tile = tile_type

    def save_level(self):
        """
        Save the current level map to a file and generate a new random map.
        """
        # Check if both START and EXIT tiles are placed
        start_tile_placed = any(tile == 'START' for row in self.level_map for tile in row)
        exit_tile_placed = any(tile == 'EXIT' for row in self.level_map for tile in row)

        if not start_tile_placed or not exit_tile_placed:
            messagebox.showwarning("Save Error", "Both the Start and Exit tiles must be placed to save the level.")
            return

        try:
            # Prompt the user to enter a level number
            level_number = simpledialog.askstring("Level Number", "Enter the number for this level:")
            if not level_number:
                messagebox.showwarning("Level Number", "Level number cannot be empty.")
                return

            # Prompt the user to enter a level name
            level_name = simpledialog.askstring("Level Name", "Enter the name for this level:")
            if not level_name:
                messagebox.showwarning("Level Name", "Level name cannot be empty.")
                return

            # Open a file dialog to select the Python file to append the level to
            file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
            if file_path:
                with open(file_path, 'a') as file:
                    # Start with two line breaks
                    file.write("\n\n# LEVEL {}\n".format(level_number))
                    file.write("# Level Title\n")
                    file.write("title.append('{}')\n\n".format(level_name))
                    file.write("# Map layout for tiles\n")
                    file.write("level_map.append([")

                    # Write the level map, replacing boxes with floor tiles
                    for row_idx, row in enumerate(self.level_map):
                        row_str = ','.join(['FLOOR' if tile in ['BOX1', 'BOX2', 'BOX3', 'BOX4'] else tile for tile in row])
                        if row_idx == 0:
                            file.write(f"{row_str},\n")
                        elif row_idx == len(self.level_map) - 1:
                            file.write(f"                  {row_str}])\n\n")
                        else:
                            file.write(f"                  {row_str},\n")

                    # Create a modified map with boxes replaced by floor tiles
                    modified_map = [
                        ['FLOOR' if tile in ['BOX1', 'BOX2', 'BOX3', 'BOX4'] else tile for tile in row]
                        for row in self.level_map]

                    # Determine the number of active boxes
                    box_count = sum(tile in ['BOX1', 'BOX2', 'BOX3', 'BOX4'] for row in self.level_map for tile in row)

                    # Write the active boxes setup
                    file.write("# Setup for active Boxes\n")
                    # Determine the status of each box
                    active_status = {
                        'BOX1': any(tile == 'BOX1' for row in self.level_map for tile in row),
                        'BOX2': any(tile == 'BOX2' for row in self.level_map for tile in row),
                        'BOX3': any(tile == 'BOX3' for row in self.level_map for tile in row),
                        'BOX4': any(tile == 'BOX4' for row in self.level_map for tile in row)}

                    # Create the active_boxes list in the correct order
                    active_boxes = [str(active_status['BOX1']).lower(), str(active_status['BOX2']).lower(), str(active_status['BOX3']).lower(), str(active_status['BOX4']).lower()]

                    file.write("active_boxes.append([{}])\n".format(', '.join(active_boxes)))

                    # Collect positions of each box type separately
                    box_positions = {'BOX1': None, 'BOX2': None, 'BOX3': None, 'BOX4': None}
                    for row_idx, row in enumerate(self.level_map):
                        for col_idx, tile in enumerate(row):
                            if tile in box_positions:
                                box_positions[tile] = f"t{col_idx+1}r{row_idx+1}"

                    # Find positions for inactive boxes
                    for box in ['BOX1', 'BOX2', 'BOX3', 'BOX4']:
                        if box_positions[box] is None:
                            # Find an unoccupied floor tile
                            for row_idx, row in enumerate(modified_map):
                                for col_idx, tile in enumerate(row):
                                    if tile == 'WALL' and f"t{col_idx+1}r{row_idx+1}" not in box_positions.values():
                                        box_positions[box] = f"t{col_idx+1}r{row_idx+1}"
                                        break
                                else:
                                    continue
                                break

                    # Write the positions in the order of box numbers
                    file.write("positions.append([{}])\n".format(', '.join(box_positions.values())))
                    file.write("\n")

                    # Write the player's starting point
                    file.write("# Set startpoint for Player\n")
                    player_start_point = None
                    for row_idx, row in enumerate(self.level_map):
                        for col_idx, tile in enumerate(row):
                            if tile == 'START':
                                player_start_point = f"t{col_idx+1}r{row_idx+1}"
                                break
                    if player_start_point:
                        file.write("player_start.append({})\n\n".format(player_start_point))

                    # Write the active exit setup
                    file.write("# Set exit to active\n")
                    file.write("active_exit.append(1)\n")

                messagebox.showinfo("Level Saved", f"The level '{level_name}' has been appended to the Python file.")

                # Generate a new random map
                self.level_map = generate_random_map(self.rows, self.cols)
                self.draw_grid()

                # Reset placed tiles and reactivate buttons
                self.placed_tiles = {tile: False for tile in self.placed_tiles}
                for button in self.tile_buttons.values():
                    button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the level: {e}")

def generate_random_map(rows, cols, max_attempts=1000):
    """
    Generate a random map with connected floor tiles and a balanced distribution of walls.

    Args:
        rows (int): Number of rows in the map.
        cols (int): Number of columns in the map.
        max_attempts (int): Maximum number of attempts to generate a valid map.

    Returns:
        List[List[str]]: A 2D list representing the map with 'FLOOR' and 'WALL' tiles.
    """
    def is_connected(level_map):
        """
        Check if all 'FLOOR' tiles are connected using Breadth-First Search (BFS).
        """
        def bfs(start):
            """
            BFS algorithm to traverse connected 'FLOOR' tiles.
            """
            queue = deque([start])  # Initialize the queue with the starting position
            visited = set()  # Set to keep track of visited floor tiles
            while queue:
                x, y = queue.popleft()  # Dequeue a position from the front
                if (x, y) in visited:
                    continue
                visited.add((x, y))  # Mark this position as visited
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Check all four directions
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and level_map[nx][ny] == 'FLOOR':
                        queue.append((nx, ny))  # Enqueue the neighboring floor tile
            return visited

        start_floors = [(i, j) for i in range(rows) for j in range(cols) if level_map[i][j] == 'FLOOR']
        if not start_floors:
            return False

        visited_floors = bfs(start_floors[0])
        return len(visited_floors) == len(start_floors)

    for attempt in range(max_attempts):
        # Start with a grid of walls
        level_map = [['WALL' for _ in range(cols)] for _ in range(rows)]

        # Create a connected path of floor tiles
        start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1)
        level_map[start_x][start_y] = 'FLOOR'
        queue = deque([(start_x, start_y)])  # Initialize the queue with the starting floor tile

        while queue:
            x, y = queue.popleft()  # Dequeue a position from the front
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)  # Randomize the order of directions to explore
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and level_map[nx][ny] == 'WALL':
                    level_map[nx][ny] = 'FLOOR'  # Convert the wall to a floor tile
                    queue.append((nx, ny))  # Enqueue the new floor tile position
                    if len(queue) >= rows * cols // 3:  # Ensure at least one-third the tiles are floors
                        break

        # Randomly convert some floor tiles to walls while maintaining connectivity
        floor_tiles = [(i, j) for i in range(rows) for j in range(cols) if level_map[i][j] == 'FLOOR']
        random.shuffle(floor_tiles)
        for i, j in floor_tiles:
            if random.random() < 0.3:  # Convert approximately 30% of floor tiles to walls
                level_map[i][j] = 'WALL'
                if not is_connected(level_map):
                    level_map[i][j] = 'FLOOR'  # Revert if connectivity is lost

        if is_connected(level_map):
            return level_map

    # Fallback: Ensure a connected path of floor tiles
    level_map = [['WALL' for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows-1 or j == 0 or j == cols-1:
                level_map[i][j] = 'WALL'  # Ensure borders are walls
            else:
                level_map[i][j] = 'FLOOR'  # Ensure inner tiles are floors
    return level_map

def main():
    """
    Main function to initialize the level editor with a custom grid size.
    """
    root = tk.Tk()
    root.title("Level Editor")

    while True:
        # # Prompt the user to enter the grid size in a single dialog
        # grid_size = simpledialog.askstring("Grid Size", "Enter rows and columns (n,n) - min 4/max 12")
        # if grid_size:
        #     try:
        #         rows, cols = map(int, grid_size.split(','))
        #         if not (4 <= rows <= 12) or not (4 <= cols <= 12):
        #             messagebox.showwarning("Input Warning", "Rows and columns must be between 4 and 12.")
        #             continue  # Ask again if the input is out of range
        #     except ValueError:
        #         messagebox.showwarning("Input Warning", "Invalid input format. Please enter rows and columns as 'rows,cols'.")
        #         continue  # Ask again if the input format is incorrect
        # else:
        #     messagebox.showwarning("Input Warning", "Grid size input was canceled or invalid.")
        #     return  # Exit if the input is canceled

        # Generate a random level map
        level_map = generate_random_map(6, 6)

        editor = LevelEditor(root, level_map)
        root.mainloop()
        break  # Exit the loop after successfully starting the editor

if __name__ == "__main__":
    main()
