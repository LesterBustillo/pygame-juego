import pygame
import random

#Definicion de colores
WIDTH = 900
HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()# sonido
screen = pygame.display.set_mode((WIDTH, HEIGHT))#Creaccion de la Pantalla de Juego
pygame.display.set_caption("Galaxy War")#Titulo del Juego
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):#creacion de barra de vida
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)



class Player(pygame.sprite.Sprite):#clase jugador crea la nave
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("grafic/player3.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0 #velocidad de la nave
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()#control de movimiento
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:#Evita que la nave(jugaor se salga del marco)
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):#creacion de la bala
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()

class Meteor(pygame.sprite.Sprite): #clase que carga los meteoros
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40 :
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):#clase de la bala
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("grafic/laser3.png")	
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0: #elimina las balas de la lista
			self.kill()		

class Explosion(pygame.sprite.Sprite):#crea explosion
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 

	def update(self):
		now = pygame.time.get_ticks()
		if now -self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center		

def show_go_screen():
	screen.blit(background, [0,0])
	draw_text(screen, "Galaxy War", 65, WIDTH // 2, HEIGHT // 4 )
	draw_text(screen, "Instucciones", 27, WIDTH // 2, HEIGHT// 2 )
	draw_text(screen, "Presione para continuar", 20, WIDTH // 2, HEIGHT  * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


meteor_images = [] #crea la lista de meteoros
meteor_list = ["grafic/meteorGrey_big1.png", "grafic/meteorGrey_big2.png", "grafic/meteorGrey_big3.png", "grafic/meteorGrey_big4.png",
				"grafic/meteorGrey_med1.png", "grafic/meteorGrey_med2.png", "grafic/meteorGrey_small1.png", "grafic/meteorGrey_small2.png",
				"grafic/meteorGrey_tiny1.png", "grafic/meteorGrey_tiny2.png"]	
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())


#Explocion
explosion_anim = []
for i in range(9):
	file = "grafic/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

#Fondo de Pantalla
background = pygame.image.load("grafic/background8.jpg").convert()

#Sonidos
laser_sound = pygame.mixer.Sound("grafic/laser5.ogg")
explosion_sound = pygame.mixer.Sound("grafic/explosion.wav")
pygame.mixer.music.load("grafic/music.ogg")
pygame.mixer.music.set_volume(0.2)

pygame.mixer.music.play(loops=-1)

#Fin del Juego
game_over = True
running = True
while running:
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		
		player = Player()
		all_sprites.add(player)
		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)
			
			score = 0


	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
   
 
	all_sprites.update()

	#Colisiones (Meteoro-lase)
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 10 #marcador
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
 
# colisiones (jugador - meteoro)
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 10 # vidas
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True

	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	#vidas
	draw_shield_bar(screen, 5, 5, player.shield)
	
	pygame.display.flip()  

pygame.quit()
