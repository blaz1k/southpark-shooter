
from time import time as timer
from random import *

from pygame import *
font.init()
font2= font.SysFont("Arial", 36)
mixer.init()
main_win = display.set_mode((700,500))
display.set_caption('омерика настаящая')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, w, h):
        super().__init__()
        self.image= transform.scale(image.load(player_image), (w, h))
        self.speed= speed
        self.rect= self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed= key.get_pressed()
        if keys_pressed[K_d] and self.rect.x<620:
            self.rect.x+= self.speed
        if keys_pressed[K_a] and self.rect.x>0:
            self.rect.x-= self.speed
    def fire(self):
        firesound = mixer.Sound("fire.ogg")
        firesound.set_volume(1)
        firesound.play()
        bullet= bull("bullet.png", self.rect.x, self.rect.y, 5, 16, 40)
        bullet.add(bullets)
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -40
            self.rect.x = randint(80,700-80)
            global lost
            lost += 1
class block(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -40
            self.rect.x = randint(80,700-80)
            

class bull(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()
clock= time.Clock()
FPS= 60
speed= 10
background= transform.scale(image.load('southpark.jpg'),(700,500))
player= Player("KennyMcCormick.png", 0, 400, 10, 100, 100)
mixer.music.load("fon.ogg")
mixer.music.set_volume(0.25)
die = mixer.Sound('diesound2.ogg')
die.set_volume(0.5)
mixer.music.play()

bullets= sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
score= 0

for i in range(5):
    monster = Enemy("tolken.png", randint(0, 500), -100 , randint(1,5), 75, 75)
    monsters.add(monster)
for i in range(2):
    asteroid = block("cartman.png", randint(0, 500), -100 , randint(1,3), 75, 75)
    asteroids.add(asteroid)
num_fire = 0
rel_time = False
lost = 0
lifes = 3
last_time = timer()
finish= True
game = True
while game!= False:
    for e in event.get():
        if e.type == QUIT:
            game= False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <10 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish == True:
        main_win.blit(background, (0, 0))
        bullets.update()
        monsters.draw(main_win)
        monsters.update()
        asteroids.draw(main_win)
        asteroids.update()
        bullets.update()
        asteroids.update()
        bullets.draw(main_win)
        player.reset()
        player.update()
        collides= sprite.groupcollide(monsters, bullets, True, True)
        for hit in collides:
            monster = Enemy("tolken.png", randint(0, 500), -40, randint(1,5), 75, 75) 
            monsters.add(monster)
            score += 1
        if score >=10:
                #TODO  score_text= font2.render("Счет:" + str(score), 1, (255,255,255))
                # ? лол
            win = font2.render("ура победа", 1, (20,255,200))
            main_win.blit(win, (200,200))
            finish= False
                
        if sprite.spritecollide(player, monsters, True):
            lifes-=1
            monster = Enemy("tolken.png", randint(0, 500), -40, randint(1,5), 75, 75) 
            monsters.add(monster)
        
        if sprite.spritecollide(player, asteroids, True):
            lifes-=1
            asteroid = block("cartman.png", randint(0, 500), -100 , randint(1,3), 75, 75)
            asteroids.add(asteroid)

        
        text_lose= font2.render("Пропущено:" + str(lost), 1, (255,255,255))
        main_win.blit(text_lose, (0,0))
        if lost >= 3 or lifes == 0:
            lose = font2.render("проигрыш, твой счет " + str(score)+" из 10", 1, (255, 0, 0))
            main_win.blit(lose, (200,200))
            finish= False
            die.play()
        lifes_text= font2.render("Жизни:" + str(lifes), 1, (255,255,255))
        main_win.blit(lifes_text, (0,72))
        score_text= font2.render("Счет:" + str(score), 1, (255,255,255))
        main_win.blit(score_text, (0,36))
        if rel_time == True:
            now_time = timer()
            if  now_time - last_time < 1:
                rel_text= font2.render("перезарядка", 1, (255,5,75))
                main_win.blit(rel_text, (300, 300))

            else:
                rel_time = False
                num_fire = 0
            
    
    keys_pressed= key.get_pressed()
    if keys_pressed[K_r]:
        lost = 0
        lifes = 3
        score = 0
        finish = True
        for i in monsters:
            i.rect.x = randint(0, 500)
            i.rect.y = -100
        for i in bullets:
            i.kill()
        for i in asteroids:
            i.rect.x = randint(0, 500)
            i.rect.y = -100
        player.rect.y = 400
        player.rect.x = 300
    
    display.update()
    clock.tick(FPS)
    
