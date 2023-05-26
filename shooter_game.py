from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x, y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(image_file), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    #метод для управления игрока стрелками клавиатуры
    def update(self):
        #получение словаря состояния клаыишь
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < width - 85:
            self.rect.x += self.speed
    #метод для стрельбы пулями
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 17, self.rect.top, -15, 35, 25)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = -50
            lost += 1

#класс для nуль
class Bullet(GameSprite):
    #движение пули
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


# размерi оkна
width = 700
height = 500
# создание окна
window = display.set_mode((width, height))
display.set_caption('стрелялка инопланетян')


# нахвания файлов
img_back = 'galaxy.jpg'#фон игры
img_hero = 'rocket.png'#игрок
img_enemy1 = 'ufo.png' #vrag 1
img_enemy2 = 'asteroid.png' #vrag 2
img_bullet = 'bullet.png' #pulay

# открываем фон
background = transform.scale(image.load(img_back), (width, height))

# подключаем мцзыку
mixer.init()
mixer.music.load('space.ogg')#фон муз
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')#выстрел

# переменная окончания игры
finish = False 

#переменная завершения программы
game = True #завершение при нажатии кнопки закрыть окно
#переменная перезарядки
reload_bullets = False #если True происходит перезарядка

#счетчики
score = 0 #счетчик сбитых
lost = 0 #счетчик проаущеных
max_lost = 10 #максимальное колво пропущеных врагов
max_score = 17 #максимальный счет
life = 3#колво жизней
max_bullets = 7#максимум пулек
num_bullet = 0 #колво пуль


#шрифт
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font2.render('Эмммм, ну ок.', True, (255, 255, 255))
lose = font2.render('ХА ХА! ПОПУСК!!!!!!!!',True, (180, 0, 0))


#внутреигровые часы и ФПС
clock = time.Clock()
FPS = 60

#сщздание спрайтов
ship = Player(img_hero, 5, height - 100,10, 80, 100)

#создание группы монстров (метеоров или НЛО)
monsters = sprite.Group()
for i in range(7):#количество мобов
    monster = Enemy(img_enemy1, randint(0, width - 80), -40, randint(1, 2), 80, 50)
    monsters.add(monster)

#создание группы астероидов
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_enemy2, randint(0, width - 50), -40, randint(1, 3), 50, 50 )
    asteroids.add(asteroid)

bullets = sprite.Group()



while game:
    #обработка нажатия книoпи закрыть окно
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #проверка возможности выстрела
                if num_bullet < 7 and reload_bullets == False:    
                    fire_sound.play()
                    ship.fire()
                    num_bullet += 1
                if num_bullet >= 7 and reload_bullets == False:
                    last_time = timer()
                    reload_bullets = True
        
    if finish != True:
        window.blit(background, (0,0))

        text = font1.render('ПОПУЩЕНО: ' + str(score), True, (255,255,255))
        window.blit(text, (10, 20))

        text_lose = font1.render('пропущено: ' + str(lost), True, (255,255,255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if reload_bullets == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font1.render('ПЕРЕЗАРЯЖАЮСЬ', True, (150, 30, 0))
                window.blit(reload_text, (260, 460))
            else:
                num_bullet = 0
                reload_bullets = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        #столкновение пуль и врагов
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy1, randint(80, width - 80), -40, randint(1, 3), 80, 50)
            monsters.add(monster)
        
        #проигрыш, проверка столкновения тгрока с врагом    
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (75, 200))
        
        #выигрыш, набрали брльше max_score очкоыв
        if score >= max_score:
            finish = True
            window.blit(win, (140, 200))

        
        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150,150,0)
        elif life == 1:
            life_color = (150,0,0)

        life_text = font2.render(str(life), True, life_color)
        window.blit(life_text, (650,10))
    else:
        finish = False
        score = 0
        lost = 0
        num_bullet = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        

        time.delay(3000)

        for i in range(7):#количество мобов
            monster = Enemy(img_enemy1, randint(80, width - 80), -40, randint(1, 3), 80, 50)
            monsters.add(monster)
        
        for i in range(3):
            asteroid = Enemy(img_enemy2, randint(0, width - 50), -40, randint(1, 3), 50, 50 )
            asteroids.add(asteroid)
        

    display.update()
    clock.tick(FPS)


    















