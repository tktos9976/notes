from pygame import* #імпорт бібліотеки 
from random import randint#імпорт рандома
from time import time as timer

init()

window = display.set_mode((700, 700))# ігрове вікно
display.set_caption("Shooter")#назва гри
display.set_icon(image.load('ufo.png'))#зображення монстрів
background = transform.scale(image.load("fon.jpg"), (700, 700))#фон ігрового поля

clock = time.Clock()#змінна часу

font.init()
font1 = font.SysFont("Arial", 20)# шрифт 
font2 = font.SysFont('Arial', 50)

class GameSprite(sprite.Sprite):#створення загального класу з основними здібностями для всіх
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()#функція для створення супер класу
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed#швидкість
        self.rect = self.image.get_rect()#рамка спрайта
        self.rect.x = player_x# переміщення по іксу
        self.rect.y = player_y# переміщення по ігрику

    def reset(self):#
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):# створеня класу головного гравця
    def update(self):#якщо клавіша нажата
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:#клавіша в ліво
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 650:#клавіша в право
            self.rect.x += self.speed


    def fire(self):# функція для пулі
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 5)#змінна для пулі
        bullets.add(bullet)#малювання пулі


lost = 0#пропущенні

class Enemy(GameSprite):#клас для ворога, клас спадкоємець
    def update(self):
        global lost
        self.rect.y += self.speed#вороги поступоп падають
        if self.rect.y > 700:#якщо вийшли за межі поля
            self.rect.y = 0 #переміщення на верх
            self.rect.x = randint(50, 600)#рандомне переміщення по іксу
            lost +=1#добавляєм одне до пропущених

class Bullet(GameSprite):#клас для пуль, клас спадкоємець
    def update(self):
        self.rect.y -=self.speed#пререміщеня пуль в гору
        if self.rect.y <0:#якщо пуля виходе за межі
            self.kill()#зникає

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed#вороги поступоп падають
        if self.rect.y > 700:#якщо вийшли за межі поля
            self.rect.y = 0 #переміщення на верх
            self.rect.x = randint(50, 600)#рандомне переміщення по іксу
           




player = Player('rocket.png', 310, 580,80, 100, 10)#змінна для головного гравця

enemys = sprite.Group()#група ворогів
for i in range(5):#щотчик
    monster = Enemy("ufo.png", randint(50, 600), -50, 80, 50, randint(1, 2))#падаючі монстри
    enemys.add(monster)#добавляєм їх

asterids = sprite.Group()#група ворогів
for i in range(5):#щотчик
    asteroid = Asteroid("asteroid.png", randint(50, 600), -50, 80, 50, randint(1, 2))#падаючі монстри
    asterids.add(asteroid)#добавляєм їх

bullets = sprite.Group()#група пуль
life = 5#життя
fps = 60
rel_time = False
game = True#активна
finish = False#завершена

mixer.init()
fire_snd = mixer.Sound('fire.ogg')#звук пострілу
killed = 0
num_fire = 0

while game :

    for e in event.get():# якщо кнопка е нажата
        if e.type == QUIT:#якщо кнопка 
            game = False#гра закінчена

        if e.type == KEYDOWN:#якщо кнопка вниз нажата
            if e.key == K_SPACE:#кнопка к нажата
                if num_fire <=5 and rel_time == False:
                    num_fire +=1
                    player.fire()#виліт пулі
                    fire_snd.play()#звук пострілу
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()


    if not finish:#якщо гра не закінчена


        window.blit(background, (0, 0))#заливка фону
        
        player.reset() 
        player.update()#запустити гравця
        
        enemys.draw(window)#намалювати вікно для ворога
        enemys.update()#запустити ворога
        
        asterids.draw(window)
        asterids.update()

        bullets.draw(window)#намалювати  вікно для пуль
        bullets.update()#запустити пулю

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('перезарядка', 1, (255, 0, 0))
                window.blit(reload,(250, 500))
            else:
                rel_time = False
                num_fire = 0



        collides = sprite.groupcollide(bullets, enemys, True, True )
        for col in collides:
            monster = Enemy("ufo.png", randint(50, 600), -50, 80, 50, randint(1, 2))
            enemys.add(monster)
            killed +=1
        if sprite.spritecollide(player, enemys, True):
            life -=1

       
        if sprite.spritecollide(player, asterids, True):
            life -=1



        score = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255 ))#надпись для пропущених
        window.blit(score,(10, 20))
        life1= font1.render(str(life), 1, (255, 255, 255))
        window.blit(life1, (600, 20))
        killed_txt = font1.render('збито: ' + str(killed), 1, (255, 255, 255))
        window.blit(killed_txt, (10, 45))
        
        if killed >= 20:
            finish = True
            win = font2.render('ти вбив всіх інопланетян!', 1, (0, 255, 0))
            win2 = font2.render('ти збив ' + str(killed) + 'HLO', 1, (0, 255, 0))
            window.blit(win, (100, 350))
            window.blit(win2, (125, 400))

        if life == 0:
            finish = True
            lose = font2.render('тебе грохнули', 1, (255, 0, 0))
            window.blit(lose, (125, 350))
        display.update()
    else:
        keys = key.get_pressed()
        if keys[K_z]:
            finish = False
            lost = 0
            killed = 0
            life = 5
            for b in bullets :
                b.kill()
            for m in enemys:
                m.kill()
            for a in asterids:
                a.kill()
            for i in range(5):#щотчик
                monster = Enemy("ufo.png", randint(50, 600), -50, 80, 50, randint(1, 2))#падаючі монстри
                enemys.add(monster)#добавляєм їх
            for i in range(5):#щотчик
                asteroid = Asteroid("asteroid.png", randint(50, 600), -50, 80, 50, randint(1, 2))#падаючі монстри
                asterids.add(asteroid)#добавляєм їх


    display.update()
    clock.tick(fps)



















