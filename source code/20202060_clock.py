import numpy as np
import pygame
import os

GRAY = (200, 200, 200)
RED = (255, 0 , 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption("20202060 이예준 clock")

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
clock_radius = 390 # 6개의 분침을 그리기 위한 기준 반지름

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets') # assets 폴더로 지정
sound2 = pygame.mixer.Sound(os.path.join(assets_path, 'clockchiming.wav'))
background = pygame.image.load(os.path.join(assets_path, 'mushroom1.png')).convert()
background_rect = background.get_rect()


font_name = pygame.font.match_font('arial') # 시작화면
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    #screen.blit(background, background_rect)
    draw_text(screen, "", 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    draw_text(screen, "CLOCK SIMULATION", 50,
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



def numbers(number, size, position): # 시계에 숫자 그리넣기
    font = pygame.font.SysFont("Arial", size, True, False)
    text = font.render(number, True, BLACK)
    text_rect = text.get_rect(center=(position))
    screen.blit(text, text_rect)

def polar_to_cartesian(r, theta): # 숫자를 표시할 x,y좌표 구하기  # theta: a plane angle
    x = r * np.sin(np.pi * theta / 180) # r: 중점에서 숫자가 떨어져 있으면 하는 거리
    y = r * np.cos(np.pi * theta / 180)
    return x + 400, -(y - 400)



class HandInfo:
    def __init__(self, arm): 
        self.hand_original = arm
        self.length = self.hand_original.get_rect()[2] # 길이
        self.rotation = 0.0

    def rotate(self, rotation): # 초당 얼마만큼의 각도를 돌 것이냐를 결정하는 곳.
        self.rotation += rotation # 입력받은 rotation 크기를 저장.
        rotated_hand = pygame.transform.rotozoom(self.hand_original, np.degrees(self.rotation), 1) # 이미지를 원하는 빠르기 만큼 돌려서 다시 저장
        rotated_rect = rotated_hand.get_rect() # 회전된 이미지의 꼭짓점위치 다시 구해서 저장
        rotated_rect.center = (0, 0) # 꼭짓점 위치의 중심점을 원상태로 reset         # 이 두 줄 다 삭제하고 rotated_사각형.center = (0, 0) 
        return rotated_hand, rotated_rect # 회전된 이미지 + reset한 꼭짓점 위치 반환 -> 이 두개를 이용하여 draw하면 될 듯.
    
def transform(rect, joint, hand):
        rect.center += np.asarray(joint)
        rect.center += np.array([np.cos(hand.rotation) * hand.length / 2.0, # arm.length / 2.0 은 offset 하는데 필요한 값임.
                                -np.sin(hand.rotation) * hand.length / 2.0])



# arm으로 쓰일 직사각형 제작
hand_hour = pygame.Surface((150, 5), pygame.SRCALPHA, 32) # 사각형 모양 라인 따서 저장
hand_hour.fill(BLACK)
hand_minute = pygame.Surface((170, 5), pygame.SRCALPHA, 32) 
hand_minute.fill(BLACK)
hand_second = pygame.Surface((200, 5), pygame.SRCALPHA, 32)
hand_second.fill(BLACK)

# ArmInfo를 이용하여 도형 arm_1에 대한 상세정보를 저장해두기 # arm1은 arm_1의 "정보 주머니"
hand1 = HandInfo(hand_hour)
hand2 = HandInfo(hand_minute) 
hand3 = HandInfo(hand_second)  


game_over = True
done = False
while not done:
    if game_over:
            show_go_screen() ###
            game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 회전주기+회전속도         도형위치 = (0,0) 
    rotatedhand1, rotatedhand1_rect = hand1.rotate(-.03)
    rotatedhand2, rotatedhand2_rect = hand2.rotate(-.08)
    rotatedhand3, rotatedhand3_rect = hand3.rotate(-.15) 

    # 구한 것들을 토대로 최종 rect값 구하기
    hand1_finalrect = rotatedhand1.get_rect() # rotatedarm1의 rect 구하기. (0,0)
    transform(hand1_finalrect, (400,400), hand1) # transform 및 위치값 삽입
    hand1_finalrect.center += np.array([-hand1_finalrect.width / 2.0, -hand1_finalrect.height / 2.0]) # 중앙계속 맟춰주기

    hand2_finalrect = rotatedhand2.get_rect() 
    transform(hand2_finalrect, (400,400), hand2) 
    hand2_finalrect.center += np.array([-hand2_finalrect.width / 2.0, -hand2_finalrect.height / 2.0])

    hand3_finalrect = rotatedhand3.get_rect() 
    transform(hand3_finalrect, (400,400), hand3) 
    hand3_finalrect.center += np.array([-hand3_finalrect.width / 2.0, -hand3_finalrect.height / 2.0])

    screen.fill(WHITE)

    mimage = pygame.image.load(os.path.join(assets_path, 'mushroom3.png')) # collision체크를 위한 버섯 이미지.
    mimage = pygame.transform.scale(mimage, (1, 1)) # 크기 아주작게 조정
    mrect = mimage.get_rect()
    mrect.center = (400, 260)

    
    if mrect.top < hand1_finalrect.bottom and hand1_finalrect.top < mrect.bottom and mrect.left < hand1_finalrect.right and hand1_finalrect.left < mrect.right:
        sound2.play()
    

    # draw
    for number in range(1, 13): # 숫자 draw
        numbers(str(number), 80, polar_to_cartesian(clock_radius - 80, number * 30))

    for number in range(0, 360, 6): # 360도를 기준으로 60개의 분침(=초침) 그리기
        if number % 5: # 5분(5초) 간격으로는 좀 더 굵은 선
            pygame.draw.line(screen, BLACK, polar_to_cartesian(clock_radius - 15, number), polar_to_cartesian(clock_radius - 30, number), 2)
        else: # 나머지는 얇은 선
            pygame.draw.line(screen, BLACK, polar_to_cartesian(clock_radius, number), polar_to_cartesian(clock_radius - 35, number), 6)

    screen.blit(mimage, [400, 260]) # 머쉬룸
    screen.blit(rotatedhand1, hand1_finalrect) # (도형, 최종rect값)
    screen.blit(rotatedhand2, hand2_finalrect)
    screen.blit(rotatedhand3, hand3_finalrect)
 
    pygame.draw.circle(screen, BLACK, (400,400), 10) # 시계 중점
    pygame.draw.circle(screen, BLACK, (400,400), 400, 20) # 시계액자

    pygame.display.update()
    clock.tick(30)

pass