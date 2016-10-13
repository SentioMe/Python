import random, time, pygame, sys
from pygame.locals import *

FPS                 =   25
WINDOW_WIDTH        =   640
WINDOW_HEGIHT       =   480
BOX_SIZE            =   20
BOARD_WIDTH         =   10
BOARD_HEIGHT        =   20
BLANK               =   '.'

MOVE_SIDE_WAYS_FREQ =   0.15
MOVE_DOWN_FREQ      =   0.1

X_MARGIN            =   int((WINDOW_WIDTH - BOARD_WIDTH * BOX_SIZE) / 2)
TOP_MARGIN          =   WINDOW_HEGIHT - (BOARD_HEIGHT * BOX_SIZE) - 5

WHITE               =   (255,   255,    255)
GRAY                =   (185,   185,    185)
BLACK               =   (0,     0,      0)
RED                 =   (155,   0,      0)
LIGHT_RED           =   (175,   0,      0)
GREEN               =   (0,     155,    0)
LIGHT_GREEN         =   (0,     175,    0)
BLUE                =   (0,     0,      155)
LIGHT_BLUE          =   (20,    20,     175)
YELLOW              =   (155,   155,    0)
LIGHT_YELLOW        =   (175,   175,    20)

BORDER_COLOR        =   BLUE
BG_COLOR            =   BLACK
TEXT_COLOR          =   WHITE
TEXT_SHADOW_COLOR   =   GRAY
COLORS              =   (BLUE,  GREEN,  RED,    YELLOW)
LIGHT_COLORS        =   (LIGHT_BLUE,    LIGHT_GREEN,    LIGHT_RED,  LIGHT_YELLOW)
assert len(COLORS) == len(LIGHT_COLORS), "Each colors must have light colors"

TEMPLATE_WIDTH      =   5
TEMPLATE_HEIGHT     =   5

S_SHAPE_TEMPLATE    =   [['.....',
                          '.....',
                          '..00.',
                          '.00..',
                          '.....'],
                         ['.....',
                          '..0..',
                          '..00.',
                          '...0.',
                          '.....']]

Z_SHAPE_TEMPLATE    =   [['.....',
                          '.....',
                          '.00..',
                          '..00.',
                          '.....'],
                         ['.....',
                          '..0..',
                          '.00..',
                          '.0...',
                          '.....']]

I_SHAPE_TEMPLATE    =   [['..0..',
                          '..0..',
                          '..0..',
                          '..0..',
                          '.....'],
                         ['.....',
                          '.....',
                          '0000.',
                          '.....',
                          '.....']]

O_SHAPE_TEMPLATE    =   [['.....',
                          '.....',
                          '.00..',
                          '.00..',
                          '.....']]

J_SHAPE_TEMPLATE    =   [['.....',
                          '.0...',
                          '.000.',
                          '.....',
                          '.....'],
                         ['.....',
                          '..00.',
                          '..0..',
                          '..0..',
                          '.....'],
                         ['.....',
                          '.....',
                          '.000.',
                          '...0.',
                          '.....'],
                         ['.....',
                          '..0..',
                          '..0..',
                          '.00..',
                          '.....']]

L_SHAPE_TEMPLATE    =   [['.....',
                          '...0.',
                          '.000.',
                          '.....',
                          '.....'],
                         ['.....',
                          '..0..',
                          '..0..',
                          '..00.',
                          '.....'],
                         ['.....',
                          '.....',
                          '.000.',
                          '.0...',
                          '.....'],
                         ['.....',
                          '.00..',
                          '..0..',
                          '..0..',
                          '.....']]

T_SHAPE_TEMPLATE    =   [['.....',
                          '..0..',
                          '.000.',
                          '.....',
                          '.....'],
                         ['.....',
                          '..0..',
                          '..00.',
                          '..0..',
                          '.....'],
                         ['.....',
                          '.....',
                          '.000.',
                          '..0..',
                          '.....'],
                         ['.....',
                          '..0..',
                          '.00..',
                          '..0..',
                          '.....']]

SHAPES              =   {'S':S_SHAPE_TEMPLATE,
                         'Z':Z_SHAPE_TEMPLATE,
                         'J':J_SHAPE_TEMPLATE,
                         'L':L_SHAPE_TEMPLATE,
                         'I':I_SHAPE_TEMPLATE,
                         'O':O_SHAPE_TEMPLATE,
                         'T':T_SHAPE_TEMPLATE}

def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, BIG_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEGIHT))
    BASIC_FONT  = pygame.font.Font('freesansbold.ttf', 18)
    BIG_FONT    = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')
    while True:
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('../SoundFiles/tetrisb.mid')
        else:
            pygame.mixer.music.load('../SoundFiles/tetrisc.mid')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():

    board = getBlankBoard()
    last_move_down_time = time.time()
    last_move_sideways_time = time.time()
    last_fall_time = time.time()

    moving_down = False
    moving_left = False
    moving_right = False

    score = 0
    level, fall_freq = calculateLevelAndFallFreq(score)

    falling_piece = getNewPiece()
    next_piece = getNewPiece()

    while True:
        if falling_piece == None:
            falling_piece = next_piece
            next_piece = getNewPiece()
            last_fall_time = time.time()

            if not isValidPosition(board, falling_piece):
                return

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if (event.key == K_p):
                    DISPLAY_SURF.fill(BG_COLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
                    last_fall_time = time.time()
                    last_move_down_time = time.time()
                    last_move_sideways_time = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    moving_left = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    moving_right = False
                elif (event.key == K_DOWN or event.key == K_s):
                    moving_down = False
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, falling_piece, adj_x=-1):
                    falling_piece['x'] -= 1
                    moving_left = True
                    moving_right = False
                    last_move_sideways_time = time.time()
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, falling_piece, adj_x=1):
                    falling_piece['x'] += 1
                    moving_right = True
                    moving_left = False
                    last_move_sideways_time = time.time()
                elif (event.key == K_UP or event.key == K_w) :
                    falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(SHAPES[falling_piece['shape']])
                    if not isValidPosition(board, falling_piece):
                        falling_piece['rotation'] =  (falling_piece['rotation'] - 1) % len(SHAPES[falling_piece['shape']])
                elif (event.key == K_q) :
                    falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(SHAPES[falling_piece['shape']])
                    if not isValidPosition(board, falling_piece):
                        falling_piece['rotation'] =  (falling_piece['rotation'] + 1) % len(SHAPES[falling_piece['shape']])
                elif (event.key == K_DOWN or event.key == K_s):
                    moving_down = True
                    if isValidPosition(board, falling_piece, adj_y=1):
                        falling_piece['y'] += 1
                    last_move_down_time = time.time()
                elif event.key == K_SPACE:
                    moving_down = False
                    moving_left = False
                    moving_right = False
                    for i in range(1, BOARD_HEIGHT):
                        if not isValidPosition(board,falling_piece, adj_y=i):
                            break
                    falling_piece['y'] += i - 1

        if (moving_left or moving_right) and time.time() - last_move_sideways_time > MOVE_SIDE_WAYS_FREQ:
            if moving_left and isValidPosition(board, falling_piece, adj_x=-1):
                falling_piece['x'] -= 1
            elif moving_right and isValidPosition(board, falling_piece, adj_x=1):
                falling_piece['x'] += 1
            last_move_sideways_time = time.time()

        if moving_down and time.time() - last_move_down_time > MOVE_DOWN_FREQ and isValidPosition(board, falling_piece, adj_y=1):
            falling_piece['y'] += 1
            last_move_down_time = time.time()

        if time.time() - last_fall_time > fall_freq:
            if not isValidPosition(board, falling_piece, adj_y=1):
                addToBoard(board, falling_piece)
                score += removeCompleteLines(board)
                level, fall_freq = calculateLevelAndFallFreq(score)
                falling_piece = None
            else:
                falling_piece['y'] += 1
                last_fall_time = time.time()

        DISPLAY_SURF.fill(BG_COLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(next_piece)
        if falling_piece != None:
            drawPiece(falling_piece)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():

    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key

    return  None

def showTextScreen(text):

    title_surf, title_rect = makeTextObjs(text, BIG_FONT, TEXT_SHADOW_COLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEGIHT / 2))
    DISPLAY_SURF.blit(title_surf, title_rect)

    title_surf, title_rect = makeTextObjs(text, BIG_FONT, TEXT_COLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEGIHT / 2) - 3)
    DISPLAY_SURF.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = makeTextObjs('Press a key to play.', BASIC_FONT, TEXT_COLOR)
    press_key_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEGIHT / 2) + 100)
    DISPLAY_SURF.blit(press_key_surf, press_key_rect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPS_CLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def calculateLevelAndFallFreq(score):
    level = int(score / 10) + 1
    fall_freq = 0.27 - (level * 0.02)
    return  level, fall_freq

def getNewPiece():

    shape = random.choice(list(SHAPES.keys()))
    new_piece = {'shape':shape,
                 'rotation':random.randint(0, len(SHAPES[shape]) - 1),
                 'x': int(BOARD_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                 'y': -2,
                 'color' : random.randint(0, len(COLORS) - 1)}

    return  new_piece

def addToBoard(board, piece):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

def getBlankBoard():
    board = []
    for i in range(BOARD_WIDTH):
        board.append([BLANK] * BOARD_HEIGHT)
    return board

def isOnBoard(x, y):
    return x >= 0 and x < BOARD_WIDTH and y < BOARD_HEIGHT

def isValidPosition(board, piece, adj_x = 0, adj_y = 0):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            if is_above_board or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return  False
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False

    return  True

def isCompleteLine(board, y):
    for x in range(BOARD_WIDTH):
        if board[x][y] == BLANK:
            return False

    return  True

def removeCompleteLines(board):
    num_lines_removed = 0
    y = BOARD_HEIGHT - 1

    while y >= 0:
        if isCompleteLine(board, y):
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARD_WIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y - 1]

            for x in range(BOARD_WIDTH):
                board[x][0] = BLANK

            num_lines_removed += 1
        else:
            y -= 1

    return  num_lines_removed

def convertToPixelCoords(box_x, box_y):
    return (X_MARGIN + (box_x * BOX_SIZE)), (TOP_MARGIN + (box_y * BOX_SIZE))

def drawBox(box_x, box_y, color, pixel_x = None, pixel_y = None):
    if color == BLANK:
        return
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convertToPixelCoords(box_x, box_y)
    pygame.draw.rect(DISPLAY_SURF, COLORS[color], (pixel_x + 1, pixel_y + 1, BOX_SIZE - 1, BOX_SIZE - 1))
    pygame.draw.rect(DISPLAY_SURF, LIGHT_COLORS[color], (pixel_x + 1, pixel_y + 1, BOX_SIZE -4 , BOX_SIZE - 4))

def drawBoard(board):
    pygame.draw.rect(DISPLAY_SURF, BORDER_COLOR, (X_MARGIN - 3, TOP_MARGIN - 7, (BOARD_WIDTH * BOX_SIZE) + 8, (BOARD_HEIGHT * BOX_SIZE) + 8), 5)
    pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (X_MARGIN, TOP_MARGIN, BOX_SIZE * BOARD_WIDTH, BOX_SIZE * BOARD_HEIGHT))

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            drawBox(x, y, board[x][y])
            
def drawStatus(score, level):
    score_surf = BASIC_FONT.render('Score: %s' % score, True, TEXT_COLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 150, 20)
    DISPLAY_SURF.blit(score_surf, score_rect)

    level_surf = BASIC_FONT.render('Level: %s' % level, True, TEXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOW_WIDTH - 150, 50)
    DISPLAY_SURF.blit(level_surf, level_rect)

def drawPiece(piece, pixel_x = None, pixel_y = None):
    shape_to_draw = SHAPES[piece['shape']][piece['rotation']]
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if shape_to_draw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixel_x + (x * BOX_SIZE), pixel_y + (y * BOX_SIZE))

def drawNextPiece(piece):
    next_surf = BASIC_FONT.render('Next: ', True, TEXT_COLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOW_WIDTH - 120, 80)

    drawPiece(piece, pixel_x = WINDOW_WIDTH - 120, pixel_y = 100)

if __name__ == '__main__':
    main()