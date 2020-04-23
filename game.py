import pygame
import random
pygame.init()
screen_x, screen_y = 800, 600
screen = pygame.display.set_mode((screen_x, screen_y))
font = pygame.font.SysFont('Times new roman', 72)
class Snake():
    def __init__(self, color, head, point, keys, coor):
        self.point = point
        self.head = head
        self.color = color
        self.dir = [1, 0]
        self.particles = [self.head, [-10,-10], [-10,-10]]
        self.keys = keys
        self.hp = 1
        self.b = keys[1]
        self.coor = coor
        self.chdirtime = 0
        self.score = 0
    def move(self):
        if self.hp>0:
            for i in range(len(self.particles)-1, 0, -1):
                self.particles[i][0] = self.particles[i-1][0]
                self.particles[i][1] = self.particles[i-1][1]
            self.head[0] += self.dir[0]
            self.head[1] += self.dir[1]
            if self.head[0]<0:
                self.head[0]=screen_x//20-1
            elif self.head[0]>screen_x//20-1:
                self.head[0]=0        
            if self.head[1]<0:
                self.head[1]=screen_y//20-1     
            elif self.head[1]>screen_y//20-1:
                self.head[1]=0
            for w in walls:
                if self.head[0] == w.x and self.head[1] == w.y:
                    self.hp -= 1
            for s in snakes:
                if all((s != self, s.head == self.head, s.hp>0)):
                    s.hp -= 1
                    self.hp -=1
                for i in range(len(s.particles)):    
                    if all((self.head[0] == s.particles[i][0], self.head[1] == s.particles[i][1], s.hp>0, any((s != self, all((s == self, i != 0)))))):
                        self.hp -= 1
                        if s != self:
                            s.score += 5
            self.draw()
    def draw(self):
        if self.hp>0:
            for i in self.particles:
                pygame.draw.circle(screen, self.color, (i[0]*20+10, i[1]*20+10) ,10)
    def chdir(self, a):
        if all((a == self.keys[0], self.b!= self.keys[1], self.chdirtime > 0)):
            self.dir = [-1, 0]
            self.chdirtime = 0
            self.b = a
        if all((a == self.keys[1], self.b!= self.keys[0], self.chdirtime > 0)):
            self.dir = [1, 0]
            self.chdirtime = 0
            self.b = a
        if all((a == self.keys[2], self.b!= self.keys[3], self.chdirtime > 0)):
            self.dir = [0, -1]
            self.b = a
            self.chdirtime = 0
        if all((a == self.keys[3] and self.b!= self.keys[2], self.chdirtime > 0)):
            self.dir = [0, 1]
            self.b = a
            self.chdirtime = 0
    def eat(self):
        b = 0
        for s in snakes:
            if all((s != self, s.hp>0)):
                b += len(s.particles)
        if self.hp>0:
            self.score += 1
            if len(self.particles)<((screen_x-1)*(screen_y-1)//400)-len(foods)- b:
                self.particles.append([-10, -10])
class Food():
    def __init__(self):
        self.coor = [5, 5]
        self.color = [0, 255, 0]
    def genfood(self):
        a = False
        while a == False:
            a = True
            for s in snakes:
                for i in s.particles:
                    if all((self.coor == i, s.hp>0)):
                        a = False
            for f in foods:
                if all((f !=self, f.coor == self.coor)):
                    a = False
            for w in walls:
                if w.x == self.coor[0] and w.y == self.coor[1]:
                    a = False
            if a == False:
                self.coor[0] = random.randint(0, screen_x//20-1)
                self.coor[1] = random.randint(0, screen_y//20-1)
    def draw(self):
            pygame.draw.circle(screen, self.color, (self.coor[0]*20+10, self.coor[1]*20+10) ,10)
class Wall():
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x*20, self.y*20, 20, 20))
def result(snake:Snake):
    text = font.render(str(snake.score), True, snake.color)
    textRect = text.get_rect() 
    textRect.center = (snake.coor)
    screen.blit(text, textRect)
def line():
    for i in range(0, screen_x+21, 20):
        pygame.draw.line(screen, (50, 50, 150), (i, 0), (i, screen_y))
    for i in range(0, screen_y+21, 20):
        pygame.draw.line(screen, (50, 50, 150), (0, i), (screen_x, i))

snake1 = Snake((255, 0, 0),[5, 5] , [5, 5],(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s), (400, 100))
snake2 = Snake((0, 0, 255),[5, 15] , [5, 15],(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), (400, 300))
snakes = [snake1, snake2]
foods = []
walls = []
def level1():
    for i in range(len(walls)):
        walls.pop()
    newlev()
def level2():
    for i in range(len(walls)):
        walls.pop()
    for i in range(40):
        walls.append(Wall(i, 0, (100, 100, 100)))
        walls.append(Wall(i, 29, (100, 100, 100)))
    for i in range(30):
        walls.append(Wall(0, i,(100, 100, 100)))
        walls.append(Wall(39, i,(100, 100, 100)))
    newlev()
def newlev():
    for s in snakes:
        s.head[0] = s.point[0]
        s.head[1] = s.point[1]
        s.particles = [s.head, [-10, -10], [-10, 10]]
        s.dir = [1, 0]
    for f in foods:
        for w in walls:
            if f.coor[0] == w.x and f.coor[1] == w.y:
                f.genfood()
def level3():
    for i in range(len(walls)):
        walls.pop()
    for i in range(4):
        walls.append(Wall(i, 0, (100, 100, 100)))
        walls.append(Wall(0, i, (100, 100, 100)))
        walls.append(Wall(i, 29, (100, 100, 100)))
        walls.append(Wall(0, 29 - i, (100, 100, 100)))
        walls.append(Wall(39 - i, 29, (100, 100, 100)))
        walls.append(Wall(39, 29 - i, (100, 100, 100)))
        walls.append(Wall(39 - i, 0, (100, 100, 100)))
        walls.append(Wall(39, i, (100, 100, 100)))
    for i in range(20):
        walls.append(Wall(i+10, 10, (100, 100, 100)))
        walls.append(Wall(i+10, 20, (100, 100, 100)))
    for f in foods:
        for w in walls:
            if f.coor[0] == w.x and f.coor[1] == w.y:
                f.genfood()
    newlev()
for i in range(3):
    foods.append(Food())
run = True
FPS = 5
clock = pygame.time.Clock()
for food in foods:
    food.genfood()
while run:
    mill = clock.tick(FPS)
    sec = mill /1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_1:
                level1()
            if event.key == pygame.K_2:
                level2()
            if event.key == pygame.K_3:
                level3()
            for s in snakes:
                for i in s.keys:
                    if event.key == i:
                        s.chdir(i)
    screen.fill((0, 0, 0))
    line()
    # print(FPS)
    for w in walls:
        w.draw()
    for f in foods:
        f.draw()
    alive = 0
    for s in snakes:
        s.move()
        s.chdirtime += sec
        # print(s.score)
        if s.hp>0:
            alive += 1
        for f in foods:
            if s.head == f.coor:
                s.eat()
                f.genfood()
    if alive<= 0:
        screen.fill((0, 0, 0))
        for snake in snakes:
            result(snake)
    else:
        FPS+=sec/20
    pygame.display.flip()
