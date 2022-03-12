import pygame
pygame.init()
import time
import random
from pongbot import track_ball, predict_ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 800
HEIGHT = 800

SCORE_FONT = pygame.font.SysFont('Arial', 50)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")

class Paddle:
    width = 10
    height = 80
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))
        

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.x_vel = random.choice([-3, 3])
        self.y_vel = 0
        self.MAX_VEL = 7

        self.radius = 10

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move_ball(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
def handle_collision(ball, p1, p2):
    if ball.y + ball.radius >= HEIGHT: # ball hits bottom of screen
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0: # ball hits top of screen
        ball.y_vel *= -1

    if ball.x_vel < 0: # ball hits left paddle
        if ball.y >= p1.y and ball.y <= p1.y + p1.height:
            if ball.x - ball.radius <= p1.x + p1.width:
                ball.x_vel *= -1

                middle_y = p1.y + p1.height/2
                y_diff = middle_y - ball.y
                normalization = p1.height / ( 2 * ball.MAX_VEL )
                ball.y_vel = - y_diff / normalization
                ball.x_vel = max(( ball.MAX_VEL**2 - ball.y_vel**2 ) ** 0.5, 3)
    
    elif ball.y >= p2.y and ball.y <= p2.y + p2.height: # ball hits right paddle
        if ball.x + ball.radius >= p2.x:
            ball.x_vel *= -1

            middle_y = p2.y + p2.height/2
            y_diff = middle_y - ball.y
            normalization = p2.height / ( 2 * ball.MAX_VEL )
            ball.y_vel = - y_diff / normalization
            ball.x_vel = min(- ( ball.MAX_VEL**2 - ball.y_vel**2 ) ** 0.5, -3)

def reset_ball(ball, p1, p2):
    ball.x = WIDTH/2
    ball.y = HEIGHT/2
    ball.x_vel = 0
    ball.y_vel = 0
    p1.y = (HEIGHT - Paddle.height)/2
    p2.y = (HEIGHT - Paddle.height)/2

    p1.draw(WIN)
    p2.draw(WIN)
    ball.draw(WIN)

    redraw_screen()

    ball.x_vel = random.choice([-3, 3])

def check_goal(ball, p1, p1_score, p2, p2_score):
    if ball.x <= 0:
        p2_score += 1
        reset_ball(ball, p1, p2)

    elif ball.x >= WIDTH:
        p1_score += 1
        reset_ball(ball, p1, p2)
        
    return p1_score, p2_score

def write_scores(p1_score, p2_score):
    p1_score_text = SCORE_FONT.render(f"{p1_score}", 1, WHITE)
    p2_score_text = SCORE_FONT.render(f"{p2_score}", 1, WHITE)

    WIN.blit(p1_score_text, (WIDTH//8 - p1_score_text.get_width()//2, 20))
    WIN.blit(p2_score_text, (7*WIDTH//8, 20))

def redraw_screen():
    pygame.display.update()


paddle_v = 5

p1 = Paddle(10, (HEIGHT - Paddle.height)/2)
p1_score = 0
p2 = Paddle(WIDTH - 10 - Paddle.width, (HEIGHT - Paddle.height)/2)
p2_score = 0
ball = Ball(400, 400)

clock = pygame.time.Clock()
FPS = 60

run = True
while run:
    clock.tick(FPS)
    WIN.fill((BLACK))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and p1.y - paddle_v > 0:
        p1.y -= paddle_v
    if keys[pygame.K_s] and p1.y + p1.height + paddle_v < HEIGHT:
        p1.y += paddle_v
    
    # FOLLOWING CODEBLOCK IS FOR IF THERE ARE TWO PEOPLE PLAYING
    # if keys[pygame.K_DOWN] and p2.y + p2.height + paddle_v < HEIGHT:
    #     p2.y += paddle_v
    # if keys[pygame.K_UP] and p2.y - paddle_v > 0:
    #     p2.y -= paddle_v

    # FOLLOWING CODEBLOCK IS FOR PLAYING AGAINST A COMPUTER
    response = predict_ball(ball, p2, HEIGHT)
    if response == 'UP' and p2.y - paddle_v > 0:
        p2.y -= paddle_v
    if response == 'DOWN' and p2.y + p2.height + paddle_v < HEIGHT:
        p2.y += paddle_v
        
    p1.draw(WIN)
    p2.draw(WIN)

    handle_collision(ball, p1, p2)
    ball.move_ball()
    
    p1_score, p2_score = check_goal(ball, p1, p1_score, p2, p2_score)
    write_scores(p1_score, p2_score)

    ball.draw(WIN)

    redraw_screen()