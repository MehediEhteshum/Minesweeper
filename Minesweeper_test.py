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

# Loading images.
imgBanner = pygame.image.load(
    "game assets/Banner.png").convert()
imgClock = pygame.image.load(
    "game assets/Clock.png").convert_alpha()
imgCross = pygame.image.load(
    "game assets/Cross.png").convert_alpha()
imgFlag = pygame.image.load(
    "game assets/Flag.png").convert_alpha()
iconImage = pygame.image.load(
    "game assets/icon.png").convert_alpha()

# Setting display icon.
screen.set_icon(iconImage)

# Setting basic colors.
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
# Initializing firstClick state.
nodes = []
randNodes = []
randIndex = []
rect_locx = []
rect_locy = []
firstClick = True
time_init = 0
time_current = 0


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


def get_randNodes(firstClick_index):
    # Getting random node points for mines
    # based on first Lclick.
    global randNodes
    randNodes.clear()
    randIndex.clear()
    # Overwriting global variables,
    # randNodes & randIndex.
    i = firstClick_index
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
        pygame.draw.rect(screenSurface,
                         pygame.Color(rect_color[(i+row) % 2]),
                         (rect_locx[i], rect_locy[i],
                          (rect_arm+1), (rect_arm+1)))
        # Cell color change when mouse hovering.
        if (i == mi) and (not gameOver):
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
        if (i == mi) and (mine_num[i] != 0) and \
                (not gameOver):
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
    # Overwriting global variable, RclickedCell.
    # Nodal (mine field) index value assignment.
    # These Rclick operations valid when not game over.
    if not gameOver:
        i = mouse_index()
        # Here, "i = None" means clicked outside the field.
        # Checking for non-outside & non-left Click.
        if (i is not None) and (i not in LclickedCell):
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
    t_max = 999
    if not gameOver:
        if firstClick:
            # Time values till the first Lclick.
            time_current = 0
        else:
            # Time values after the first Lclick.
            t_tot = pygame.time.get_ticks()
            time_current = (t_tot-t_init)//1000
        if time_current > t_max:
            # Time value can't exceed its max set value.
            time_current = t_max
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
    # firstClick, time_init.
    # These Lclick operations valid when not game over.
    global firstClick, time_init
    if not gameOver:
        # Nodal (mine field) index value assignment.
        i = mouse_index()
        # Here, "i = None" means clicked outside the field.
        # Checking for non-outside & non-right Click.
        if (i is not None) and (i not in RclickedCell):
            # First Lclick operation to generate mines.
            if firstClick:
                get_randNodes(i)
                time_init = pygame.time.get_ticks()
                firstClick = False
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
    # These Lclick operations valid when game over.
    elif gameOver:
        # Nodal (mine field) index value assignment.
        i = mouse_index()
        # Here, "i = None" means clicked outside the field.
        # Checking for outside & non-right Click.
        if (i is None) and (i not in RclickedCell):
            # Reset game.
            game_reset()


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
    # If empty cell, consider as clicked empty cell.
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


def minedCell_click(index):
    # Operations if clicked mine
    # (reveal all mine cells).
    # Overwriting global variable, LclickedCell
    # & mine_clicked.
    # Reveal clicked mine cell.
    global mine_clicked
    if index not in LclickedCell:
        LclickedCell.append(index)
    # Reveal all other mine cells (randNodes)
    # except those are flagged.
    for i in randIndex:
        if (i not in LclickedCell) and \
                (i not in RclickedCell):
            LclickedCell.append(i)
    mine_clicked = True


def draw_cross(image):
    # Draw cross if game over and wrong flag.
    # Scaling image to the cell.
    image = pygame.transform.smoothscale(
        image, (int(rect_arm), int(rect_arm)))
    for i in RclickedCell:
        # Draw cross for wrong flag.
        if i not in randIndex:
            screenSurface.blit(image, nodes[i])


def draw_banner(img_banner, img_flag, img_clock, t_init):
    # Draw banner, border, flag count, flag.
    # Scaling image to the field.
    img_banner = pygame.transform.smoothscale(
        img_banner, (int(rect_numx*rect_arm), int(rect_arm*1.25)))
    # Get new height of the image.
    img_h = img_banner.get_height()
    screenSurface.blit(img_banner, (nodes[0][0],
                                    (nodes[0][1]-img_h)))
    # Draw a white border around the field and the banner
    # to keep the borders smooth.
    # Plus '1' to cover pixel gap.
    pygame.draw.rect(screenSurface, WHITE,
                     (nodes[0][0], (nodes[0][1]-img_h),
                      ((rect_arm*rect_numx)+1),
                      ((rect_arm*rect_numx)+img_h)), 2)
    # Draw flag count.
    flag_count(img_h)
    # Draw flags.
    draw_flag(img_flag, img_h)
    # Draw clock.
    draw_clock(img_clock, img_h, t_init)


# Setting game as running (true).
isRunning = True
firstTime = True


def game_reset():
    # Reset key game values.
    # Overwriting global variables, firstTime.
    global firstTime
    print("Game reset.")
    firstTime = True


# Running the game till exiting.
while isRunning:
    # Getting nodal points of the main rectangle.
    get_nodes()
    # Handle user-input.
    for event in pygame.event.get():
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
    if firstTime:
        # Runs only for the first loop.
        # Reset key game values.
        # Initializing clicked cell's nodal index.
        # Initializing mine_clicked, firstClick
        # & gameOver state.
        LclickedCell = []
        RclickedCell = []
        mine_clicked = False
        gameOver = False
        firstClick = True
        # first Lclick (mouse_LClick()) to generate mines,
        # get_randNodes() & mine_count().
        # Initializing a list for nodal mine numbers.
        mine_num = [0]*(rect_numx*rect_numy)
        firstTime = False
        print("One time")
    # Filling screen color. Updating screen.
    screenSurface.fill(WHITE)
    # """ screenSurface.blit(sampleImage, sampleImageRect) """
    draw_field()
    draw_hiddenField()
    draw_mines()
    draw_mineNum()
    if mine_clicked:
        # Draw cross if wrong flag.
        draw_cross(imgCross)
        gameOver = True
        print("TRY AGAIN")
    elif (len(nodes)-len(LclickedCell)) == mine_tot:
        gameOver = True
        print("SCORE. PLAY AGAIN")
    # Drawing banner and border (calling position important).
    draw_banner(imgBanner, imgFlag, imgClock, time_init)
    screen.flip()

pygame.quit()
