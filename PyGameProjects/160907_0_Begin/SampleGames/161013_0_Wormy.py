import random, pygame, sys
from pygame.locals import *

FPS                     =   15
WINDOW_WIDTH            =   640
WINDOW_HEIGHT           =   480
CELL_SIZE               =   20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH              =   int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT             =   int(WINDOW_HEIGHT / CELL_SIZE)

WHITE                   =   (255,   255,    255)
BLACK                   =   (0,     0,      0)
RED                     =   (255,   0,      0)
GREEN                   =   (0,     255,    0)
DARK_GREEN              =   (0,     155,    0)
DARK_GRAY               =   (40,    40,     40)
BG_COLOR                =   BLACK

UP                      =   'up'
DOWN                    =   'down'
LEFT                    =   'left'
RIGHT                   =   'right'

HEAD                    =   0

def main():
    global  FPS_CLOCK,  DISPLAY_SURF,   BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF    =   pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT      =   pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartsScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():

    start_x = random.randint(5, CELL_WIDTH - 6)
    start_y = random.randint(5, CELL_HEIGHT - 6)

    '''
    worm_coords data
    type : list
    item : dictionary
            [x, y coordinate]
    '''
    worm_coords = [{'x': start_x,       'y': start_y},
                   {'x': start_x - 1,   'y': start_y},
                   {'x': start_x - 2,   'y': start_y}]

    direction = RIGHT

    apple = getRandomLocation()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            #The worm can not move in the opposite direction in which conducted
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                        direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                        direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                        direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        #GameOver : Collide between wall and worm head
        if worm_coords[HEAD]['x'] == -1 or worm_coords[HEAD]['x'] == CELL_WIDTH or worm_coords[HEAD]['y'] == -1 or worm_coords[HEAD]['y'] == CELL_HEIGHT:
            return
        #GameOver : Collide between worm head and body parts
        for worm_body in worm_coords[1:]:
            if worm_body['x'] == worm_coords[HEAD]['x'] and worm_body['y'] == worm_coords[HEAD]['y']:
                return
        #Collide between apple and worm head -> move apple by new position
        if worm_coords[HEAD]['x'] == apple['x'] and worm_coords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()
        #Worm move is very simple in this game logic
        #One Frame : Loop{ [0][1][2] => remove last item => [0][1] => insert new item at first position with direction [new][0][1] == [0][1][2] }
        else:
            del worm_coords[-1]

        if direction == UP:
            newHead = {'x':worm_coords[HEAD]['x'], 'y':worm_coords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x':worm_coords[HEAD]['x'], 'y':worm_coords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x':worm_coords[HEAD]['x'] - 1, 'y':worm_coords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x':worm_coords[HEAD]['x'] + 1, 'y':worm_coords[HEAD]['y']}

        worm_coords.insert(0, newHead)
        DISPLAY_SURF.fill(BG_COLOR)
        drawGrid()
        drawWorm(worm_coords)
        drawApple(apple)
        drawScore(len(worm_coords) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def drawPressKeyMsg():
    press_key_surf = BASIC_FONT.render('Press a key to play.', True, DARK_GRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAY_SURF.blit(press_key_surf, press_key_rect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return  None
    if key_up_events[0].key == K_ESCAPE:
        terminate()

    return key_up_events[0].key

def showStartsScreen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surf1 = title_font.render('Wormy!', True, WHITE, DARK_GREEN)
    title_surf2 = title_font.render('Wormy!', True, GREEN)

    degrees1    =   0
    degrees2    =   0

    while True:
        DISPLAY_SURF.fill(BG_COLOR)

        '''
               pygame.transform.rotate : Doesn't change the surface object what passed param
                                         It's create a new surface(copied param) and rotate

                note : Rotate must have original surface, and rotated surface doesn't rotate one more
                       Because, pixel not matching from rotated image
         '''

        rotated_surf1   =   pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1   =   rotated_surf1.get_rect()
        rotated_rect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY_SURF.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY_SURF.blit(rotated_surf2, rotated_rect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x':random.randint(0, CELL_WIDTH - 1), 'y':random.randint(0, CELL_HEIGHT - 1)}

def showGameOverScreen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surf       = game_over_font.render('Game', True, WHITE)
    over_surf       = game_over_font.render('Over', True, WHITE)
    game_rect       = game_surf.get_rect()
    over_rect       = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    DISPLAY_SURF.blit(game_surf, game_rect)
    DISPLAY_SURF.blit(over_surf, over_rect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    score_surf = BASIC_FONT.render('Score: %s' % (score), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY_SURF.blit(score_surf, score_rect)

def drawWorm(worm_coords):
    for coord in worm_coords:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, DARK_GREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY_SURF, GREEN, worm_inner_segment_rect)

def drawApple(coord):
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, RED, apple_rect)

def drawGrid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(DISPLAY_SURF, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(DISPLAY_SURF, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

if __name__ == '__main__':
    main()