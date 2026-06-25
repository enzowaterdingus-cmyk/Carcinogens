import pygame
import constants
import sys

pygame.init()



class button:
    def __init__(self, x, y, w, h, txt : str):
        self.rect = pygame.Rect(x-w/2, y-h/2, w, h)
        self.text_surface = constants.GAME_FONT.render(txt, True, "black")
        self.x = x
        self.y = y
        
        self.highlighted = False
        self.activated = False
        self.size = 0.1
        self.w = w
        self.h = h

    def smooth_load(self):
        self.rect = pygame.Rect(self.x-(self.w*self.size)/2, self.y-(self.h*self.size)/2, self.w*self.size, self.h*self.size)
        self.size += (1 - self.size)/10

    def draw(self, screen):
        if not self.activated:
            if self.highlighted:
                color = (200, 200, 255)
            else:
                color = (100, 100, 255)
            #draw rounded text box
            round_width = 30
            pygame.draw.line(screen, color, self.rect.topleft, self.rect.topright, round_width)
            pygame.draw.line(screen, color, self.rect.topright, self.rect.bottomright, round_width)
            pygame.draw.line(screen, color, self.rect.bottomright, self.rect.bottomleft, round_width)
            pygame.draw.line(screen, color, self.rect.bottomleft, self.rect.topleft, round_width)
            
            pygame.draw.circle(screen, color, self.rect.topleft, (round_width-1 )/2, 0)
            pygame.draw.circle(screen, color, self.rect.topright, (round_width-1 )/2, 0)
            pygame.draw.circle(screen, color, self.rect.bottomleft, (round_width-1 )/2, 0)
            pygame.draw.circle(screen, color, self.rect.bottomright, (round_width-1 )/2, 0)

            pygame.draw.rect(screen, color, self.rect, 0)

            screen.blit(self.text_surface, (self.rect.centerx-self.text_surface.get_rect().width/2, self.rect.top))
    
    def check_click(self):
        if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()):
            if True in pygame.mouse.get_pressed():
                self.process_click()
            
            self.highlighted = True
        else:
            self.highlighted = False
    
    def process_click(self):
        self.activated = True
        
