import os
import random
import sys
import pygame

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 70, 50
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BULLET_WIDTH, BULLET_HEIGHT = 25, 25


SANTA_CAR = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'santa-caracter.png')), (OBJ_WIDTH, OBJ_HEIGHT))
SNOW_MAN = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'snow-man.png')), (OBJ_WIDTH, OBJ_HEIGHT))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'fireworks.png')), (OBJ_WIDTH + 30, OBJ_HEIGHT + 30))
SANTA = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'santa.png')), (WIDTH, HEIGHT))
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'button1.png')), (BUTTON_WIDTH + 40, BUTTON_HEIGHT + 40))
SANTA_RIDING = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'santa-riding.png')), (180, 100)), -15)
BULLET = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level3_images', 'present.png')), (BULLET_WIDTH, BULLET_HEIGHT))
BACKGROUND_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level3_images', 'jingle_bell.ogg'))
clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()


class Level_3:

    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level3_images', 'fireworks-noise1.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level3_images', 'merry-christmas.ogg'))
        self.MAX_ENEMY = 15
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.VEL = 7
        self.BULLET_VEL = 7
        self.MAX_BULLETS = 5
        self.my_health = 5
        self.START_BULLET_DEV = 25
        self.SNOW_BALLS_LOC = []
        self.RAD_SNOW_BALL = 4
        self.rotation = 0
        self.explo_size = [OBJ_WIDTH, OBJ_HEIGHT, OBJ_WIDTH, OBJ_HEIGHT]
        self.bullets = []
        BACKGROUND_SOUND.set_volume(0.5)
        BACKGROUND_SOUND.play(-1)




    def game_over_screen(self, WIN, WINNER_FONT, text):
        self.BULLET_HIT_SOUND.stop()
        ridingRec = pygame.Rect(WIDTH // 2 + BUTTON_WIDTH // 2 + 120, HEIGHT // 2 - BUTTON_HEIGHT // 2 - 100, 160, 110)
        # Wait for a mouse click
        while True:
            WIN.blit(SANTA, (0, 0))
            if len(self.SNOW_BALLS_LOC) < 350:
                self.SNOW_BALLS_LOC.append([random.uniform(1, WIDTH - 1), 1])
            for snow in self.SNOW_BALLS_LOC:
                snow[1] += 1.3
                if snow[1] > HEIGHT:
                    snow[0] = random.uniform(1, WIDTH - 1)
                    snow[1] = random.uniform(1, HEIGHT // 5 - 1)
                pygame.draw.circle(WIN, WHITE, (snow[0], snow[1]), self.RAD_SNOW_BALL)
            if ridingRec.y + ridingRec.height < 0 or ridingRec.x + ridingRec.width < 0:
                ridingRec.x = WIDTH // 2 + BUTTON_WIDTH // 2 + 120
                ridingRec.y = HEIGHT // 2 - BUTTON_HEIGHT // 2 - 100
            else:
                ridingRec.x -= 4
                ridingRec.y -= 0.6
            WIN.blit(SANTA_RIDING, (ridingRec.x, ridingRec.y))
            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 150))
            WIN.blit(BUTTON, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2))
            # Draw a button
            if text == "YOU LOST!!!":
                rendered_text = pygame.font.SysFont('Comic Sans MS', 40).render("RESTART", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 30, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 60))
            else:
                if self.explo_size[0] > 140 or self.explo_size[1] > 100:
                    self.explo_size[0] = OBJ_WIDTH
                    self.explo_size[1] = OBJ_HEIGHT
                if self.explo_size[2] > 140 or self.explo_size[3] > 100:
                    self.explo_size[2] = OBJ_WIDTH
                    self.explo_size[3] = OBJ_HEIGHT
                scaled_fire = pygame.transform.scale(EXPLOSION, (self.explo_size[0], self.explo_size[1]))
                scaled_fire2 = pygame.transform.scale(EXPLOSION, (self.explo_size[2], self.explo_size[3]))
                WIN.blit(scaled_fire, (WIDTH // 2 - BUTTON_WIDTH // 2 - 80, HEIGHT // 2 - BUTTON_HEIGHT // 2 - 50))
                WIN.blit(scaled_fire2, (WIDTH // 2 - BUTTON_WIDTH // 2 - 80, HEIGHT // 2 - BUTTON_HEIGHT // 2))
                self.explo_size[0] += 1
                self.explo_size[1] += 1
                self.explo_size[2] += 0.8
                self.explo_size[3] += 0.8
                rendered_text = pygame.font.SysFont('Comic Sans MS', 36).render("NEXT LEVEL", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 20, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 65))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH//2 - BUTTON_WIDTH//2 <= mouse_x <= WIDTH//2 - BUTTON_WIDTH//2 + BUTTON_WIDTH and HEIGHT // 2 - (BUTTON_HEIGHT + 40) // 2 +30\
                            <= mouse_y <= HEIGHT//2 - (BUTTON_HEIGHT + 40)//2 + BUTTON_HEIGHT + 60:
                        BACKGROUND_SOUND.stop()
                        # Restart the game
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN,HEALTH_FONT, my_obj, TOTAL_CRUSH , rectangles):
        WIN.blit(SANTA, (0, 0))

        if len(self.SNOW_BALLS_LOC) < 350:
            self.SNOW_BALLS_LOC.append([random.uniform(1, WIDTH - 1), 1])
        for snow in self.SNOW_BALLS_LOC:
            snow[1] += 1.3
            if snow[1] > HEIGHT:
                snow[0] = random.uniform(1, WIDTH - 1)
                snow[1] = random.uniform(1, HEIGHT//5 - 1)
            pygame.draw.circle(WIN, WHITE, (snow[0], snow[1]), self.RAD_SNOW_BALL)
        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))
        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(SANTA_CAR, (my_obj.x, my_obj.y))

        for enemy in rectangles:
            if enemy.getX() >= WIDTH:
                rectangles.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangles.remove(enemy)
            else:
                WIN.blit(SNOW_MAN, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            rotated_gift = pygame.transform.rotate(BULLET, (self.rotation % 360))
            WIN.blit(rotated_gift, (bullet.x, bullet.y))
            if (self.rotation + 5) == 360:
                self.rotation = 0
            else:
                self.rotation += 5
        pygame.display.update()

    def get_enemy_details(self):
        # velocity_x, velocity_y, life, obj_height, obj_width
        return random.randint(2, 5), random.randint(-3, 3), random.randint(1, 3), self.OBJ_HEIGHT, self.OBJ_WIDTH, 0

    def next_enemy(self):
        return random.uniform(1000, 3000)
    def play_dead_sound(self,enemy):
        self.BULLET_HIT_SOUND.play()