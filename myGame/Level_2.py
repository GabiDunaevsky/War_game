import os
import random
import sys
import pygame

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 55, 40
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BULLET_WIDTH, BULLET_HEIGHT = 15, 15
ANGEL = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'angel.png')), (OBJ_WIDTH, OBJ_HEIGHT))
DEVIL = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'demon.png')), (OBJ_WIDTH, OBJ_HEIGHT))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'halo.png')), (OBJ_WIDTH, OBJ_HEIGHT))
HELL = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'Hell.jpg')), (WIDTH, HEIGHT))
FIRE = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'explosion-1.png')), (OBJ_WIDTH, OBJ_HEIGHT))
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'red-button.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
DROP = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'drop1.png')), (20, 40))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level2_images', 'ball-light.png')), (BULLET_WIDTH, BULLET_HEIGHT))
EXPLOSION_NOISE = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level2_images', 'explosion-noise.ogg'))
DROP_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level4_images', 'drope_sound.ogg'))
clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()

class Level_2:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level2_images', 'dead-sound1.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level2_images', 'halleluja.mp3'))
        self.VEL = 6
        self.BULLET_VEL = 5
        self.MAX_BULLETS = 3
        self.my_health = 3
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.MAX_ENEMY = 15
        self.START_BULLET_DEV = 2
        self.fire_loc = []
        self.fire_size = []
        self.bullets = []

    def game_over_screen(self, WIN, WINNER_FONT, text):
        self.BULLET_HIT_SOUND.stop()
        dropCallTimer = pygame.time.get_ticks()
        dropRec = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2 + BUTTON_HEIGHT - 5, 40, 20)
        dropRec1 = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2 + BUTTON_HEIGHT - 5, 40, 20)
        dropLst = [dropRec, dropRec1]
        i = 1
        # Wait for a mouse click
        while True:
            WIN.blit(HELL, (0, 0))
            WIN.blit(DROP, (dropRec.x, dropRec.y))
            curr_time = pygame.time.get_ticks()
            if curr_time - dropCallTimer > 1300:
                i = 2
            for drop in range(i):
                WIN.blit(DROP, (dropLst[drop].x, dropLst[drop].y))
                if dropLst[drop].y + 1 > HEIGHT:
                    DROP_SOUND.play()
                    dropLst[drop].y = HEIGHT // 2 - BUTTON_HEIGHT // 2 + BUTTON_HEIGHT - 5
                else:
                    dropLst[drop].y += 3

            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 150))
            WIN.blit(BUTTON, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2))
            # Draw a button
            if text == "YOU LOST!!!":
                rendered_text = pygame.font.SysFont('Comic Sans MS', 40).render("RESTART", True, (0, 0, 0))
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 60, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 10))
            else:
                rendered_text = pygame.font.SysFont('Comic Sans MS', 36).render("NEXT LEVEL", True, (0, 0, 0))
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 40, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 15))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH//2 - BUTTON_WIDTH//2 <= mouse_x <= WIDTH//2 - BUTTON_WIDTH//2 + BUTTON_WIDTH and HEIGHT//2 - BUTTON_HEIGHT//2\
                            <= mouse_y <= HEIGHT//2 - BUTTON_HEIGHT//2 + BUTTON_HEIGHT:
                        # Restart the game
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN,HEALTH_FONT, my_obj, TOTAL_CRUSH , rectangles):
        global my_health, last_rect_creation_time
        WIN.blit(HELL, (0, 0))

        current_time = pygame.time.get_ticks()
        if len(self.fire_size) < 4:
            if current_time - last_rect_creation_time > 1000:
                x = random.uniform(0 + OBJ_WIDTH, WIDTH - OBJ_WIDTH)
                y = random.uniform(0 + OBJ_HEIGHT, HEIGHT - OBJ_HEIGHT)
                self.fire_loc.append((x, y))
                self.fire_size.append([OBJ_WIDTH, OBJ_HEIGHT])
                EXPLOSION_NOISE.play()
                last_rect_creation_time = current_time
        else:
            if current_time - last_rect_creation_time > 1000:
                del self.fire_loc[0]
                del self.fire_size[0]
                x = random.uniform(0 + OBJ_WIDTH, WIDTH - OBJ_WIDTH)
                y = random.uniform(0 + OBJ_HEIGHT, HEIGHT - OBJ_HEIGHT)
                self.fire_loc.append((x, y))
                self.fire_size.append([OBJ_WIDTH, OBJ_HEIGHT])
                EXPLOSION_NOISE.play()
                last_rect_creation_time = current_time
        for i in range(len(self.fire_loc)):
            scaled_fire = pygame.transform.scale(FIRE, (self.fire_size[i][0], self.fire_size[i][1]))
            WIN.blit(scaled_fire, self.fire_loc[i])
            self.fire_size[i][0] += 0.2
            self.fire_size[i][1] += 0.2

        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))

        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(ANGEL, (my_obj.x, my_obj.y))
        for enemy in rectangles:
            if enemy.getX() >= WIDTH:
                rectangles.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangles.remove(enemy)
            else:
                WIN.blit(DEVIL, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            WIN.blit(BULLET, (bullet.x, bullet.y))
        pygame.display.update()

    def get_enemy_details(self):
        # velocity_x, velocity_y, life, obj_height, obj_width
        return random.randint(2, 6), random.randint(-3, 3), 1, self.OBJ_HEIGHT, self.OBJ_WIDTH, 0

    def next_enemy(self):
        return 3000
    def play_dead_sound(self,enemy):
        self.BULLET_HIT_SOUND.play()