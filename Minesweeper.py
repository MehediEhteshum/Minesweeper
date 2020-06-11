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
LclickedCell = []
RclickedCell = []


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
    # Drawing adjusted nodes as mines when clicked.
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
        # Drawing mines when clicked.
        if index in LclickedCell:
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
    # Calculating mine numbers for 8 adjacent nodes.
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
    # """ Checking node
    # if it is within the range and
    # not in the mine list, randNodes. """
    if (index not in randIndex) and \
            (0 <= index < (rect_numx*rect_numy)):
        # When mine cell is not on the 2 side boundaries.
        if ((mine_index+1) % rect_numx != 1) and \
                ((mine_index+1) % rect_numx != 0):
            mine_num[index] = mine_num[index] + 1
        # When mine cell is on the left boundary,
        # declude its left side cells.
        elif ((mine_index+1) % rect_numx == 1) and \
            (index != (mine_index-1)) and \
            (index != (mine_index-(rect_numx+1))) and \
                (index != (mine_index+(rect_numx-1))):
            mine_num[index] = mine_num[index] + 1
        # When mine cell is on the right boundary,
        # declude its right side cells.
        elif ((mine_index+1) % rect_numx == 0) and \
            (index != (mine_index+1)) and \
            (index != (mine_index+(rect_numx+1))) and \
                (index != (mine_index-(rect_numx-1))):
            mine_num[index] = mine_num[index] + 1


def draw_mineNum():
    # Drawing nodal mine numbers when clicked.
    # Setting font & font color.
    # font size adjustable with window size.
    fontSize = round(rect_arm*0.70)
    numFont = pygame.font.SysFont("Arial", fontSize, True)
    # Color index corresponds to mine number at the spot.
    numColor = [WHITE, pygame.Color("#3232d2"),
                pygame.Color("#649619"),
                pygame.Color("#e11919"), BLACK]
    for i in LclickedCell:
        # Drawing nodal mine numbers when clicked.
        num = mine_num[i]
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
    # Draw lower level rectangles as hidden field,
    # when clicked.
    # Rectangle color options.
    rect_color = ("#c8beaf", "#e6d7c3")
    for i in LclickedCell:
        # Calculate row & column of the clicked cell.
        r, c = (i//rect_numx), (i % rect_numx)
        # Choosing cell color option.
        # When row and column = odd-odd.
        if (r % 2 == 1) and (c % 2 == 1):
            color_opt = 1
        # When row and column = even-even.
        elif (r % 2 == 0) and (c % 2 == 0):
            color_opt = 1
        # When row and column = even-odd or odd-even.
        else:
            color_opt = 0
        pygame.draw.rect(screenSurface, pygame.Color
                         (rect_color[color_opt]),
                         (rect_locx[i], rect_locy[i],
                          (rect_arm+1), (rect_arm+1)))
        # (rect_arm+1): '1' added to remove pixel gap.


def mouse_click():
    # Detecting and classifying different mouse clicks.
    # Left click.
    if event.button == 1:
        mouse_LClick()
    # Right click.
    elif event.button == 3:
        mouse_RClick()    
    print((mine_tot-len(RclickedCell)))


def mouse_RClick():
    # Right click operations.
    # Overwriting global variable, RclickedCell.
    # Nodal (mine field) index value assignment.
    i = node_click()
    # Here, "i = None" means clicked outside the field.
    # Checking for non-outside & non-left Click.
    if (i is not None) and (i not in LclickedCell):
        # Registering Rclick if not Rclicked before.
        if i not in RclickedCell:
            RclickedCell.append(i)
        # Unregistering Rclick if Rclicked before.
        elif i in RclickedCell:
            RclickedCell.remove(i)


def draw_flag():
    # Draw flag if Rclicked.
    flag_size = round(0.20*rect_arm)
    for i in RclickedCell:
        pygame.draw.circle(screenSurface, BLUE,
                           (int(round((rect_locx[i] +
                                       (rect_arm/2)), 0)),
                            int(round((rect_locy[i] +
                                       (rect_arm/2)), 0))),
                           flag_size)


def mouse_LClick():
    # Left click operations.
    # Overwriting global variable, LclickedCell.
    # Nodal (mine field) index value assignment.
    i = node_click()
    # Here, "i = None" means clicked outside the field.
    # Checking for non-outside & non-right Click.
    if (i is not None) and (i not in RclickedCell):
        # Detecting mined cell click.
        if i in randIndex:
            minedCell_click(i)
        # Detecting empty cell click.
        elif (i not in randIndex) and \
                (mine_num[i] == 0):
            emptyCell_click(i)
        # Detecting numbered cell click.
        elif (i not in LclickedCell) and \
                (mine_num[i] != 0):
            LclickedCell.append(i)


def node_click():
    # Get mouse click nodal position on the field.
    # Nodal index default = None i.e. outside field.
    i = None
    x, y = pygame.mouse.get_pos()
    # Field range.
    x_min = round(wndwCenter[0]-(rect_numx*rect_arm/2)-1)
    x_max = round(wndwCenter[0]+(rect_numx*rect_arm/2)-1)
    y_min = round(wndwCenter[1]-(rect_numy*rect_arm/2)-1)
    y_max = round(wndwCenter[1]+(rect_numy*rect_arm/2)-1)
    # Minus '1' for pixel gap adjustment.
    # Detecting click within the field range.
    if (x_min <= x <= x_max) and (y_min <= y <= y_max):
        # First node on the field and its coordinate.
        node0 = nodes[0]
        x0, y0 = node0[0], node0[1]
        # c, r = column and row of (x, y)
        c, r = (abs(x-(x0-1)) // rect_arm), \
            (abs(y-(y0-1)) // rect_arm)
        # Minus '1' for pixel gap adjustment.
        # Nodal (mine field) index of (x, y)
        i = int(c+(r*rect_numx))
    return i


def emptyCell_click(index):
    # Operations if clicked empty cell
    # (reveal all empty and numbered cells in that area).
    # Overwriting global variable, LclickedCell.
    if index not in LclickedCell:
        LclickedCell.append(index)
        # Check 8 adjacent cells.
        # Left cell check.
        cell_check(index-1, index)
        # Right cell check.
        cell_check(index+1, index)
        # Top cell check.
        cell_check((index-rect_numx), index)
        # Bottom cell check.
        cell_check((index+rect_numx), index)
        # Top-left cell check.
        cell_check((index-(rect_numx+1)), index)
        # Top-right cell check.
        cell_check((index-(rect_numx-1)), index)
        # Bottom-left cell check.
        cell_check((index+(rect_numx-1)), index)
        # Bottom-right cell check.
        cell_check((index+(rect_numx+1)), index)


def cell_check(index, ec_index):
    # Checking the cell adjacent to the empty cell.
    # Checking cell if it is within the range and
    # not in the mine list (randNodes).
    if (index not in randIndex) and \
            (0 <= index < (rect_numx*rect_numy)):
        # When clicked cell is not on the 2 side boundaries.
        if ((ec_index+1) % rect_numx != 1) and \
                ((ec_index+1) % rect_numx != 0):
            ec_check(index)
        # When clicked cell is on the left boundary,
        # declude its left side cells.
        elif ((ec_index+1) % rect_numx == 1) and \
            (index != (ec_index-1)) and \
            (index != (ec_index-(rect_numx+1))) and \
                (index != (ec_index+(rect_numx-1))):
            ec_check(index)
        # When clicked cell is on the right boundary,
        # declude its right side cells.
        elif ((ec_index+1) % rect_numx == 0) and \
            (index != (ec_index+1)) and \
            (index != (ec_index+(rect_numx+1))) and \
                (index != (ec_index-(rect_numx-1))):
            ec_check(index)


def ec_check(index):
    # Checking the cell for emptyness.
    # Overwriting global variable, LclickedCell.
    # If empty cell, consider as clicked empty cell.
    if (mine_num[index] == 0) and (index not in randIndex):
        # Revealed empty cell, removed from Rclicked.
        if index in RclickedCell:
            RclickedCell.remove(index)
        emptyCell_click(index)
    # Else if numbered cell, register as clicked and
    # stop recursion.
    elif mine_num[index] != 0:
        # Revealed numbered cell, removed from Rclicked.
        if index in RclickedCell:
            RclickedCell.remove(index)
        # Register as clicked and stop recursion.
        if index not in LclickedCell:
            LclickedCell.append(index)


mine_clicked = False


def minedCell_click(index):
    # Operations if clicked mine
    # (reveal all mine cells).
    # Overwriting global variable, LclickedCell
    # & mine_clicked.
    # Reveal clicked mine cell.
    if index not in LclickedCell:
        LclickedCell.append(index)
    # Reveal all other mine cells (randNodes)
    # except those are flagged.
    for i in randIndex:
        if (i not in LclickedCell) and \
                (i not in RclickedCell):
            LclickedCell.append(i)
    global mine_clicked
    mine_clicked = True


def draw_cross():
    # Draw cross if wrong flag.
    cross_size = round(0.20*rect_arm)
    for i in RclickedCell:
        if i not in randIndex:
            pygame.draw.circle(screenSurface, BLACK,
                               (int(round((rect_locx[i] +
                                           (rect_arm/2)), 0)),
                                int(round((rect_locy[i] +
                                           (rect_arm/2)), 0))),
                               cross_size)


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
        print("One time")
    draw_field()
    draw_hiddenField()
    draw_mines()
    draw_mineNum()
    draw_flag()
    if mine_clicked:
        # Draw cross if wrong flag.
        draw_cross()
    screen.flip()

pygame.quit()
