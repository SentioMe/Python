import random, sys, copy, os, pygame
from pygame.locals import *

FPS                     =   30
WIN_WIDTH               =   800
WIN_HEIGHT              =   600
HALF_WIN_WIDTH          =   int(WIN_WIDTH / 2)
HALF_WIN_HEIGHT         =   int(WIN_HEIGHT / 2)

TILE_WIDTH              =   50
TILE_HEIGHT             =   85
TILE_FLOOR_HEIGHT       =   45

CAM_MOVE_SPEED          =   5

OUTSIDE_DECORATION_PCT  =   20

BRIGHT_BLUE             =   (0,     170,    255)
WHITE                   =   (255,   255,    255)
BG_COLOR                =   BRIGHT_BLUE
TEXT_COLOR              =   WHITE

UP                      =   'up'
DOWN                    =   'down'
LEFT                    =   'left'
RIGHT                   =   'right'

FONT_NAME               =   'freesansbold.ttf'

def main():
    global FPS_CLOCK, DISPLAY_SURF, IMAGES_DICT, TILE_MAPPING, OUTSIDE_DECO_MAPPING, BASIC_FONT, PLAYER_IMAGES, CURRENT_IMAGE

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()

    DISPLAY_SURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.display.set_caption('Star Pusher')
    BASIC_FONT = pygame.font.Font(FONT_NAME, 18)

    IMAGES_DICT = {'uncovered_goal' :   loadImage('RedSelector'),
                   'covered_goal'   :   loadImage('Selector'),
                   'star'           :   loadImage('Star'),
                   'corner'         :   loadImage('Wall_Block_Tall'),
                   'wall'           :   loadImage('Wood_Block_Tall'),
                   'inside_floor'   :   loadImage('Plain_Block'),
                   'outside_floor'  :   loadImage('Grass_Block'),
                   'title'          :   loadImage('star_title'),
                   'solved'         :   loadImage('star_solved'),
                   'princess'       :   loadImage('princess'),
                   'boy'            :   loadImage('boy'),
                   'cat_girl'       :   loadImage('catgirl'),
                   'horn_girl'      :   loadImage('horngirl'),
                   'pink_girl'      :   loadImage('pinkgirl'),
                   'rock'           :   loadImage('Rock'),
                   'short_tree'     :   loadImage('Tree_Short'),
                   'tall_tree'      :   loadImage('Tree_Tall'),
                   'ugly_tree'      :   loadImage('Tree_Ugly')}

    TILE_MAPPING = {'x' :   IMAGES_DICT['corner'],
                    '#' :   IMAGES_DICT['wall'],
                    'o' :   IMAGES_DICT['inside_floor'],
                    ' ' :   IMAGES_DICT['outside_floor']}

    OUTSIDE_DECO_MAPPING = {'1' :   IMAGES_DICT['rock'],
                            '2' :   IMAGES_DICT['short_tree'],
                            '3' :   IMAGES_DICT['tall_tree'],
                            '4' :   IMAGES_DICT['ugly_tree']}

    CURRENT_IMAGE   =   0
    PLAYER_IMAGES   =   [IMAGES_DICT['princess'],
                         IMAGES_DICT['boy'],
                         IMAGES_DICT['cat_girl'],
                         IMAGES_DICT['horn_girl'],
                         IMAGES_DICT['pink_girl']]

    startScreen()

    levels = readLevelsFile('../DataFiles/StarPusher/starPusherLevels.txt')
    current_level_index = 0

    while True:
        result = runLevel(levels, current_level_index)

        if result in ('solved', 'next'):
            current_level_index += 1
            if current_level_index >= len(levels):
                current_level_index = 0
        elif result == 'back':
            current_level_index -= 1
            if current_level_index < 0:
                current_level_index = len(levels) - 1
        elif result == 'reset':
            pass

def runLevel(levels, level_num):
    global CURRENT_IMAGE
    level_obj = levels[level_num]
    map_obj = decorateMap(level_obj['map_obj'], level_obj['start_state']['player'])
    game_state_obj = copy.deepcopy(level_obj['start_state'])
    map_needs_redraw = True
    level_surf = BASIC_FONT.render('Level %s of %s' % (level_obj['level_num'] + 1, len(levels)), 1, TEXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.bottomleft = (20, WIN_HEIGHT - 35)
    map_width = len(map_obj) * TILE_WIDTH
    map_height = (len(map_obj[0]) - 1) * (TILE_HEIGHT - TILE_FLOOR_HEIGHT) + TILE_HEIGHT

    MAX_CAM_X_PAN = abs(HALF_WIN_HEIGHT - int(map_height / 2)) + TILE_WIDTH
    MAX_CAM_Y_PAN = abs(HALF_WIN_WIDTH - int(map_width / 2)) + TILE_HEIGHT

    level_is_complete = False

    camera_offset_x = 0
    camera_offset_y = 0

    camera_up = False
    camera_down = False
    camera_left = False
    camera_right = False

    while True:
        player_move_to = None
        key_pressed = False

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                key_pressed = True
                if event.key == K_LEFT:
                    player_move_to = LEFT
                elif event.key == K_RIGHT:
                    player_move_to = RIGHT
                elif event.key == K_UP:
                    player_move_to = UP
                elif event.key == K_DOWN:
                    player_move_to = DOWN
                elif event.key == K_a:
                    camera_left = True
                elif event.key == K_d:
                    camera_right = True
                elif event.key == K_w:
                    camera_up = True
                elif event.key == K_s:
                    camera_down = True

                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'

                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_BACKSPACE:
                    return 'reset'
                elif event.key == K_p:
                    CURRENT_IMAGE += 1
                    if CURRENT_IMAGE >= len(PLAYER_IMAGES):
                        CURRENT_IMAGE = 0
                    map_needs_redraw = True
            elif event.type == KEYUP:
                if event.key == K_a:
                    camera_left = False
                elif event.key == K_d:
                    camera_right = False
                elif event.key == K_w:
                    camera_up = False
                elif event.key == K_s:
                    camera_down = False

        if player_move_to != None and not level_is_complete:
            moved = makeMove(map_obj, game_state_obj, player_move_to)

            if moved:
                game_state_obj['step_counter'] += 1
                map_needs_redraw = True
            if isLevelFinished(level_obj, game_state_obj):
                level_is_complete = True
                key_pressed = False

        DISPLAY_SURF.fill(BG_COLOR)

        if map_needs_redraw:
            map_surf = drawMap(map_obj, game_state_obj, level_obj['goals'])
            map_needs_redraw = False

        if camera_up and camera_offset_y < MAX_CAM_X_PAN:
            camera_offset_y += CAM_MOVE_SPEED
        elif camera_down and camera_offset_y > -MAX_CAM_X_PAN:
            camera_offset_y -= CAM_MOVE_SPEED

        if camera_left and camera_offset_x < MAX_CAM_Y_PAN:
            camera_offset_x += CAM_MOVE_SPEED
        elif camera_right and camera_offset_x > -MAX_CAM_Y_PAN:
            camera_offset_x -= CAM_MOVE_SPEED

        map_surf_rect = map_surf.get_rect()
        map_surf_rect.center = (HALF_WIN_WIDTH + camera_offset_x, HALF_WIN_HEIGHT + camera_offset_y)

        DISPLAY_SURF.blit(map_surf, map_surf_rect)

        DISPLAY_SURF.blit(level_surf, level_rect)
        step_surf = BASIC_FONT.render('Steps: %s' % (game_state_obj['step_counter']), 1, TEXT_COLOR)
        step_rect = step_surf.get_rect()
        step_rect.bottomleft = (20, WIN_HEIGHT - 10)
        DISPLAY_SURF.blit(step_surf, step_rect)

        if level_is_complete:
            solved_rect = IMAGES_DICT['solved'].get_rect()
            solved_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)
            DISPLAY_SURF.blit(IMAGES_DICT['solved'], solved_rect)

            if key_pressed:
                return 'solved'

        pygame.display.update()
        FPS_CLOCK.tick()

def isWall(map_obj, x, y):
    if x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
        return  False
    elif map_obj[x][y] in ('#', 'x'):
        return  True

    return  False

def decorateMap(map_obj, start_x_y):

    start_x, start_y = start_x_y
    map_obj_copy = copy.deepcopy(map_obj)

    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):
            if map_obj_copy[x][y] in ('$', '.', '@', '+', '*'):
                map_obj_copy[x][y] = ' '

    floodFill(map_obj_copy, start_x, start_y, ' ', 'o')

    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):

            if map_obj_copy[x][y] == '#':
                if (isWall(map_obj_copy, x, y - 1) and isWall(map_obj_copy, x + 1, y)) or\
                    (isWall(map_obj_copy, x + 1, y) and isWall(map_obj_copy, x, y + 1)) or\
                    (isWall(map_obj_copy, x, y + 1) and isWall(map_obj_copy, x - 1, y)) or\
                    (isWall(map_obj_copy, x - 1, y) and isWall(map_obj_copy, x, y - 1)):
                    map_obj_copy[x][y] = 'x'
            elif map_obj_copy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
                map_obj_copy[x][y] = random.choice(list(OUTSIDE_DECO_MAPPING.keys()))

    return  map_obj_copy

def isBlocked(map_obj, game_state_obj, x, y):

    if isWall(map_obj, x, y):
        return  True
    elif x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[0]):
        return  True
    elif (x, y) in game_state_obj['stars']:
        return True

    return  False

def makeMove(map_obj, game_state_obj, player_move_to):
    player_x, player_y = game_state_obj['player']
    stars = game_state_obj['stars']

    if player_move_to == UP:
        x_offset = 0
        y_offset = -1
    elif player_move_to == RIGHT:
        x_offset = 1
        y_offset = 0
    elif player_move_to == DOWN:
        x_offset = 0
        y_offset = 1
    elif player_move_to == LEFT:
        x_offset = -1
        y_offset = 0

    if isWall(map_obj, player_x + x_offset, player_y + y_offset):
        return False
    else:
        if (player_x + x_offset, player_y + y_offset) in stars:
            if not isBlocked(map_obj, game_state_obj, player_x + (x_offset * 2), player_y + (y_offset * 2)):
                ind = stars.index((player_x + x_offset, player_y + y_offset))
                stars[ind] = (stars[ind][0] + x_offset, stars[ind][1] + y_offset)
            else:
                return False

        game_state_obj['player'] = (player_x + x_offset, player_y + y_offset)
        return True

def startScreen():
    title_rect = IMAGES_DICT['title'].get_rect()
    top_coord = 50
    title_rect.top = top_coord
    title_rect.centerx = HALF_WIN_WIDTH
    top_coord += title_rect.height

    instruction_text = ['Push the stars over the marks.',
                        'Arrow keys to move, WASD for camera control, P to change character.',
                        'Backspace to reset level, Esc to quit.',
                        'N for next level, B to go back a level.']

    DISPLAY_SURF.fill(BG_COLOR)
    DISPLAY_SURF.blit(IMAGES_DICT['title'], title_rect)

    for i in range(len(instruction_text)):
        inst_surf = BASIC_FONT.render(instruction_text[i], 1, TEXT_COLOR)
        inst_rect = inst_surf.get_rect()
        top_coord += 10
        inst_rect.top = top_coord
        inst_rect.centerx = HALF_WIN_WIDTH
        top_coord += inst_rect.height
        DISPLAY_SURF.blit(inst_surf, inst_rect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        FPS_CLOCK.tick()

def readLevelsFile(file_name):
    assert os.path.exists(file_name), 'Cannot find the level file: %s' % (file_name)

    map_file = open(file_name, 'r')
    content = map_file.readlines() + ['\r\n']
    map_file.close()

    levels = []
    level_num = 0
    map_text_lines = []
    map_obj = []
    for line_num in range(len(content)):
        line = content[line_num].rstrip('\r\n')

        if ';' in line:
            line = line[:line.find(';')]

        if line != '':
            map_text_lines.append(line)
        elif line == '' and len(map_text_lines) > 0:

            max_width = -1
            for i in range(len(map_text_lines)):
                if len(map_text_lines[i]) > max_width:
                    max_width = len(map_text_lines[i])

            for i in range(len(map_text_lines)):
                map_text_lines[i] += ' ' * (max_width - len(map_text_lines[i]))

            for x in range(len(map_text_lines[0])):
                map_obj.append([])
            for y in range(len(map_text_lines)):
                for x in range(max_width):
                    map_obj[x].append(map_text_lines[y][x])

            start_x = None
            start_y = None
            goals = []
            stars = []

            for x in range(max_width):
                for y in range(len(map_obj[x])):
                    if map_obj[x][y] in ('@', '+'):
                        start_x = x
                        start_y = y
                    if map_obj[x][y] in ('.', '+', '*'):
                        goals.append((x, y))
                    if map_obj[x][y] in ('$', '*'):
                        stars.append((x, y))

            assert start_x != None and start_y != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (level_num + 1, line_num, file_name)
            assert len(goals) > 0, 'Level %s (around line %s) in %s must have at least one goal.' % (level_num + 1, line_num, file_name)
            assert len(stars) >= len(goals), 'Level %s (around line %s) in %s is impossible to solve. It has %s goals but only %s stars.' % (level_num + 1, line_num, file_name, len(goals), len(stars))

            game_state_obj = {'player'          :   (start_x, start_y),
                              'step_counter'    :   0,
                              'stars'           :   stars}

            level_obj = {'width'        :   max_width,
                         'height'       :   len(map_obj),
                         'map_obj'      :   map_obj,
                         'goals'        :   goals,
                         'start_state'  :   game_state_obj,
                         'level_num'    :   level_num}

            levels.append(level_obj)

            map_text_lines = []
            map_obj = []
            game_state_obj = {}
            level_num += 1

    return  levels

def floodFill(map_obj, x, y, old_character, new_character):

    if map_obj[x][y] == old_character:
        map_obj[x][y] = new_character

    if x < len(map_obj) - 1 and map_obj[x + 1][y] == old_character:
        floodFill(map_obj, x + 1, y, old_character, new_character)
    if x > 0 and map_obj[x - 1][y] == old_character:
        floodFill(map_obj, x - 1, y, old_character, new_character)
    if y < len(map_obj[x]) - 1 and map_obj[x][y + 1] == old_character:
        floodFill(map_obj, x, y + 1, old_character, new_character)
    if y > 0 and map_obj[x][y - 1] == old_character:
        floodFill(map_obj, x, y - 1, old_character, new_character)

def drawMap(map_obj, game_state_obj, goals):

    map_surf_width = len(map_obj) * TILE_WIDTH
    map_surf_height = (len(map_obj[0]) - 1) * (TILE_HEIGHT - TILE_FLOOR_HEIGHT) + TILE_HEIGHT
    map_surf = pygame.Surface((map_surf_width, map_surf_height))
    map_surf.fill(BG_COLOR)

    for x in range(len(map_obj)):
        for y in range(len(map_obj[x])):
            space_rect = pygame.Rect((x * TILE_WIDTH, y * (TILE_HEIGHT - TILE_FLOOR_HEIGHT), TILE_WIDTH, TILE_HEIGHT))
            if map_obj[x][y] in TILE_MAPPING:
                base_tile = TILE_MAPPING[map_obj[x][y]]
            elif map_obj[x][y] in OUTSIDE_DECO_MAPPING:
                base_tile = TILE_MAPPING[' ']

            map_surf.blit(base_tile, space_rect)

            if map_obj[x][y] in OUTSIDE_DECO_MAPPING:
                map_surf.blit(OUTSIDE_DECO_MAPPING[map_obj[x][y]], space_rect)
            elif (x, y) in game_state_obj['stars']:
                if (x, y) in goals:
                    map_surf.blit(IMAGES_DICT['covered_goal'], space_rect)
                map_surf.blit(IMAGES_DICT['star'], space_rect)
            elif (x, y) in goals:
                map_surf.blit(IMAGES_DICT['uncovered_goal'], space_rect)

            if (x, y) == game_state_obj['player']:
                map_surf.blit(PLAYER_IMAGES[CURRENT_IMAGE], space_rect)

    return  map_surf

def isLevelFinished(level_obj, game_state_obj):
    for goal in level_obj['goals']:
        if goal not in game_state_obj['stars']:
            return False

    return  True

def terminate():
    pygame.quit()
    sys.exit()

def loadImage(file_name):
    return pygame.image.load('../ImageFiles/StarPusher/%s.png' %file_name)

if __name__ == '__main__':
    main()