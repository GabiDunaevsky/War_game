import os
import random
import pygame
import sys

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 55, 40
BUTTON_WIDTH, BUTTON_HEIGHT = 450, 180
BULLET_WIDTH, BULLET_HEIGHT = 40, 30

DOG = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'dog_killer.png')), (OBJ_WIDTH, OBJ_HEIGHT))
CAT = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'cat.png')), (OBJ_WIDTH, OBJ_HEIGHT))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'grave.png')), (OBJ_WIDTH, OBJ_HEIGHT + 50))
DOG_PLAY_GROUND = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'dog_play_ground.png')), (WIDTH, HEIGHT))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'green_snack1.png')), (BULLET_WIDTH, BULLET_HEIGHT))
BACK_TO_END = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'background_to_end.png')), (WIDTH, HEIGHT))
SHIBA_TO_END = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level5_images', 'shiba_to_end.png')), (120, 200))

clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()

class Level_5:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level5_images', 'meow.ogg'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level5_images', 'bark.ogg'))
        self.START_BULLET_DEV = 25
        self.VEL = 7
        self.BULLET_VEL = 7
        self.MAX_BULLETS = 8
        self.my_health = 5
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.MAX_ENEMY = 20
        self.rotation = 0
        self.bullets = []




    def game_over_screen(self, WIN, WINNER_FONT, text):
        # Wait for a mouse click
        shibaRect = pygame.Rect(140, 80, 120, 200)
        self.BULLET_HIT_SOUND.stop()
        dir = 0 ## 0 = up, 1 = down
        while True:
            WIN.blit(BACK_TO_END, (0, 0))
            if shibaRect.y < 40:
                dir = 1
            if shibaRect.y > 80:
                dir = 0
            if dir == 0:
                shibaRect.y -= 2
            else:
                shibaRect.y += 3

            WIN.blit(SHIBA_TO_END, (shibaRect.x, shibaRect.y))
            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 200))
            if text == "YOU LOST!!!":
                rendered_text = pygame.font.SysFont('Comic Sans MS', 60).render("RESTART", True, (0, 0, 0))
                WIN.blit(rendered_text, (WIDTH // 4 + 90, HEIGHT // 2 + BUTTON_HEIGHT // 2 - 45))
            else:
                rendered_text = pygame.font.SysFont('Comic Sans MS', 60).render("NEXT LEVEL", True, (0, 0, 0))
                WIN.blit(rendered_text, (WIDTH // 4 + 40, HEIGHT // 2 + BUTTON_HEIGHT // 2 - 45))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH // 4 <= mouse_x <= WIDTH // 0.75 and HEIGHT // 2 + BUTTON_HEIGHT // 2 - 40\
                            <= mouse_y <= HEIGHT // 2 + BUTTON_HEIGHT // 2 + 20:
                        # Restart the game
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN, HEALTH_FONT, my_obj, TOTAL_CRUSH, rectangles):
        global rotation, last_rect_creation_time
        WIN.blit(DOG_PLAY_GROUND, (0, 0))
        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))

        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(DOG, (my_obj.x, my_obj.y))

        for enemy in rectangles:
            if enemy.getX() >= WIDTH:
                rectangles.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangles.remove(enemy)
            else:
                WIN.blit(CAT, (enemy.getX(), enemy.getY()))

        for bullet in self.bullets:
            rotated_ball = pygame.transform.rotate(BULLET, (self.rotation % 360))
            WIN.blit(rotated_ball, (bullet.x, bullet.y))
            if (self.rotation + 5) == 360:
                self.rotation = 0
            else:
                self.rotation += 20
        pygame.display.update()

    def get_enemy_details(self):
        # type = 0 regular, type = 1 zigzag, type 2 = Sprinter
        # velocity_x, velocity_y, life, obj_height, obj_width, type
        x = random.randint(1, 2)
        if x == 1:
            x = 0
        return random.randint(2, 6), random.randint(-4, 4), random.randint(1, 2), self.OBJ_HEIGHT, self.OBJ_WIDTH, x

    def next_enemy(self):
        return random.uniform(1000, 3000)
    def play_dead_sound(self,enemy):
        self.BULLET_HIT_SOUND.play()

