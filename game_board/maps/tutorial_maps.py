from game_board.elements import gfx

# Set tile coordinate for X
x1 = 0
x2 = 100
x3 = 200
x4 = 300
x5 = 400
x6 = 500

# Set tile coordinate for Y
y1 = 0
y2 = 100
y3 = 200
y4 = 300
y5 = 400
y6 = 500

# Tile coordinates
t1r1 = (x1, y1)
t2r1 = (x2, y1)
t3r1 = (x3, y1)
t4r1 = (x4, y1)
t5r1 = (x5, y1)
t6r1 = (x6, y1)
t1r2 = (x1, y2)
t2r2 = (x2, y2)
t3r2 = (x3, y2)
t4r2 = (x4, y2)
t5r2 = (x5, y2)
t6r2 = (x6, y2)
t1r3 = (x1, y3)
t2r3 = (x2, y3)
t3r3 = (x3, y3)
t4r3 = (x4, y3)
t5r3 = (x5, y3)
t6r3 = (x6, y3)
t1r4 = (x1, y4)
t2r4 = (x2, y4)
t3r4 = (x3, y4)
t4r4 = (x4, y4)
t5r4 = (x5, y4)
t6r4 = (x6, y4)
t1r5 = (x1, y5)
t2r5 = (x2, y5)
t3r5 = (x3, y5)
t4r5 = (x4, y5)
t5r5 = (x5, y5)
t6r5 = (x6, y5)
t1r6 = (x1, y6)
t2r6 = (x2, y6)
t3r6 = (x3, y6)
t4r6 = (x4, y6)
t5r6 = (x5, y6)
t6r6 = (x6, y6)

# Game Board coordinates
tiles = (t1r1, t2r1, t3r1, t4r1, t5r1, t6r1,\
        t1r2, t2r2, t3r2, t4r2, t5r2, t6r2,\
        t1r3, t2r3, t3r3, t4r3, t5r3, t6r3,\
        t1r4, t2r4, t3r4, t4r4, t5r4, t6r4,\
        t1r5, t2r5, t3r5, t4r5, t5r5, t6r5,\
        t1r6, t2r6, t3r6, t4r6, t5r6, t6r6,)

# Value of Game Board elements
START = 0
PIT1 = 1
PIT2 = 2
PIT3 = 3
PIT4 = 4
PIT_WALL = 5  # Pit as Wall - not able to put box in it
FLOOR = 6
WALL = 7
EXIT = 8

# If gfx.debug = True
# - DEBUG LEVEL
if gfx.debug:
    # DEBUG LEVEL
    # Tutorial title
    title = [' Debugging Mode']

    # Map layout for tiles
    tutorial_map = [[FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, EXIT,
                     FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR,
                     FLOOR, FLOOR ,FLOOR, FLOOR, FLOOR, FLOOR,
                     FLOOR, FLOOR ,START, FLOOR, FLOOR, FLOOR,
                     FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR,
                     FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR]]

    # Setup for active Boxes
    active_boxes = [[True, True, True, True]]
    # Setup of Boxes startpoints
    positions = [[t3r3, t3r6, t4r3, t4r5]]

    # Set startpoint for Player
    player_start = [t3r4]

    # Set exit to active
    active_exit = [1]

# Else
# - TUTORIAL LEVELS
else:
    # TUTORIAL 1
    # Tutorial title
    title = ['Push the Box to reach Exit']

    # Map layout for tiles
    tutorial_map = [[WALL, WALL, WALL, WALL, WALL, WALL,
                     WALL, WALL, FLOOR, WALL, WALL, WALL,
                     WALL, WALL ,FLOOR, EXIT, WALL, WALL,
                     WALL, WALL ,FLOOR, WALL, WALL, WALL,
                     WALL, WALL, START, WALL, WALL, WALL,
                     WALL, WALL, WALL, WALL, WALL, WALL]]

    # Setup for active Boxes
    active_boxes = [[True, False, False, False]]
    # Setup of Boxes startpoints
    positions = [[t3r4, t1r1, t2r1, t3r1]]

    # Set startpoint for Player
    player_start = [t3r5]

    # Set exit to active
    active_exit = [1]


    # TUTORIAL 2
    # Tutorial title
    title.append('Pits are DANGEROUS! Push the Box into the Pit to be able to cross')

    # Map layout for tiles
    tutorial_map.append([WALL, WALL, WALL, WALL, WALL, WALL,
                         WALL, PIT4, PIT1, EXIT, WALL, WALL,
                         WALL, PIT3, FLOOR, WALL, WALL, WALL,
                         WALL, PIT2, FLOOR, WALL, WALL, WALL,
                         WALL, WALL, START, WALL, WALL, WALL,
                         WALL, WALL, WALL, WALL, WALL, WALL])

    # Setup for active Boxes
    active_boxes.append([True, False, False, False])
    # Setup of Boxes startpoints
    positions.append([t3r4, t1r1, t2r1, t3r1])

    # Set startpoint for Player
    player_start.append(t3r5)

    # Set exit to active
    active_exit.append(1)


    # TUTORIAL 3
    # Tutorial title
    title.append('Two Boxes in a row cannot be pushed')

    # Map layout for tiles
    tutorial_map.append([WALL, WALL, FLOOR, WALL, WALL, WALL,
                         WALL, EXIT, FLOOR, WALL, WALL, WALL,
                         WALL, FLOOR, FLOOR, FLOOR, WALL, WALL,
                         WALL, WALL, FLOOR, FLOOR, WALL, WALL,
                         WALL, WALL, FLOOR, WALL, WALL, WALL,
                         WALL, WALL, START, WALL, WALL, WALL])

    # Setup for active Boxes
    active_boxes.append([True, True, False, False])
    # Setup of Boxes startpoints
    positions.append([t3r3, t3r2, t1r1, t2r1])

    # Set startpoint for Player
    player_start.append(t3r6)

    # Set exit to active
    active_exit.append(1)


    # TUTORIAL 4
    # Tutorial title
    title.append('To pull a Box stand close to it, hold space bar while moving away from the Box')

    # Map layout for tiles
    tutorial_map.append([WALL, WALL, WALL, EXIT, WALL, WALL,
                         WALL, WALL, WALL, FLOOR, FLOOR, WALL,
                         WALL, WALL, WALL, FLOOR, FLOOR, WALL,
                         WALL, WALL, WALL, FLOOR, FLOOR, WALL,
                         WALL, WALL, FLOOR, FLOOR, WALL, WALL,
                         WALL, WALL, START, WALL, WALL, WALL])

    # Setup for active Boxes
    active_boxes.append([True, False, False, False])
    # Setup of Boxes startpoints
    positions.append([t4r2, t1r1, t2r1, t3r1])

    # Set startpoint for Player
    player_start.append(t3r6)

    # Set exit to active
    active_exit.append(1)
