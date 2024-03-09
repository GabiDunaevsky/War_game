import os
import random
import sys
import pygame

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
WIDTH, HEIGHT = 900, 500
OBJ_WIDTH, OBJ_HEIGHT = 55, 40
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (OBJ_WIDTH, OBJ_HEIGHT)), 270)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (OBJ_WIDTH, OBJ_HEIGHT)), 90)
EXPLOSION_IMAGE = pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'nuclear-explosion.png'))
EXPLOSION = pygame.transform.scale(EXPLOSION_IMAGE, (OBJ_WIDTH, OBJ_HEIGHT))
ALIEN_BUTTON_IMAGE = pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'alien-button.png'))
ALIEN_BUTTON = pygame.transform.scale(ALIEN_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
SPACESHIP_END_IMAGE = pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'spaceship-for-buty.png'))
SPACESHIP_END = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_END_IMAGE, (120, 96)), -40)
ALIEN_IMAGE = pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'alien.png'))
ALIEN = pygame.transform.rotate(pygame.transform.scale(ALIEN_IMAGE, (90, 80)), 15)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level1_images', 'space.png')), (WIDTH, HEIGHT))



class Level_1:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level1_images', 'Grenade+1.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level1_images', 'Gun+Silencer.mp3'))
        self.VEL = 5
        self.BULLET_VEL = 5
        self.MAX_BULLETS = 3
        self.my_health = 3
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.MAX_ENEMY = 10
        self.START_BULLET_DEV = 2
        self.BULLET_WIDTH, self.BULLET_HEIGHT = 10, 5
        self.bullets = []

    def game_over_screen(self, WIN, WINNER_FONT, text):
        self.BULLET_HIT_SOUND.stop()
        WIN.blit(SPACE, (0, 0))
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 150))
        WIN.blit(ALIEN, (WIDTH // 2 - BUTTON_WIDTH//2 + 10, HEIGHT // 2 - BUTTON_HEIGHT // 2 - 40))
        WIN.blit(ALIEN_BUTTON, (WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2))
        WIN.blit(SPACESHIP_END, (WIDTH//2 - BUTTON_WIDTH//2 + BUTTON_WIDTH - 20, HEIGHT//2 - BUTTON_HEIGHT//2 - 140))

        # Draw a button
        if text == "YOU LOST!!!":
            rendered_text = pygame.font.SysFont('Comic Sans MS', 40).render("RESTART", True, WHITE)
            WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 60, HEIGHT // 2 - BUTTON_HEIGHT // 2 + 10))
        else:
            rendered_text = pygame.font.SysFont('Comic Sans MS', 36).render("NEXT LEVEL", True, WHITE)
            WIN.blit(rendered_text, (WIDTH//2 - BUTTON_WIDTH//2 + 40, HEIGHT//2 - BUTTON_HEIGHT//2 + 15))

        # Update the display
        pygame.display.flip()

        # Wait for a mouse click
        while True:
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
        global my_health
        WIN.blit(SPACE, (0, 0))
        yellow_health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))

        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(YELLOW_SPACESHIP, (my_obj.x, my_obj.y))

        for enemy in rectangles:
            if enemy.getX() >= WIDTH:
                rectangles.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangles.remove(enemy)
            else:
                WIN.blit(RED_SPACESHIP, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            WIN.fill(YELLOW, bullet)
        pygame.display.update()


    def get_enemy_details(self):
        # velocity_x, velocity_y, life, obj_height, obj_width, type
        return random.randint(2 , 4), 0, 1, self.OBJ_HEIGHT, self.OBJ_WIDTH, 0

    def next_enemy(self):
        return 3000
    def play_dead_sound(self,enemy):
        self.BULLET_HIT_SOUND.play()
