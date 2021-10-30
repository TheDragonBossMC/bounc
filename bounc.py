import pygame
import random as rand
from math import *
from pygame.math import Vector2
import time

gui_size = 600

gravity = 20
gravity_toggle = False
air_res = 0.1
air_res_toggle = False
physics_render = False
prev_time = pygame.time.get_ticks()/1000
sec_frames = []
paused = False
next_frame = True
bounce = True
playing = False


def start_animation():
    global paused
    global playing
    paused = True
    playing = True

    global start_time
    start_time = pygame.time.get_ticks()/1000

def play_animation(win):
    def draw_title(win, t):
        surf = pygame.Surface((gui_size, gui_size), pygame.SRCALPHA)
        surf.fill((255, 255, 255))

        pygame.draw.rect(surf, (0,0,0), (25, 200, 25, 200), 3)

        pygame.draw.rect(surf, (0,0,0), (295, 300, 25, 100), 3)
        pygame.draw.rect(surf, (0,0,0), (345, 300, 25, 100), 3)
        pygame.draw.rect(surf, (0,0,0), (320, 375, 25, 25 ), 3)

        pygame.draw.rect(surf, (0,0,0), (395, 300, 25, 100), 3)
        pygame.draw.rect(surf, (0,0,0), (445, 300, 25, 100), 3)
        pygame.draw.rect(surf, (0,0,0), (420, 300, 25, 25 ), 3)

        pygame.draw.rect(surf, (0,0,0), (495, 300, 25, 100), 3)
        pygame.draw.rect(surf, (0,0,0), (520, 375, 50, 25 ), 3)
        pygame.draw.rect(surf, (0,0,0), (520, 300, 50, 25 ), 3)

        if t < 1.5:
            pygame.draw.circle(surf, (255, 0, 0), (25*abs(t-1/2)+100, 350), 50)
            pygame.draw.circle(surf, (0, 0, 255), (225, 350), 50)
        elif t < 3:
            pygame.draw.circle(surf, (255, 0, 0), (125, 350), 50)
            pygame.draw.circle(surf, (0, 0, 255), (-25*abs(t-2.25)+245,350), 50)
        else:
            pygame.draw.circle(surf, (255, 0, 0), (125, 350), 50+150*(t-3)**2)
            pygame.draw.circle(surf, (0, 0, 255), (225, 350), 50+150*(t-3)**2)

            surf.set_alpha(-64*(t-3)**2+255)

        win.blit(surf, (0, 0))

    play_time = pygame.time.get_ticks()/1000 - start_time

    draw_title(win, play_time)

    if play_time >= 5:
        global playing
        playing = False
        global paused
        global next_frame
        paused = False
        next_frame = True


def dist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return sqrt((y2-y1) ** 2 + (x2-x1) ** 2) # kon ante

def pause():
    global paused
    global next_frame
    next_frame = paused
    paused = not paused

def toggle_physics_render():
    global physics_render
    physics_render = not physics_render

def toggle_gravity():
    global gravity_toggle
    gravity_toggle = not gravity_toggle

def toggle_air_res():
    global air_res_toggle
    air_res_toggle = not air_res_toggle

def frame_advance():
    global next_frame
    next_frame = True

def angle(x, y):
    return atan2(y, x)

def smooth_fr(secs):
    global sec_frames
    sec_frames.append(pygame.time.get_ticks()/1000)
    for i in sec_frames:
        if i < pygame.time.get_ticks()/1000 - secs:
            sec_frames.remove(i)
        else:
            break
    return len(sec_frames) // secs

def new_ball():
    ball = Ball(0,0,0,0,0)
    ball.dx = rand.randint(-750, 750)   # tawa seme
    ball.dy = rand.randint(-750, 750)
    ball.size = rand.randint(10, 80)     # suli seme
    ball.mass = rand.randint(10, 20) * ball.size/50 # wawa seme
    ball.color = (rand.randint(0,200),rand.randint(0,200),rand.randint(0,200)) # kule seme
    attempts = 0
    while len(ball.check_collision()) != 0 and attempts < 100:
        ball.x = rand.randint(ball.size, gui_size - ball.size) # ma seme
        ball.y = rand.randint(ball.size, gui_size - ball.size)
        attempts += 1
    if attempts >= 100:
        Ball.balls.remove(ball)

def draw_line(win, color, start_pos, end_pos, width=1):
    pos1 = Vector2(start_pos)
    pos2 = Vector2(end_pos)
    perp_line = Vector2(pos1 - pos2).rotate(90)
    perp_line.scale_to_length(width)
    points = [pos1 + perp_line, pos1 - perp_line, pos2 - perp_line, pos2 + perp_line]
    return pygame.draw.polygon(win, color, points)

def draw_text(win, color, pos, size, text, type_font='consolas'):
    font = pygame.font.SysFont(type_font, size)
    text_surface = font.render(text, True, color)
    win.blit(text_surface, pos)

def delete_balls():
    Ball.balls = []

class Ball:
    # poki pi sike
    balls = []
    def __init__(self, x, y, dx, dy, color):
        Ball.balls.append(self)

        # o jo e nanpa
        self.x = x # ma seme
        self.y = y
        self.dx = dx   # tawa seme
        self.dy = dy
        self.size = 50     # suli seme
        self.mass = 10     # wawa seme
        self.color = color # kule seme

    def set_pos(self, pos):
        self.x, self.y = pos

    def set_vel(self, vel):
        self.dx, self.dy = vel

    def handle_collision(self, obj):
        if type(obj) == type('string'):
            if obj == 'bottom':         # sike li kama poka pi ante anpa?
                while self.y <= self.size:
                    self.y += 1             # o lon anpa ala
                self.dy *= -1     # o jasima e tawa
            if obj == 'top':    # sike li kama poka pi ante sewi?
                while self.y >= gui_size - self.size:
                    self.y -= 1             # o lon sewi ala
                self.dy *= -1     # o jasima e tawa
            if obj == 'left':         # sike li kama poka pi ante anpa?
                while self.x <= self.size:
                    self.x += 1             # o lon anpa ala
                self.dx *= -1     # o jasima e tawa
            if obj == 'right':    # sike li kama poka pi ante sewi?
                while self.x >= gui_size - self.size:
                    self.x -= 1             # o lon sewi ala
                self.dx *= -1     # o jasima e tawa
        else:
            if bounce:
                self.bounce(obj)
            self.correct_clip(obj)

    def bounce(self, ball):
        # Base off of previous code, use equations online
        # https://scipython.com/blog/two-dimensional-collisions/
        m1, m2 = self.mass, ball.mass
        M = m1 + m2
        r1, r2 = Vector2(self.x, self.y), Vector2(ball.x, ball.y)
        d = (r1 - r2).magnitude()**2
        v1, v2 = Vector2(self.dx, self.dy), Vector2(ball.dx, ball.dy)
        u1 = v1 - 2*m2 / M * (v1-v2)*(r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * (v2-v1)*(r2-r1) / d * (r2 - r1)
        self.set_vel(u1)
        ball.set_vel(u2)


    def correct_clip(self, ball):
        r1, r2 = Vector2(self.x, self.y), Vector2(ball.x, ball.y)
        diff = r1 - r2
        size_compen = diff.normalize() * (self.size + ball.size)
        diff -= size_compen
        self.x -= diff.x
        self.y -= diff.y
        ball.x += diff.x
        ball.y += diff.y

    def check_collision(self):
        collisions = []
        if self.y <= self.size:
            collisions.append('bottom')
        if self.y >= gui_size - self.size:
            collisions.append('top')
        if self.x <= self.size:
            collisions.append('left')
        if self.x >= gui_size - self.size:
            collisions.append('right')

        for ball in Ball.balls:
            if ball == self:
                continue
            if dist((ball.x, ball.y), (self.x, self.y)) <= ball.size + self.size:
                collisions.append(ball)
        return collisions

    def tick(self):
        if gravity_toggle:
            self.dy += gravity # tawa anpa
        self.x += self.dx * (clock.get_time()/1000)  # o tawa
        self.y += self.dy * (clock.get_time()/1000)

        for collision in self.check_collision():
            self.handle_collision(collision)


        self.dx *= 1 - air_res/self.mass * int(air_res_toggle)
        self.dy *= 1 - air_res/self.mass * int(air_res_toggle)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
        if physics_render:
            try:
                draw_line(win, (255, 255, 255), (self.x, self.y), (self.x + self.dx * (clock.get_time()/1000), self.y + self.dy * (clock.get_time()/1000)), int(self.mass))
            except:
                pass


def draw_handler(win):
    global next_frame
    for ball in Ball.balls:
        if next_frame:
            ball.tick()
        ball.draw(win)
    if paused:
        next_frame = False
    if physics_render:
        draw_text(win, (0, 0, 0), (1, 0 ), 12, 'FPS: %d' % int(clock.get_fps()))
        draw_text(win, (0, 0, 0), (1, 15), 12, 'Gravity: %s' % str(gravity_toggle))
        draw_text(win, (0, 0, 0), (1, 30), 12, 'Air Resistance: %s' % str(air_res_toggle))
        if not (1073742049 in keys_down or 1073742053 in keys_down): # Left & Right Shift
            draw_text(win, (0, 0, 0), (1, 45), 12, 'Hold Shift to see controls')
        else:
            draw_text(win, (0, 0, 0), (1, 45 ), 12, 'Left Click: New Ball')
            draw_text(win, (0, 0, 0), (1, 60 ), 12, 'Space: Pause/Play')
            draw_text(win, (0, 0, 0), (1, 75 ), 12, 'Right Click: Delete Ball')
            draw_text(win, (0, 0, 0), (1, 90 ), 12, 'Shift + Right Click: Delete All Balls')
            draw_text(win, (0, 0, 0), (1, 105), 12, 'Right Arrow (if paused): Next Frame')
            draw_text(win, (0, 0, 0), (1, 120), 12, 'Forward Slash (/): Show Debug Info')
            draw_text(win, (0, 0, 0), (1, 135), 12, 'g: Toggle Gravity')
            draw_text(win, (0, 0, 0), (1, 150), 12, 'a: Toggle Air Resistance/Friction')
            draw_text(win, (0, 0, 0), (1, 165), 12, 'i: Replay Intro Animation')


    if playing:
        play_animation(win)

Ball(200, 301, 300, 0, (0,0,255))
Ball(500, 300, 0  , 0, (255,0,0))

paused = True


def click(pos, button):
    if button == 1:
        new_ball()
    elif button == 3:
        if 1073742049 in keys_down or 1073742053 in keys_down: # Left & Right Shift
            delete_balls()
        else:
            for ball in Ball.balls:
                if dist(pos, (ball.x, ball.y)) < ball.size:
                    Ball.balls.remove(ball)

def key_press(key):
    if key == 32: # spacebar
        pause()
    elif key == 47: # /
        toggle_physics_render()
    elif key == 1073741903: # right arrow
        frame_advance()
    elif key == 103: # g
        toggle_gravity()
    elif key == 97: # a
        toggle_air_res()
    elif key == 105: # i
        start_animation()

pygame.init()
pygame.display.init()
pygame.font.init()

print('After the animation, hit / and hold shift to see controls.')
time.sleep(1)

win = pygame.display.set_mode((gui_size, gui_size))
pygame.display.set_caption('bounc - Simple Physics')

time.sleep(0.1)

start_animation()

mouse_pos = (-1,-1)
prev_mouse_buttons = [False, False, False]
keys_down = []

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            click(event.pos, event.button)
        if event.type == pygame.KEYDOWN:
            keys_down.append(event.key)
        if event.type == pygame.KEYUP:
            keys_down.remove(event.key)
            key_press(event.key)


    win.fill((255,255,255))

    draw_handler(win)

    pygame.display.update()

pygame.quit()
