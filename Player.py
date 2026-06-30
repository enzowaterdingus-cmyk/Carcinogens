import pygame
from dynamicPoint import *
import constants


r = 50

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.forward_speed = 0
        self.direction = 0 #direction in degrees of forward vector
        self.point = dynamicPoint(self.x, self.y)

        self.cancer_killed = 0
        self.healthy_killed = 0
        self.score = 0
        
        

        self.rect = pygame.Rect(self.x-r/2, self.y-r/2, r, r)
        self.bigRect = pygame.Rect(self.x-r, self.y-r, r*2, r*2)
    
    def updateForwardVector(self):
        real_direction = -(math.atan2(self.vy, self.vx)*180/math.pi)
        self.direction += real_direction - self.direction/10




    def draw(self, screen):
        img_width = r*2
        img_height = r*2

        transformed = pygame.transform.scale(constants.PLAYER_IMAGE, (img_width, img_height))
        transformed = pygame.transform.scale(transformed, (img_width+math.sqrt(self.vx**2+self.vy**2)*3, img_height-math.sqrt(self.vx**2+self.vy**2)*3))
        transformed = pygame.transform.rotate(transformed, self.direction)
        screen.blit(transformed, (self.point.x-img_width/2, self.point.y-img_width/2))
      




        """pygame.draw.circle(screen, "red", (self.point.x, self.point.y), 20, 2)
        pygame.draw.line(screen, "red", (self.dev_shape.left, self.dev_shape.top), (self.dev_shape.right, self.dev_shape.bottom), 2)
        pygame.draw.line(screen, "red", (self.dev_shape.right, self.dev_shape.top), (self.dev_shape.left, self.dev_shape.bottom), 2)
        pygame.draw.line(screen, "red", (self.point.x, self.point.y), (self.point.x+50*math.sin(self.direction), self.point.y+50*math.cos(self.direction)))"""
        
        


    def update_controls(self):
        if self.vy>0 and self.vx>0:
            self.direction = math.atan2(self.vy, self.vx)
        else:
            self.direction = 0
        
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
            
            self.vy -= PLAYER_SPEED
        elif keys[pygame.K_DOWN]:
           
            self.vy += PLAYER_SPEED
        
        if keys [pygame.K_LEFT]:
            self.vx -= PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.vx += PLAYER_SPEED
        
        self.vx *= 0.9
        self.vy *= 0.9

        constants.SCROLL_X += ((self.x-constants.CENTER_X) - constants.SCROLL_X)/4
        constants.SCROLL_Y += ((self.y-constants.CENTER_Y) - constants.SCROLL_Y)/4

        if self.healthy_killed == 0:
            self.score = 1
        else:
            self.score = self.cancer_killed/(self.healthy_killed+self.cancer_killed)
        
        self.rect = pygame.Rect(self.point.x-r/2, self.point.y-r/2, r, r)
        self.bigRect = pygame.Rect(self.point.x-r, self.point.y-r, r*2, r*2)

    
    def bound_camera(self, level):
        if constants.SCROLL_X > level.widthHigh - CENTER_X - 50:
            constants.SCROLL_X = level.widthHigh - CENTER_X - 50
        elif constants.SCROLL_X < level.widthLow + CENTER_X + 50:
            constants.SCROLL_X = level.widthLow + CENTER_X + 50

        if constants.SCROLL_Y > level.heightHigh - CENTER_Y - 50:
            constants.SCROLL_Y = level.heightHigh - CENTER_Y - 50
        if constants.SCROLL_Y < level.heightLow + CENTER_Y + 50:
            constants.SCROLL_Y = level.heightLow + CENTER_Y + 50
