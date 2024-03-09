import pygame
import os
import sys
import button


pygame.font.init()
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
parent_directory = os.path.dirname(os.getcwd())
END_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Level8_images', 'END_BACKGROUND.png')), (WIDTH, HEIGHT))
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Start', 'button.png')), (235, 60))
BUTTON_BACK = pygame.transform.scale(pygame.image.load(os.path.join(parent_directory, 'Assets', 'Start', 'button.png')), (120, 80))

# Define font
font1 = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 40)


def draw_menu(WIN):
    text = font1.render("About the game", True, WHITE)
    WIN.blit(BUTTON, (-25, -20))
    WIN.blit(text, (0, 0))
    text1 = font1.render("Game levels", True, WHITE)
    WIN.blit(BUTTON, (175, -20))
    WIN.blit(text1, (215, 0))


def draw_about_the_game(WIN):
    lines = [
        "The purpose of the game is to prevent all the enemies",
        "coming from the left side to reach the right side.",
        "This is done by using the space button to shoot and the arrows to move.",
        "There are 8 levels you need to pass to win the game.",
        "each level have his own limits (read more in \"Game levels\" button).",
        "NOTE: If you collide with one of the enemies",
        "it will bring the game to a state of total crush",
        "which will lead to the disqualification of the level.",
        "Each enemy can have number of lives depending on the level.",
        "Therefore there will be enemies that will die only after several shots.",
    ]
    text_surfaces = [pygame.font.SysFont('Comic Sans MS', 25).render(line, True, WHITE) for line in lines]
    while True:
        WIN.blit(END_BACKGROUND, (0, 0))
        WIN.blit(BUTTON_BACK, (-25, -20))
        rendered_text = pygame.font.SysFont('Comic Sans MS', 30).render("BACK", True, WHITE)
        WIN.blit(rendered_text, (0, 0))
        y = 50
        for text_surface in text_surfaces:
            WIN.blit(text_surface, (70, y))
            y += text_surface.get_height() + 10
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 0 <= mouse_x <= 88 and 0 <= mouse_y <= 44:
                    return True
        pygame.time.Clock().tick(30)  # Limit frame rate

def draw_levels(WIN):
    while True:
        WIN.blit(END_BACKGROUND, (0, 0))
        WIN.blit(BUTTON_BACK, (-25, -20))
        rendered_text = pygame.font.SysFont('Comic Sans MS', 30).render("BACK", True, WHITE)
        WIN.blit(rendered_text, (0, 0))
        width_coff = -0.6
        height_coff = -3.5
        for i in range(1, 9):
            rendered_text = pygame.font.SysFont('Comic Sans MS', 30).render("Level" + str(i), True, WHITE)
            x, y = (WIDTH//2 + width_coff * rendered_text.get_width() - 40, HEIGHT//2 + height_coff * rendered_text.get_height())
            WIN.blit(BUTTON_BACK, (x - 15, y - 20))
            WIN.blit(rendered_text, (x, y))
            width_coff *= -1
            if i % 2 == 0:
                height_coff += 2
        # pygame.draw.circle(WIN, WHITE, (200, 200), 3)
        # pygame.draw.circle(WIN, WHITE, (300, 0), 3)
        # pygame.draw.circle(WIN, WHITE, (88, 42), 3)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 0 <= mouse_x <= 88 and 0 <= mouse_y <= 44:
                    return True
                elif WIDTH//2 + (-0.6) * rendered_text.get_width() - 40 <= mouse_x <= WIDTH//2 + (-0.6) * rendered_text.get_width() + 55:
                    if HEIGHT//2 +(-3.5) * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + (-3.5) * rendered_text.get_height() + 44:
                        draw_level(WIN, 1)
                    elif HEIGHT//2 + (-1.5) * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + (-1.5) * rendered_text.get_height() + 44:
                        draw_level(WIN, 3)
                    elif HEIGHT//2 + 0.5 * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + 0.5 * rendered_text.get_height() + 44:
                        draw_level(WIN, 5)
                    elif HEIGHT//2 + 2.5 * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + 2.5 * rendered_text.get_height() + 44:
                        draw_level(WIN, 7)
                elif WIDTH//2 + 0.6 * rendered_text.get_width() - 40 <= mouse_x <= WIDTH//2 + 0.6 * rendered_text.get_width() + 56:
                    if HEIGHT//2 + (-3.5) * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + (-3.5) * rendered_text.get_height() + 44:
                        draw_level(WIN, 2)
                    elif HEIGHT//2 + (-1.5) * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + (-1.5) * rendered_text.get_height() + 44:
                        draw_level(WIN, 4)
                    elif HEIGHT//2 + 0.5 * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + 0.5 * rendered_text.get_height() + 44:
                        draw_level(WIN, 6)
                    elif HEIGHT//2 + 2.5 * rendered_text.get_height() <= mouse_y <= HEIGHT//2 + 2.5 * rendered_text.get_height() + 44:
                        draw_level(WIN, 8)


        pygame.time.Clock().tick(30)  # Limit frame rate



def start(WIN):
    # Wait for a mouse click
    while True:
        WIN.blit(END_BACKGROUND, (0, 0))
        # Draw a button
        draw_menu(WIN)
        rendered_text = pygame.font.SysFont('Comic Sans MS', 50).render("START GAME", True, WHITE)
        WIN.blit(rendered_text, (WIDTH // 2 - 170, HEIGHT // 2 - 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (WIDTH // 2 - 150) <= mouse_x <= WIDTH // 2 + 200 and HEIGHT // 2 - 20 \
                        <= mouse_y <= HEIGHT // 2 + 50:
                    # Restart the game
                    return True  # Signal to restart the game
                elif 0 <= mouse_y <= 30:
                    if 0 <= mouse_x <= 185: ## about the game
                        draw_about_the_game(WIN)
                    elif 200 <= mouse_x <= 385:
                        draw_levels(WIN)
        pygame.time.Clock().tick(30)  # Limit frame rate

def draw_level(WIN,level):
    num_enemys, health, vel, bullet_vel, max_bullets, frq, types = data_level(level)
    lines = [
        "ENEMYS NUMBER: " + num_enemys,
        "HEALTH: " + health,
        "MY VELOCITY: " + vel,
        "BULLET VELOCITY: " + bullet_vel,
        "MAX BULLETS: " + max_bullets,
        "ENEMY FREQUENCY: " + frq,
        "ENEMY TYPES: " + types
    ]
    text_surfaces = [pygame.font.SysFont('Comic Sans MS', 30).render(line, True, WHITE) for line in lines]
    while True:
        WIN.blit(END_BACKGROUND, (0, 0))
        WIN.blit(BUTTON_BACK, (-25, -20))
        y = 70
        for text_surface in text_surfaces:
            WIN.blit(text_surface, (100, y))
            y += text_surface.get_height() + 10
        rendered_text = pygame.font.SysFont('Comic Sans MS', 30).render("BACK", True, WHITE)
        WIN.blit(rendered_text, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 0 <= mouse_x <= 88 and 0 <= mouse_y <= 44:
                    return True
        pygame.time.Clock().tick(30)  # Limit frame rate

def data_level(level):
    match level:
        case 1:
            return "10", "3", "5", "5", "3", "3 Seconds", "Regular"
        case 2:
            return "15", "3", "6", "5", "5", "3 Seconds", "Regular"
        case 3:
            return "15", "5", "7", "7", "5", "Randomly between 1-3 Seconds", "Regular"
        case 4:
            return "15", "3", "7", "7", "5", "Randomly between 1-3.5 Seconds", "Regular/Zigzag"
        case 5:
            return "20", "5", "7", "7", "8", "Randomly between 1-3 Seconds", "Regular/Teleport"
        case 6:
            return "20", "5", "6", "10", "8", "Randomly between 1-3 Seconds", "Regular/Hover"
        case 7:
            return "20", "8", "8", "10", "8", "Randomly between 1-2 Seconds", "Regular/Zigzag/Teleport/Hover"
        case 8:
            return "21", "10", "8", "10", "10", "Randomly between 0.5-3 Seconds", "Regular/Zigzag/Hover"
