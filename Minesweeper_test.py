# Just adding a line
import os
import ctypes
import random
import pygame

pygame.init()

# Initializing display.
screen = pygame.display
# To get true resolution info (for WINDOWS OS).
if os.name == "nt":
    ctypes.windll.user32.SetProcessDPIAware()
# Setting display/screen size and name.
screenInfo = screen.Info()
screenSize = (screenWidth, screenHeight) = (
    screenInfo.current_w, screenInfo.current_h)
SCREEN_NAME = "Minesweeper"
screenCenter = (screenWidth/2, screenHeight/2)
# Initializing the screen surface, setting the screen name.
screenSurface = screen.set_mode(screenSize,
                                pygame.RESIZABLE)
screen.set_caption(SCREEN_NAME)
# Setting display icon.
iconImage = pygame.image.load(
    "game assets/icon.png")
screen.set_icon(iconImage)

# Setting basic colors.
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Samples.
# """ sampleImage = pygame.image.load(
#     "game assets/minesweeper.png")
# sampleImageRect = sampleImage.get_rect() """
# For easy game mode.
# Limiting unit rectangle arm. Height & width percentage.
minRectArm = 30
hgtPerc, wdthPerc = 0.6, 0.8
# Total mines (easy mode).
mine_tot = 10
# Unit arm length and rectangle numbers in row and column.
rect_num = (rect_numx, rect_numy) = (10, 8)
rect_arm = max(min((screenHeight*hgtPerc/rect_numy),
                   (screenWidth*wdthPerc/rect_numx)),
               minRectArm)

# Initializing window size and setting limit.
wndwSize = (wndwWidth, wndwHeight) = screenSize
wndwCenter = (wndwWidth/2, wndwHeight/2)
minWndwWidth = (minRectArm*rect_numx)/wdthPerc
minWndwHeight = (minRectArm*rect_numy)/hgtPerc

# Initializing node parameters.
nodes = []
randNodes = []
randIndex = []


def get_nodes():
    # Getting nodal points of the main rectangle,
    # left to right and then top to bottom.
    nodes.clear()
    for row in range(rect_numy):
        for column in range(rect_numx):
            # Location of the unit rectangles.
            rect_loc = (rect_locx, rect_locy) = (
                ((wndwCenter[0]-(rect_numx*rect_arm/2))
                 + column*rect_arm),
                ((wndwCenter[1]-(rect_numy*rect_arm/2))
                 + row*rect_arm))
            # Overwriting global variable, nodes.
            nodes.append(rect_loc)


def draw_nodes():
    # Drawing nodes.
    for node in nodes:
        pygame.draw.circle(screenSurface, BLACK,
                           (int(round(node[0], 0)),
                            int(round(node[1], 0))),
                           3)
    for index in randIndex:
        pygame.draw.circle(screenSurface, RED,
                           (int(round(nodes[index][0], 0)),
                            int(round(nodes[index][1], 0))),
                           8)


def get_randNodes():
    # Getting random node points.
    global randNodes
    randNodes.clear()
    # Overwriting global variables,
    # randNodes & randIndex.
    randNodes = random.sample(nodes, mine_tot)
    for node in randNodes:
        # Getting the index of random nodes at nodes list.
        randIndex.append(nodes.index(node))


# Initializing a list for nodal mine numbers.
mine_num = [0]*(rect_numx*rect_numy)


def mine_count():
    # Calculating mine numbers at nodes.
    # Calculating mine numbers for 8 surrounding nodes.
    for index in randIndex:
        # Left rectangle.
        calc_mines(index-1, index)
        # Right rectangle.
        calc_mines(index+1, index)
        # Top rectangle.
        calc_mines(index-10, index)
        # Bottom rectangle.
        calc_mines(index+10, index)
        # Top-left rectangle.
        calc_mines(index-11, index)
        # Top-right rectangle.
        calc_mines(index-9, index)
        # Bottom-left rectangle.
        calc_mines(index+9, index)
        # Bottom-right rectangle.
        calc_mines(index+11, index)


def calc_mines(index, mine_index):
    # Overwriting global variable, mine_num.
    # """ Checking nodes
    # which are within the range and
    # not in the randNodes list. """
    if (index not in randIndex) and \
            (0 <= index < (rect_numx*rect_numy)):
        # which are not on the 2 side boundaries.
        if ((mine_index+1) % rect_numx != 1) and \
                ((mine_index+1) % rect_numx != 0):
            mine_num[index] = mine_num[index] + 1
        # which are on the left boundary.
        elif ((mine_index+1) % rect_numx == 1) and \
            (index != (mine_index-1)) and \
            (index != (mine_index-(rect_numx+1))) and \
                (index != (mine_index+(rect_numx-1))):
            mine_num[index] = mine_num[index] + 1
        # which are on the right boundary.
        elif ((mine_index+1) % rect_numx == 0) and \
            (index != (mine_index+1)) and \
            (index != (mine_index+(rect_numx+1))) and \
                (index != (mine_index-(rect_numx-1))):
            mine_num[index] = mine_num[index] + 1


def draw_mineNum():
    # Drawing nodal mine numbers.
    # Index.
    i = 0
    # Setting font & font color.
    numFont = pygame.font.SysFont("Arial", 30, True)
    numColor = [WHITE, BLUE, GREEN, RED, BLACK]
    for num in mine_num:
        if num != 0:
            # Getting text surface and rectangle.
            textSurf, textRect = text_object(
                str(num), numFont,
                numColor[num if (num < 4) else 4])
            # Setting text rectangle's center.
            textRect.center = nodes[i]
            # Drawing text.
            screenSurface.blit(textSurf, textRect)
        # Index increment.
        i = i + 1


def text_object(text, font, color):
    # Returns text surface and rectangle.
    textSurf = font.render(text, True, color)
    return textSurf, textSurf.get_rect()


# Setting game as running (true).
# gameRun = True
firstTime = True


def isRunning():
    # Returns true if running else false.
    if event.type == pygame.QUIT:
        # Stopping the game.
        return False
    return True


# Pygame events initialization.
# """ pygame.event.pump() """
event = pygame.event.wait()

# Running the game till exiting.
while isRunning():
    # """ pygame.event.pump() """
    event = pygame.event.wait()
    if event.type == pygame.VIDEORESIZE:
        # Window size.
        wndwSize = wndwWidth, wndwHeight \
            = event.w, event.h
        # Limiting minimum window size.
        if wndwWidth < minWndwWidth:
            wndwWidth = int(round(minWndwWidth, 0))
        if wndwHeight < minWndwHeight:
            wndwHeight = int(round(minWndwHeight, 0))
        wndwSize = wndwWidth, wndwHeight
        # Unit rectangle arm length.
        rect_arm = max(min((wndwHeight*hgtPerc/rect_numy),
                           (wndwWidth*wdthPerc/rect_numx)),
                       minRectArm)
        wndwCenter = (wndwWidth/2, wndwHeight/2)
        screenSurface = screen.set_mode(wndwSize,
                                        pygame.RESIZABLE)
    # Filling screen color. Updating screen.
    screenSurface.fill(WHITE)
    # """ screenSurface.blit(sampleImage, sampleImageRect) """
    get_nodes()
    if firstTime:
        # Runs only for the first loop.
        get_randNodes()
        mine_count()
        firstTime = False
        print(mine_num)
    draw_nodes()
    draw_mineNum()
    screen.flip()

pygame.quit()
