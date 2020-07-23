import os
import sys
import ctypes
import random
import csv
import pygame
import pandas
from Classes import Mode

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

# Loading images.
imgBanner = pygame.image.load(
    "game assets/Banner.png").convert()
imgBlack = pygame.image.load(
    "game assets/Solid.png").convert()
imgLclick = pygame.image.load(
    "game assets/Lclick.png").convert_alpha()
imgRclick = pygame.image.load(
    "game assets/Rclick.png").convert_alpha()
imgClock = pygame.image.load(
    "game assets/Clock.png").convert_alpha()
imgCross = pygame.image.load(
    "game assets/Cross.png").convert_alpha()
imgFlag = pygame.image.load(
    "game assets/Flag.png").convert_alpha()
imgMine = pygame.image.load(
    "game assets/Mine.png").convert_alpha()
imgLoss = pygame.image.load(
    "game assets/TA.png").convert_alpha()
imgLoss1 = pygame.image.load(
    "game assets/TA-bg.png").convert_alpha()
imgWin = pygame.image.load(
    "game assets/PA.png").convert_alpha()
imgWin1 = pygame.image.load(
    "game assets/PA-bg.png").convert_alpha()
imgCup = pygame.image.load(
    "game assets/Cup.png").convert_alpha()
imgList = pygame.image.load(
    "game assets/List.png").convert_alpha()
imgEasy = pygame.image.load(
    "game assets/List-easy.png").convert_alpha()
imgMedium = pygame.image.load(
    "game assets/List-medium.png").convert_alpha()
imgHard = pygame.image.load(
    "game assets/List-hard.png").convert_alpha()
imgTick = pygame.image.load(
    "game assets/List-tick.png").convert_alpha()
rectModeImg = [0, 0, 0, 0]
drawModeList = 0
hoverList = False
rectListImg = [0, 0, 0, 0]

# Setting display icon.
screen.set_icon(imgMine)

# Setting basic colors.
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initializing game modes.
easy = Mode("Easy", imgEasy, 10, 10, 8, 0.6, 0.6)
medium = Mode("Medium", imgMedium, 40, 18, 14, 0.7, 0.7)
hard = Mode("Hard", imgHard, 99, 24, 20, 0.8, 0.8)
mode_list = (easy, medium, hard)
index_mode = 0

# For easy game mode.
# Limiting unit rectangle arm. Height & width percentage.
minRectArm = 0.03*min(screenWidth, screenHeight)
wdthPerc, hgtPerc = mode_list[index_mode].wdthPerc,\
    mode_list[index_mode].hgtPerc
# Total mines.
mine_tot = mode_list[index_mode].mine_tot
# Unit arm length and rectangle numbers in row and column.
rect_num = (rect_numx, rect_numy)\
    = (mode_list[index_mode].rect_numx,
       mode_list[index_mode].rect_numy)
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
# Initializing first click states.
nodes = []
randNodes = []
randIndex = []
rect_locx = []
rect_locy = []
firstLClick = True
firstRClick = True
time_init = 0
time_current = 0
time_max = 999


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


def draw_mines(img_mine):
    # Drawing mines when clicked and gameOver.
    # Overwriting global variable, LclickedCell.
    # Drawing nodes.
    # """ for node in nodes:
    #     pygame.draw.circle(screenSurface, BLACK,
    #                        (int(round(node[0], 0)),
    #                         int(round(node[1], 0))),
    #                        3) """
    # Mine size adjustable with window size.
    if gameOver and mine_clicked:
        # Setting image dimension.
        imgDim = int(rect_arm*0.75)
        # Scaling image to the cell.
        img_mine = pygame.transform.smoothscale(
            img_mine, (imgDim, imgDim))
        rectMine = img_mine.get_rect()
        for index in randIndex:
            # Drawing mines when clicked, if not flagged.
            if index not in RclickedCell:
                # Setting image center at cell center.
                rectMine.center = \
                    (nodes[index][0]+rect_arm/2), \
                    (nodes[index][1]+rect_arm/2)
                # Drawing image.
                screenSurface.blit(img_mine, rectMine)
                LclickedCell.append(index)


def get_randNodes(firstLClick_index):
    # Getting random node points for mines
    # based on first Lclick.
    global randNodes
    randNodes.clear()
    randIndex.clear()
    # Overwriting global variables,
    # randNodes & randIndex.
    i = firstLClick_index
    # 9 no-mine cells' indices based on first Lclick.
    # Check 8 adjacent cells.
    # (click + 8 adjacent cells, in left to right &
    # top to bottom order).
    cells_index = ((i-(rect_numx+1)), (i-rect_numx),
                   (i-(rect_numx-1)), (i-1), i, (i+1),
                   (i+(rect_numx-1)), (i+rect_numx),
                   (i+(rect_numx+1)))
    # Cells where no mines are allowed based on first Lclick.
    noMineCells = []
    # Checking for valid cell index.
    for x in cells_index:
        if x != i:
            # v = valid cell index.
            v = cell_check(x, i)
        elif x == i:
            # v = valid cell index.
            v = i
        # For valid v, modify noMineCells.
        if v is not None:
            noMineCells.append(nodes[v])
    # Cells where mines are allowed based on first Lclick.
    mineCells = list(set(nodes)-set(noMineCells))
    # Set up mines on random cells/nodes and
    # know their indices.
    randNodes = random.sample(mineCells, mine_tot)
    for node in randNodes:
        # Getting the index of random nodes at nodes list.
        randIndex.append(nodes.index(node))
    # Calculating mine numbers at nodes/cells.
    mine_count()


def mine_count():
    # Calculating mine numbers at nodes/cells.
    # Overwriting global variable, mine_num.
    # Calculating mine numbers for 8 adjacent nodes/cells.
    for i in randIndex:
        # Check 8 adjacent cells.
        # (index + 8 adjacent cells, in left to right &
        # top to bottom order).
        cells_index = ((i-(rect_numx+1)), (i-rect_numx),
                       (i-(rect_numx-1)), (i-1), i, (i+1),
                       (i+(rect_numx-1)), (i+rect_numx),
                       (i+(rect_numx+1)))
        # Checking for valid cell index.
        for x in cells_index:
            if x != i:
                # v = valid cell index.
                v = cell_check(x, i)
                # For valid v which is not a mine cell.
                if (v is not None) and (v not in randIndex):
                    # Counting mines at adjacent cells.
                    mine_num[v] = mine_num[v] + 1


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


def flag_count(banner_h):
    # Drawing flag count (num).
    num = mine_tot-len(RclickedCell)
    # Setting font & font color.
    # font size adjustable with window size.
    fontSize = round(rect_arm*0.50)
    numFont = pygame.font.SysFont("Arial", fontSize, True)
    numColor = WHITE
    # Getting text surface and rectangle.
    textSurf, textRect = text_object(str(num),
                                     numFont, numColor)
    # Setting text rectangle's center.
    textRect.center = (
        (nodes[0][0]+(rect_arm*rect_numx/2)-(rect_arm*0.50)),
        (nodes[0][1]-(banner_h/2)))
    # Drawing text.
    screenSurface.blit(textSurf, textRect)


def text_object(text, font, color):
    # Returns text surface and rectangle.
    textSurf = font.render(text, True, color)
    return textSurf, textSurf.get_rect()


def draw_field():
    # Draw top level 'green' rectangles as minefield.
    # Rectangle color options.
    rect_color = ("#8ccc14", "#a2e345", "#d2f0c8")
    row = 0
    # Tracking mouse position as nodal index.
    mi = mouse_index()
    for node in nodes:
        i = nodes.index(node)
        # Rectangle color switching purpose.
        if (i % rect_numx) == 0:
            row = row+1
        pygame.draw.rect(
            screenSurface,
            pygame.Color(rect_color[(i+row) % 2]),
            (rect_locx[i], rect_locy[i],
             (rect_arm+1), (rect_arm+1))
        )
        # (rect_arm+1): '1' added to remove pixel gap.
        # Cell color change when mouse hovering.
        if (i == mi) and (not gameOver) and (not hoverList):
            pygame.draw.rect(screenSurface,
                             pygame.Color(rect_color[2]),
                             (rect_locx[i], rect_locy[i],
                              (rect_arm+1), (rect_arm+1)))
        # (rect_arm+1): '1' added to remove pixel gap.


def draw_hiddenField():
    # Draw lower level rectangles as hidden field,
    # when clicked.
    # Rectangle color options.
    rect_color = ("#c8beaf", "#e6d7c3", "#f0e6e1")
    # Tracking mouse position as nodal index.
    mi = mouse_index()
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
        # Cell color change when mouse hovering.
        if (i == mi) and (mine_num[i] != 0) and \
                (not gameOver) and (not hoverList):
            pygame.draw.rect(screenSurface, pygame.Color
                             (rect_color[2]),
                             (rect_locx[i], rect_locy[i],
                              (rect_arm+1), (rect_arm+1)))
        # (rect_arm+1): '1' added to remove pixel gap.


def mouse_click(mouse_event):
    # Detecting and classifying different mouse clicks.
    # Left click.
    if mouse_event.button == 1:
        mouse_LClick()
    # Right click.
    elif mouse_event.button == 3:
        mouse_RClick()


def mouse_RClick():
    # Right click operations.
    # Overwriting global variable, RclickedCell,
    # firstRClick.
    # Nodal (mine field) index value assignment.
    # These Rclick operations valid when not game over.
    global firstRClick
    if not gameOver:
        i = mouse_index()
        # Here, "i = None" means clicked outside the field.
        # Checking for non-outside & non-left Click.
        if (i is not None) and (i not in LclickedCell) and \
                (not hoverList) and (not drawModeList):
            # First Rclick operation to stop drawing
            # game controls' image.
            if firstRClick:
                firstRClick = False
            # Registering Rclick if not Rclicked before.
            if i not in RclickedCell:
                RclickedCell.append(i)
            # Unregistering Rclick if Rclicked before.
            elif i in RclickedCell:
                RclickedCell.remove(i)


def draw_flag(image, banner_h):
    # Draw flag if Rclicked, & banner flag.
    # Scaling image to the cell.
    image = pygame.transform.smoothscale(
        image, (int(rect_arm), int(rect_arm)))
    for i in RclickedCell:
        # Draw all flags if game not over.
        if not gameOver:
            screenSurface.blit(image, nodes[i])
        # Draw only correct flags if game over.
        elif i in randIndex:
            screenSurface.blit(image, nodes[i])
    # Scaling image for the banner.
    image = pygame.transform.smoothscale(
        image, (int(rect_arm*0.75), int(rect_arm*0.75)))
    imgRect = image.get_rect()
    # Setting image center.
    imgRect.center = (
        (nodes[0][0]+(rect_arm*rect_numx/2)-(rect_arm*1.1)),
        (nodes[0][1]-(banner_h/2))
    )
    # Draw banner flag.
    screenSurface.blit(image, imgRect)


def draw_clock(image, banner_h, t_init):
    # Draw clock on banner, time.
    # Scaling image for the banner.
    image = pygame.transform.smoothscale(
        image, (int(rect_arm*0.7), int(rect_arm*0.7)))
    imgRect = image.get_rect()
    # Setting image center.
    imgRect.center = (
        (nodes[0][0]+(rect_arm*rect_numx/2)+(rect_arm*0.5)),
        (nodes[0][1]-(banner_h/2))
    )
    # Draw clock.
    screenSurface.blit(image, imgRect)
    # Draw time value after first Lclick.
    draw_time(t_init, banner_h)


def draw_time(t_init, banner_h):
    # Draw time.
    # Draw time value after first Lclick.
    # Overwriting global variable, time_current
    global time_current
    # Set max time value.
    if not gameOver:
        if firstLClick:
            # Time values till the first Lclick.
            time_current = 0
        else:
            # Time values after the first Lclick.
            t_tot = pygame.time.get_ticks()
            time_current = (t_tot-t_init)//1000
        if time_current > time_max:
            # Time value can't exceed its max set value.
            time_current = time_max
    # Setting font & font color.
    # font size adjustable with window size.
    fontSize = round(rect_arm*0.50)
    numFont = pygame.font.SysFont("Arial", fontSize, True)
    numColor = WHITE
    # Getting text surface and rectangle.
    textSurf, textRect = text_object(
        str(time_current).zfill(3), numFont, numColor)
    # Setting text rectangle's center.
    textRect.center = (
        (nodes[0][0]+(rect_arm*rect_numx/2)+(rect_arm*1.25)),
        (nodes[0][1]-(banner_h/2)))
    # Drawing text.
    screenSurface.blit(textSurf, textRect)


def mouse_LClick():
    # Left click operations.
    # Overwriting global variable, LclickedCell,
    # firstLClick, time_init, drawModeList.
    # These Lclick operations valid when not game over.
    global firstLClick, time_init, mine_clicked, drawModeList,\
        index_mode, hoverList
    if not gameOver:
        # Nodal (mine field) index value assignment.
        i = mouse_index()
        # Here, "i = None" means clicked outside the field.
        # Checking for non-outside & non-right Click.
        if (i is not None) and (i not in RclickedCell) and \
                (not hoverList) and (not drawModeList):
            # First Lclick operation to generate mines
            # and remove game controls' image.
            if firstLClick:
                get_randNodes(i)
                time_init = pygame.time.get_ticks()
                firstLClick = False
            # Detecting mined cell click.
            if i in randIndex:
                mine_clicked = True
            # Detecting empty cell click.
            elif (i not in randIndex) and \
                    (mine_num[i] == 0):
                emptyCell_click(i)
            # Detecting numbered cell click.
            elif (i not in LclickedCell) and \
                    (mine_num[i] != 0):
                LclickedCell.append(i)
        # Checking Lclick position for accessing game modes list.
        # Lclick position.
        x, y = pygame.mouse.get_pos()
        # Setting valid position range.
        x_min = rectModeImg[0]
        x_max = rectModeImg[0] + rectModeImg[2]
        y_min = rectModeImg[1]
        y_max = rectModeImg[1] + rectModeImg[3]
        # Unused white gap (top & bottom) on the list
        # and 1/3rd of effective list height. (used in 2
        # places to make compatible with windows touch.)
        fPosImg = rectListImg[3]/15
        h = (rectListImg[3]-fPosImg*2)/3
        # Selecting a game mode.
        if drawModeList:
            # When clicked on unused white gap, keeping list on.
            drawModeList = 1
            # Detecting clicking zone on the list for
            # mode selection.
            if (rectListImg[0] <= x <=
                    (rectListImg[0]+rectListImg[2])):
                if (y_max+fPosImg) <= y < (y_max+fPosImg+h):
                    # If already selected, ignore.
                    if index_mode != 0:
                        game_reset()
                        index_mode = 0
                    # Making hoverList & drawModeList false/off,
                    # after mode selection.
                    hoverList, drawModeList = False, 0
                elif (y_max+fPosImg+h) <= y < (y_max+fPosImg+h*2):
                    # ""
                    if index_mode != 1:
                        game_reset()
                        index_mode = 1
                    # ""
                    hoverList, drawModeList = False, 0
                elif (y_max+fPosImg+h*2) <= y <= \
                        (y_max+fPosImg+h*3):
                    # ""
                    if index_mode != 2:
                        game_reset()
                        index_mode = 2
                    # ""
                    hoverList, drawModeList = False, 0
        # Checking Lclick position within valid range
        # for accessing mode list.
        if (x_min <= x <= x_max) and (y_min <= y <= y_max):
            # List on/off every click on the selected mode.
            drawModeList = (drawModeList+1) % 2
        elif (rectListImg[0] <= x <=
              (rectListImg[0]+rectListImg[2])) and \
            ((y_max < y < (y_max+fPosImg)) or
             ((y_max+fPosImg+h*3) < y < (y_max+fPosImg*2+h*3))):
            # List on for click on unused white space.
            drawModeList = 1
        else:
            # List off for all other clicks.
            drawModeList = 0


def draw_modeList():
    # Draw mode list.
    global hoverList
    # Scaling image for the banner.
    factor = imgList.get_width()/imgList.get_height()
    image = pygame.transform.smoothscale(
        imgList, (int(rect_arm*2*factor),
                  int(rect_arm*2)))
    imgRect = image.get_rect()
    # Setting image top left.
    imgRect.topleft = (
        (rectModeImg[0]), (rectModeImg[1]+rectModeImg[3]))
    # Draw image.
    screenSurface.blit(image, imgRect)
    rectImgList = imgRect
    # Mouse position.
    x, y = pygame.mouse.get_pos()
    # Valid position range.
    x_min = imgRect[0]
    x_max = imgRect[0]+imgRect[2]
    y_min = imgRect[1]
    y_max = imgRect[1]+imgRect[3]
    # Initializong hover area rect/dummy value.
    rectImgHover = [0, 0, 0, 0]
    # Detecting mouse hover within the range.
    if (x_min <= x <= x_max) and (y_min <= y <= y_max):
        # To activate/deactivate cell (underneath list) clicks.
        hoverList = True
        # Unused white gap (top & bottom) on the list
        # and 1/3rd of effective list height. (used in 2 places
        # to make compatible with windows touch.)
        fPosImg = imgRect[3]/15
        h = (imgRect[3]-fPosImg*2)/3
        # Scaling image and setting alpha.
        imgHover = pygame.transform.smoothscale(
            imgBlack, (int(imgRect[2]), int(h)))
        alphaImg = 50
        imgHover.set_alpha(alphaImg)
        rectImgHover = imgHover.get_rect()
        # Detecting hovering zone on the list.
        if (y_min+fPosImg) <= y < (y_min+fPosImg+h):
            # Setting image top left.
            rectImgHover.topleft = (
                imgRect[0], (imgRect[1]+fPosImg))
            screenSurface.blit(imgHover, rectImgHover)
        elif (y_min+fPosImg+h) <= y < (y_min+fPosImg+h*2):
            # Setting image top left.
            rectImgHover.topleft = (
                imgRect[0], (imgRect[1]+fPosImg+h))
            screenSurface.blit(imgHover, rectImgHover)
        elif (y_min+fPosImg+h*2) <= y <= (y_min+fPosImg+h*3):
            # Setting image top left.
            rectImgHover.topleft = (
                imgRect[0], (imgRect[1]+fPosImg+h*2))
            screenSurface.blit(imgHover, rectImgHover)
    else:
        # To activate/deactivate cell (underneath list) clicks.
        hoverList = False
    return rectImgList


def mouse_index():
    # Get mouse click nodal index on the field.
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
    i = index
    if i not in LclickedCell:
        LclickedCell.append(i)
        # Check 8 adjacent cells.
        # (click + 8 adjacent cells, in left to right &
        # top to bottom order).
        cells_index = ((i-(rect_numx+1)), (i-rect_numx),
                       (i-(rect_numx-1)), (i-1), i, (i+1),
                       (i+(rect_numx-1)), (i+rect_numx),
                       (i+(rect_numx+1)))
        # Checking for valid cell index.
        for x in cells_index:
            if x != i:
                # v = valid cell index.
                v = cell_check(x, i)
                if v is not None:
                    # Checking cell for emptyness.
                    ec_check(v)


def cell_check(cell_index, init_index):
    # Checking the cell for index validity.
    # Checking cell if it is within the range.
    if 0 <= cell_index < (rect_numx*rect_numy):
        # When clicked cell is not on the 2 side boundaries.
        if ((init_index+1) % rect_numx != 1) and \
                ((init_index+1) % rect_numx != 0):
            return cell_index
        # When clicked cell is on the left boundary,
        # declude its left side cells.
        if ((init_index+1) % rect_numx == 1) and \
            (cell_index != (init_index-1)) and \
            (cell_index != (init_index-(rect_numx+1))) and \
                (cell_index != (init_index+(rect_numx-1))):
            return cell_index
        # When clicked cell is on the right boundary,
        # declude its right side cells.
        if ((init_index+1) % rect_numx == 0) and \
            (cell_index != (init_index+1)) and \
            (cell_index != (init_index+(rect_numx+1))) and \
                (cell_index != (init_index-(rect_numx-1))):
            return cell_index
        return None
    return None


def ec_check(index):
    # Checking the cell for emptyness.
    # Overwriting global variable, LclickedCell &
    # RclickedCell.
    # If empty cell (and not a mined cell),
    # consider as clicked empty cell.
    if (mine_num[index] == 0) and (index not in randIndex):
        # Revealed empty cell, removed from Rclicked (flag).
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


def draw_cross(image):
    # Draw cross if game over and wrong flag.
    if gameOver:
        # Scaling image to the cell.
        image = pygame.transform.smoothscale(
            image, (int(rect_arm), int(rect_arm)))
        for i in RclickedCell:
            # Draw cross for wrong flag.
            if i not in randIndex:
                screenSurface.blit(image, nodes[i])


def draw_banner(img_banner, img_flag, img_clock, t_init):
    # Draw banner, border, flag count, flag.
    global rectModeImg
    # Scaling image to the field.
    img_banner = pygame.transform.smoothscale(
        img_banner, (int(rect_numx*rect_arm),
                     int(rect_arm*1.25)))
    # Get new height of the image.
    img_h = img_banner.get_height()
    screenSurface.blit(img_banner, (nodes[0][0],
                                    (nodes[0][1]-img_h)))
    # Draw a white border around the field and the banner
    # to keep the borders smooth.
    # Plus '1' to cover pixel gap.
    # Plus '10' to leave pixel gap at the field bottom.
    pygame.draw.rect(screenSurface, WHITE,
                     (nodes[0][0], (nodes[0][1]-img_h),
                      ((rect_arm*rect_numx)+1),
                      ((rect_arm*rect_numy)+img_h+10)), 2)
    # Draw flag count.
    flag_count(img_h)
    # Draw flags.
    draw_flag(img_flag, img_h)
    # Draw clock.
    draw_clock(img_clock, img_h, t_init)
    # Draw selected mode and get its rect.
    rectModeImg = mode_list[index_mode].draw_selected(img_h)


def draw_control(img_lclick, img_rclick, img_black):
    # Draw game controls till the first click on the field.
    # Setting image dimensions and alpha.
    imgDim = int(rect_numx*rect_arm*0.25)
    imgAlpha = 175
    # Scaling image to the field.
    img_black = pygame.transform.smoothscale(
        img_black, (imgDim, imgDim))
    img_lclick = pygame.transform.smoothscale(
        img_lclick, (imgDim, imgDim))
    img_rclick = pygame.transform.smoothscale(
        img_rclick, (imgDim, imgDim))
    imgLC_rect = img_lclick.get_rect()
    # Setting image center at window center.
    imgLC_rect.center = (wndwCenter[0],
                         (wndwCenter[1]-rect_arm))
    # Setting image alpha.
    img_black.set_alpha(imgAlpha)
    # Drawing images.
    images = (img_lclick, img_rclick)
    screenSurface.blit(img_black, imgLC_rect)
    # Changing image index every 2.5 seconds.
    t_tot = pygame.time.get_ticks()
    i = int(((t_tot//1000)//2.5) % 2)
    screenSurface.blit(images[i], imgLC_rect)


def draw_end(img_black, img_WinLoss, img_WinLoss1, img_clock,
             img_cup):
    # Draw game-over images and messages.
    # Filling screen with color. Updating screen.
    screenSurface.fill(WHITE)
    # Calling multiple common draw functions.
    draw_multiple()
    # Setting image dimensions' factors and alpha.
    f_dimx = int(rect_numx*rect_arm*0.5)
    f_dimy = int(rect_numy*rect_arm)
    imgAlpha = 175
    # Scaling image to the field.
    img_black = pygame.transform.smoothscale(
        img_black, (wndwWidth, wndwHeight))
    # "Play Again"/"Try Again" - image & background image.
    img_WinLoss1 = pygame.transform.smoothscale(
        img_WinLoss1, (f_dimx,
                       int(f_dimx*(img_WinLoss1.get_height() /
                                   img_WinLoss1.get_width()))))
    img_WinLoss = pygame.transform.smoothscale(
        img_WinLoss, (f_dimx,
                      int(f_dimx*(img_WinLoss.get_height() /
                                  img_WinLoss.get_width()))))
    img_clock = pygame.transform.smoothscale(
        img_clock, (int(f_dimx/5), int(f_dimx/5)))
    img_cup = pygame.transform.smoothscale(
        img_cup, (int(f_dimx*0.8/5),
                  int(f_dimx*0.8*(img_cup.get_height() /
                                  img_cup.get_width())/5)))
    # Setting image alpha.
    img_black.set_alpha(imgAlpha)
    # Drawing images.
    rectWinLoss = img_WinLoss.get_rect()
    rectWinLoss1 = img_WinLoss1.get_rect()
    rectImg_clock = img_clock.get_rect()
    rectImg_cup = img_cup.get_rect()
    rectWinLoss.center = (wndwCenter[0],
                          (wndwCenter[1]+0.25*f_dimy))
    rectWinLoss1.center = (
        wndwCenter[0],
        (rectWinLoss[1]-f_dimy/25-img_WinLoss1.get_height()/2))
    rectImg_clock.center = ((wndwCenter[0]-f_dimx/4.5),
                            (wndwCenter[1]-f_dimy/5))
    rectImg_cup.center = ((wndwCenter[0]+f_dimx/4.5),
                          (wndwCenter[1]-f_dimy/5))
    screenSurface.blit(img_black, img_black.get_rect())
    screenSurface.blit(img_WinLoss, rectWinLoss)
    screenSurface.blit(img_WinLoss1, rectWinLoss1)
    screenSurface.blit(img_clock, rectImg_clock)
    screenSurface.blit(img_cup, rectImg_cup)
    # Handle events (it's IMPORTANT to check them
    # at the end of the function to avoid unwanted
    # flag drawing by draw_banner).
    event = pygame.event.wait()
    # Checking different events.
    event_check(event)
    # Checking if game is quiting to set gameOver as false,
    # so to get out of game-over loop and proceed to exit.
    if event.type == pygame.QUIT:
        game_reset()
    # Checking Lclick position for game reset.
    if (event.type == pygame.MOUSEBUTTONDOWN) and \
            (event.button == 1):
        # Lclick position.
        x, y = pygame.mouse.get_pos()
        # Setting valid position range for game reset.
        x_min = rectWinLoss[0]
        x_max = rectWinLoss[0] + rectWinLoss[2]
        y_min = rectWinLoss[1]
        y_max = rectWinLoss[1] + rectWinLoss[3]
        # Checking Lclick position within valid range
        # for game reset.
        if (x_min <= x <= x_max) and (y_min <= y <= y_max):
            game_reset()


def event_check(event):
    # Checking different events.
    # Overwriting global variables, isRunning, wndwSize,
    # wndwWidth, wndwWidth, rect_arm, wndwCenter,
    # screenSurface.
    global isRunning, wndwSize, wndwWidth, wndwHeight, \
        rect_arm, wndwCenter, screenSurface
    # Checking if game is running.
    if event.type == pygame.QUIT:
        isRunning = False
    # Checking mouse click (down).
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_click(event)
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
        # Getting nodal points of the main rectangle.
        get_nodes()


def draw_multiple():
    # Calling multiple common draw functions.
    global rectListImg
    # Draw top-level field.
    draw_field()
    # Draw lower-level field when clicked.
    draw_hiddenField()
    # Draw nodal mine numbers.
    draw_mineNum()
    # draw cross when game-over and wrong flag.
    draw_cross(imgCross)
    # Draw mines when clicked and game-over.
    draw_mines(imgMine)
    # Drawing banner and border (calling position important).
    draw_banner(imgBanner, imgFlag, imgClock, time_init)
    # Drawing mode list and getting its rect.
    if drawModeList:
        rectListImg = draw_modeList()


def draw_result(score, pos_mirrFac):
    # Drawing result.
    # Setting font & font color.
    # Font size adjustable with window size.
    # Setting dimension/position factors.
    f_dimx = int(rect_numx*rect_arm*0.5)
    f_dimy = int(rect_numy*rect_arm)
    fontSize = round(f_dimx*0.1)
    numFont = pygame.font.SysFont("Arial", fontSize, True)
    numColor = WHITE
    # Getting text surface and rectangle.
    textSurf, textRect = text_object(
        str(score).zfill(3), numFont, numColor)
    # Setting text rectangle's center.
    textRect.center = ((wndwCenter[0]-f_dimx*pos_mirrFac/4.5),
                       (wndwCenter[1]-f_dimy/10))
    # Drawing text.
    screenSurface.blit(textSurf, textRect)


def save_result():
    # Saving result & returning the best score.
    # File directory (current & new).
    cur_path = os.getcwd()
    new_path = os.path.join(
        cur_path, "game assets", "score.csv")
    # No data-frame for pandas (before csv file creation).
    df = None
    # Pandas can't create data-frame for 'JUST' created
    # csv file. Hence it's important to try creating DF
    # when csv file already existed.
    try:
        # Data-frame for pandas (when csv file existed).
        df = pandas.read_csv(new_path)
    # pylint: disable = broad-except
    except Exception:
        # Avoiding unnecessary errors before csv file creation.
        pass
    # Columns representing game modes.
    columns = (mode_list[0].name, mode_list[1].name,
               mode_list[2].name)
    # If file doesn't exist.
    if not os.path.exists(new_path):
        # Creating a csv file (if not exists).
        f = open(new_path, "a+")
        # Creating the column headers.
        writer = csv.DictWriter(
            f, columns, lineterminator="\n")
        writer.writeheader()
    # Opening the csv file for appending operation.
    f = open(new_path, "a+")
    row = []
    # When csv file just created i.e. first time.
    if df is None:
        # First time.
        best_scr = time_current
        # Adding row to the file; time_max as dummy value.
        for mode in mode_list:
            # For current mode, add current time.
            if mode == mode_list[index_mode]:
                row.append(time_current)
            # Else add dummy value (max time).
            else:
                row.append(time_max)
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(row)
    # When csv file already existed.
    else:
        # Adding value to the file if not existed.
        if time_current not in list(df[columns[index_mode]]):
            # Adding row to the file; time_max as dummy value.
            for mode in mode_list:
                # For current mode, add current time.
                if mode == mode_list[index_mode]:
                    row.append(time_current)
                # Else add dummy value (max time).
                else:
                    row.append(time_max)
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(row)
        # Finding best score for a game mode.
        list_best = min(list(df[columns[index_mode]]))
        best_scr = list_best if (list_best < time_current) \
            else time_current
    f.close()
    return best_scr


# Setting game as running (true).
isRunning = True
firstTime = True


def game_reset():
    # Reset key game values.
    # Overwriting global variables, firstTime, gameOver.
    global firstTime, gameOver
    print("Game reset.")
    firstTime = True
    gameOver = False


# Running the game till exiting.
while isRunning:
    # Handle events.
    for e in pygame.event.get():
        # Checking different events.
        event_check(e)
    if firstTime:
        # Runs only for the first loop.
        # Reset key game values.
        wdthPerc, hgtPerc = mode_list[index_mode].wdthPerc,\
            mode_list[index_mode].hgtPerc
        mine_tot = mode_list[index_mode].mine_tot
        rect_num = (rect_numx, rect_numy)\
            = (mode_list[index_mode].rect_numx,
               mode_list[index_mode].rect_numy)
        rect_arm = max(min((wndwHeight*hgtPerc/rect_numy),
                           (wndwWidth*wdthPerc/rect_numx)),
                       minRectArm)
        minWndwWidth = (minRectArm*rect_numx)/wdthPerc
        minWndwHeight = (minRectArm*rect_numy)/hgtPerc
        # Limiting minimum window size.
        if wndwWidth < minWndwWidth:
            wndwWidth = int(round(minWndwWidth, 0))
        if wndwHeight < minWndwHeight:
            wndwHeight = int(round(minWndwHeight, 0))
        wndwSize = wndwWidth, wndwHeight
        # Getting nodal points of the main rectangle.
        get_nodes()
        # Initializing clicked cell's nodal index.
        # Initializing mine_clicked, firstLClick,
        # firstRClick, waitTime & gameOver state.
        LclickedCell = []
        RclickedCell = []
        mine_clicked = False
        gameOver = False
        firstLClick = True
        firstRClick = True
        waitTime = 2000
        # first Lclick (mouse_LClick()) to generate mines,
        # get_randNodes() & mine_count().
        # first Rclick (mouse_RClick()) to stop drawing
        # game control.
        # Initializing a list for nodal mine numbers.
        mine_num = [0]*(rect_numx*rect_numy)
        firstTime = False
        print("One time")
        screenSurface = screen.set_mode(wndwSize,
                                        pygame.RESIZABLE)
    # Filling screen with color. Updating screen.
    screenSurface.fill(WHITE)
    # Calling multiple common draw functions.
    draw_multiple()
    # Draw game controls till the first click on the field.
    if firstLClick and firstRClick:
        draw_control(imgLclick, imgRclick, imgBlack)
    if mine_clicked:
        gameOver = True
        # Detect mine cells and draw mines.
        draw_mines(imgMine)
        # Calling multiple common draw functions.
        draw_multiple()
        # Update screen.
        screen.flip()
        # wait for sometime in milisecs.
        pygame.time.wait(waitTime)
        # Making a dummy event to solve touch-input
        # issue with continuing to gameOver loop.
        pygame.event.post(
            pygame.event.Event(pygame.USEREVENT, attr="Dummy"))
        while gameOver:
            # Draw game-over images and messages.
            draw_end(imgBlack, imgLoss, imgLoss1, imgClock,
                     imgCup)
            # Update the screen.
            screen.flip()
    # If all mines are found.
    elif (len(nodes)-len(LclickedCell)) == mine_tot:
        gameOver = True
        # Update screen.
        screen.flip()
        # Saving result & getting the best score.
        best_score = save_result()
        # wait for sometime in milisecs.
        pygame.time.wait(waitTime)
        # Making a dummy event to solve touch-input
        # issue with continuing to gameOver loop.
        pygame.event.post(
            pygame.event.Event(pygame.USEREVENT, attr="Dummy"))
        while gameOver:
            # Draw game-over images and messages.
            draw_end(imgBlack, imgWin, imgWin1, imgClock,
                     imgCup)
            # Drawing current score
            # (1 is drawing position factor).
            draw_result(time_current, 1)
            # Drawing best score
            # (-1 is drawing position factor).
            draw_result(best_score, -1)
            # Update the screen.
            screen.flip()
    # Update screen.
    screen.flip()
    # Running the loop at specific FPS.
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit(0)
