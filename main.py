import pygame
import random
from Player import *
import constants
from cell import *
import levels
import ui
import dynamicPoint
from pyvidplayer2 import Video



pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((186, 81, 70))

pygame.display.flip()

BG_COLOR = (186, 81, 70)

widthLow = -200
widthHigh = 1800
heightLow = -200
heightHigh = 1800

cells = []
player = Player(CENTER_X+100, CENTER_Y)
uiBorder = ui.uiContainer()

#level class
class Level:
    def __init__(self, center_x, center_y, width, height):
        self.widthLow = math.floor(center_x - width/2)
        self.widthHigh = math.floor(center_x + width/2)
        self.heightLow = math.floor(center_y - height/2)
        self.heightHigh = math.floor(center_y + height/2)
    
    def createCellBox(self):
        
        
        for i in range(self.widthLow, self.widthHigh, 40):
            new_cell(self.widthLow+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(self.widthHigh+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
        for i in range(self.heightLow, self.heightHigh, 40):
            new_cell(i+random.randint(-10, 10), self.heightLow+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(i+random.randint(-10, 10), self.heightHigh+random.randint(-10, 10), random.randint(30, 50), False)
        

        for i in range(50):
            new_cell(random.randint(self.widthLow, self.widthHigh), random.randint(self.widthLow, self.widthHigh), random.randint(30, 50), False)
        
        for i in range(5):
            new_cell(random.randint(self.widthLow, self.widthHigh), random.randint(self.widthLow, self.widthHigh), random.randint(30, 50), False)
            cells[len(cells)-1].isCancer = True
    
    def run(self):
        SCORE = 0

        #level 1 loop
        title1 = ui.topTitle(100, CENTER_X, 200, "LEVEL ONE")
        subtitle = ui.subTitle(CENTER_X, 300, "Bone Marrow")

        



        clock = pygame.time.Clock()
        running = True
        time = 0

        CANCER_DIVIDE = pygame.USEREVENT + 2
        pygame.time.set_timer(CANCER_DIVIDE, 50000)
        while running:
            title1.smooth_load()





            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == CANCER_DIVIDE:
                    for i in range(len(cells)-1, -1, -1):
                        this_cell = cells[i]
                        if this_cell.isCancer:
                            new_cell(this_cell.x+5, this_cell.y + 5, random.randint(30, 50), True)
                            cells[-1].isCancer = True
                            new_cell(this_cell.x-5, this_cell.y-5, random.randint(30, 50), True)
                            cells[-1].isCancer = True
                            del cells[i]
                    pygame.time.set_timer(CANCER_DIVIDE, 20000) 



            subtitle.time += 1
            if subtitle.time > 240:
                subtitle.showing = False

            title1.time += 1
            if title1.time > 240:
                for i in range(10):
                    title1.smooth_close()
                title1.showing = False
            clock.tick(60)
            screen.fill(BG_COLOR)

            #draw_background()
            player.draw(screen)


            title1.draw(screen)
            player.update_controls()
            player.updateForwardVector()
            player.bound_camera(LEVEL_1)
            update_cells()
            cell_push_apart()
            check_cell_kill()
            subtitle.draw(screen)
            title1.draw(screen)

            uiBorder.draw(screen)
            uiBorder.drawScore(screen, player)



            pygame.display.set_caption(f"Cancer:healthy {player.cancer_killed}:{player.healthy_killed} ||| overall {round(player.score, 3)*100}%")
            pygame.display.flip()


        








#push cells away from each other
def cell_push_apart():
    for this in cells:
        for other in cells:
            if other != this:
                #find distance, ux, uy
                dx = other.x-this.x
                dy = other.y-this.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance<5:
                    distance = 5
                if distance < this.radius+other.radius:
                    ux = dx/distance
                    uy = dy/distance
                    overlap = other.radius + this.radius - distance
                    fx = this.x - ux*overlap
                    fy = this.y - uy*overlap
                    
                    this.x += (fx-this.x)/4
                    this.y += (fy-this.y)/4
                
        #check collision with player
        dx = player.x-this.x
        dy = player.y-this.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance<5:
            distance = 5
        if distance < this.radius+other.radius:
            ux = dx/distance
            uy = dy/distance
            overlap = 50 + this.radius - distance
            fx = this.x - ux*overlap
            fy = this.y - uy*overlap 
            this.x += (fx-this.x)/4
            this.y += (fy-this.y)/4
    
    #don't go beyond borders
        if this.x > widthHigh - 50:
            this.vx -= 1
        if this.x < widthLow + 50:
            this.vx += 1
        if this.y > heightHigh - 50:
            this.vy -= 1
        if this.y < heightLow + 50:
            this.vy += 1


def draw_background():
   
    #first draw middleground
    img_width = (widthHigh-widthLow)*2
    img_height = (heightHigh-heightLow)*2
    transformed = pygame.transform.scale(constants.MIDDLEGROUND_IMG, (img_width, img_height))

    screen.blit(transformed, (widthLow*2-constants.SCROLL_X, heightLow*2-constants.SCROLL_Y))






def update_cells():
    for i in range(len(cells)-1, -1, -1):
        this = cells[i]
        this.update()
        this.draw(screen)
        


def check_cell_kill():
    pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    global player
    for i in range(len(cells)-1, -1, -1):
        
        this = cells[i]
        if pygame.Rect.colliderect(this.rect, player.bigRect):
            this.highlighted = True
            this.draw(screen)
            
        else:
            this.highlighted = False
        
        reticle_rotation = 0
        mouse_dist = math.dist(this.point.coord, pos)
        if pygame.Rect.collidepoint(this.rect, pos[0], pos[1]) and this.highlighted:
            reticle_rotation += 1
            #spawn reticle
            r = 50
            transformed = pygame.transform.scale(RETICLE, (r, r))
            transformed = pygame.transform.rotate(transformed, reticle_rotation)
            
            screen.blit(transformed, (pos[0]-r/2, pos[1]-r/2))
            if mouse_pressed:
                #kill cell
                if this.isCancer:
                    player.cancer_killed += 1
                else:
                    player.healthy_killed += 1

                del cells[i]
        
        
def new_cell(x, y, r, isCancer : bool):
    new = cell(x, y, r)
    new.ID = len(cells)
    new.isCancer = isCancer
    cells.append(new)

"""def createCellBox():
        
        
        for i in range(widthLow, widthHigh, 40):
            new_cell(widthLow+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(widthHigh+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
        for i in range(heightLow, heightHigh, 40):
            new_cell(i+random.randint(-10, 10), heightLow+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(i+random.randint(-10, 10), heightHigh+random.randint(-10, 10), random.randint(30, 50), False)
        

        for i in range(50):
            new_cell(random.randint(widthLow, widthHigh), random.randint(widthLow, widthHigh), random.randint(30, 50), False)
        
        for i in range(5):
            new_cell(random.randint(widthLow, widthHigh), random.randint(widthLow, widthHigh), random.randint(30, 50), False)
            cells[len(cells)-1].isCancer = True"""




#title screen
def gradual_text(text: str, x, y,):
    text_surface = constants.GAME_FONT.render("", True, "black")
    for i in range(len(text)):
        text_surface = constants.GAME_FONT.render(text[:i], True, "black")
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        clock.tick(16000)
        pygame.time.wait(50)

































playButton = ui.button(CENTER_X, 500, 300, 100, "Start")
quitButton = ui.button(CENTER_X, HEIGHT-100, 200, 50, "quit")

title = constants.GAME_FONT.render("CANCER GAME THING", True, "white")


title_screen_new_cell_event = pygame.USEREVENT + 1
pygame.time.set_timer(title_screen_new_cell_event, 2000)
clock = pygame.time.Clock()
new_cell(CENTER_X, CENTER_Y, 50, True)

IN_TITLE_SCREEN = True

while IN_TITLE_SCREEN:
    

    playButton.smooth_load()
    quitButton.smooth_load()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IN_TITLE_SCREEN = False
            pygame.quit()
        elif event.type == title_screen_new_cell_event:
            
            for i in range(len(cells)-1, -1, -1):
                this_cell = cells[i]
                if this_cell.isCancer:
                    new_cell(this_cell.x+5, this_cell.y + 5, random.randint(30, 50), True)
                    cells[-1].isCancer = True
                    cells[-1].vy = random.randint(-2, 2)
                    cells[-1].vx = random.randint(-2, 2)
                    cells[-1].friction = 0.999
                    new_cell(this_cell.x-5, this_cell.y-5, random.randint(30, 50), True)
                    cells[-1].isCancer = True
                    cells[-1].vy = random.randint(-2, 2)
                    cells[-1].vx = random.randint(-2, 2)
                    cells[-1].friction = 0.999
                    del cells[i]
            pygame.time.set_timer(title_screen_new_cell_event, 2000) 
        if len(cells) > 256:
            cells = []
            new_cell(CENTER_X, CENTER_Y, 50, True)
    
    for this in cells:
        
        if this.y > constants.HEIGHT:
            
            this.y = constants.HEIGHT
        
        if this.x < 0:
            this.x = 0
        elif this.x > WIDTH:
            this.x = WIDTH
        

    
    if playButton.activated:
        IN_TITLE_SCREEN = False
        #move on to game
    
    if quitButton.activated:
        IN_TITLE_SCREEN = False
        pygame.quit()
    

    

    clock.tick(60)
    screen.fill(BG_COLOR)
    screen.blit(title, (CENTER_X-title.get_rect().width/2, 100))
    update_cells()
    playButton.draw(screen)
    playButton.check_click()

    quitButton.draw(screen)
    quitButton.check_click()
    
    
    
    cell_push_apart()
    pygame.display.flip()















cells = []
#opening cutscene start
skipButton = ui.button(WIDTH-100, HEIGHT-100, 100, 50, "Skip")
OPENING_CUTSCENE.play()

running = True
while running:
    skipButton.smooth_load()

    clock.tick(60)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))


    OPENING_CUTSCENE.draw(screen, (0, 0))
    skipButton.draw(screen)
    skipButton.check_click()

    pygame.display.update()

    if not OPENING_CUTSCENE.active or skipButton.activated:
        running = False
        


OPENING_CUTSCENE.close()

pygame.mixer.init()
background_music = pygame.mixer.music.load("5462458621362176.wav")
pygame.mixer.music.play(loops=-1, fade_ms=2000)

#do slide sequence
##AI!!
def helper(text):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False 
        screen.fill(BG_COLOR)
        gradual_text(text, CENTER_X - 400, 200)
        pygame.display.flip()
        clock.tick(60) 
    screen.fill(BG_COLOR)
    pygame.display.flip()

helper("You are a white blood cell\n\n       enter to continue")
helper("Your job is to kill cancer cells\n\n       enter to continue")
helper("Use WASD to move around\n\n       enter to continue")
helper("Click on cells to kill them.\n\n       enter to continue")
# Fixed this line to match your 2-argument helper structure
helper("Good luck!\n\n       enter to continue") 



#START GAME
LEVEL_1 = Level(CENTER_X, CENTER_Y, 2000, 2000)
LEVEL_1.createCellBox()
LEVEL_1.run()

        self.heightHigh = math.floor(center_y + height/2)
    
    def createCellBox(self):
        
        
        for i in range(self.widthLow, self.widthHigh, 40):
            new_cell(self.widthLow+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(self.widthHigh+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
        for i in range(self.heightLow, self.heightHigh, 40):
            new_cell(i+random.randint(-10, 10), self.heightLow+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(i+random.randint(-10, 10), self.heightHigh+random.randint(-10, 10), random.randint(30, 50), False)
        

        for i in range(50):
            new_cell(random.randint(self.widthLow, self.widthHigh), random.randint(self.widthLow, self.widthHigh), random.randint(30, 50), False)
        
        for i in range(5):
            new_cell(random.randint(self.widthLow, self.widthHigh), random.randint(self.widthLow, self.widthHigh), random.randint(30, 50), False)
            cells[len(cells)-1].isCancer = True
    
    def run(self):
        SCORE = 0

        #level 1 loop
        title1 = ui.topTitle(100, CENTER_X, 200, "LEVEL ONE")
        subtitle = ui.subTitle(CENTER_X, 300, "Bone Marrow")

        



        clock = pygame.time.Clock()
        running = True
        time = 0

        CANCER_DIVIDE = pygame.USEREVENT + 2
        pygame.time.set_timer(CANCER_DIVIDE, 50000)
        while running:
            title1.smooth_load()





            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == CANCER_DIVIDE:
                    for i in range(len(cells)-1, -1, -1):
                        this_cell = cells[i]
                        if this_cell.isCancer:
                            new_cell(this_cell.x+5, this_cell.y + 5, random.randint(30, 50), True)
                            cells[-1].isCancer = True
                            new_cell(this_cell.x-5, this_cell.y-5, random.randint(30, 50), True)
                            cells[-1].isCancer = True
                            del cells[i]
                    pygame.time.set_timer(CANCER_DIVIDE, 20000) 



            subtitle.time += 1
            if subtitle.time > 240:
                subtitle.showing = False

            title1.time += 1
            if title1.time > 240:
                for i in range(10):
                    title1.smooth_close()
                title1.showing = False
            clock.tick(60)
            screen.fill(BG_COLOR)

            #draw_background()
            player.draw(screen)


            title1.draw(screen)
            player.update_controls()
            player.updateForwardVector()
            player.bound_camera(LEVEL_1)
            update_cells()
            cell_push_apart()
            check_cell_kill()
            subtitle.draw(screen)
            title1.draw(screen)

            uiBorder.draw(screen)
            uiBorder.drawScore(screen, player)



            pygame.display.set_caption(f"Cancer:healthy {player.cancer_killed}:{player.healthy_killed} ||| overall {round(player.score, 3)*100}%")
            pygame.display.flip()


        








#push cells away from each other
def cell_push_apart():
    for this in cells:
        for other in cells:
            if other != this:
                #find distance, ux, uy
                dx = other.x-this.x
                dy = other.y-this.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance<5:
                    distance = 5
                if distance < this.radius+other.radius:
                    ux = dx/distance
                    uy = dy/distance
                    overlap = other.radius + this.radius - distance
                    fx = this.x - ux*overlap
                    fy = this.y - uy*overlap
                    
                    this.x += (fx-this.x)/4
                    this.y += (fy-this.y)/4
                
        #check collision with player
        dx = player.x-this.x
        dy = player.y-this.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance<5:
            distance = 5
        if distance < this.radius+other.radius:
            ux = dx/distance
            uy = dy/distance
            overlap = 50 + this.radius - distance
            fx = this.x - ux*overlap
            fy = this.y - uy*overlap 
            this.x += (fx-this.x)/4
            this.y += (fy-this.y)/4
    
    #don't go beyond borders
        if this.x > widthHigh - 50:
            this.vx -= 1
        if this.x < widthLow + 50:
            this.vx += 1
        if this.y > heightHigh - 50:
            this.vy -= 1
        if this.y < heightLow + 50:
            this.vy += 1


def draw_background():
   
    #first draw middleground
    img_width = (widthHigh-widthLow)*2
    img_height = (heightHigh-heightLow)*2
    transformed = pygame.transform.scale(constants.MIDDLEGROUND_IMG, (img_width, img_height))

    screen.blit(transformed, (widthLow*2-constants.SCROLL_X, heightLow*2-constants.SCROLL_Y))






def update_cells():
    for i in range(len(cells)-1, -1, -1):
        this = cells[i]
        this.update()
        this.draw(screen)
        


def check_cell_kill():
    pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    global player
    for i in range(len(cells)-1, -1, -1):
        
        this = cells[i]
        if pygame.Rect.colliderect(this.rect, player.bigRect):
            this.highlighted = True
            this.draw(screen)
            
        else:
            this.highlighted = False
        
        reticle_rotation = 0
        mouse_dist = math.dist(this.point.coord, pos)
        if pygame.Rect.collidepoint(this.rect, pos[0], pos[1]) and this.highlighted:
            reticle_rotation += 1
            #spawn reticle
            r = 50
            transformed = pygame.transform.scale(RETICLE, (r, r))
            transformed = pygame.transform.rotate(transformed, reticle_rotation)
            
            screen.blit(transformed, (pos[0]-r/2, pos[1]-r/2))
            if mouse_pressed:
                #kill cell
                if this.isCancer:
                    player.cancer_killed += 1
                else:
                    player.healthy_killed += 1

                del cells[i]
        
        
def new_cell(x, y, r, isCancer : bool):
    new = cell(x, y, r)
    new.ID = len(cells)
    new.isCancer = isCancer
    cells.append(new)

"""def createCellBox():
        
        
        for i in range(widthLow, widthHigh, 40):
            new_cell(widthLow+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(widthHigh+random.randint(-10, 10), i+random.randint(-10, 10), random.randint(30, 50), False)
        for i in range(heightLow, heightHigh, 40):
            new_cell(i+random.randint(-10, 10), heightLow+random.randint(-10, 10), random.randint(30, 50), False)
            new_cell(i+random.randint(-10, 10), heightHigh+random.randint(-10, 10), random.randint(30, 50), False)
        

        for i in range(50):
            new_cell(random.randint(widthLow, widthHigh), random.randint(widthLow, widthHigh), random.randint(30, 50), False)
        
        for i in range(5):
            new_cell(random.randint(widthLow, widthHigh), random.randint(widthLow, widthHigh), random.randint(30, 50), False)
            cells[len(cells)-1].isCancer = True"""




#title screen
def gradual_text(text: str, x, y,):
    text_surface = constants.GAME_FONT.render("", True, "black")
    for i in range(len(text)):
        text_surface = constants.GAME_FONT.render(text[:i], True, "black")
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        clock.tick(16000)
        pygame.time.wait(50)

































playButton = ui.button(CENTER_X, 500, 300, 100, "Start")
quitButton = ui.button(CENTER_X, HEIGHT-100, 200, 50, "quit")

title = constants.GAME_FONT.render("Echoes of The Cells", True, "white")


title_screen_new_cell_event = pygame.USEREVENT + 1
pygame.time.set_timer(title_screen_new_cell_event, 2000)
clock = pygame.time.Clock()
new_cell(CENTER_X, CENTER_Y, 50, True)

IN_TITLE_SCREEN = True

while IN_TITLE_SCREEN:
    

    playButton.smooth_load()
    quitButton.smooth_load()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IN_TITLE_SCREEN = False
            pygame.quit()
        elif event.type == title_screen_new_cell_event:
            
            for i in range(len(cells)-1, -1, -1):
                this_cell = cells[i]
                if this_cell.isCancer:
                    new_cell(this_cell.x+5, this_cell.y + 5, random.randint(30, 50), True)
                    cells[-1].isCancer = True
                    cells[-1].vy = random.randint(-2, 2)
                    cells[-1].vx = random.randint(-2, 2)
                    cells[-1].friction = 0.999
                    new_cell(this_cell.x-5, this_cell.y-5, random.randint(30, 50), True)
                    cells[-1].isCancer = True
                    cells[-1].vy = random.randint(-2, 2)
                    cells[-1].vx = random.randint(-2, 2)
                    cells[-1].friction = 0.999
                    del cells[i]
            pygame.time.set_timer(title_screen_new_cell_event, 2000) 
        if len(cells) > 256:
            cells = []
            new_cell(CENTER_X, CENTER_Y, 50, True)
    
    for this in cells:
        
        if this.y > constants.HEIGHT:
            
            this.y = constants.HEIGHT
        
        if this.x < 0:
            this.x = 0
        elif this.x > WIDTH:
            this.x = WIDTH
        

    
    if playButton.activated:
        IN_TITLE_SCREEN = False
        #move on to game
    
    if quitButton.activated:
        IN_TITLE_SCREEN = False
        pygame.quit()
    

    

    clock.tick(60)
    screen.fill(BG_COLOR)
    screen.blit(title, (CENTER_X-title.get_rect().width/2, 100))
    update_cells()
    playButton.draw(screen)
    playButton.check_click()

    quitButton.draw(screen)
    quitButton.check_click()
    
    
    
    cell_push_apart()
    pygame.display.flip()















cells = []
#opening cutscene start
skipButton = ui.button(WIDTH-100, HEIGHT-100, 100, 50, "Skip")
OPENING_CUTSCENE.play()

running = True
while running:
    skipButton.smooth_load()

    clock.tick(60)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))


    OPENING_CUTSCENE.draw(screen, (0, 0))
    skipButton.draw(screen)
    skipButton.check_click()

    pygame.display.update()

    if not OPENING_CUTSCENE.active or skipButton.activated:
        running = False
        


OPENING_CUTSCENE.close()

pygame.mixer.init()
background_music = pygame.mixer.music.load("5462458621362176.wav")
pygame.mixer.music.play(loops=-1, fade_ms=2000)

#do slide sequence
##AI!!
def helper(text):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False 
        screen.fill(BG_COLOR)
        gradual_text(text, CENTER_X - 400, 200)
        pygame.display.flip()
        clock.tick(60) 
    screen.fill(BG_COLOR)
    pygame.display.flip()

helper("You are a white blood cell\n\n       enter to continue")
helper("Your job is to kill cancer cells\n\n       enter to continue")
helper("Use WASD to move around\n\n       enter to continue")
helper("Click on cells to kill them.\n\n       enter to continue")
# Fixed this line to match your 2-argument helper structure
helper("Good luck!\n\n       enter to continue") 



#START GAME
LEVEL_1 = Level(CENTER_X, CENTER_Y, 2000, 2000)
LEVEL_1.createCellBox()
LEVEL_1.run()

