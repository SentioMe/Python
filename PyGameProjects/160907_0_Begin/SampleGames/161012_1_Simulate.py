import random, sys, time, pygame
from pygame.locals import *

FPS                 =   30
WINDOW_WIDTH        =   640
WINDOW_HEIGHT       =   480
FLASH_SPEED         =   500
FLASH_DELAY         =   200
BUTTON_SIZE         =   200
BUTTON_GAP_SIZE     =   20
TIME_OUT            =   4

WHITE               =   (255,   255,    255)
BLACK               =   (0,     0,      0)
BRIGHT_RED          =   (255,   0,      0)
RED                 =   (155,   0,      0)
BRIGHT_GREEN        =   (0,     255,    0)
GREEN               =   (0,     155,    0)
BRIGHT_BLUE         =   (0,     0,      255)
BLUE                =   (0,     0,      155)
BRIGHT_YELLOW       =   (255,   255,    0)
YELLOW              =   (155,   155,    0)
DARK_GRAY           =   (40,    40,     40)

BG_COLOR            =   BLACK

X_MARGIN            =   int((WINDOW_WIDTH - (2 * BUTTON_SIZE) - BUTTON_GAP_SIZE) / 2)
Y_MARGIN            =   int((WINDOW_HEIGHT - (2 * BUTTON_SIZE) - BUTTON_GAP_SIZE) / 2)

YELLOW_RECT         =   pygame.Rect(X_MARGIN, Y_MARGIN, BUTTON_SIZE, BUTTON_SIZE)
BLUE_RECT           =   pygame.Rect(X_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, Y_MARGIN, BUTTON_SIZE, BUTTON_SIZE)
RED_RECT            =   pygame.Rect(X_MARGIN, Y_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, BUTTON_SIZE, BUTTON_SIZE)
GREEN_RECT          =   pygame.Rect(X_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, Y_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, BUTTON_SIZE, BUTTON_SIZE)

def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Simulate')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)

    info_surf = BASIC_FONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys', 1, DARK_GRAY)
    info_rect = info_surf.get_rect()
    info_rect.topleft = (10, WINDOW_HEIGHT - 25)

    BEEP1 = pygame.mixer.Sound('../SoundFiles/beep1.ogg')
    BEEP2 = pygame.mixer.Sound('../SoundFiles/beep2.ogg')
    BEEP3 = pygame.mixer.Sound('../SoundFiles/beep3.ogg')
    BEEP4 = pygame.mixer.Sound('../SoundFiles/beep4.ogg')

    pattern = []
    current_step = 0
    last_click_time = 0
    score = 0

    waiting_for_input = False

    while True:
        clicked_button = None

        DISPLAY_SURF.fill(BG_COLOR)
        drawButtons()

        score_surf = BASIC_FONT.render('Score : ' + str(score), 1, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOW_WIDTH - 100, 10)
        DISPLAY_SURF.blit(score_surf, score_rect)

        DISPLAY_SURF.blit(info_surf, info_rect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                clicked_button = getButtnClicked(mouse_x, mouse_y)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clicked_button = YELLOW
                elif event.key == K_w:
                    clicked_button = BLUE
                elif event.key == K_a:
                    clicked_button = RED
                elif event.key == K_s:
                    clicked_button = GREEN

        if not waiting_for_input:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASH_DELAY)
            waiting_for_input = True
        else:
            if clicked_button and clicked_button == pattern[current_step]:
                flashButtonAnimation(clicked_button)
                current_step += 1
                waiting_for_input = False
                current_step = 0
            elif (clicked_button and clicked_button != pattern[current_step]) or (current_step != 0 and time.time() - TIME_OUT > last_click_time):
                gameOverAnimation()
                pattern = []
                current_step = 0
                waiting_for_input = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

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

def flashButtonAnimation(color, animation_speed = 50):
    if color == YELLOW:
        sound = BEEP1
        flash_color = BRIGHT_YELLOW
        rectangle = YELLOW_RECT
    elif color == BLUE:
        sound = BEEP2
        flash_color = BRIGHT_BLUE
        rectangle = BLUE_RECT
    elif color == RED:
        sound = BEEP3
        flash_color = BRIGHT_RED
        rectangle = RED_RECT
    elif color == GREEN:
        sound = BEEP4
        flash_color = BRIGHT_GREEN
        rectangle = GREEN_RECT

    orign_surf = DISPLAY_SURF.copy()
    flash_surf = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
    flash_surf = flash_surf.convert_alpha()
    r, g, b = flash_color
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animation_speed * step):
            checkForQuit()
            DISPLAY_SURF.blit(orign_surf, (0, 0))
            flash_surf.fill((r,g,b,alpha))
            DISPLAY_SURF.blit(flash_surf, rectangle.topleft)
            pygame.display.update()
            FPS_CLOCK.tick(FPS)

    DISPLAY_SURF.blit(orign_surf, (0, 0))

def drawButtons():
    pygame.draw.rect(DISPLAY_SURF, YELLOW, YELLOW_RECT)
    pygame.draw.rect(DISPLAY_SURF, BLUE, BLUE_RECT)
    pygame.draw.rect(DISPLAY_SURF, RED, RED_RECT)
    pygame.draw.rect(DISPLAY_SURF, GREEN, GREEN_RECT)

def changeBackgroundAnimation(animation_seed = 40):
    global BG_COLOR
    new_bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    new_bg_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    new_bg_surf = new_bg_surf.convert_alpha()
    r, g, b = new_bg_color
    for alpha in range(0, 255, animation_seed):
        checkForQuit()
        DISPLAY_SURF.fill(BG_COLOR)

        new_bg_surf.fill((r,g,b,alpha))
        DISPLAY_SURF.blit(new_bg_surf, (0, 0))

        drawButtons()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)
    BG_COLOR = new_bg_color


def gameOverAnimation(color = WHITE, animation_speed = 50):

    origin_surf = DISPLAY_SURF.copy()
    flash_surf = pygame.Surface(DISPLAY_SURF.get_size())
    flash_surf = flash_surf.convert_alpha()

    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()

    r,g,b = color

    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animation_speed * step):
                checkForQuit()
                flash_surf.fill((r,g,b,alpha))
                DISPLAY_SURF.blit(origin_surf, (0, 0))
                DISPLAY_SURF.blit(flash_surf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPS_CLOCK.tick(FPS)
                
def getButtnClicked(x, y):
    if YELLOW_RECT.collidepoint((x, y)):
        return YELLOW
    elif BLUE_RECT.collidepoint((x, y)):
        return BLUE
    elif RED_RECT.collidepoint((x, y)):
        return RED
    elif GREEN_RECT.collidepoint((x, y)):
        return GREEN

if __name__ == '__main__':
    main()
