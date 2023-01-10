import sys
from random import randint
import pygame as pg

pg.init()
pg.time.set_timer(pg.USEREVENT, 1000)

FPS = 60
W = 2 ** 9
H = 2 ** 9
SPEED = 4
GRAY = (60, 60, 60)
LIGHT_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARS = ('images/car1.png', 'images/car2.png', 'images/car3.png')
CARS_UP = ('images/car4.png', 'images/car5.png', 'images/car6.png')
# для хранения готовых машин-поверхностей
CARS_SURF = []
CARS_SURF_UP = []
FONT = pg.font.SysFont('comicsansms', 30)
FONT_2 = pg.font.SysFont('comicsansms', 15)
explosion_s = pg.mixer.Sound('sounds/explosion.mp3')
boom_s = pg.mixer.Sound('sounds/boom.mp3')
game_s = pg.mixer.Sound('sounds/game.mp3')
defeat_s = pg.mixer.Sound('sounds/defeat.mp3')
game_over = False

# надо установить видео режим
# до вызова image.load()
sc = pg.display.set_mode((W, H))
explosion = pg.image.load('images/explosion.png').convert_alpha()
boom = pg.image.load('images/boom.png').convert_alpha()

truck = pg.image.load('images/car.png').convert_alpha()

for i in CARS:
    CARS_SURF.append(
        pg.image.load(i).convert_alpha())

for i in CARS_UP:
    CARS_SURF_UP.append(
        pg.image.load(i).convert_alpha())


class Car(pg.sprite.Sprite):
    def __init__(self, x, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(
            center=(x, -50))
        # добавляем в группу
        self.add(group)
        # у машин будет разная скорость
        self.speed = randint(1, 3)

    def update(self):
        if self.rect.y < H + 50:
            self.rect.y += self.speed
        else:
            # теперь не перебрасываем вверх,
            # а удаляем из всех групп
            self.kill()

    def boom(self):
        if self.image != boom:
            a = pg.sprite.Group()
            for i in cars:
                if i != self:
                    i.add(a)
            if pg.sprite.spritecollideany(self, a):
                self.image = boom
                self.rect = self.image.get_rect(center=self.rect.center)
                boom_s.play()

class Car_up(pg.sprite.Sprite):
    def __init__(self, x, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(
            center=(x, H + 50))
        # добавляем в группу
        self.add(group)
        # у машин будет разная скорость
        self.speed = randint(1, 3)

    def update(self):
        if self.rect.y > -50:
            self.rect.y -= self.speed
        else:
            # теперь не перебрасываем вверх,
            # а удаляем из всех групп
            self.kill()

    def boom(self):
        if self.image != boom:
            a = pg.sprite.Group()
            for i in cars:
                if i != self:
                    i.add(a)
            if pg.sprite.spritecollideany(self, a):
                self.image = boom
                self.rect = self.image.get_rect(center=self.rect.center)
                boom_s.play()


class lane_marking():
    start_y = -H // 2
    size = H // 8
    x = W // 2 - 20
    y = start_y

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def move(self):
        pg.draw.rect(sc, WHITE, (self.x, self.y, 10, self.size))
        if self.y < H:
            self.y += SPEED
        else:
            self.y = self.start_y


class road_center():
    start_y = -H // 2
    size = H // 2
    x = W // 2 - 15
    y = start_y

    def __init__(self, y):
        self.y = y

    def move(self):
        pg.draw.rect(sc, LIGHT_GRAY, (self.x, self.y, 15, self.size))
        if self.y < H:
            self.y += SPEED
        else:
            self.y = self.start_y


class Hero(pg.sprite.Sprite):
    def __init__(self, x, surf):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, H - 50))

    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def update(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            if self.rect.x > SPEED:
                self.rect.x -= SPEED
        elif pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            if self.rect.x < W - self.rect.w - SPEED:
                self.rect.x += SPEED

        if pressed[pg.K_UP] or pressed[pg.K_w]:
            if self.rect.y > SPEED:
                self.rect.y -= SPEED
        elif pressed[pg.K_DOWN] or pressed[pg.K_s]:
            if self.rect.y < H - self.rect.h - SPEED:
                self.rect.y += SPEED


    def end(self):
        self.image = explosion
        self.rect = self.image.get_rect(center=self.rect.center)


def close(e):
    if e.type == pg.QUIT:
        sys.exit()


cars = pg.sprite.Group()
pg.display.set_caption('DRIVEPECKER SIMULATOR')
pg.display.set_icon(pg.image.load('images/boom.png'))
clock = pg.time.Clock()
score = 0


def run():
    global score, game_over
    defeat_s.stop()
    game_s.play()
    Car(randint(30, W // 2 - 30),
        CARS_SURF[randint(0, 2)], cars)
    hero = Hero(W // 2 - W // 4, truck)
    lines = [lane_marking(0, W // 4 - 10), lane_marking(lane_marking.size * 4, W // 4 - 10),
             lane_marking(lane_marking.size * 8, W // 4 - 10), lane_marking(lane_marking.size * 16, W // 4 - 10),
             lane_marking(0, W // 2 + W // 4 - 10), lane_marking(lane_marking.size * 4, W // 2 + W // 4 - 10),
             lane_marking(lane_marking.size * 8, W // 2 + W // 4 - 10),
             lane_marking(lane_marking.size * 16, W // 2 + W // 4 - 10),
             road_center(34), road_center(road_center.size + 34)]
    game_over = False
    message = False
    tip = False
    while 1:
        if not game_over:
            game_over = pg.sprite.spritecollideany(hero, cars)\
                        or sc.get_at((hero.rect.x, hero.rect.y)) == LIGHT_GRAY \
                        or sc.get_at((hero.rect.x + hero.rect.w, hero.rect.y + hero.rect.h)) == LIGHT_GRAY \
                        or sc.get_at((hero.rect.x, hero.rect.y + hero.rect.h)) == LIGHT_GRAY \
                        or sc.get_at((hero.rect.x + hero.rect.w, hero.rect.y)) == LIGHT_GRAY
        event = pg.event.get()
        if game_over:
            if not message:
                game_s.stop()
                hero.end()
                hero.draw(sc)
                pg.display.update(hero.rect)
                explosion_s.play()
                pg.time.wait(1000)
                defeat_s.play()
                dumbpoints = ' DUMBPOINTS'
                if score < 2:
                    dumbpoints = ' DUMBPOINT'
                crush = FONT.render('!!!YOU GET CRUSHED!!!', True, WHITE, BLACK)
                crush_rect = crush.get_rect(center=(W // 2, H // 3))
                score = FONT_2.render('YOUR SCORE IS ' + str(score) + dumbpoints,
                                      True, WHITE, BLACK)
                score_rect = score.get_rect(center=(W // 2, H // 2))
                sc.blit(crush, crush_rect)
                sc.blit(score, score_rect)
                message = True
            for i in event:
                close(i)
                if i.type == pg.KEYDOWN:
                    score = 0
                    for i in cars:
                        i.kill()
                    run()
                    break
                elif i.type == pg.USEREVENT:
                    reset = FONT_2.render('PRESS ANY KEY TO RESET', True, WHITE, BLACK)
                    rect = reset.get_rect(center=(W // 2, H // 1.5))
                    if tip:
                        sc.blit(reset, rect)
                    else:
                        reset.fill(BLACK)
                        sc.blit(reset, rect)
                    tip = not tip
            pg.display.update()

        else:
            for i in event:
                close(i)
                if i.type == pg.USEREVENT:
                    Car(randint(30, W // 2 - 30),
                        CARS_SURF[randint(0, 2)], cars)
                    Car_up(randint(W // 2 + 30, W - 30),
                        CARS_SURF_UP[randint(0, 2)], cars)
                    score += 1

            sc.fill(GRAY)
            for i in lines:
                i.move()
            for i in cars:
                i.boom()
            hero.update()

            cars.draw(sc)
            hero.draw(sc)
            clock.tick(FPS)

            cars.update()
            scoretable = FONT.render(str(score), True, WHITE, BLACK)
            sc.blit(scoretable, (0, 0))

        pg.display.update()


run()
