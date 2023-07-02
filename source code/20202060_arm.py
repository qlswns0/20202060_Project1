import pygame
import numpy as np
import os

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GREEN = (100, 200, 100)
LIME = (0, 255, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption("20202060 이예준")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
sound = pygame.mixer.Sound(os.path.join(assets_path, 'grab.mp3'))
sound2 = pygame.mixer.Sound(os.path.join(assets_path, 'eatramen.wav'))
background_image = pygame.image.load(os.path.join(assets_path, 'ramen.jpg'))

GRAY = (200, 200, 200)
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
    draw_text(screen, "", 40, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    draw_text(screen, "ARM SIMULATION", 50,
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
    points = np.array([ [0, 0], # rect 정보 저장하기
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y] # rect의 4개정보에 (x,y)위치값을 각각 더한다.
    return points

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]], dtype='float')
    return R 

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

def draw(M, points, color=(0,0,0), p0=None):
    # M 은 Tmat Rmat을 이용하여 회전을 끝마친 모형의 rect값.

    # transform 하는데에 필요한 재료 R, t
    R = M[0:2, 0:2] # (행렬 0~2번, 행렬 0~2번) 따로 저장
    t = M[0:2, 2] # (행렬 0~2번, 행렬 2번) 따로 저장

    points_transformed = ( R @ points.T ).T + t # rect.를 T해주고 R을 곱해준다음 다시 T하여 transform 완료.
    pygame.draw.polygon(screen, color, points_transformed, 0)
    if p0 is not None:
        print(points_transformed)
        if space_count == 0 or space_count % 2 == 0: # 젓가락 풀린것 그리기
            gripper2 = gripper @ Tmat(width4, 0) @ Tmat(0, height4/2.) @ Rmat(angle3 - 90) @ Rmat(angle3 + 90) @ Tmat(0, -height4/2.)
            draw(gripper2, rect5, LIME)
            gripper3 = gripper @ Tmat(width4, 0) @ Tmat(0, height4/2.) @ Rmat(angle3 - 90) @ Rmat(angle3 + 90) @ Tmat(0, height4/2.)
            draw(gripper3, rect5, LIME)
        elif space_count % 2 != 0: # 젓가락 가동된 형태 그리기
            gripper2 = gripper @ Tmat(width4, 0) @ Tmat(0, height4/2.) @ Rmat(angle3 - 65) @ Rmat(angle3+90) @ Tmat(0, -height4/2.)
            draw(gripper2, rect5, LIME)
            gripper3 = gripper @ Tmat(width4, 0) @ Tmat(0, height4/2.) @ Rmat(angle3 - 115) @ Rmat(angle3+90) @ Tmat(0, height4/2.)
            draw(gripper3, rect5, LIME)
        
space_count = 0

center1_1 = [50, 780.]
angle1 = 20 # 첫번째 팔 정보 입력
width1 = 200
height1 = 70
rect1 = getRectangle(width1, height1)

gap12 = 30

angle2 = 0 # 두번째 팔 정보 입력
width2 = 170
height2 = 50
rect2 = getRectangle(width2, height2)

gap23 = 30

angle3 = 0 # 세번째 팔 정보 입력
width3 = 130
height3 = 30
rect3 = getRectangle(width3, height3)

width4 = 10
height4 = 170
rect4 = getRectangle(width4, height4)

width5 = 200
height5 = 10
rect5 = getRectangle(width5, height5)

game_over = True
done = False
while not done:
    if game_over:
        show_go_screen() ###
        game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button Pressed!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: # capital A
                angle1 += 10
            elif event.key == pygame.K_a:
                angle1 -= 10   
            elif event.key == pygame.K_c:
                angle2 += 10
            elif event.key == pygame.K_s:
                angle2 -= 10
            elif event.key == pygame.K_v:
                angle3 += 10
            elif event.key == pygame.K_d:
                angle3 -= 10
            elif event.key == pygame.K_SPACE:
                space_count += 1
                if space_count % 2 != 0:
                    sound.play() # 딱! 하고 집는 소리
                elif space_count % 2 == 0:
                    sound2.play() # 놓으면 후루룩 소리
            
    screen.fill(WHITE)
    screen.blit(background_image, background_image.get_rect())

    # 팔뚝들 draw
    arm1 = np.eye(3) @ Tmat(center1_1[0], center1_1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)
    draw(arm1, rect1, LIME) # 1번팔 draw
    arm2 = arm1 @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Tmat(gap12, 0) @ Rmat(angle2) @ Tmat(0, -height2/2.)
    draw(arm2, rect2, LIME) # 2번팔 draw
    arm3 = arm2 @ Tmat(width2, 0) @ Tmat(0, height2/2.) @ Tmat(gap23, 0) @ Rmat(angle3) @ Tmat(0, -height3/2.)
    draw(arm3, rect3, LIME) # 3번팔 draw

    gripper = arm3 @ Tmat(width3, 0) @ Tmat(0, height3/2.) @ Rmat(angle3) @ Rmat(angle3) @ Tmat(0, -height4/2.)
    draw(gripper, rect4, LIME, 1) # gripper 바닥: 이걸 그릴 때 space count에 따라 추가로 젓가락 구현.

    # 중심점들 draw
    pygame.draw.circle(screen, (0,0,0), center1_1, 20) # 1_1 circle
    C = arm1 @ Tmat(width1, 0) @ Tmat(0, height1/2.)
    center1_2 = C[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center1_2, 10) # 1_2 circle
    C2 = C @ Tmat(gap12, 0)
    center2_1 = C2[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center2_1, 10) # 2_1 circle
    pygame.draw.line(screen, (0,0,0), center1_2, center2_1, 20) # joint1

    C3 = arm2 @ Tmat(width2, 0) @ Tmat(0, height2/2.)
    center2_2 = C3[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center2_2, 10) # 2_2 circle
    C4 = C3 @ Tmat(gap23, 0)
    center3_1 = C4[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center3_1, 10) # 3_1 circle
    pygame.draw.line(screen, (0,0,0), center2_2, center3_1, 20) # joint2


    pygame.display.flip()
    clock.tick(60)

pygame.quit()