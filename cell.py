import pygame
from dynamicPoint import *
import constants as c
class cell:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.point = dynamicPoint(self.x, self.y)
        self.vx = 0
        self.vy = 0
        
    
    def draw(self, screen):
        pygame.draw.circle(screen, "blue", (self.point.x, self.point.y), self.radius*c.ZOOM, 2)
        pygame.draw.line(screen, "blue", (self.point.x+0.7011*self.radius*c.ZOOM, self.point.y+0.7011*self.radius*c.ZOOM), (self.point.x-0.7011*self.radius*c.ZOOM, self.point.y-0.7011*self.radius*c.ZOOM), 2)
        pygame.draw.line(screen, "blue", (self.point.x-0.7011*self.radius*c.ZOOM, self.point.y+0.7011*self.radius*c.ZOOM), (self.point.x+0.7011*self.radius*c.ZOOM, self.point.y-0.7011*self.radius*c.ZOOM), 2)

    def update(self):
        self.point.x = self.x
        self.point.y = self.y
        #offset based off scroll
        self.point = self.point.translate(-c.SCROLL_X, -c.SCROLL_Y)
        #push cells away from each other
        self.x += self.vx
        self.y += self.vy
        
        self.vx *= 0.8
        self.vy *= 0.8
        
        
