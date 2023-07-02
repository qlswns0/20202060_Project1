import pygame
import numpy as np
import os

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
PINK = (255, 105, 255)
AQUA = (0, 255, 255)
MAROON = (128,0,0)
LIME = (0, 255, 0)

pygame.init()  # 1! initialize the whole pygame system!
pygame.display.set_caption("20202060 이예준")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
background_image = pygame.image.load(os.path.join(assets_path, 'galaxy.jpg'))
sun_image = pygame.image.load(os.path.join(assets_path, 'Sun1.png'))
spaceship = pygame.image.load(os.path.join(assets_path, 'flying spaceship.png'))
pygame.mixer.music.load(os.path.join(assets_path, 'Taking Flight.mp3'))
pygame.mixer.music.play(-1) # 무한 반복 재생
sound3 = pygame.mixer.Sound(os.path.join(assets_path, 'Funny Boy Laugh.mp3'))

background = pygame.image.load(os.path.join(assets_path, 'mushroom1.png')).convert()
background_rect = background.get_rect()



font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y): ###
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    #screen.blit(background, background_rect)
    draw_text(screen, "", 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    draw_text(screen, "SOLAR SYSTEM SIMULATION", 50,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3)
    draw_text(screen, "20202060 Ye-jun Lee", 30, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        #clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False




def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def getRectangle(width, height, x=0, y=0):
    points = np.array([ [0, 0], 
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y]
    return points

def Rmat(degree): # 제자리 회전 = 거리안주면 본체
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]], dtype='float')
    return R 

def Tmat(tx, ty): # 거리주기
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = ( R @ points.T ).T + t 
    pygame.draw.polygon(screen, color, points_transformed, 0)
    #if p0 is not None:
    #    pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])



Sun = getRegularPolygon(20, 90)
distSE = 160
Earth = getRegularPolygon(20, 20)
distEM = 40
Moon = getRegularPolygon(20, 6)
Earth2 = getRegularPolygon(20, 15)
Earth3 = getRegularPolygon(20, 30)
Planet = getRegularPolygon(20, 16)
Planet2 = getRegularPolygon(20, 10)
Earth4 = getRegularPolygon(20, 100)

angle = 0
angleSE = 0
angleE = 0
angleM = 0
angleEM = 0

xx = 800
yy = 250

game_over = True
done = False
while not done:
    if game_over:
        show_go_screen() ###
        game_over = False
    #angle += 3
    angleSE += .3 # Sun과 Earth 간의 각도
    angleE += 1 # 지구속도
    angleEM += .5 # Earth와 Moon 간의 각도
    angleM += 1 # 달속도
    xx -= 4
    yy += 4
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if xx < 0:
            xx = 800
            yy = 250
            sound3.play()
    
    screen.fill(GREEN)
    # 배경 이미지 띄우기
    screen.blit(background_image, background_image.get_rect())
    # 태양 지점 본체
    center=(300., 300.)
    Msun = Tmat(center[0], center[1]) @ Rmat(angleE)
    draw(Msun, Sun, RED, center)
    # 메인 지구
    Mearth = Tmat(center[0], center[1]) @ Rmat(angleSE) @ Tmat(distSE + 50, 0) @ Rmat(-angleSE) @ Rmat(angleE)
    draw(Mearth, Earth, BLUE, Mearth[:2, 2])
    # 지구를 도는 달
    Mmoon = Mearth @ Rmat(angleEM) @ Tmat(distEM, 0) @ Rmat(angleM)
    draw(Mmoon, Moon, (100, 100, 100), Mmoon[:2,2])
    # 달이 두개있는 행성
    Mearth2 = Tmat(center[0], center[1]) @ Rmat(angleSE + 140) @ Tmat(distSE + 50, 0)
    draw(Mearth2, Earth2, AQUA, Mearth2[:2, 2])
    Mmoon2 = Mearth2 @ Rmat(angleEM) @ Tmat(distEM, 0) @ Rmat(angleM)
    draw(Mmoon2, Moon, (100, 100, 100), Mmoon2[:2,2])
    Mmoon3 = Mearth2 @ Rmat(angleEM + 140) @ Tmat(distEM, 0) @ Rmat(angleM)
    draw(Mmoon3, Moon, (100, 100, 100), Mmoon3[:2,2])
    # 추가로 행성 만들기
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 230) @ Tmat(distSE + 100, 0)
    draw(Mearth3, Earth3, PINK, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 260) @ Tmat(distSE + 130, 0)
    draw(Mearth3, Moon, MAROON, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 130) @ Tmat(distSE + 150, 0)
    draw(Mearth3, Planet, MAROON, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 50) @ Tmat(distSE + 100, 0)
    draw(Mearth3, Planet2, LIME, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 300) @ Tmat(distSE + 100, 0)
    draw(Mearth3, Planet2, YELLOW, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 100) @ Tmat(distSE + 400, 0)
    draw(Mearth3, Earth3, AQUA, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 300) @ Tmat(distSE + 350, 0)
    draw(Mearth3, Earth4, MAROON, Mearth3[:2, 2])
    Mearth3 = Tmat(center[0], center[1]) @ Rmat(angleSE + 50) @ Tmat(distSE + 500, 0)
    draw(Mearth3, Earth3, PINK, Mearth3[:2, 2])
    
    screen.blit(sun_image, [50, 50])
    screen.blit(spaceship, [xx, yy])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()