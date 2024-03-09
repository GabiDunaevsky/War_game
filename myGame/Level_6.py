import os
import random
import pygame
import sys

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 80, 60
BUTTON_WIDTH, BUTTON_HEIGHT = 400, 110
BULLET_WIDTH, BULLET_HEIGHT = 30, 20
clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()
POLICE_MAN = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'policeman.png')), (OBJ_WIDTH, OBJ_HEIGHT))
THIEF = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'thief.png')), (OBJ_WIDTH, OBJ_HEIGHT))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'money.png')), (OBJ_WIDTH, OBJ_HEIGHT + 50))
BANK = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'bank.png')), (WIDTH, HEIGHT))
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'button.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'gun_bullet1.png')), (BULLET_WIDTH, BULLET_HEIGHT))
BILL = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level6_images', 'bill.png')), (100, 36)), 90)
DOLLAR_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level6_images', 'need_dollar_sound.ogg'))


class Level_6:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level6_images', 'money_sound.ogg'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level6_images', 'shoot.ogg'))
        self.POLICE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level6_images', 'police_sound.ogg'))
        self.VEL = 6
        self.BULLET_VEL = 10
        self.MAX_BULLETS = 8
        self.my_health = 5
        self.START_BULLET_DEV = 25
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.MAX_ENEMY = 20
        self.bullets = []


    def game_over_screen(self, WIN, WINNER_FONT, text):
        # Wait for a mouse click
        self.BULLET_HIT_SOUND.stop()
        self.POLICE_SOUND.stop()
        DOLLAR_SOUND.play(-1)
        money = []
        while True:
            WIN.blit(BANK, (0, 0))
            if len(money) < 350:
                money.append(pygame.Rect(random.uniform(1, WIDTH - 1), 1, 36, 100))
            for bill in money:
                bill.y += 2.5
                if bill.y > HEIGHT:
                    bill.x = random.uniform(1, WIDTH - 1)
                    bill.y = random.uniform(-10, -5)
                WIN.blit(BILL, (bill.x, bill.y))
            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 200))
            WIN.blit(BUTTON, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2))
            # Draw a button
            if text == "YOU LOST!!!":
                rendered_text = pygame.font.SysFont('Comic Sans MS', 50).render("RESTART", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 100, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 10))
            else:
                rendered_text = pygame.font.SysFont('Comic Sans MS', 46).render("NEXT LEVEL", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 90, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 15))
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
                        DOLLAR_SOUND.stop()
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN, HEALTH_FONT, my_obj, TOTAL_CRUSH , rectangles):
        WIN.blit(BANK, (0, 0))
        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))
        police_sound = random.randint(1, 500)
        if police_sound == 236:
            self.POLICE_SOUND.play()
        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(POLICE_MAN, (my_obj.x, my_obj.y))

        for enemy in rectangles:
            if enemy.getX() >= WIDTH:
                rectangles.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangles.remove(enemy)
            else:
                WIN.blit(THIEF, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            WIN.blit(BULLET, (bullet.x, bullet.y))
        pygame.display.update()


    def get_enemy_details(self):
        # type = 0 regular, type = 1 zigzag, type 2 = Sprinter, type 3 = stopEnemy
        # velocity_x, velocity_y, life, obj_height, obj_width, type
        x = random.randint(1, 2)
        if x == 2:
            x = 3
        return random.randint(2, 8), random.randint(-5, 5), random.randint(1, 3), self.OBJ_HEIGHT, self.OBJ_WIDTH, x

    def next_enemy(self):
        return random.uniform(1000, 3000)
    def play_dead_sound(self,enemy):
        self.BULLET_HIT_SOUND.play()

