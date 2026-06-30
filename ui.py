import pygame
import constants
import sys

pygame.init()

class topTitle:
    def __init__(self, size, x, y, txt : str): #size as percentage
        self.text_surface = constants.GAME_FONT.render(txt, True, "white")
        self.width = self.text_surface.get_rect().width
        self.height = self.text_surface.get_rect().height
        self.text_surface = pygame.transform.scale(self.text_surface, (self.width*size/100, self.height*size/100))
        self.width = self.text_surface.get_rect().width
        self.height = self.text_surface.get_rect().height
        self.text_size = 100
        
        self.x = x #center coordinates
        self.y = y

        self.thingy_image = pygame.image.load("./thingy.png")
        self.thingy_image = pygame.transform.scale(self.thingy_image, (self.thingy_image.get_rect().width/4, self.thingy_image.get_rect().height/4))
        self.thingy_width = self.thingy_image.get_rect().width
        self.leftthingyx = self.x-self.thingy_width/2
        self.rightthingyx = self.x+self.thingy_width/2
        self.leftx = self.x-300*size/100
        self.rightx = self.x+300*size/100
        self.time = 0
        self.showing = True
    def draw(self, screen : pygame.Surface):
        if self.showing:
            self.text_surface = pygame.transform.scale(self.text_surface, (self.width*self.text_size/100, self.height*self.text_size/100))
            screen.blit(self.text_surface, (self.x-self.width/2, self.y-self.height/2))

            #draw left thingy
            screen.blit(self.thingy_image, (self.leftthingyx-self.thingy_width, self.y-self.height/2))
            #draw right thingy
            screen.blit(pygame.transform.flip(self.thingy_image, True, False), (self.rightthingyx, self.y-self.height/2))
    
    def smooth_load(self):
        self.leftthingyx += (self.leftx-self.leftthingyx)/5
        self.rightthingyx += (self.rightx-self.rightthingyx)/5
    
    def smooth_close(self):
        self.leftthingyx += 5
        self.rightthingyx -= 5

        
            

        


class subTitle:
    def __init__(self, x, y, text : str):
        self.text_surface = constants.GAME_FONT.render(text, True, "white")
        self.x = x
        self.y = y
        self.showing = True
        self.time = 0
    
    def draw(self, screen : pygame.Surface):
        if self.showing:
            #self.x and self.y are supposed to be center coordinates, so find tl coords for pygame.rect to use
            w = self.text_surface.get_rect().width
            h = self.text_surface.get_rect().height
            tl_x = self.x - w/2
            tl_y = self.y - h/2
            screen.blit(self.text_surface, (tl_x, tl_y))
    
    







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



class uiContainer:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, constants.WIDTH, constants.HEIGHT)
        self.img = constants.UI_CONTAINER_IMAGE
    
    def draw(self, screen : pygame.Surface):
        img = pygame.transform.scale(self.img, (constants.WIDTH, constants.HEIGHT))
        screen.blit(img, (0, 0))
    
    def drawScore(self, screen : pygame.Surface, player):
        text = constants.GAME_FONT.render(f"SCORE : {player.score}", True, "white")
        screen.blit(text, (constants.CENTER_X, 50))
        

        
