import pygame
from dynamicPoint import *
#from constants import *
import constants
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.forward_speed = 0
        self.direction = 0
        self.point = dynamicPoint(self.x, self.y)
        

        self.dev_shape = pygame.Rect(self.point.x-20, self.point.y-30, 40, 60)
    def draw(self, screen):
        pygame.draw.rect(screen, "red", self.dev_shape, 2)
        pygame.draw.line(screen, "red", (self.dev_shape.left, self.dev_shape.top), (self.dev_shape.right, self.dev_shape.bottom), 2)
        pygame.draw.line(screen, "red", (self.dev_shape.right, self.dev_shape.top), (self.dev_shape.left, self.dev_shape.bottom), 2)

    def update_controls(self):
        
        #global SCROLL_X
        #global SCROLL_Y
    
        self.x += self.vx
        self.y += self.vy
        self.point.x = self.x
        self.point.y = self.y
        self.point = self.point.translate(-constants.SCROLL_X, -constants.SCROLL_Y)
        self.dev_shape = pygame.Rect(self.point.x-20, self.point.y-30, 40, 60)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            
            self.vy -= 1
        elif keys[pygame.K_DOWN]:
           
            self.vy += 1
        
        if keys [pygame.K_LEFT]:
            self.vx -= 1
        elif keys[pygame.K_RIGHT]:
            self.vx += 1
        
        self.vx *= 0.9
        self.vy *= 0.9

        constants.SCROLL_X += ((self.x-constants.CENTER_X) - constants.SCROLL_X)/4
        constants.SCROLL_Y += ((self.y-constants.CENTER_Y) - constants.SCROLL_Y)/4
