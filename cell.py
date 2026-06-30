import pygame
from dynamicPoint import *
import constants




class cell:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.point = dynamicPoint(self.x, self.y)
        self.vx = 0
        self.vy = 0
        self.ID = 0
        self.highlighted = False

        self.isCancer = False
        self.toDivide = None #if cancer have this work
        self.rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
        self.friction = 0.8

        
    
    def draw(self, screen):
        img_width = self.radius*2
        img_height = self.radius*2

        if self.highlighted:
            CELL_IMAGE = constants.CELL_RED
        else:
            CELL_IMAGE = constants.CELL_NORMAL

        transformed = pygame.transform.scale(CELL_IMAGE, (img_width, img_height))
        transformed = pygame.transform.rotate(transformed, self.ID)

        screen.blit(transformed, (self.point.x-1.5*self.radius, self.point.y-1.5*self.radius))

        if self.isCancer: pygame.draw.rect(screen, "green", self.rect)
        
        

    def update(self):
        self.point.x = self.x
        self.point.y = self.y
        #offset based off scroll
        self.point = self.point.translate(-constants.SCROLL_X, -constants.SCROLL_Y)
        #push cells away from each other
        self.x += self.vx
        self.y += self.vy
        
        self.vx *= self.friction
        self.vy *= self.friction

        self.rect = pygame.Rect(self.point.x-self.radius, self.point.y-self.radius, self.radius*2, self.radius*2)

        
    def __str__(self):
        return f"cell({self.x}, {self.y}, {self.radius})"
        
        
