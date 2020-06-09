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
S = 0  # Start
F = 1  # Floor
W = 2  # Wall
P1 = 3  # Pit1
P2 = 4  # Pit2
P3 = 5  # Pit3
P4 = 6  # Pit4
PW = 7  # Pit as Wall - not able to put box in it
E = 8  # Exit


# For Debug Level - uncomment line 77 -98 and comment line 101-122

# # DEBUG LÈVEL
# # Tutorial title
# titel = [' Debugging Mode']

# # Map layout for tiles 
# tutorial_map = [[F, F, F, F, F, E,\
#                 F, F, W, W, F, F,\
#                 F, F ,F, F, F, F,\
#                 F, F ,S, F, F, F,\
#                 F, F, F, F, F, F,
#                 F, F, F, F, F, F]]

# # Setup for active Boxes
# active_boxes = [[True, True, True, True]]
# # Setup of Boxes startpoints
# positions = [[t3r3, t4r3, t3r6, t4r4]]

# # Set startpoint for Player
# player_start = [t3r4]

# # Set exit to active
# active_exit = [1]


# TUTORIAL 1
# Tutorial title
titel = [' Tutorial: Push Box to reach Exit']

# Map layout for tiles
tutorial_map = [[W, W, W, W, W, W,\
                W, W, F, W, W, W,\
                W, W ,F, E, W, W,\
                W, W ,F, W, W, W,\
                W, W, S, W, W, W,
                W, W, W, W, W, W]]

# Setup for active Boxes
active_boxes = [[True, False, False, False]]
# Setup of Boxes startpoints
positions = [[t3r4, t4r3, t5r3, t4r5]]

# Set startpoint for Player
player_start = [t3r5]

# Set exit to active
active_exit = [1]


# TUTORIAL 2
# Tutorial title
titel.append('Tutorial: Pits are DANGEROUS! Push Box into the Pit to be able to cross')

# Map layout for tiles
tutorial_map.append([W, W, W, W, W, W,\
                    W, PW, P1, E, W, W,\
                    W, PW, F, W, W, W,\
                    W, PW, F, W, W, W,\
                    W, W, S, W, W, W,
                    W, W, W, W, W, W])

# Setup for active Boxes
active_boxes.append([True, False, False, False])
# Setup of Boxes startpoints
positions.append([t3r4, t2r1, t6r2, t3r6])

# Set startpoint for Player
player_start.append(t3r5)

# Set exit to active
active_exit.append(1)


# TUTORIAL 3
# Tutorial title
titel.append('Tutorial: Two Boxes in a row cannot be pushed')

# Map layout for tiles
tutorial_map.append([W, W, F, W, W, W,\
                    W, E, F, W, W, W,\
                    W, F, F, F, W, W,\
                    W, W, F, F, W, W,\
                    W, W, F, W, W, W,
                    W, W, S, W, W, W])

# Setup for active Boxes
active_boxes.append([True, True, False, False])
# Setup of Boxes startpoints
positions.append([t3r2, t3r3, t4r1, t3r4])

# Set startpoint for Player
player_start.append(t3r6)

# Set exit to active
active_exit.append(1)


# TUTORIAL 4
# Tutorial title
titel.append('Tutorial: To drag Box stand close to it, hold space bar while moving away from Box')

# Map layout for tiles
tutorial_map.append([W, W, W, E, W, W,\
                    W, W, W, F, F, W,\
                    W, W, W, F, F, W,\
                    W, W, W, F, F, W,\
                    W, W, F, F, W, W,
                    W, W, S, W, W, W])

# Setup for active Boxes
active_boxes.append([True, False, False, False])
# Setup of Boxes startpoints
positions.append([t4r2, t5r2, t4r1, t3r4])

# Set startpoint for Player
player_start.append(t3r6)

# Set exit to active
active_exit.append(1)
