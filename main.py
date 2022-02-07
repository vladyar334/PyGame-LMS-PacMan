import pygame
import copy
import os
import sys

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

smallDotCoords = [(350, 72), (350, 423), (485, 185), (125, 185), (445, 424), (485, 136), (125, 378), (395, 378),
                  (485, 72), (395, 424), (445, 72), (445, 136), (165, 424), (255, 185), (395, 136), (125, 104),
                  (205, 424), (205, 136), (395, 474), (165, 520), (255, 136), (165, 72), (205, 72), (255, 378),
                  (395, 330), (205, 330), (350, 104), (525, 185), (525, 378), (525, 474), (485, 474), (445, 185),
                  (525, 424), (300, 72), (350, 474), (350, 232), (485, 520), (445, 520), (485, 424), (445, 280),
                  (165, 378), (395, 185), (445, 378), (125, 474), (205, 520), (205, 185), (350, 185), (255, 520),
                  (350, 378), (350, 136), (300, 136), (300, 104), (445, 232), (205, 232), (445, 330), (300, 474),
                  (125, 424), (255, 72), (125, 136), (300, 520), (395, 520), (205, 281), (205, 104), (300, 185),
                  (255, 330), (165, 185), (165, 136), (205, 474), (205, 378), (255, 474), (395, 232), (165, 474),
                  (255, 232), (300, 378), (350, 330), (255, 280), (525, 104), (300, 330), (525, 136), (395, 72),
                  (485, 378), (445, 104), (350, 520), (300, 424), (300, 232), (445, 474), (395, 280), (255, 424)]

bigDotCoords = [(125, 72), (125, 520), (525, 72), (525, 520)]

pygame.mixer.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Music(object):
    radio = pygame.mixer.Channel(2)
    eat_small = pygame.mixer.Sound("data/eating_small.wav")
    eat_big = pygame.mixer.Sound("data/eating_big.wav")
    start_game = pygame.mixer.Sound("data/start.wav")
    ghostEaten = pygame.mixer.Sound("data/ghosteaten.wav")
    round_end = pygame.mixer.Sound("data/round_end.wav")


class Pellets(object):
    images = [pygame.image.load('data/dot.png'), pygame.image.load('data/bigdot.png')]
    images_rect = [images[0].get_rect(), images[1].get_rect()]
    shifts_images = [(-images[0].get_width() / 2, -images[0].get_height() / 2),
                     (-images[1].get_width() / 2, -images[1].get_height() / 2)]

    def createListBigDot(self):
        pellets = []
        for bigDot in bigDotCoords:
            pellets.append(bigDot)
        return pellets

    def createListSmallDot(self):
        pellets = []
        for smallDot in smallDotCoords:
            pellets.append(smallDot)
        return pellets

    def checkEaten(self, pellets_s, pellets_b, pacman_player, ghosts):
        for i, pellet_s in enumerate(pellets_s[:]):
            pellet_rect = Pellets.images_rect[0]
            (pellet_rect.centerx, pellet_rect.centery) = pellet_s
            if pellet_rect.colliderect(pacman_player.rect):
                pacman.score += 10
                del pellets_s[i]
                if not Music.radio.get_busy():
                    Music.radio.play(Music.eat_small)
        for i, pellet_b in enumerate(pellets_b[:]):
            pellet_rect = Pellets.images_rect[1]
            (pellet_rect.centerx, pellet_rect.centery) = pellet_b
            if pellet_rect.colliderect(pacman_player.rect):
                del pellets_b[i]
                Music.radio.play(Music.eat_big)
                for ghost in ghosts:
                    Ghost.makeGhostBlue(ghost)


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
            self.rect.left += self.speed
        elif direction == 2:
            self.rect.left -= self.speed
        elif direction == 3:
            self.rect.top += self.speed
        elif direction == 0:
            self.rect.top -= self.speed

    def copy(self):
        copyobj = Character()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj


class Ghost(Character):
    images = [pygame.image.load("data/orange_0.png"), pygame.image.load("data/cyan_0.png")]
    isBlueTime = 600
    addTime = 1800
    add_time = addTime

    def __init__(self):
        super().__init__()
        self.surface = Ghost.images[0]
        self.rect = self.surface.get_rect()
        self.rect.left = 315
        self.rect.top = 275
        self.speed = 1
        self.course = [0] * (50 // self.speed)
        self.isBlue = False
        self.isBlue_time = 0
        self.old_choises = [-1, -1, -1, -1]

    def makeGhostBlue(self):
        self.isBlue = True
        self.isBlue_time = Ghost.isBlueTime
        self.surface = Ghost.images[1]
        self.course = []

    def makeGhostNotBlue(self):
        self.isBlue = False
        self.isBlue_time = 0
        self.surface = Ghost.images[0]
        self.course = []

    def checkGhostBlue(self):
        self.isBlue_time -= 1
        if self.isBlue_time < 0:
            self.makeGhostNotBlue()

    def end_round(self):
        self.makeGhostNotBlue()
        self.rect.left = 315
        self.rect.top = 275
        self.course = [0] * (50 // self.speed)

    def addNewGhost(self, ghosts):
        Ghost.add_time -= 1
        if len(ghosts) == 0:
            if Ghost.add_time > int(Ghost.addTime / 10):
                Ghost.add_time = int(Ghost.addTime / 10)

        if Ghost.add_time <= 0:
            ghosts.append(Ghost())
            Ghost.add_time = Ghost.addTime

    def copyGhost(self):
        copyobj = Ghost()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj

    def canGhostMoveDistance(self, direction, walls):
        test = self.copyGhost()
        counter = 0
        while True:
            if not Character.canMove(test, direction, walls):
                break
            Character.move(test, direction)
            counter += 1
        return counter

    def GhostMove(self, walls, pacman):
        if len(self.course) > 0:
            if self.canGhostMoveDistance(self.course[0], walls) or self.rect.colliderect(
                    pygame.Rect((268, 248), (112, 64))):
                Character.move(self, self.course[0])
                del self.course[0]
            else:
                self.course = []
        else:
            xDistance = pacman.rect.left - self.rect.left
            yDistance = pacman.rect.top - self.rect.top
            choices = [-1, -1, -1, -1]
            if abs(xDistance) > abs(yDistance):
                if xDistance > 0:
                    choices[0] = 1
                    choices[3] = 2
                elif xDistance < 0:
                    choices[0] = 2
                    choices[3] = 1
                if yDistance > 0:
                    choices[1] = 3
                    choices[2] = 0
                elif yDistance < 0:
                    choices[1] = 0
                    choices[2] = 3
                else:
                    if self.canGhostMoveDistance(3, walls) < self.canGhostMoveDistance(0, walls):
                        choices[1] = 3
                        choices[2] = 0
                    elif self.canGhostMoveDistance(0, walls) < self.canGhostMoveDistance(3, walls):
                        choices[1] = 0
                        choices[2] = 3
            elif abs(yDistance) >= abs(xDistance):
                if yDistance > 0:
                    choices[0] = 3
                    choices[3] = 0
                elif yDistance < 0:
                    choices[0] = 0
                    choices[3] = 3
                if xDistance > 0:
                    choices[1] = 1
                    choices[2] = 2
                elif xDistance < 0:
                    choices[1] = 2
                    choices[2] = 1
                else:
                    if self.canGhostMoveDistance(1, walls) < self.canGhostMoveDistance(2, walls):
                        choices[1] = 1
                        choices[2] = 2
                    elif self.canGhostMoveDistance(2, walls) < self.canGhostMoveDistance(1, walls):
                        choices[1] = 2
                        choices[2] = 1
            if self.isBlue:
                choices.reverse()
            choices_original = choices[:]
            for i, x in enumerate(choices[:]):
                if x == -1 or (not Character.canMove(self, x, walls)):
                    del choices[choices.index(x)]
            if self.old_choises[0] == choices[1] and self.old_choises[1] == choices[0]:
                for i in range(int(60 * 1.5)):
                    self.course.append(choices[1])
            self.old_choises = choices
            if len(choices) > 0:
                Character.move(self, choices[0])
                if choices_original.index(choices[0]) >= 2:
                    for i in range(int(60 * 1.5)):
                        self.course.append(choices[0])


class Pacman(Character):
    images = [pygame.image.load('data/pacman_0.png'), pygame.image.load('data/pacman_1.png'),
              pygame.image.load("data/icon.png")]
    for pic in range(len(images)):
        images[pic].set_colorkey((0, 0, 0))

    def __init__(self):
        super().__init__()
        self.image = Pacman.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = 315
        self.rect.top = 315
        self.direction = 0
        self.speed = 5
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

    def scoreDisplayPacman(self):
        return pygame.font.SysFont("Arial", 30).render(f"Очки: {str(self.score)}", True, 'yellow')

    def livesDisplayPacman(self):
        surface = pygame.font.SysFont("Arial", 30).render("Жизни:                        ", True, 'yellow')
        x = 100
        for i in range(self.lives):
            surface.blit(Pacman.images[2], (x, 5))
            x += 25
        return surface


class GameOver(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("end.jpg"), (650, 300))
        self.rect = self.image.get_rect()
        self.rect.x = -600
        self.rect.y = 150

    def update(self, *args):
        if self.rect.x + 1 <= -2:
            self.rect.x += 1
        else:
            pygame.time.set_timer(game_over, 0)


class TimerStart(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.seconds = 4
        self.image = pygame.font.SysFont("Arial", 48).render("До начала: " + str(self.seconds), True, 'red')
        self.rect = self.image.get_rect()
        self.rect.x = 325 - self.image.get_rect().centerx
        self.rect.y = 500

    def update(self, *args):
        self.seconds -= 1
        self.image = pygame.font.SysFont("Arial", 48).render("До начала: " + str(self.seconds), True, 'red')


class StartFon(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("start.jpg"), (650, 600))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, return_sec=False):
        if self.rect.x - 1 >= -650:
            self.rect.x -= 1
        else:
            pygame.time.set_timer(game_over, 0)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pacman')
    image = pygame.image.load('data/map.png')
    size = width, height
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    game_over_sprite = pygame.sprite.Group()
    game_start_sprites = pygame.sprite.Group()
    start_fon_anim_sprites = pygame.sprite.Group()
    StartFon(start_fon_anim_sprites)
    TimerStart(game_start_sprites)
    GameOver(game_over_sprite)
    ghosts = [Ghost()]
    pacman = Pacman()
    game_over = pygame.USEREVENT + 1
    game_start = pygame.USEREVENT + 2
    start_fon_anim = pygame.USEREVENT + 3
    pygame.mixer.music.load("data/music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pellets_small = Pellets.createListSmallDot(Pellets())
    pellets_big = Pellets.createListBigDot(Pellets())
    for wall in walls_coords:
        Walls(*wall)
    pygame.display.flip()
    Music.radio.play(Music.start_game)
    pygame.time.set_timer(game_start, 1000)
    while True:
        screen.fill('black')
        start_fon_anim_sprites.draw(screen)
        game_start_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == game_start:
                game_start_sprites.update()
        if not pygame.mixer.get_busy():
            break
        pygame.display.flip()
    pygame.time.set_timer(start_fon_anim, 1)
    while True:
        screen.fill('black')
        start_fon_anim_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == start_fon_anim:
                start_fon_anim_sprites.update()
        if start_fon_anim_sprites.sprites()[0].rect.x == -650:
            break
        pygame.display.flip()

    game = True

    while game:
        keepGoing_round = True
        pygame.mixer.music.play(-1, 0.0)
        while keepGoing_round:
            clock.tick(60)
            screen.fill('black')
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
            Ghost.addNewGhost(Ghost(), ghosts)
            screen.blit(image, (100, 0))
            screen.blit(pacman.image, pacman.rect)
            Pellets.checkEaten(Pellets(), pellets_small, pellets_big, pacman, ghosts)
            for g in ghosts:
                if g.isBlue:
                    g.checkGhostBlue()
            for g in ghosts:
                g.GhostMove(wall_sprites, pacman)
            for pellet in pellets_small:
                screen.blit(Pellets.images[0],
                            (pellet[0] + Pellets.shifts_images[0][0], pellet[1] + Pellets.shifts_images[0][1]))
            for pellet in pellets_big:
                screen.blit(Pellets.images[1],
                            (pellet[0] + Pellets.shifts_images[1][0], pellet[1] + Pellets.shifts_images[1][1]))
            for ghost in ghosts:
                screen.blit(ghost.surface, ghost.rect)
            for g in ghosts[:]:
                if pacman.rect.colliderect(g.rect):
                    if not g.isBlue:
                        keepGoing_round = False
                        pacman.lives -= 1
                        if pacman.lives == 0:
                            with open('data/record.txt', 'r') as f:
                                score_record, lives_record = [int(i) for i in f.read().split('\n')]
                                if score_record < pacman.score and lives_record <= pacman.lives:
                                    with open('data/record.txt', 'w') as w:
                                        w.write(f"{pacman.score}\n{pacman.lives}")
                            game = False
                        else:
                            Music.radio.play(Music.round_end)
                        break
                    else:
                        del ghosts[ghosts.index(g)]
                        pacman.score += 100
                        Music.radio.play(Music.ghostEaten)
            else:
                if len(pellets_small) == 0 and len(pellets_big) == 0:
                    game = keepGoing_round = False
                    with open('data/record.txt', 'r') as f:
                        score_record, lives_record = [int(i) for i in f.read().split('\n')]
                        if score_record < pacman.score and lives_record <= pacman.lives:
                            with open('data/record.txt', 'w') as w:
                                w.write(f"{pacman.score}\n{pacman.lives}")
            screen.blit(pacman.scoreDisplayPacman(), (10, 10))
            screen.blit(pacman.livesDisplayPacman(), (450, 10))
            pygame.display.flip()
        pacman.end_round()
        for g in ghosts:
            g.end_round()
        while True:
            if not pygame.mixer.get_busy():
                break
        pygame.mixer.music.stop()
    print('gameEnd')
    pygame.time.set_timer(game_over, 2)
    while True:
        for event in pygame.event.get():
            if event.type == game_over:
                screen.fill((0, 0, 0))
                game_over_sprite.update(event)
                game_over_sprite.draw(screen)
            if game_over_sprite.sprites()[0].rect.x == -2:
                score_finally = pygame.font.SysFont("Arial", 30).render("Всего очков: " + str(pacman.score), True,
                                                                        'yellow')
                lives_finally = pygame.font.SysFont("Arial", 30).render("Жизней осталось: " + str(pacman.lives), True,
                                                                        'yellow')
                score_record_display = pygame.font.SysFont("Arial", 30).render(
                    "Ваш прошлый рекорд: " + str(score_record) + f" ({lives_record} жиз.)", True,
                    'yellow')
                screen.blit(score_finally, (325 - score_finally.get_rect().centerx, 20))
                screen.blit(lives_finally, (325 - lives_finally.get_rect().centerx, 70))
                screen.blit(score_record_display, (325 - score_record_display.get_rect().centerx, 550))
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
