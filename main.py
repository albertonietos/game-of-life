"""
Main file to the game of life project.
This project is based on John Conway's Game of Life.
"""

import numpy as np
import pygame
import time

# class GameOfLife:
#     def __init__(self):
#         """Initialize a new `game of life` game """
#         pygame.init()
#
#         # Set up the window display
#         self.width = 1000
#         self.height = 1000
#         self.screen = pygame.display.set_mode((self.width, self.height))
#
#         # define background color
#         self.bg_color = 25, 25, 25
#         screen.fill(self.bg_color)


pygame.init()

# Initialize the window display
width, height = 500, 500
screen = pygame.display.set_mode((height, width))

# Define background
bg = 25, 25, 25
screen.fill(bg)

# Define the number of cells
nxC, nyC = 50, 50

# Define the dimension of each cell
dimCW = width / nxC
dimHW = height / nyC

# Define game state (1=Alive, 0=Dead)
gameState = np.zeros((nxC, nyC))

# Initialize certain cells
gameState[10, 10] = 1
gameState[11, 10] = 1
gameState[12, 10] = 1
gameState[12, 11] = 1
gameState[10, 12] = 1
gameState[12, 12] = 1
gameState[10, 13] = 1
gameState[11, 13] = 1
gameState[12, 13] = 1
# gameState[4, 5] = 1
# gameState[4, 6] = 1
# gameState[4, 7] = 1

# Initialize variable to pause game
game_stop = False

while True:
    # Update game state variable once per step
    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # Register possible input by user
    event_lst = pygame.event.get()
    for event in event_lst:
        if event.type == pygame.KEYDOWN:
            # If key down is pressed, stop the execution of the game
            game_stop = not game_stop
        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            # If mouse is pressed, turn that cell alive
            posX, posY = pygame.mouse.get_pos()
            celX, celY = np.floor(posX / dimCW).astype(int), np.floor(posY / dimHW).astype(int)
            newGameState[celX, celY] = not mouse_click[2]

    # Loop through every cell
    for y in range(nxC):
        for x in range(nyC):
            if not game_stop:
                # Compute each cell's neighborhood
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + gameState[x % nxC, (y-1) % nyC] + \
                    gameState[(x+1) % nxC, (y-1) % nyC] + gameState[(x-1) % nxC, y % nyC] + \
                    gameState[(x+1) % nxC, y % nyC] + gameState[(x-1) % nxC, (y+1) % nyC] + \
                    gameState[x % nxC, (y+1) % nyC] + gameState[(x+1) % nxC, (y+1) % nyC]

                # 1st rule: Any live cell with two or three live neighbors survives.
                if gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0
                # 2nd rule: Any dead cell with three live neighbors becomes a live cell.
                elif n_neigh == 3 and gameState[x, y] == 0:
                    newGameState[x, y] = 1
                else:
                    pass

                # Define each polygon's cell
                poly = [(x * dimCW, y * dimHW),
                        ((x + 1) * dimCW, y * dimHW),
                        ((x + 1) * dimCW, (y + 1) * dimHW),
                        (x * dimCW, (y + 1) * dimHW)]

                # Draw the cell structure
                if newGameState[x, y] == 0:
                    # Dead cell (black, empty)
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                else:
                    # Alive (white, full)
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

                # Update game state
                gameState = np.copy(newGameState)
    # Update the display
    pygame.display.flip()
