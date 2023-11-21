#Создай собственный Шутер!

from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, site_x, site_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (site_x, site_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


lost = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()






class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1




class Player(GameSprite):
    def update(self):
      keys = key.get_pressed()
      if keys[K_LEFT] and self.rect.x > 5:
          self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < 620:
          self.rect.x += self.speed
    def fire(self):
        pass
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)






window = display.set_mode((700, 500))
display.set_caption("Galaxy Шутер 228")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))


run = True
clock = time.Clock()
FPS = 60


ship = Player("rocket.png", 300, 400, 80, 100, 10)


from random import randint
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, 620), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

score = 0
font.init()
font2 = font.Font(None, 36)

finish = False
scope = 0
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not finish:
        window.blit(background,(0, 0))

        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text,(10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(10, 50))

        ship.update()
        ship.reset()
        asteroids.update()
        asteroids.draw(window)
        monsters.update()

        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        display.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:

          score = score + 1
          monster = Enemy("ufo.png", randint(80, win_width -80), -40, 80, 50, randint(1,5))
          monsters.add(monster)


    if sprite.spritecollide(ship, monsters, False) or lost >= 3 or sprite.spritecollide(ship, asteroids, False):
         finish = True
         window.blit(lose, (200, 200))

    if score >= 10:
         finish = True
         window.blit(win, (200, 200))