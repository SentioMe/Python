import pygame, sys,random
from pygame.locals import *

BOARD_WIDTH     =   4
BOARD_HEIGHT    =   4
TILE_SIZE       =   80
WINDOW_WIDTH    =   640
WINDOW_HEIGHT   =   480
FPS             =   30
BLANK           =   None

BLACK           =   (0,     0,      0)
WHITE           =   (255,   255,    255)
BRIGHT_BLUE     =   (0,     50,     255)
DARK_TURQUOISE  =   (3,     54,     73)
GREEN           =   (0,     204,    0)

BG_COLOR        =   DARK_TURQUOISE
TILE_COLOR      =   GREEN
TEXT_COLOR      =   WHITE
BORDER_COLOR    =   BRIGHT_BLUE
BASIC_FONT_SIZE =   20

BUTTON_COLOR    =   WHITE
BUTTON_TEXT_COLOR   =   BLACK
MESSAGE_COLOR   =   WHITE

X_MARGIN        =   int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1)))/2)
Y_MARGIN        =   int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1)))/2)

UP              =   'up'
DOWN            =   'down'
LEFT            =   'left'
RIGHT           =   'right'

def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF    =   pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASIC_FONT      =   pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    #create menu button surface and rect
    RESET_SURF, RESET_RECT  = makeText('Reset',     TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 90)
    NEW_SURF, NEW_RECT      = makeText('New Game',  TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT  = makeText('Solve',     TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 30)


    main_board, solution_seq = generateNewPuzzle(80)    #create game data and automation moved record
    SOLVED_BOARD    = getStartingBoard()                #one more get start board it means, compaired solve data

    '''
    Exist many algorithm what solve slide puzzle
    but this game used simple clear logic
    It this mean, saved automation and manual all move
    And needs solve, reverse data
    ex)
    123     user move           123         solve                   123
    456     =>                  456         =>                      456
    78N                         7N8                                 78N
            saved N left move               reverse N right move
    '''
    all_moves   =   []

    while True:
        slide_to = None                     #check is moved?
        msg = ''

        if main_board == SOLVED_BOARD:
            msg = 'Solved!'

        drawBoard(main_board, msg)

        #This game checked first event, what quit a game
        checkForQuit()

        #Checked controller with mouse and keyboard(arrow and wasd)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spot_x, spot_y = getSpotClicked(main_board, event.pos[0], event.pos[1])
                if (spot_x, spot_y) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(main_board, all_moves)
                    elif NEW_RECT.collidepoint(event.pos):
                        main_board, solution_seq = generateNewPuzzle(80)
                        all_moves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(main_board, solution_seq + all_moves)
                        all_moves = []
                else:
                    blank_x, blank_y = getBlankPosition(main_board)
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        slide_to = LEFT
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        slide_to = RIGHT
                    elif spot_x == blank_x and spot_y == blank_y + 1:
                        slide_to = UP
                    elif spot_x == blank_x and spot_y == blank_y - 1:
                        slide_to = DOWN

            elif event.type == KEYUP:
                # event.key in (key value1, ...) == event.key == 'key value1' or event.key == ...
                if event.key in (K_LEFT, K_a) and isValidMove(main_board, LEFT):
                    slide_to = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(main_board, RIGHT):
                    slide_to = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(main_board, UP):
                    slide_to = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(main_board, DOWN):
                    slide_to = DOWN

        #If moved tile then slide tile
        if slide_to:
            slideAnimation(main_board, slide_to, 'Click tile or press arrow keys to slide.', 8)
            makeMove(main_board, slide_to)
            all_moves.append(slide_to)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def getStartingBoard():

    '''
    Create board datas
    1. This datas are 2d list
    2. [[1, 1 + column count * i, ...],[2, 2 + column count * i],...]
    3. The last item is null
    '''

    counter = 1
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(counter)
            counter += BOARD_WIDTH
        board.append(column)
        counter -= BOARD_WIDTH * (BOARD_HEIGHT - 1) + BOARD_WIDTH - 1

    board[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = None
    return board

def getBlankPosition(board):

    #Find null item and return index
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == None:
                return (x, y)

def makeMove(board, move):

    blank_x, blank_y = getBlankPosition(board)
    move_x, move_y = blank_x, blank_y

    if move == UP:
        move_y += 1
    elif move == DOWN:
        move_y -= 1
    elif move == LEFT:
        move_x += 1
    elif move == RIGHT:
        move_x -= 1

    #swap blank, moved position
    board[blank_x][blank_y], board[move_x][move_y] = board[move_x][move_y], board[blank_x][blank_y]

def isValidMove(board, move):

    '''
    We remember what board is 2D list
    It is means, 'board[0] is 1d list', len(board[0]) is means size of board row
    '''
    blank_x, blank_y = getBlankPosition(board)

    # '\' is means not end this line
    return (move == UP and blank_y != len(board[0]) - 1) \
           or (move == DOWN and blank_y != 0) \
           or (move == LEFT and blank_x != len(board) - 1) \
           or (move == RIGHT and blank_x != 0)

def getRandomMove(board, last_move = None):

    valid_moves = [UP, DOWN, LEFT, RIGHT]

    if last_move == UP or not isValidMove(board, DOWN):
        valid_moves.remove(DOWN)
    if last_move == DOWN or not isValidMove(board, UP):
        valid_moves.remove(UP)
    if last_move == LEFT or not isValidMove(board, RIGHT):
        valid_moves.remove(RIGHT)
    if last_move == RIGHT or not isValidMove(board, LEFT):
        valid_moves.remove(LEFT)

    return random.choice(valid_moves)

def getLeftTopOfTIle(tile_x, tile_y):
    left = X_MARGIN + (tile_x * TILE_SIZE) + (tile_x - 1)
    top = Y_MARGIN + (tile_y * TILE_SIZE) + (tile_y - 1)

    return  (left, top)

def getSpotClicked(board, x, y):

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            left, top = getLeftTopOfTIle(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tile_rect.collidepoint(x, y):
                return (tile_x, tile_y)

    return (None, None)

def drawTile(tile_x, tile_y, number, adj_x = 0, adj_y = 0):

    left, top = getLeftTopOfTIle(tile_x, tile_y)
    pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, (left + adj_x, top + adj_y, TILE_SIZE, TILE_SIZE))
    text_surf = BASIC_FONT.render(str(number), True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(TILE_SIZE / 2) + adj_x, top + int(TILE_SIZE / 2) + adj_y
    DISPLAY_SURF.blit(text_surf, text_rect)

def makeText(text, color, bg_color, top, left):
    #pygame needs many code in text rendering => functionize
    text_surf = BASIC_FONT.render(text, True, color, bg_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return (text_surf, text_rect)

def drawBoard(board, message):

    DISPLAY_SURF.fill(BG_COLOR)
    if message:
        text_surf, text_rect = makeText(message, MESSAGE_COLOR, BG_COLOR, 5, 5)
        DISPLAY_SURF.blit(text_surf, text_rect)

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            if board[tile_x][tile_y]:
                drawTile(tile_x, tile_y, board[tile_x][tile_y])

    left, top = getLeftTopOfTIle(0, 0)
    width = BOARD_WIDTH * TILE_SIZE
    height = BOARD_HEIGHT * TILE_SIZE
    pygame.draw.rect(DISPLAY_SURF, BORDER_COLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAY_SURF.blit(RESET_SURF, RESET_RECT)
    DISPLAY_SURF.blit(NEW_SURF, NEW_RECT)
    DISPLAY_SURF.blit(SOLVE_SURF, SOLVE_RECT)

def slideAnimation(board, direction, message, animation_speed):

    blank_x, blank_y = getBlankPosition(board)
    move_x, move_y = blank_x, blank_y

    if direction == UP:
        move_y += 1
    elif direction == DOWN:
        move_y -= 1
    elif direction == LEFT:
        move_x += 1
    elif direction == RIGHT:
        move_x -= 1

    '''
    Very impoartant!
    Why copied surface?
    : Under the loop, updated rendering frame
      If not copied original surface, we seem stretch a moved tile
    '''

    drawBoard(board, message)
    base_surf = DISPLAY_SURF.copy()
    move_left, move_top = getLeftTopOfTIle(move_x, move_y)
    pygame.draw.rect(base_surf, BG_COLOR, (move_left, move_top, TILE_SIZE, TILE_SIZE))

    for i in range(0, TILE_SIZE, animation_speed):
        checkForQuit()
        DISPLAY_SURF.blit(base_surf, (0, 0))
        if direction == UP:
            drawTile(move_x, move_y, board[move_x][move_y], 0, -i)
        if direction == DOWN:
            drawTile(move_x, move_y, board[move_x][move_y], 0, i)
        if direction == LEFT:
            drawTile(move_x, move_y, board[move_x][move_y], -i, 0)
        if direction == RIGHT:
            drawTile(move_x, move_y, board[move_x][move_y], i, 0)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def generateNewPuzzle(num_slides):

    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)           #User check time (answer)
    last_move = None

    '''
    Create randomize data
    -> must be current time move not equal opposite of prev time move
       getRandomMove() returend current time move direction
    '''

    for i in range(num_slides):
        move = getRandomMove(board, last_move)
        slideAnimation(board, move, 'Generating new puzzle...', int(TILE_SIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        last_move = move

    return (board, sequence)

def resetAnimation(board, all_moves):

    #copied all_moves list, and reverse items
    rev_all_moves = all_moves[:]    #This operator '[:]' is not reference copy, it this create same size list and copy items
    rev_all_moves.reverse()

    for move in rev_all_moves:
        if move == UP:
            opposite_move = DOWN
        elif move == DOWN:
            opposite_move = UP
        elif move == RIGHT:
            opposite_move = LEFT
        elif move == LEFT:
            opposite_move = RIGHT
        slideAnimation(board, opposite_move, '', int(TILE_SIZE / 2))
        makeMove(board, opposite_move)

if __name__ == '__main__':
    main()