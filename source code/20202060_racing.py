import sys
import pygame
import random
import os

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("20202060 이예준")

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')


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
    draw_text(screen, "RACING SIMULATION", 50,
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

class Car:
    car_image = ['mushroom1.png', 'mushroom2.png', 'mushroom3.png']

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx # 움직인 정도
        self.dy = dy
        self.rect = ""

    def load_car(self, p = ""):
        if p == "p": # 플레이어 차량
            self.image = pygame.image.load(os.path.join(assets_path, 'player.png'))
            self.image = pygame.transform.scale(self.image, (40, 102)) # 크기 조정
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else: # 상대방 자동차 # 3개의 버섯 이미지 중 랜덤선택.
            self.image = pygame.image.load(random.choice(self.car_image)) 
            self.rect = self.image.get_rect()

            if self.rect.width <= 55: # 이미지 크기 조절 - 이미지마다 크기가 다 다르므로 가로 세로 비율 유지하면서 변경
                carwidth = self.rect.width - 15
                carheight = round((self.rect.height * carwidth) / self.rect.width)
            else:
                carwidth = self.rect.width
                carheight = self.rect.height

            self.image = pygame.transform.scale(self.image, (carwidth, carheight))
            self.rect.width = carwidth
            self.rect.height = carheight

            # 생성 위치 - 스크린 크기 안에서 랜덤으로 x 좌표 생성. y 좌표는 스크린 밖 위에 생성
            self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)

            # 다양한 속도차이를 위해 5 ~ speed 사이에서 랜덤으로 속도를 선택하게 한다.
            speed = 10
            self.dy = random.randint(5, speed)

    def draw_car(self): # 해당 물체 띄우기
        screen.blit(self.image, [self.rect.x, self.rect.y])

    def move_x(self): # x 좌표 이동
        self.rect.x += self.dx

    def move_y(self): # y 좌표 이동
        self.rect.y += self.dy

    def check_screen(self): # 화면 밖으로 못 나가게 하기
        if self.rect.right > WINDOW_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

    def check_collision(self, car, distance = 0): # distance : 오른쪽, 왼쪽, 아래쪽, 위쪽 이미지의 간격 설정
        if (self.rect.top + distance < car.rect.bottom) and (car.rect.top < self.rect.bottom - distance) and (self.rect.left + distance < car.rect.right) and (car.rect.left < self.rect.right - distance):
            return True
        else:
            return False


CAR_COUNT = 5
CARS = []

def main():
    #global SCREEN, CAR_COUNT, WINDOW_WIDTH, WINDOW_HEIGHT

    player = Car(round(WINDOW_WIDTH / 2), round(WINDOW_HEIGHT - 150), 0, 0)
    player.load_car("p") # 플레이어 자동차 생성.

    for i in range(CAR_COUNT): # 5개씩 계속 생성하기 위함.
        car = Car(0, 0, 0, 0)
        car.load_car()
        CARS.append(car)

    game_over = True
    done = False
    while not done:
        if game_over:
            show_go_screen() ###
            game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 5
                elif event.key == pygame.K_LEFT:
                    player.dx = -5
                if event.key == pygame.K_DOWN:
                    player.dy = 5
                elif event.key == pygame.K_UP:
                    player.dy = -5
            if event.type == pygame.KEYUP: # 키 안 누를 때엔 가만히.
                if event.key == pygame.K_RIGHT:
                    player.dx = 0
                elif event.key == pygame.K_LEFT:
                    player.dx = 0
                if event.key == pygame.K_DOWN:
                    player.dy = 0
                elif event.key == pygame.K_UP:
                    player.dy = 0
 
        screen.fill(GRAY)



        # 게임 코드 작성
        player.draw_car() # 플레이어
        player.move_x() # x좌표 무브 반영.
        player.move_y() # y좌표 무브 반영.
        player.check_screen() # 화면 밖으로 못나가게 하기.

        for i in range(CAR_COUNT): # 다른 자동차들 띄우기
            CARS[i].draw_car()
            CARS[i].rect.y += CARS[i].dy

            if CARS[i].rect.y > WINDOW_HEIGHT:
                CARS[i].load_car() # y 넘어간 차량은 새로 생성

        for i in range(CAR_COUNT): # 플레이어와 다른 차량간의 충돌감지
            if player.check_collision(CARS[i], 5):
                if player.rect.x > CARS[i].rect.x: # 부딪혔을 경우 상대방 차량 튕겨나게 함. 좌우 튕김
                    CARS[i].rect.x -= CARS[i].rect.width + 10
                else:
                    CARS[i].rect.x += CARS[i].rect.width + 10

                if player.rect.y > CARS[i].rect.y: # 위 아래 튕김
                    CARS[i].rect.y -= 30
                else:
                    CARS[i].rect.y += 30

        for i in range(CAR_COUNT): # 다른 차량끼리의 충돌감지, 각 자동차들을 순서대로 서로 비교
            for j in range(i + 1, CAR_COUNT):

                if CARS[i].check_collision(CARS[j]):
                    if CARS[i].rect.x > CARS[j].rect.x: # 왼쪽에 있는 차는 왼쪽으로 오른쪽 차는 오른쪽으로 튕김
                        CARS[i].rect.x += 4
                        CARS[j].rect.x -= 4
                    else:
                        CARS[i].rect.x -= 4
                        CARS[j].rect.x += 4

                    if CARS[i].rect.y > CARS[j].rect.y: # 위쪽 차는 위로, 아래쪽차는 아래로 튕김
                        CARS[i].rect.y += CARS[i].dy
                        CARS[j].rect.y -= CARS[j].dy
                    else:
                        CARS[i].rect.y -= CARS[i].dy
                        CARS[j].rect.y += CARS[j].dy

        #
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()