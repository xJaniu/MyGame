import os
import pygame
import pygame.examples.moveit
from pygame import mixer

import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60
tile_size = 60
game_over = 0
shoot = False

screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption('Prosta gra platformowa...')

# define fonts
font = pygame.font.SysFont('Courier Regular', 30)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
skyblue = (70, 200, 255)
black = (0,0,0)

#load sounds
theme_fx = pygame.mixer.Sound('theme.mp3')
theme_fx.set_volume(0.1)
pew_fx = pygame.mixer.Sound('pew.mp3')
pew_fx.set_volume(0.1)

class Energy_Bar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw_bar(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, blue, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, skyblue, (self.x, self.y, 150 * ratio, 20))

class Hp_Bar(Energy_Bar):

    def draw_bar(self, hp):
        self.hp = hp

        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 104, 8))
        pygame.draw.rect(screen, green, (self.x, self.y, 104 * ratio, 8))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        screen.blit(self.image, self.rect)
        # mouse pos
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

        # # self.dead_image = gm.DEAD_BODIES[0]
        # self.dead_image = pygame.transform.scale(gm.DEAD_BODIES[0], (80,80))
        # self.image = gm.PLAYER_WALK_LIST_D[0]
        # self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.energy = 0
        # self._count = 0
        # self.turn = 'S'
        # self.width = self.image.get_width()
        # self.height = self.image.get_height()

    def update(self, game_over):

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        movement_x = 0
        movement_y = 0
        if game_over == 0:
            if self.energy < 6000:
                # pygame.time.wait(1000)
                self.energy += 10

            screen.blit(self.image, self.rect)
            key = pygame.key.get_pressed()

            if key[pygame.K_LEFT]:
                movement_x -= 5
                if key[pygame.K_SPACE] and self.energy > 200:
                    movement_x -= 10
                    self.energy -= 50
                self._move(gm.PLAYER_WALK_LIST_L)
                self.turn = "w"

            if key[pygame.K_RIGHT]:
                movement_x += 5
                if key[pygame.K_SPACE] and self.energy > 200:
                    movement_x += 10
                    self.energy -= 50
                self._move(gm.PLAYER_WALK_LIST_R)
                self.turn = "e"

            if key[pygame.K_UP]:
                movement_y -= 5
                if key[pygame.K_SPACE] and self.energy > 200:
                    movement_y -= 10
                    self.energy -= 50
                self._move(gm.PLAYER_WALK_LIST_U)
                self.turn = "n"

            if key[pygame.K_DOWN]:
                movement_y += 5
                if key[pygame.K_SPACE] and self.energy > 200:
                    movement_y += 10
                    self.energy -= 50
                self._move(gm.PLAYER_WALK_LIST_D)
                self.turn = "s"

            if key[pygame.K_UP] == False and key[pygame.K_DOWN] == False and key[pygame.K_RIGHT] == False and key[
                pygame.K_LEFT] == False:
                if self.turn == "n":
                    self.image = gm.PLAYER_WALK_LIST_U[0]
                if self.turn == "s":
                    self.image = gm.PLAYER_WALK_LIST_D[0]
                if self.turn == "w":
                    self.image = gm.PLAYER_WALK_LIST_L[0]
                if self.turn == "e":
                    self.image = gm.PLAYER_WALK_LIST_R[0]

            # collision with terrain
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + movement_x, self.rect.y, self.width, self.height):
                    movement_x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + movement_y, self.width, self.height):
                    movement_y = 0
            # collision with enemies
            if pygame.sprite.spritecollide(self, smok_group, False):
                self.hp = 0






            self.rect.x += movement_x
            self.rect.y += movement_y

            # colission with water
            if self.rect.bottom > gm.SIZESCREEN[1] - 42:
                self.rect.bottom = gm.SIZESCREEN[1] - 42
            if self.rect.top < 7:
                self.rect.top = 7
            if self.rect.left < 21:
                self.rect.left = 21
            if self.rect.right > gm.SIZESCREEN[0] - 28:
                self.rect.right = gm.SIZESCREEN[0] - 28
            # animation counter
            if self._count < 21:
                self._count += 1
            else:
                self._count = 0
        elif game_over == -1:
            self.image = self.dead_image

        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        return game_over

    def _move(self, image_list):
        if self._count < 7:
            self.image = image_list[0]
        elif self._count < 14:
            self.image = image_list[1]
        elif self._count < 21:
            self.image = image_list[2]

    def reset(self, x, y):
        self.dead_image = pygame.transform.scale(gm.DEAD_BODIES[0], (80, 80))
        self.image = gm.PLAYER_WALK_LIST_D[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.energy = 0
        self._count = 0
        self.turn = 'S'
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.shoot_cooldown = 0
        self.hp = 10
        self.dmg_multiplier = 1
        self.level = 1

    def shoot(self):
        if self.shoot_cooldown == 0 and self.energy > 200:
            self.shoot_cooldown = 10
            self.energy -= 200
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.turn)
            bullet_group.add(bullet)
            pew_fx.play()


class Senzu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.transform.scale(gm.TERRAIN_LIST[3], (35, 35))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class World():
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(gm.TERRAIN_LIST[0], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(gm.TERRAIN_LIST[1], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(gm.TERRAIN_LIST[2], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    smok = Enemy(col_count * tile_size, row_count * tile_size, 500)
                    smok_group.add(smok)
                if tile == 5:
                    senzu = Senzu(col_count * tile_size, row_count * tile_size)
                    senzu_group.add(senzu)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255,255,255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gm.DRAGON_D[0], (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movespeed = 2
        self.health = health
        self._count = 0
        self.turn = 's'
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.cooldown = 0

    def spell(self):
        if self.cooldown == 0:
            self.cooldown = 50
            spell = Spell(self.rect.centerx, self.rect.centery, self.turn)
            spell_group.add(spell)


    def _move(self, image_list):
        if self._count < 6:
            self.image = pygame.transform.scale(image_list[0], (120, 120))
        elif self._count < 12:
            self.image = pygame.transform.scale(image_list[1], (120, 120))
        elif self._count < 18:
            self.image = pygame.transform.scale(image_list[2], (120, 120))

        if self._count == 18:
            self._count = 0

    def update(self, player_x, player_y, game_over):

        if self.cooldown > 0:
            self.cooldown -= 1

        # for tile in world.tile_list:
        #     if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
        #         self.rect.x -= 5
        #     if tile[1].colliderect(self.rect.x, self.rect.y + 20, self.width, self.height):
        #         self.rect.y += 5
        #     if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
        #         self.rect.x += 5
        #     if tile[1].colliderect(self.rect.x, self.rect.top, self.width, self.height):
        #         self.rect.y -= 5
        # for tile in world.tile_list:
        #     if tile[1].colliderect(self.rect.x + movement_x, self.rect.y, self.width, self.height):
        #         movement_x = 0
        #     if tile[1].colliderect(self.rect.x, self.rect.y + movement_y, self.width, self.height):
        #         movement_y = 0

        # print(self.health)
        if self.health <= 0:
            self.kill()

        if game_over == -1:
            self.kill()

        if self.rect.x > player_x:
            self.turn = 'w'
            self._move(gm.DRAGON_L)
            self.rect.x -= self.movespeed
        if self.rect.x < player_x:
            self.turn = 'e'
            self._move(gm.DRAGON_R)
            self.rect.x += self.movespeed
        if self.rect.y > player_y:
            self.turn = 'n'
            self._move(gm.DRAGON_G)
            self.rect.y -= self.movespeed
        if self.rect.y < player_y:
            self.turn = 's'
            self._move(gm.DRAGON_D)
            self.rect.y += self.movespeed

        if self._count < 21:
            self._count += 1


class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = gm.BULLET[1]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        #movingbullets
        if self.direction == "s":
            self.rect.y += self.speed
        if self.direction == "n":
            self.rect.y -= self.speed
        if self.direction == "e":
            self.rect.x += self.speed
        if self.direction == "w":
            self.rect.x -= self.speed

        #deletingbulletoutofscreen
        if self.rect.right < 0 or self.rect.left > gm.SIZESCREEN[0]:
            self.kill()
        if self.rect.top < 0 or self.rect.bottom > gm.SIZESCREEN[1]:
            self.kill()

        #checkcolissionwithenemy
        if player.hp > 0:
            if pygame.sprite.spritecollide(player, spell_group, False):
                if game_over == 0:
                    self.kill()
                    player.hp -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = gm.BULLET[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        #movingbullets
        if self.direction == "s":
            self.rect.y += self.speed
        if self.direction == "n":
            self.rect.y -= self.speed
        if self.direction == "e":
            self.rect.x += self.speed
        if self.direction == "w":
            self.rect.x -= self.speed

        #deletingbulletoutofscreen
        if self.rect.right < 0 or self.rect.left > gm.SIZESCREEN[0]:
            self.kill()
        if self.rect.top < 0 or self.rect.bottom > gm.SIZESCREEN[1]:
            self.kill()

        #checkcolissionwithenemy
        for smok in smok_group:
            if smok.health > 0:
                if pygame.sprite.spritecollide(smok, bullet_group, False):
                    if game_over == 0:
                        self.kill()
                        smok.health -= player.dmg_multiplier * 10


spell_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
senzu_group = pygame.sprite.Group()

world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

world_data2 = [
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
]



player = Player(600, 450)
smok_group = pygame.sprite.Group()

world = World(world_data)
restart_button = Button(gm.SIZESCREEN[0] // 2 - 50, 10, gm.BUTTONS[0])

player_energy_bar = Energy_Bar(1100, 14, player.energy, 6000)
player_hp_bar = Hp_Bar(770, 8, player.hp, 10)


window_open = True
theme_fx.play()
while window_open:

    clock.tick(fps)
    screen.blit(gm.BACKGROUND, (0, 0))

    world.draw()
    player_energy_bar.draw_bar(player.energy)
    player_hp_bar.draw_bar(player.hp)



    spell_group.update()
    spell_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)
    senzu_group.draw(screen)

    game_over = player.update(game_over)

    if game_over == 0: #when alive
        smok_group.update(player.rect.x, player.rect.y, game_over)

        if pygame.sprite.spritecollide(player, senzu_group, True):
            player.dmg_multiplier += 1


        if shoot:
            player.shoot()


    smok_group.draw(screen)
    for smok in smok_group:
        smok.spell()

        boss_hp_bar = Hp_Bar(smok.rect.x + 5, smok.rect.y - 15, smok.health, 500)
        boss_hp_bar.draw_bar(smok.health)
        draw_text(f'{smok.health}', font, black, smok.rect.x + 40, smok.rect.y - 35)

    draw_text(f'Poziom: {player.level}', font, green, 20, 10)
    draw_text(f'DMG x {player.dmg_multiplier}', font, green, 900, 15)
    draw_text(f'HP: {player.hp} / 10', font, green, 770, 20)
    draw_text(f'ENERGIA:', font, skyblue, 1000, 15)

    if smok.health <= 0 and player.level == 1:
        smok.health = 0
        world = World(world_data2)
        world.draw()
        player.level = 2
        if restart_button.draw():
            smok_group.update(player.rect.x, player.rect.y, game_over)
            player.reset(600, 450)
            game_over = 0
            world = World(world_data)

    if smok.health <= 0 and player.level == 2:
        smok.health = 0
        draw_text(f'WYGRALES!', font, green, 600, 430)
        if restart_button.draw():
            smok_group.update(player.rect.x, player.rect.y, game_over)
            player.reset(600, 450)
            game_over = 0
            world = World(world_data)


    if player.hp == 0:
        game_over = -1

    if game_over == -1:
        draw_text(f'PRZEGRALES!', font, green, 600, 430)
        if restart_button.draw():
            smok_group.update(player.rect.x, player.rect.y, game_over)
            player.reset(600, 450)
            game_over = 0
            world = World(world_data)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                window_open = False
        elif event.type == pygame.QUIT:
            window_open = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                shoot = False

    pygame.display.update()
pygame.quit()
