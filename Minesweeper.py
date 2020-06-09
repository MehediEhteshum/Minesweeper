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

# Initializing node parameters
# (all nodes, random nodes & indices, unit rectangle location,
# clicked cell's nodal index).
nodes = []
randNodes = []
randIndex = []
rect_locx = []
rect_locy = []
clickedCell = []


def get_nodes():
    # Getting nodal points of the main rectangle,
    # left to right and then top to bottom.
    nodes.clear()
    rect_locx.clear()
    rect_locy.clear()
    for row in range(rect_numy):
        for column in range(rect_numx):
            # Location of the unit rectangles.
            rect_loc = (((wndwCenter[0]-(rect_numx*rect_arm/2))
                         + column*rect_arm),
                        ((wndwCenter[1]-(rect_numy*rect_arm/2))
                         + row*rect_arm))
            # Overwriting global variable, nodes,
            # rect_locx, rect_locy.
            nodes.append(rect_loc)
            rect_locx.append(rect_loc[0])
            rect_locy.append(rect_loc[1])


def draw_mines():
    # Drawing adjusted nodes as mines.
    # Drawing nodes.
    # """ for node in nodes:
    #     pygame.draw.circle(screenSurface, BLACK,
    #                        (int(round(node[0], 0)),
    #                         int(round(node[1], 0))),
    #                        3) """
    # Mine size adjustable with window size.
    mine_size = round(rect_arm*0.25)
    mine_color = pygame.Color("#e15a19")
    for index in randIndex:
        pygame.draw.circle(screenSurface, mine_color,
                           (int(round((rect_locx[index] +
                                       (rect_arm/2)), 0)),
                            int(round((rect_locy[index] +
                                       (rect_arm/2)), 0))),
                           mine_size)


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
        calc_mines((index-rect_numx), index)
        # Bottom rectangle.
        calc_mines((index+rect_numx), index)
        # Top-left rectangle.
        calc_mines((index-(rect_numx+1)), index)
        # Top-right rectangle.
        calc_mines((index-(rect_numx-1)), index)
        # Bottom-left rectangle.
        calc_mines((index+(rect_numx-1)), index)
        # Bottom-right rectangle.
        calc_mines((index+(rect_numx+1)), index)


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
    # font size adjustable with window size.
    fontSize = round(rect_arm*0.70)
    numFont = pygame.font.SysFont("Arial", fontSize, True)
    # Color index corresponds to mine number at the spot.
    numColor = [WHITE, pygame.Color("#3232d2"),
                pygame.Color("#649619"),
                pygame.Color("#e11919"), BLACK]
    for num in mine_num:
        if num != 0:
            # Getting text surface and rectangle.
            textSurf, textRect = text_object(
                str(num), numFont,
                numColor[num if (num < 4) else 4])
            # Setting text rectangle's center.
            textRect.center = ((rect_locx[i]+(rect_arm/2)),
                               (rect_locy[i]+(rect_arm/2)))
            # Drawing text.
            screenSurface.blit(textSurf, textRect)
        # Index increment.
        i = i + 1


def text_object(text, font, color):
    # Returns text surface and rectangle.
    textSurf = font.render(text, True, color)
    return textSurf, textSurf.get_rect()


def draw_field():
    # Draw top level 'green' rectangles as minefield.
    # Rectangle color options.
    rect_color = ("#8ccc14", "#a2e345")
    row = 0
    for node in nodes:
        i = nodes.index(node)
        # Rectangle color switching purpose.
        if (i % rect_numx) == 0:
            row = row+1
        pygame.draw.rect(screenSurface,
                         pygame.Color(rect_color[(i+row) % 2]),
                         (rect_locx[i], rect_locy[i],
                          (rect_arm+1), (rect_arm+1)))
        # (rect_arm+1): '1' added to remove pixel gap.


def draw_hiddenField():
    # Draw lower level rectangles as hidden field.
    # Rectangle color options.
    # "#edc095", "#b99777"
    rect_color = ("#ffdcb4", "#d2b99b")
    row = 0
    for node in nodes:
        i = nodes.index(node)
        # Rectangle color switching purpose.
        if (i % rect_numx) == 0:
            row = row+1
        if i in clickedCell:
            pygame.draw.rect(screenSurface, pygame.Color
                             (rect_color[(i+row) % 2]),
                             (rect_locx[i], rect_locy[i],
                              (rect_arm+1), (rect_arm+1)))
        # (rect_arm+1): '1' added to remove pixel gap.


def mouse_click():
    # Detecting and classifying different mouse clicks.
    if event.button == 1:
        mouse_LClick()


def mouse_LClick():
    # Left click operations.
    # Mouse click position.
    x, y = pygame.mouse.get_pos()
    # Field range.
    x_min = round(wndwCenter[0]-(rect_numx*rect_arm/2)-1)
    x_max = round(wndwCenter[0]+(rect_numx*rect_arm/2)-1)
    y_min = round(wndwCenter[1]-(rect_numy*rect_arm/2)-1)
    y_max = round(wndwCenter[1]+(rect_numy*rect_arm/2)-1)
    # Minus '1' for pixel gap adjustment.
    # Detecting click within the field range.
    if (x_min <= x <= x_max) and (y_min <= y <= y_max):
        for node in nodes:
            # Unit cell range.
            xn_min, xn_max = (node[0]-1), (node[0]+rect_arm-1)
            yn_min, yn_max = (node[1]-1), (node[1]+rect_arm-1)
            # Minus '1' for pixel gap adjustment.
            # Detecting clicked unit cell by nodal index.
            if (xn_min <= x <= xn_max) and \
                    (yn_min <= y <= yn_max):
                i = nodes.index(node)
                # Detecting mined cell click.
                if i in randIndex:
                    minedCell_click()
                # Detecting empty cell click.
                if (i not in randIndex) and \
                        (mine_num[i] == 0):
                    emptyCell_click()
                if i not in clickedCell:
                    clickedCell.append(i)


def emptyCell_click():
    # Operations if clicked empty cell.
    print("You clicked empty cell.")


def minedCell_click():
    # Operations if clicked mine.
    for i in randIndex:
        clickedCell.append(i)


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
    # Checking mouse click (down).
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_click()
    # Checking window size.
    if event.type == pygame.VIDEORESIZE:
        # Window size.
        wndwSize = wndwWidth, wndwHeight\
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
        print('One time ' + str(mine_num))
    draw_field()
    draw_hiddenField()
    draw_mines()
    draw_mineNum()
    screen.flip()

pygame.quit()
