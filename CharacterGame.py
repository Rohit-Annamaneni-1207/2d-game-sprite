import pygame
import os
pygame.font.init()
pygame.mixer.init()
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.walk_right = []
        self.walk_left = []
        self.jump_right = []
        self.jump_left = []
        self.attack_right = []
        self.attack_left = []
        self.run_right = []
        self.run_left = []
        self.idle_right = []
        self.idle_left = []
        self.facing = "right"

        self.WIDTH = 65
        self.HEIGHT = 75

        self.gMag = 6
        self.gravity = -self.gMag

        self.collided = False

        currentFolder = os.path.join("CharacterManipulation","reqAssets","main","walk")
        for filename in os.listdir(currentFolder):
            im = pygame.image.load(os.path.join(currentFolder, filename))
            im = pygame.transform.scale(im, (self.WIDTH,self.HEIGHT))
            self.walk_right.append(im)
            self.walk_left.append(pygame.transform.flip(im, True, False))

        currentFolder = os.path.join("CharacterManipulation","reqAssets","main","run")
        for filename in os.listdir(currentFolder):
            im = pygame.image.load(os.path.join(currentFolder, filename))
            im = pygame.transform.scale(im, (self.WIDTH,self.HEIGHT))
            self.run_right.append(im)
            self.run_left.append(pygame.transform.flip(im, True, False))

        currentFolder = os.path.join("CharacterManipulation","reqAssets","main","jump")
        for filename in os.listdir(currentFolder):
            im = pygame.image.load(os.path.join(currentFolder, filename))
            im = pygame.transform.scale(im, (self.WIDTH,self.HEIGHT))
            self.jump_right.append(im)
            self.jump_left.append(pygame.transform.flip(im, True, False))

        currentFolder = os.path.join("CharacterManipulation","reqAssets","main","attack")
        for filename in os.listdir(currentFolder):
            im = pygame.image.load(os.path.join(currentFolder, filename))
            im = pygame.transform.scale(im, (self.WIDTH,self.HEIGHT))
            self.attack_right.append(im)
            self.attack_left.append(pygame.transform.flip(im, True, False))

        currentFolder = os.path.join("CharacterManipulation","reqAssets","main","idle")
        for filename in os.listdir(currentFolder):
            im = pygame.image.load(os.path.join(currentFolder, filename))
            im = pygame.transform.scale(im, (self.WIDTH,self.HEIGHT))
            self.idle_right.append(im)
            self.idle_left.append(pygame.transform.flip(im, True, False))

        self.is_idle = True
        self.movement_status = "walk"
        
        self.current_sprite_mode = self.idle_right
        self.sprite_iterator = 0
        self.image = self.current_sprite_mode[self.sprite_iterator]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]
        

    def jump(self):

        pass

    def update(self, speed):

        print(self.rect.bottomright)

        if self.collided == False:
            self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1]-int(self.gravity))

        if self.is_idle == True:
            if self.facing == "right":
                self.current_sprite_mode = self.idle_right
            elif self.facing == "left":
                self.current_sprite_mode = self.idle_left
        elif self.movement_status == "walk":
            if self.facing == "right":
                self.current_sprite_mode = self.walk_right
            elif self.facing == "left":
                self.current_sprite_mode = self.walk_left
        elif self.movement_status == "run":
            if self.facing == "right":
                self.current_sprite_mode = self.run_right
            elif self.facing == "left":
                self.current_sprite_mode = self.run_left
        elif self.movement_status == "jump":
            if self.facing == "right":
                self.current_sprite_mode = self.jump_right
            elif self.facing == "left":
                self.current_sprite_mode = self.jump_left

        self.sprite_iterator += speed
        if int(self.sprite_iterator >= len(self.current_sprite_mode)):
            self.sprite_iterator = 0
        # print(self.sprite_iterator)
        self.image = self.current_sprite_mode[int(self.sprite_iterator)]

class tiles:
    def __init__(self,x, y, length, height):
        self.length = length
        self.height = height
        self.x = x
        self.y = y

        self.rect = pygame.Rect(x, y, self.length, self.height)

    def draw_tile(self, WIN, COLOUR):
        pygame.draw.rect(WIN, COLOUR, self.rect)

clock = pygame.time.Clock()
WIDTH = 900
HEIGHT = 500
BLACK = (0, 0, 0)
AQUA = (0, 200, 200)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite")

moving_sprites = pygame.sprite.Group()
Owl = Player(300, 100) #195
# Owl.rect.topleft = [20, 20]
moving_sprites.add(Owl)

def MovementHandle(keysPressed, Owl):
    if keysPressed[pygame.K_a]:
        Owl.facing = "left"
        if keysPressed[pygame.K_LSHIFT]:
            Owl.is_idle = False
            Owl.movement_status = "run"
            Owl.rect.topleft = (Owl.rect.topleft[0]-4, Owl.rect.topleft[1])
        else:
            Owl.is_idle = False
            Owl.movement_status = "walk"
            Owl.rect.topleft = (Owl.rect.topleft[0]-2, Owl.rect.topleft[1])
    elif keysPressed[pygame.K_d]:
        Owl.facing = "right"
        if keysPressed[pygame.K_LSHIFT]:
            Owl.is_idle = False
            Owl.movement_status = "run"
            Owl.rect.topleft = (Owl.rect.topleft[0]+4, Owl.rect.topleft[1])
        else:
            Owl.is_idle = False
            Owl.movement_status = "walk"
            Owl.rect.topleft = (Owl.rect.topleft[0]+2, Owl.rect.topleft[1])
    else:
        Owl.is_idle = True
    pass

def main():
    speed = 0.15
    floor = tiles(0, 275, 900, 300)
    run = True
    jump_iterator = 0
    jump_counter = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

            if event.type == pygame.KEYDOWN:
                # Jump controls go here
                if event.key == pygame.K_SPACE and jump_counter < 2:
                    jump_counter += 1
                    jump_iterator = 5
                pass
        
        if (jump_iterator > 0):
            Owl.is_idle = False
            Owl.movement_status = "jump"
            Owl.gravity = Owl.gMag
        else:
            if (Owl.gravity == -Owl.gMag):
                Owl.is_idle = True
            elif (Owl.gravity > -Owl.gMag):
                Owl.is_idle = False
                Owl.movement_status = "jump"
                Owl.gravity -= 0.3

        keysPressed = pygame.key.get_pressed()
        MovementHandle(keysPressed, Owl)

        tiles_list = [floor]

        
        for tile in tiles_list:
            if Owl.rect.colliderect(tile):
                Owl.collided = True
                jump_counter = 0
                impact_depth = Owl.rect.topleft[1] + Owl.HEIGHT - tile.y
                Owl.rect.topleft = (Owl.rect.topleft[0], Owl.rect.topleft[1]-impact_depth)
                break
            else:
                Owl.collided = False

        WIN.fill((255, 255, 255))
        moving_sprites.draw(WIN)
        moving_sprites.update(speed)
        # Owl.update(0.15)
        floor.draw_tile(WIN, AQUA)
        pygame.display.update()
        jump_iterator -= 1
        clock.tick(60)
    pygame.quit()

main()

