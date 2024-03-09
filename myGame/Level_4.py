import os
import random
import sys
import pygame

pygame.mixer.init()
parent_directory = os.path.dirname(os.getcwd())
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
BUTTON_WIDTH, BUTTON_HEIGHT = 450, 180
OBJ_WIDTH, OBJ_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 20, 20
FAN_VOICE = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level4_images', 'yeled_daniel.mpeg'))
ANKARA_MESSI = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level4_images', 'ankare_messi.ogg'))
GOAL_KIPPER = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'goal_kipper.png')), (OBJ_WIDTH, OBJ_HEIGHT))
FOOTBALL_PLAYER = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'football_player.png')), (OBJ_WIDTH, OBJ_HEIGHT))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'goal_sticker.png')), (OBJ_WIDTH, OBJ_HEIGHT))
FOOTBALL_FIELD = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'football-field.png')), (WIDTH, HEIGHT))
FOOTBALL_FAN = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'football_fan.png')), (150, 100))
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'button.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
FOOTBALL_PLAYER_END = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'football_player.png')), (OBJ_WIDTH + 50, OBJ_HEIGHT + 50))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level4_images', 'ball-good.png')), (BULLET_WIDTH, BULLET_HEIGHT))
BACKGROUND_SOUND = pygame.mixer.Sound(
            os.path.join(parent_directory, 'Assets', 'Level4_images', 'crowd.mp3'))



clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()


class Level_4:
    def __init__(self):
        self.BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level4_images', 'golazo.ogg'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(parent_directory, 'Assets', 'Level4_images', 'shoot.mp3'))
        self.VEL = 7
        self.BULLET_VEL = 7
        self.MAX_BULLETS = 5
        self.my_health = 3
        self.START_BULLET_DEV = 25
        self.OBJ_WIDTH, self.OBJ_HEIGHT = OBJ_WIDTH, OBJ_HEIGHT
        self.BULLET_WIDTH, self.BULLET_HEIGHT = BULLET_WIDTH, BULLET_HEIGHT
        self.MAX_ENEMY = 15
        self.rotation = 0
        self.bullets = []
        BACKGROUND_SOUND.set_volume(0.3)
        BACKGROUND_SOUND.play(-1)




    def game_over_screen(self, WIN, WINNER_FONT, text):
        # Wait for a mouse click
        BACKGROUND_SOUND.stop()
        self.BULLET_HIT_SOUND.stop()
        playerRect = pygame.Rect(-100, 30, OBJ_WIDTH + 50, OBJ_HEIGHT + 50)
        ANKARA_MESSI.play()
        while True:
            WIN.blit(FOOTBALL_FIELD, (0, 0))
            if playerRect.x > WIDTH:
                playerRect.x = -100
                ANKARA_MESSI.play()
            else:
                playerRect.x += 7
            WIN.blit(FOOTBALL_PLAYER_END, (playerRect.x, playerRect.y))
            draw_text = WINNER_FONT.render(text, 1, WHITE)
            WIN.blit(draw_text,
                     ((WIDTH / 2 - draw_text.get_width() / 2) + 20, HEIGHT / 2 - draw_text.get_height() / 2 + 150))
            # WIN.blit(ALIEN, (WIDTH // 2 - BUTTON_WIDTH//2 + 10, HEIGHT // 2 - BUTTON_HEIGHT // 2 - 40))
            WIN.blit(BUTTON, (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2))
            # Draw a button
            if text == "YOU LOST!!!":
                rendered_text = pygame.font.SysFont('Comic Sans MS', 40).render("RESTART", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 135, HEIGHT // 2 + BUTTON_HEIGHT // 2 - 60))
            else:
                rendered_text = pygame.font.SysFont('Comic Sans MS', 30).render("NEXT LEVEL", True, WHITE)
                WIN.blit(rendered_text, (WIDTH // 2 - BUTTON_WIDTH // 2 + 125, HEIGHT // 2 + BUTTON_HEIGHT // 2 - 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH // 2 - BUTTON_WIDTH // 2 + 120 <= mouse_x <= WIDTH // 2 - BUTTON_WIDTH // 2 + 330 and HEIGHT // 2 + BUTTON_HEIGHT // 2 - 60\
                            <= mouse_y <= HEIGHT // 2 + BUTTON_HEIGHT // 2:
                        ANKARA_MESSI.stop()
                        # Restart the game
                        return True  # Signal to restart the game
            pygame.time.Clock().tick(30)  # Limit frame rate

    def draw_window(self, WIN, HEALTH_FONT, my_obj, TOTAL_CRUSH , rectangles):
        global last_rect_creation_time
        WIN.blit(FOOTBALL_FIELD, (0, 0))
        health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
        WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))

        if TOTAL_CRUSH:
            WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
        else:
            WIN.blit(GOAL_KIPPER, (my_obj.x, my_obj.y))
        r = random.randint(1, 1500)
        if r == 2:
            x = random.uniform((0 + 150), (WIDTH - 150))
            fanRect = pygame.Rect(x, HEIGHT, 100, 100)
            FAN_VOICE.play()
            while (fanRect.y + 100) > 0:
                WIN.blit(FOOTBALL_FIELD, (0, 0))
                health_text = HEALTH_FONT.render("Health: " + str(self.my_health), 1, WHITE)
                WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))

                if TOTAL_CRUSH:
                    WIN.blit(EXPLOSION, (my_obj.x, my_obj.y))
                else:
                    WIN.blit(GOAL_KIPPER, (my_obj.x, my_obj.y))
                WIN.blit(FOOTBALL_FAN, (fanRect.x, fanRect.y))
                # Update display
                pygame.display.update()
                fanRect.y -= 2

        for enemy in rectangles:
            if enemy.getX() >= WIDTH:
                rectangles.remove(enemy)
            elif enemy.getLife() <= 0:
                WIN.blit(EXPLOSION, (enemy.getX(), enemy.getY()))
                enemy.setLife(enemy.getLife() - 1)
                if enemy.getLife() <= -3:
                    rectangles.remove(enemy)
            else:
                WIN.blit(FOOTBALL_PLAYER, (enemy.getX(), enemy.getY()))
        for bullet in self.bullets:
            rotated_ball = pygame.transform.rotate(BULLET, (self.rotation % 360))
            WIN.blit(rotated_ball, (bullet.x, bullet.y))
            if (self.rotation + 5) == 360:
                self.rotation = 0
            else:
                self.rotation += 30
        pygame.display.update()

    def get_enemy_details(self):
        # type = 0 regular, type = 1 zigzag
        # velocity_x, velocity_y, life, obj_height, obj_width, type
        return random.randint(2, 7), random.randint(-4, 4), random.randint(1, 2), self.OBJ_HEIGHT, self.OBJ_WIDTH, random.randint(0, 1)

    def next_enemy(self):
        return random.uniform(1000, 3500)
    def play_dead_sound(self,enemy):
        self.BULLET_HIT_SOUND.play()

