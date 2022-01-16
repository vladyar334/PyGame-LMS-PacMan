import pygame
import copy

s_p = 50
width = 650
height = 600
walls_coords = [[(100, 48), (448, 8)], [(100, 55), (7, 152)], [(180, 200), (8, 64)], [(268, 248), (8, 64)],
                [(140, 88), (48, 32)], [(220, 88), (64, 32)], [(364, 88), (65, 32)], [(460, 88), (49, 32)],
                [(100, 200), (86, 8)], [(140, 152), (48, 16)], [(316, 55), (16, 65)], [(540, 55), (8, 153)],
                [(460, 200), (88, 8)], [(460, 152), (49, 16)], [(412, 152), (16, 112)], [(364, 200), (50, 16)],
                [(268, 152), (112, 16)], [(316, 166), (16, 50)], [(220, 152), (16, 112)], [(235, 200), (49, 16)],
                [(100, 256), (88, 8)], [(460, 256), (89, 8)], [(460, 296), (89, 8)], [(460, 352), (88, 8)],
                [(460, 296), (9, 64)], [(412, 296), (17, 65)], [(220, 296), (16, 64)], [(460, 200), (8, 64)],
                [(100, 296), (88, 8)], [(179, 296), (9, 64)], [(100, 352), (88, 8)], [(100, 352), (8, 193)],
                [(107, 440), (33, 16)], [(100, 536), (448, 9)], [(540, 352), (8, 193)], [(508, 440), (34, 16)],
                [(268, 248), (40, 8)], [(340, 248), (41, 8)], [(460, 200), (9, 64)], [(139, 392), (49, 17)],
                [(171, 406), (17, 51)], [(220, 392), (64, 17)], [(364, 392), (65, 17)], [(460, 392), (49, 17)],
                [(460, 406), (17, 51)], [(412, 440), (17, 50)], [(364, 488), (145, 17)], [(267, 440), (114, 17)],
                [(316, 358), (16, 51)], [(220, 440), (16, 50)], [(139, 488), (145, 17)], [(372, 248), (9, 64)],
                [(268, 304), (113, 7)], [(268, 344), (112, 16)], [(316, 455), (16, 50)], [(268, 248), (112, 64)], ]


class Walls(pygame.sprite.Sprite):
    def __init__(self, coord, sizes):
        super().__init__(wall_sprites)
        self.image = pygame.Surface((sizes[0], sizes[1]))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]


class Character(object):
    def __init__(self):
        self.surface = None
        self.rect = None
        self.speed = None

    def canMove(self, direction, walls):
        a = self.copy()
        if direction == 1:
            a.rect.x += self.speed
        elif direction == 2:
            a.rect.x -= self.speed
        elif direction == 3:
            a.rect.y += self.speed
        else:
            a.rect.y -= self.speed
        if pygame.sprite.spritecollideany(a, walls):
            return False
        return True

    def move(self, direction):
        if direction == 1:
            self.rect.x += self.speed
        elif direction == 2:
            self.rect.x -= self.speed
        elif direction == 3:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed


class Ghost(Character):
    pass


class Pacman(Character):
    images = [pygame.image.load('data/pacman_0.png'), pygame.image.load('data/pacman_1.png')]
    for pic in range(len(images)):
        images[pic].set_colorkey((0, 0, 0))

    def __init__(self):
        super().__init__()
        self.image = Pacman.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = 315
        self.rect.top = 315
        self.direction = 0
        self.speed = 3
        self.moveUp = self.moveLeft = self.moveDown = self.moveRight = False
        self.score = 0
        self.lives = 3
        self.frame = 0
        self.isFirstPic = True

    def end_round(self):
        self.image = Pacman.images[0]
        self.isFirstPic = True
        self.frame = 0
        self.rect.left = 315
        self.rect.top = 315
        self.direction = 0
        self.moveUp = self.moveLeft = self.moveDown = self.moveRight = False

    def RotateImage(self):
        self.frame += 1
        if self.frame == 3:
            self.isFirstPic = not self.isFirstPic
            self.frame = 0
        if self.direction == 1:
            self.image = pygame.transform.rotate(Pacman.images[self.isFirstPic], 270)
        elif self.direction == 2:
            self.image = pygame.transform.rotate(Pacman.images[self.isFirstPic], 90)
        elif self.direction == 3:
            self.image = pygame.transform.rotate(Pacman.images[self.isFirstPic], 180)
        else:
            self.image = Pacman.images[self.isFirstPic]

    def pacman_move(self):
        if self.moveUp and self.canMove(0, wall_sprites):
            Character.move(self, 0)
            self.RotateImage()
        elif self.moveLeft and self.canMove(2, wall_sprites):
            Character.move(self, 2)
            self.RotateImage()
        elif self.moveRight and self.canMove(1, wall_sprites):
            Character.move(self, 1)
            self.RotateImage()
        elif self.moveDown and self.canMove(3, wall_sprites):
            Character.move(self, 3)
            self.RotateImage()

    def copy(self):
        copyobj = Pacman()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj

    def switch_pos(self):
        if self.rect.colliderect(((100, 100), (1, 200))):
            self.rect.x += 448 - self.image.get_rect().width
        elif self.rect.colliderect(((100 + 448, 100), (1, 200))):
            self.rect.x -= 448 - self.image.get_rect().width


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Boom them all')
    image = pygame.image.load('data/bg.png')
    print(image.get_rect())
    size = width, height
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    pacman = Pacman()
    for wall in walls_coords:
        Walls(*wall)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type != pygame.QUIT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pacman.moveUp = True
                        pacman.moveLeft = pacman.moveDown = pacman.moveRight = False
                        pacman.direction = 0
                    if event.key == pygame.K_DOWN:
                        pacman.moveDown = True
                        pacman.moveUp = pacman.moveLeft = pacman.moveRight = False
                        pacman.direction = 3
                    if event.key == pygame.K_RIGHT:
                        pacman.moveRight = True
                        pacman.moveUp = pacman.moveLeft = pacman.moveDown = False
                        pacman.direction = 1
                    if event.key == pygame.K_LEFT:
                        pacman.moveLeft = True
                        pacman.moveUp = pacman.moveDown = pacman.moveRight = False
                        pacman.direction = 2
                elif event.type == pygame.KEYUP:
                    pacman.moveUp = pacman.moveLeft = pacman.moveRight = pacman.moveDown = False
            else:
                pygame.quit()
        pacman.pacman_move()
        pacman.switch_pos()
        screen.blit(image, (100, 0))
        screen.blit(pacman.image, pacman.rect)
        # wall_sprites.draw(screen)
        pygame.display.flip()
