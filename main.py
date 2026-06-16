import pygame
import random
from Player import *
from constants import *
from cell import *
import levels

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill("black")
pygame.display.flip()

cells = []

def update_cells():
    for cell in cells:
        cell.update()
        cell.draw(screen)
        
def new_cell(x, y, r):
    new = cell(x, y, r)
    cells.append(new)


#graphics transformations

for i in range(10):
    new_cell(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(40, 50))

new_cell(CENTER_X, 50, 30)
new_cell(50, CENTER_Y, 50)


player = Player(CENTER_X+100, CENTER_Y)
l1 = levels.one()
l2 = levels.two()
l3 = levels.three()
l4 = levels.four()
l5 = levels.five()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)
    screen.fill("white")
    player.draw(screen)
    player.update_controls()
    update_cells()
    
    pygame.draw.circle(screen, "green", (player.point.x, player.point.y), 10) #center of cell rotation(test)
    
    pygame.display.flip()


pygame.quit()
