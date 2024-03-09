import os
import random
import pygame
import sys
from mainGame import EnemyTypes as tyEn

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 120, 90
BUTTON_WIDTH, BUTTON_HEIGHT = 500, 200
BULLET_WIDTH, BULLET_HEIGHT = 30, 20
MY_ֹֹOBJ = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'soldier.png')), (OBJ_WIDTH, OBJ_HEIGHT))
TERROR_1 = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'terrorist1.png')), (OBJ_WIDTH - 20, OBJ_HEIGHT - 20))
TERROR_2 = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'terrorist2.png')), (OBJ_WIDTH - 20, OBJ_HEIGHT - 20))
TERROR_3 = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'terorist3.png')), (OBJ_WIDTH - 20, OBJ_HEIGHT - 20))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'nuclear-explosion.png')), (OBJ_WIDTH - 20, OBJ_HEIGHT - 20))
WARZONE = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'warzone.png')), (WIDTH, HEIGHT))
END_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'END_BACKGROUND.png')), (WIDTH, HEIGHT))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'gun_bullet1.png')), (BULLET_WIDTH, BULLET_HEIGHT))
BOSS = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'boss.png')), (BULLET_WIDTH + 105, BULLET_HEIGHT + 105))
FIRE_WORK = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'fireworks.png')), (OBJ_WIDTH + 30, OBJ_HEIGHT + 30))
# BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level7_images', 'jungle_button.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()


class Level_8:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level8_images', 'alla.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level6_images', 'shoot.ogg'))
        self.WARZONE_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level8_images', 'warzone_sound.ogg'))
        self.BOSS_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level8_images', 'boss_sound.ogg'))
        self.FIRE_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level8_images', 'fireworks.mp3'))
        self.play_war_sound()
        self.VEL = 8
        self.BULLET_VEL = 10
        self.MAX_BULLETS = 10
        self.my_health = 10
        self.START_BULLET_DEV = 25
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.MAX_ENEMY = 20
        self.bullets = []
        self.boss = False
        self.explo_size = [OBJ_WIDTH, OBJ_HEIGHT, OBJ_WIDTH, OBJ_HEIGHT]

    def play_war_sound(self):
        self.WARZONE_SOUND.set_volume(0.2)
        self.WARZONE_SOUND.play(-1)

    def game_over_screen(self, WIN, WINNER_FONT, text):
        # Wait for a mouse click
        self.WARZONE_SOUND.stop()
        if text == "YOU WON!!!":
            self.FIRE_SOUND.play(-1)
        while True:
            WIN.blit(END_BACKGROUND, (0, 0))
            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 200))
            # WIN.blit(BUTTON, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2))
            # Draw a button
            if text == "YOU WON!!!":
                if self.explo_size[0] > 200 or self.explo_size[1] > 170:
                    self.explo_size[0] = OBJ_WIDTH
                    self.explo_size[1] = OBJ_HEIGHT
                if self.explo_size[2] > 200 or self.explo_size[3] > 170:
                    self.explo_size[2] = OBJ_WIDTH
                    self.explo_size[3] = OBJ_HEIGHT
                scaled_fire = pygame.transform.scale(FIRE_WORK, (self.explo_size[0], self.explo_size[1]))
                scaled_fire2 = pygame.transform.scale(FIRE_WORK, (self.explo_size[2], self.explo_size[3]))
                WIN.blit(scaled_fire, (WIDTH // 2 - BUTTON_WIDTH // 2 - 80, HEIGHT // 2 - BUTTON_HEIGHT // 2 - 50))
                WIN.blit(scaled_fire2, (WIDTH // 2 - BUTTON_WIDTH // 2 - 80, HEIGHT // 2 - BUTTON_HEIGHT // 2))
                self.explo_size[0] += 1
                self.explo_size[1] += 1
                self.explo_size[2] += 0.8
                self.explo_size[3] += 0.8
            rendered_text = pygame.font.SysFont('Comic Sans MS', 50).render("RESTART", True, WHITE)
            WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 135, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 65))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (WIDTH // 2 - BUTTON_WIDTH // 2) <= mouse_x <= (WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH) and (HEIGHT // 2 - BUTTON_HEIGHT // 2)\
                            <= mouse_y <= (HEIGHT // 2 - BUTTON_HEIGHT // 2 + BUTTON_HEIGHT):
                        # Restart the game
                        self.FIRE_SOUND.stop()
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN, HEALTH_FONT, my_obj, TOTAL_CRUSH , rectangels):
        WIN.blit(WARZONE, (0, 0))
        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))
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
                     WIN.blit(TERROR_1, (enemy.getX(), enemy.getY()))
                elif isinstance(enemy, tyEn.EnemyStop):
                    WIN.blit(TERROR_2, (enemy.getX(), enemy.getY()))
                else:
                    if self.boss:
                        WIN.blit(BOSS, (enemy.getX(), enemy.getY()))
                    else:
                        WIN.blit(TERROR_3, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            WIN.blit(BULLET, (bullet.x, bullet.y))
        pygame.display.update()


    def get_enemy_details(self):
        # type = 0 regular, type = 1 zigzag, type 2 = Sprinter, type 3 = stopEnemy
        # velocity_x, velocity_y, life, obj_height, obj_width, type

        if self.boss:
            velocity_x, velocity_y, life, obj_height, obj_width, type = self.create_boss_details()
            return velocity_x, velocity_y, life, obj_height, obj_width, type
        return random.randint(2, 8), random.randint(-5, 5), random.randint(1, 3), self.OBJ_HEIGHT, self.OBJ_WIDTH, random.randint(0, 3)

    def create_boss_details(self):
        return 1, random.randint(1, 3), 60, self.OBJ_HEIGHT + 50, self.OBJ_WIDTH + 50, 0

    def next_enemy(self):
        if self.boss:
            return 5000
        return random.randint(500, 3000)

    def play_dead_sound(self, enemy):
        self.BULLET_HIT_SOUND.play()

