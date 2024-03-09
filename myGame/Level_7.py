import os
import random
import pygame
import sys
from mainGame import EnemyTypes as tyEn

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 80, 60
BUTTON_WIDTH, BUTTON_HEIGHT = 500, 200
BULLET_WIDTH, BULLET_HEIGHT = 30, 20
MY_ֹֹOBJ = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'monkey.png')), (OBJ_WIDTH, OBJ_HEIGHT)), -20)
SNAKE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'snake.png')), (OBJ_WIDTH, OBJ_HEIGHT)), -40)
LEOPARD = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'leopard.png')), (OBJ_WIDTH + 30, OBJ_HEIGHT + 50))
TRANTULA = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'Tarantula.png')), (OBJ_WIDTH, OBJ_HEIGHT)), 90)
CROCODILE = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'Crocodile.png')), (OBJ_WIDTH + 30, OBJ_HEIGHT + 50))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'grave.png')), (OBJ_WIDTH, OBJ_HEIGHT + 50))
JUNGLE = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'jungle.png')), (WIDTH, HEIGHT))
BULLET = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'bannana.png')), (BULLET_WIDTH + 10, BULLET_HEIGHT + 20)), -90)
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'jungle_button.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()


class Level_7:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level7_images', 'crocodile_sound.ogg'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level7_images', 'monkey_sound.ogg'))
        self.LIGHTNING_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level7_images', 'lightning.ogg'))
        self.BULLET_HIT_SOUND_SNAKE = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level7_images', 'snake_sound.mp3'))
        self.BULLET_HIT_SOUND_LEO = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level7_images', 'leopard_sound.ogg'))
        self.BULLET_HIT_SOUND_SPIDER = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level7_images', 'spider_sound.ogg'))
        self.RAIN_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level7_images', 'rain.mp3'))
        self.LIGHTNING_SOUND.set_volume(0.5)
        self.play_rain_sound()
        self.VEL = 8
        self.BULLET_VEL = 10
        self.MAX_BULLETS = 8
        self.my_health = 8
        self.START_BULLET_DEV = 25
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.MAX_ENEMY = 20
        self.rainDrop = []
        self.bullets = []
        self.rotation = 0

    def play_rain_sound(self):
        self.RAIN_SOUND.set_volume(0.3)
        self.RAIN_SOUND.play(-1)

    def game_over_screen(self, WIN, WINNER_FONT, text):
        # Wait for a mouse click
        money = []
        dir = 0 ## 0 = up, 1 = down
        while True:
            WIN.blit(JUNGLE, (0, 0))
            if (len(self.rainDrop) < 500):
                self.rainDrop.append([random.uniform(0, WIDTH), random.uniform(0, 1)])
            for drop in self.rainDrop:
                drop[1] += 4
                if drop[1] > HEIGHT:
                    drop[1] = random.uniform(0, HEIGHT // 5)
                    drop[0] = random.uniform(0, WIDTH)
                pygame.draw.rect(WIN, (128, 128, 128), pygame.Rect(drop[0], drop[1], 5, 10))
            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 200))
            WIN.blit(BUTTON, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2))
            # Draw a button
            r = random.randint(1, 400)
            if (r == 98):
                self.LIGHTNING_SOUND.play()
                WIN.fill(WHITE)
            if text == "YOU LOST!!!":
                rendered_text = pygame.font.SysFont('Comic Sans MS', 50).render("RESTART", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 135, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 65))
            else:
                rendered_text = pygame.font.SysFont('Comic Sans MS', 46).render("NEXT LEVEL", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 120, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 70))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (WIDTH // 2 - BUTTON_WIDTH // 2) <= mouse_x <= (WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH) and (HEIGHT // 2 - BUTTON_HEIGHT // 2)\
                            <= mouse_y <= (HEIGHT // 2 - BUTTON_HEIGHT // 2 + BUTTON_HEIGHT):
                        self.RAIN_SOUND.stop()
                        # Restart the game
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN, HEALTH_FONT, my_obj, TOTAL_CRUSH , rectangels):
        WIN.blit(JUNGLE, (0, 0))
        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))
        if(len(self.rainDrop) < 500):
            self.rainDrop.append([random.uniform(0, WIDTH), random.uniform(0, 1)])
        for drop in self.rainDrop:
            drop[1] += 1.8
            if drop[1] > HEIGHT:
                drop[1] = random.uniform(0, HEIGHT//5)
                drop[0] = random.uniform(0, WIDTH)
            pygame.draw.rect(WIN, (128, 128, 128), pygame.Rect(drop[0], drop[1], 5, 10))

        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(MY_ֹֹOBJ, (my_obj.x, my_obj.y))

        for enemy in rectangels:
            if enemy.getX() >= WIDTH:
                rectangels.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangels.remove(enemy)
            else:
                if isinstance(enemy, tyEn.EnemyZigzag):
                     WIN.blit(SNAKE, (enemy.getX(), enemy.getY()))
                elif isinstance(enemy, tyEn.EnemySprinter):
                    WIN.blit(LEOPARD, (enemy.getX(), enemy.getY()))
                elif isinstance(enemy, tyEn.EnemyStop):
                    WIN.blit(TRANTULA, (enemy.getX(), enemy.getY()))
                else:
                    WIN.blit(CROCODILE, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            rotated_ban = pygame.transform.rotate(BULLET, (self.rotation % 360))
            WIN.blit(rotated_ban, (bullet.x, bullet.y))
            if (self.rotation + 5) == 360:
                self.rotation = 0
            else:
                self.rotation += 10
        r = random.randint(1, 400)
        if (r == 98):
            self.LIGHTNING_SOUND.play()
            WIN.fill(WHITE)
        pygame.display.update()


    def get_enemy_details(self):
        # type = 0 regular, type = 1 zigzag, type 2 = Sprinter, type 3 = stopEnemy
        # velocity_x, velocity_y, life, obj_height, obj_width, type
        return random.randint(2, 8), random.randint(-5, 5), random.randint(1, 3), self.OBJ_HEIGHT, self.OBJ_WIDTH, random.randint(0, 3)

    def next_enemy(self):
        return random.randint(1000, 2000)
    def play_dead_sound(self,enemy):
        if isinstance(enemy, tyEn.EnemyZigzag):
            self.BULLET_HIT_SOUND_SNAKE.play()
        elif isinstance(enemy, tyEn.EnemySprinter):
            self.BULLET_HIT_SOUND_LEO.play()
        elif isinstance(enemy, tyEn.EnemyStop):
            self.BULLET_HIT_SOUND_SPIDER.play()
        else:
            self.BULLET_HIT_SOUND.play()

