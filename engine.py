import pygame
import math
import random

WIDTH = 800
HEIGHT = 800
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2

#game engine components
SCROLL_X = 0
SCROLL_Y = 0
DIRECTION = 0 # in degrees
ZOOM = 0.5 #in times scale

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill("black")
pygame.display.flip()




class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.forward_speed = 0
        self.direction = 0

        self.dev_shape = pygame.Rect(self.x-20, self.y-30, 40, 60)
    def draw(self):
        pygame.draw.rect(screen, "red", self.dev_shape, 2)
        pygame.draw.line(screen, "red", (self.dev_shape.left, self.dev_shape.top), (self.dev_shape.right, self.dev_shape.bottom), 2)
        pygame.draw.line(screen, "red", (self.dev_shape.right, self.dev_shape.top), (self.dev_shape.left, self.dev_shape.bottom), 2)

    def update_controls(self):
        global DIRECTION
        global SCROLL_X
        global SCROLL_Y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.x += 3*math.sin(DIRECTION)
            self.y += 3*math.cos(DIRECTION)
        elif keys[pygame.K_DOWN]:
            self.x -= 3*math.sin(DIRECTION)
            self.y -= 3*math.cos(DIRECTION)
        
        if keys [pygame.K_LEFT]:
            DIRECTION -= 1
        elif keys[pygame.K_RIGHT]:
            DIRECTION += 1
        
        



class cell:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.point = dynamicPoint(self.x, self.y)
        
    
    def draw(self):
        pygame.draw.circle(screen, "blue", (self.point.x, self.point.y), self.radius*ZOOM, 2)
        pygame.draw.line(screen, "blue", (self.point.x+0.7011*self.radius*ZOOM, self.point.y+0.7011*self.radius*ZOOM), (self.point.x-0.7011*self.radius*ZOOM, self.point.y-0.7011*self.radius*ZOOM), 2)
        pygame.draw.line(screen, "blue", (self.point.x-0.7011*self.radius*ZOOM, self.point.y+0.7011*self.radius*ZOOM), (self.point.x+0.7011*self.radius*ZOOM, self.point.y-0.7011*self.radius*ZOOM), 2)

    def update(self, player_x, player_y):
        self.point.x = self.x
        self.point.y = self.y
        # rotate and scale point around player x, y
        self.point = self.point.translate(-player_x, -player_y)
        self.point = self.point.rotate(DIRECTION)
        self.point = self.point.scale(ZOOM)
        self.point = self.point.translate(player_x, player_y)
        #offset based off scroll x
        self.point = self.point.translate(-SCROLL_X, -SCROLL_Y)





cells = []

def update_cells():
    for cell in cells:
        cell.draw()
        cell.update(player.x, player.y)

def new_cell(x, y, r):
    new = cell(x, y, r)
    cells.append(new)

#graphics transformations
class dynamicPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        translated = dynamicPoint(self.x+dx, self.y+dy)
        return translated
    
    def rotate(self, theta):
        #first convert degrees to radians : 360 deg = 2pi rad, 180 deg = pi rad, deg/180 = pirad / 180
        radians = theta*math.pi/180

        sine = math.sin(radians)
        cosine = math.cos(radians)

        rx = cosine*self.x - sine*self.y
        ry = sine*self.x + cosine*self.y

        rotated = dynamicPoint(rx, ry)
        return rotated
    
    def scale(self, factor):
        sx = self.x*factor
        sy = self.y*factor

        scaled = dynamicPoint(sx, sy)
        return scaled














#for i in range(10):
    #new_cell(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(40, 50))

new_cell(CENTER_X, 50, 30)
new_cell(50, CENTER_Y, 50)


player = Player(CENTER_X, CENTER_Y)


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)
    screen.fill("white")
    player.draw()
    player.update_controls()
    update_cells()
    
    pygame.display.flip()


pygame.quit()









