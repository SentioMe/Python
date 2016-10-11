import random, pygame, sys
from pygame.locals import *

#---------------------------------------------------------------------------------------------------------------------
'''
GAME SETTINGS
'''
FPS                 =   30
WINDOW_WIDTH        =   640
WINDOW_HEIGHT       =   480
REVEAL_SPEED        =   8
BOX_SIZE            =   40
GAP_SIZE            =   10
BOARD_WIDTH         =   10
BOARD_HEIGHT        =   7
assert  (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
X_MARGIN            =   int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN            =   int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

#                        R      G       B
GRAY                =   (100,   100,    100)
NAVY_BLUE           =   ( 60,    60,    100)
WHITE               =   (255,   255,    255)
RED                 =   (255,     0,      0)
GREEN               =   (  0,   255,      0)
BLUE                =   (  0,     0,    255)
YELLOW              =   (255,   255,      0)
ORANGE              =   (255,   128,      0)
PURPLE              =   (255,     0,    255)
CYAN                =   (  0,   255,    255)

BG_COLOR            =   NAVY_BLUE
LIGHT_BG_COLOR      =   GRAY
BOX_COLOR           =   WHITE
HIGH_LIGHT_COLOR    =   BLUE

DONUT               =   'donut'
SQUARE              =   'square'
DIAMOND             =   'diamond'
LINES               =   'lines'
OVAL                =   'oval'

ALL_COLORS          =   (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES          =   (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert  len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT,    'Board is too big for the number of shapes / colors defines.'
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
'''
GAME LOGIC
'''

def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    #coordinate of mouse event
    mouse_x = 0
    mouse_y = 0
    pygame.display.set_caption('Memory Game')

    main_board = getRandomizedBoard()
    revealed_boxes = generateRevealedBoxesData(False)

    first_selection = None

    DISPLAY_SURF.fill(BG_COLOR)
    startGameAnimation(main_board)

    while True:
        mouse_clicked = False

        DISPLAY_SURF.fill(BG_COLOR)
        drawBoard(main_board, revealed_boxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        box_x, box_y = getBoxAtPixel(mouse_x, mouse_y)
        if box_x != None and box_y != None:
            if not revealed_boxes[box_x][box_y]:
                drawHighlightBox(box_x, box_y)
            if not revealed_boxes[box_x][box_y] and mouse_clicked:
                revealBoxesAnimation(main_board, [(box_x, box_y)])
                revealed_boxes[box_x][box_y] = True

                if first_selection == None:
                    first_selection = (box_x, box_y)
                else:
                    icon1shape, icon1color = getShapeAndColor(main_board, first_selection[0], first_selection[1])
                    icon2shape, icon2color = getShapeAndColor(main_board, box_x, box_y)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(main_board, [(first_selection[0], first_selection[1]), (box_x, box_y)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[box_x][box_y] = False
                    elif hasWon(revealed_boxes):
                        gameWonAnimation(main_board)
                        pygame.time.wait(2000)

                        main_board = getRandomizedBoard()
                        revealed_boxes = generateRevealedBoxesData(False)

                        drawBoard(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(main_board)
                    first_selection = None

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def generateRevealedBoxesData(val):
    revealed_boxes = []
    for i in range(BOARD_WIDTH):
        revealed_boxes.append([val] * BOARD_HEIGHT)
    return revealed_boxes

def getRandomizedBoard():

    #create list what in all colors & shapes data
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape, color))

    #list randomize
    random.shuffle(icons)
    num_icons_used = int(BOARD_WIDTH * BOARD_HEIGHT / 2)
    icons = icons[:num_icons_used] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons.pop())      #origin source : column.append(icons[0]), del icons[0]
        board.append(column)

    return board

def splitIntoGroupOf(groups_size, the_list):

    result = []
    for i in range(0, len(the_list), groups_size):
        result.append(the_list[i:i + groups_size])

    return result

def leftTopCoordsOfBox(box_x, box_y):

    #Convert board coordinates to pixel coordinates
    left    = box_x * (BOX_SIZE + GAP_SIZE) + X_MARGIN
    top     =   box_y * (BOX_SIZE + GAP_SIZE) + Y_MARGIN

    return (left,top)

def getBoxAtPixel(x, y):

    for box_x in range(BOARD_WIDTH):
        for box_y in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box_rect.collidepoint(x, y):
                return (box_x, box_y)

    return (None, None)

def drawIcon(shape, color, box_x, box_y):
    quarter = int(BOX_SIZE * 0.25)
    half    = int(BOX_SIZE * 0.5)

    left, top = leftTopCoordsOfBox(box_x, box_y)

    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY_SURF, BG_COLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURF, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY_SURF, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAY_SURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAY_SURF, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURF, color, (left, top + quarter, BOX_SIZE, half))

def getShapeAndColor(board, box_x, box_y):
    return board[box_x][box_y][0], board[box_x][box_y][1]

def drawBoxCovers(board, boxes, coverage):

    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (left, top, BOX_SIZE, BOX_SIZE))

        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, coverage, BOX_SIZE))

    pygame.display.update()
    FPS_CLOCK.tick(FPS)

def revealBoxesAnimation(board, boxes_to_reveal):

    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, - REVEAL_SPEED):
        drawBoxCovers(board, boxes_to_reveal, coverage)

def coverBoxesAnimation(board, boxes_to_cover):

    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
        drawBoxCovers(board, boxes_to_cover, coverage)

def drawBoard(board, revealed):

    for box_x in range(BOARD_WIDTH):
        for box_y in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            if not revealed[box_x][box_y]:
                pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                shape, color = getShapeAndColor(board, box_x, box_y)
                drawIcon(shape, color, box_x, box_y)

def drawHighlightBox(box_x, box_y):
    left, top = leftTopCoordsOfBox(box_x, box_y)
    pygame.draw.rect(DISPLAY_SURF, HIGH_LIGHT_COLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)

def startGameAnimation(board):

    covered_boxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    box_groups = splitIntoGroupOf(8, boxes)

    drawBoard(board, covered_boxes)
    for box_group in box_groups:
        revealBoxesAnimation(board, box_group)
        coverBoxesAnimation(board, box_group)

def gameWonAnimation(board):

    covered_boxes = generateRevealedBoxesData(True)
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAY_SURF.fill(color1)
        drawBoard(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealed_boxes):

    for i in revealed_boxes:
        if False in i:
            return False

    return True

if __name__ == '__main__':
    main()

#---------------------------------------------------------------------------------------------------------------------