#База игры
import random
from os import path
import pygame

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 8000

#обозначение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (9, 133, 59)

#включаем pygame и создаем окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars on field")
clock = pygame.time.Clock()


#функция отвечающая за спавн мобов
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
#функция для отрисовки текста
font_name = pygame.font.match_font("times new roman")
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


#функция для отрисовки здоровья
def draw_hp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 130
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outlane_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, DARK_GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outlane_rect, 2)

#функция для отрисовки жизней
def draw_lives(surf, x, y, lives, img):
    for i in range (lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

#Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.radius = 20
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()



    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 3000:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


#функция для скрытия персонажа после смерти
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1:
                shoot_sound.play()
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power == 2:
                shoot_sound.play()
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet2)
                bullets.add(bullet2)





#Класс мобов
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.radius = int(self.rect.width * 0.9 / 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


    #функция для прокрутки
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


#класс отвечаюий за выстрел
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#Класс за взрывы
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#класс за баффы
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


#Функция для создания меню
def showmenu():
    screen.blit(menu, menu_rect)
    draw_text(screen, "Starfield", 72, WIDTH / 2, HEIGHT / 4, WHITE)
    draw_text(screen, "Game control: A,D,SPACE", 22, WIDTH / 2, HEIGHT / 2, WHITE)
    draw_text(screen, "Press any key to play", 18, WIDTH / 2, HEIGHT / 4 * 3, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#закгрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
menu = pygame.image.load(path.join(img_dir, "menu.png")).convert()
menu_rect = menu.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Ship_blue.png")).convert()
heart_img = pygame.image.load(path.join(img_dir, "h.png")).convert()
h_img = pygame.transform.scale(heart_img, (35, 35))
h_img.set_colorkey(BLACK)
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png", "meteorBrown_med1.png",
                "meteorBrown_med3.png", "meteorBrown_small1.png",
                "meteorGrey_big1.png" , "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorBrown_small2.png",
                "meteorGrey_big4.png", "meteorBrown_tiny1.png", "meteorBrown_tiny2.png",
                "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png",
                "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
laser_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []

for i in range(0, 9):
    filename = f"regularExplosion0{i}.png".format()
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim["sm"].append(img_sm)
    filename = f"sonicExplosion0{i}.png".format()
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim["player"].append(img)

powerup_images = {}
powerup_images["shield"] = pygame.image.load(path.join(img_dir, "powerupRed_star.png")).convert()
powerup_images["gun"] = pygame.image.load(path.join(img_dir, "powerupYellow_bolt.png")).convert()






#Загрузка всей музыки
pygame.mixer.music.load(path.join(snd_dir, "StarW.wav"))
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(loops = -1)
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser.wav"))
expl_sounds = []
for snd in ["Explosion1.wav", "Explosion2.wav"]:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, "rumble1.ogg"))




#цикл игры
GAMEOVER = True
running = True
while running:
    if GAMEOVER:
        showmenu()
        GAMEOVER = False
        #группы спрайтов
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range (1, 9):
            newmob()

        score = 0
    clock.tick(FPS)

    #ввод ивента(события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #обновление спрайтов
    all_sprites.update()

    #проверка задел ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 1.5
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_expl = Explosion(player.rect.center, "player")
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            player.shield = 100

    #Если персонаж погиб и анимация взрыва прошла
    if player.lives == 0 and not death_expl.alive():
        GAMEOVER = True




    #проверка задела ли пуля врага
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += 75 - hit.radius
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    #проверка задел ли плэйер бафф
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += random.randrange(10, 25)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "gun":
            player.powerup()



    #рендеринг(графическая отрисовка)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "SCORE", 16, WIDTH / 2, 15, YELLOW)
    draw_text(screen, str(score), 32, WIDTH / 2, 30, YELLOW )
    draw_hp_bar(screen, 10, 10, player.shield)
    draw_text(screen, str(player.shield), 16, 69, 10, WHITE)
    draw_lives(screen, WIDTH -100, 5, player.lives, h_img)
    pygame.display.flip()










pygame.quit()








