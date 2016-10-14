import random, sys, time, math, pygame
from pygame.locals import *

FPS                 =   30
WIN_WIDTH           =   640
WIN_HEIGHT          =   480
HALF_WIN_WIDTH      =   int(WIN_WIDTH / 2)
HALF_WIN_HEIGHT     =   int(WIN_HEIGHT / 2)

GRASS_COLOR         =   (24,    255,    0)
WHITE               =   (255,   255,    255)
RED                 =   (255,   0,      0)

CAMERA_SLACK        =   90
MOVE_RATE           =   9
BOUNCE_RATE         =   6
BOUNCE_HEIGHT       =   30
START_SIZE          =   25
WIN_SIZE            =   300
INVULN_TIME         =   2
GAME_OVER_TIME      =   4
MAX_HELATH          =   3
NUM_GRASS           =   80
NUM_SQUIRRELS       =   30
SQURREL_MIN_SPEED   =   3
SQURREL_MAX_SPEED   =   7
DIR_CHANGE_FREQ     =   2
LEFT                =   'left'
RIGHT               =   'right'

def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, L_SQUIR_IMG, R_SQUIR_IMG, GRASS_IMAGES

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('../ImageFiles/SquirrelEatSquirrel/gameicon.png'))
    DISPLAY_SURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Squirrel Eat Squirrel')
    BASIC_FONT  = pygame.font.Font('freesansbold.ttf', 32)

    L_SQUIR_IMG = pygame.image.load('../ImageFiles/SquirrelEatSquirrel/squirrel.png')
    R_SQUIR_IMG = pygame.transform.flip(L_SQUIR_IMG, True, False)
    GRASS_IMAGES = []
    for i in range(1, 5):
        GRASS_IMAGES.append(pygame.image.load('../ImageFiles/SquirrelEatSquirrel/grass%s.png' % i))

    while True:
        runGame()

def runGame():
    invulnerable_mode = False
    invulnerable_start_time = 0
    game_over_mode = False
    game_over_start_time = 0
    win_mode = False

    game_over_surf = BASIC_FONT.render('Game Over', True, WHITE)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)

    win_surf = BASIC_FONT.render('You have achieved OMEGA SQUIRREL!', True, WHITE)
    win_rect = win_surf.get_rect()
    win_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)

    win_surf2 = BASIC_FONT.render('(Press "r" to restart.)', True, WHITE)
    win_rect2 = win_surf2.get_rect()
    win_rect2.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT + 30)

    camera_x = 0
    camera_y = 0

    grass_objs = []
    squirrel_objs = []
    player_obj = {'surface' : pygame.transform.scale(L_SQUIR_IMG, (START_SIZE, START_SIZE)),
                  'facing'  : LEFT,
                  'size'    : START_SIZE,
                  'x'       : HALF_WIN_WIDTH,
                  'y'       : HALF_WIN_HEIGHT,
                  'bounce'  : 0,
                  'health'  : MAX_HELATH}

    move_left = False
    move_right = False
    move_up = False
    move_down = False

    for i in range(10):
        grass_objs.append(makeNewGrass(camera_x, camera_y))
        grass_objs[i]['x'] = random.randint(0, WIN_WIDTH)
        grass_objs[i]['y'] = random.randint(0, WIN_HEIGHT)

    while True:
        if invulnerable_mode and time.time() - invulnerable_start_time > INVULN_TIME:
            invulnerable_mode = False

        for s_obj in squirrel_objs:
            s_obj['x'] += s_obj['move_x']
            s_obj['y'] += s_obj['move_y']
            s_obj['bounce'] += 1
            if s_obj['bounce'] > s_obj['bounce_rate']:
                s_obj['bounce'] = 0

            if random.randint(0, 99) < DIR_CHANGE_FREQ:
                s_obj['move_x'] = getRandomVelocity()
                s_obj['move_y'] = getRandomVelocity()
                if s_obj['move_x'] > 0:
                    s_obj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (s_obj['width'], s_obj['height']))
                else:
                    s_obj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (s_obj['width'], s_obj['height']))

        for i in range(len(grass_objs) - 1, -1, -1):
            if isOutsideActiveArea(camera_x, camera_y, grass_objs[i]):
                del grass_objs[i]
        for i in range(len(squirrel_objs) - 1, -1, -1):
            if isOutsideActiveArea(camera_x, camera_y, squirrel_objs[i]):
                del squirrel_objs[i]

        while len(grass_objs) < NUM_GRASS:
            grass_objs.append(makeNewGrass(camera_x, camera_y))
        while len(squirrel_objs) < NUM_SQUIRRELS:
            squirrel_objs.append(makeNewSquirrel(camera_x, camera_y))

        player_center_x = player_obj['x'] + int(player_obj['size'] / 2)
        player_center_y = player_obj['y'] + int(player_obj['size'] / 2)
        
        if (camera_x + HALF_WIN_WIDTH) - player_center_x > CAMERA_SLACK:
            camera_x = player_center_x + CAMERA_SLACK - HALF_WIN_WIDTH
        elif player_center_x - (camera_x + HALF_WIN_WIDTH) > CAMERA_SLACK:
            camera_x = player_center_x - CAMERA_SLACK - HALF_WIN_WIDTH
            
        if (camera_y + HALF_WIN_HEIGHT) - player_center_y > CAMERA_SLACK:
            camera_y = player_center_y + CAMERA_SLACK - HALF_WIN_HEIGHT
        elif player_center_y - (camera_y + HALF_WIN_HEIGHT) > CAMERA_SLACK:
            camera_y = player_center_y - CAMERA_SLACK - HALF_WIN_HEIGHT

        DISPLAY_SURF.fill(GRASS_COLOR)

        for g_obj in grass_objs:
            g_rect = pygame.Rect((g_obj['x'] - camera_x, g_obj['y'] - camera_y, g_obj['width'], g_obj['height']))
            DISPLAY_SURF.blit(GRASS_IMAGES[g_obj['grass_image']], g_rect)

        for s_obj in squirrel_objs:
            s_obj['rect'] = pygame.Rect((s_obj['x'] - camera_x, s_obj['y'] - camera_y - getBounceAmount(s_obj['bounce'], s_obj['bounce_rate'], s_obj['bounce_height']), s_obj['width'], s_obj['height']))
            DISPLAY_SURF.blit(s_obj['surface'], s_obj['rect'])

        flash_is_on = round(time.time(), 1) * 10 % 2 == 1
        if not game_over_mode and not (invulnerable_mode and flash_is_on):
            player_obj['rect'] = pygame.Rect((player_obj['x'] - camera_x, player_obj['y'] - camera_y - getBounceAmount(s_obj['bounce'], BOUNCE_RATE, BOUNCE_HEIGHT), player_obj['size'], player_obj['size']))
            DISPLAY_SURF.blit(player_obj['surface'], player_obj['rect'])

        drawHealthMeter(player_obj['health'])

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    move_down = False
                    move_up = True
                elif event.key in (K_DOWN, K_s):
                    move_up = False
                    move_down = True
                elif event.key in (K_LEFT, K_a):
                    move_right = False
                    move_left = True
                    if player_obj['facing'] == RIGHT:
                        player_obj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (player_obj['size'], player_obj['size']))
                    player_obj['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d):
                    move_left = False
                    move_right = True
                    if player_obj['facing'] == LEFT:
                        player_obj['surface'] = pygame.transform.scale(R_SQUIR_IMG,
                                                                       (player_obj['size'], player_obj['size']))
                    player_obj['facing'] = RIGHT
                elif win_mode and event.key == K_r:
                    return
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    move_left = False
                elif event.key in (K_RIGHT, K_d):
                    move_right = False
                elif event.key in (K_UP, K_w):
                    move_up = False
                elif event.key in (K_DOWN, K_s):
                    move_down = False

                elif event.key == K_ESCAPE:
                    terminate()

        if not game_over_mode:
            if move_left:
                player_obj['x'] -= MOVE_RATE
            if move_right:
                player_obj['x'] += MOVE_RATE
            if move_up:
                player_obj['y'] -= MOVE_RATE
            if move_down:
                player_obj['y'] += MOVE_RATE

            if (move_left or move_right or move_up or move_down) or player_obj['bounce'] != 0:
                player_obj['bounce'] += 1
            if player_obj['bounce'] > BOUNCE_RATE:
                player_obj['bounce'] = 0

            for i in range(len(squirrel_objs) - 1, -1, -1):
                sq_obj = squirrel_objs[i]
                if 'rect' in sq_obj and player_obj['rect'].colliderect(sq_obj['rect']):
                    if sq_obj['width'] * sq_obj['height'] <= player_obj['size'] ** 2:
                        player_obj['size'] += int((sq_obj['width'] * sq_obj['height']) ** 0.2) + 1
                        del squirrel_objs[i]

                        if player_obj['facing'] == LEFT:
                            player_obj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (player_obj['size'], player_obj['size']))
                        if player_obj['facing'] == RIGHT:
                            player_obj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (player_obj['size'], player_obj['size']))

                        if player_obj['size'] > WIN_SIZE:
                            win_mode = True
                    elif not invulnerable_mode:
                        invulnerable_mode = True
                        invulnerable_start_time = time.time()
                        player_obj['health'] -= 1
                        if player_obj['health'] == 0:
                            game_over_mode = True
                            game_over_start_time = time.time()

        else:
            DISPLAY_SURF.blit(game_over_surf, game_over_rect)
            if time.time() - game_over_start_time > GAME_OVER_TIME:
                return

        if win_mode:
            DISPLAY_SURF.blit(win_surf, win_rect)
            DISPLAY_SURF.blit(win_surf2, win_rect2)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def drawHealthMeter(current_health):
    for i in range(current_health):
        pygame.draw.rect(DISPLAY_SURF, RED, (15, 5 + (10 * MAX_HELATH) - i * 10, 20, 10))
    for i in range(MAX_HELATH):
        pygame.draw.rect(DISPLAY_SURF, WHITE, (15, 5 + (10 * MAX_HELATH) - i * 10, 20, 10), 1)

def terminate():
    pygame.quit()
    sys.exit()

def getBounceAmount(current_bounce, bounce_rate, bounce_height):
    return  int(math.sin((math.pi / float(bounce_rate)) * current_bounce) * bounce_height)

def getRandomVelocity():
    speed = random.randint(SQURREL_MIN_SPEED, SQURREL_MAX_SPEED)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return  -speed

def getRandomOffCameraPos(camera_x, camera_y, obj_width, obj_height):
    camera_rect = pygame.Rect(camera_x, camera_y, WIN_WIDTH, WIN_HEIGHT)
    while True:
        x = random.randint(camera_x - WIN_WIDTH, camera_x + (2 * WIN_WIDTH))
        y = random.randint(camera_y - WIN_HEIGHT, camera_y + (2 * WIN_HEIGHT))
        obj_rect = pygame.Rect(x, y, obj_width, obj_height)
        if not obj_rect.colliderect(camera_rect):
            return x, y

def makeNewSquirrel(camera_x, camera_y):
    sq                  = {}
    general_size        = random.randint(5, 25)
    multiplier          = random.randint(1, 3)
    sq['width']         = (general_size + random.randint(0, 10)) * multiplier
    sq['height']        = (general_size + random.randint(0, 10)) * multiplier
    sq['x'], sq['y']    = getRandomOffCameraPos(camera_x, camera_y, sq['width'], sq['height'])
    sq['move_x']        = getRandomVelocity()
    sq['move_y']        = getRandomVelocity()
    if sq['move_x'] < 0:
        sq['surface']   = pygame.transform.scale(L_SQUIR_IMG, (sq['width'], sq['height']))
    else:
        sq['surface']   = pygame.transform.scale(R_SQUIR_IMG, (sq['width'], sq['height']))
    sq['bounce']        = 0
    sq['bounce_rate']   = random.randint(10, 18)
    sq['bounce_height'] = random.randint(10, 50)
    return  sq

def makeNewGrass(camera_x, camera_y):
    gr                  = {}
    gr['grass_image']   = random.randint(0, len(GRASS_IMAGES) - 1)
    gr['width']         = GRASS_IMAGES[0].get_width()
    gr['height']        = GRASS_IMAGES[0].get_height()
    gr['x'], gr['y']    = getRandomOffCameraPos(camera_x, camera_y, gr['width'], gr['height'])
    gr['rect']          = pygame.Rect((gr['x'], gr['y'], gr['width'], gr['height']))
    return gr

def isOutsideActiveArea(camera_x, camera_y, obj):
    bounds_left_edge = camera_x - WIN_WIDTH
    bounds_top_edge = camera_y - WIN_HEIGHT
    bounds_rect = pygame.Rect(bounds_left_edge, bounds_top_edge, WIN_WIDTH * 3, WIN_HEIGHT * 3)
    obj_rect    = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return  not bounds_rect.colliderect(obj_rect)

if __name__ == '__main__':
    main()