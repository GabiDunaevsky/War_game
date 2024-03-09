import EnemyTypes as enemy
import myGame
import pygame

pygame.font.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ships")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont('Comic Sans MS', 40)
WINNER_FONT = pygame.font.SysFont('Comic Sans MS', 100)
LEVEL = 0
LEVEL_TO_PRESENT = 1
MY_HEALTH = 0
FPS = 60

YELLOW_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2
ENEMY_PRODUCED = 0
rectangles = []
TOTAL_CRUSH = False
TOTAL_CRUSH_TINE = 4

OBJ_LEVEL = None

# # Clock for controlling frame rate and timing
clock = pygame.time.Clock()
last_rect_creation_time = pygame.time.get_ticks()

def init_game():
    global last_rect_creation_time, ENEMY_PRODUCED, rectangles, TOTAL_CRUSH, TOTAL_CRUSH_TINE, LEVEL_TO_PRESENT, OBJ_LEVEL
    last_rect_creation_time = pygame.time.get_ticks()
    ENEMY_PRODUCED = 0
    rectangles = []
    TOTAL_CRUSH = False
    TOTAL_CRUSH_TINE = 4
    LEVEL_TO_PRESENT = LEVEL
    OBJ_LEVEL = None


def yellow_handle_movement(keys_pressed, yellow, VEL, obj_hight, ob_j_width):
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        if yellow.x - VEL <= 0:
            yellow.x = 0
        else:
            yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        if yellow.x + obj_hight + VEL >= WIDTH:
            yellow.x = WIDTH - obj_hight
        else:
            yellow.x += VEL
    if keys_pressed[pygame.K_UP]:  # UP
        if yellow.y <= 0:
            yellow.y = 0
        else:
            yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN]:  # Down
        if yellow.y + ob_j_width + VEL >= HEIGHT:
            yellow.y = HEIGHT - ob_j_width
        else:
            yellow.y += VEL


def handle_bullets():
    global rectangles, OBJ_LEVEL
    for bullet in OBJ_LEVEL.bullets:
        bullet.x -= OBJ_LEVEL.BULLET_VEL
        if rectangles:
            for enemy in rectangles:
                if enemy.getRect().colliderect(bullet):
                    OBJ_LEVEL.play_dead_sound(enemy)
                    enemy.setLife((enemy.getLife() - 1))
                    OBJ_LEVEL.bullets.remove(bullet)
        if bullet.x < 0 - OBJ_LEVEL.OBJ_WIDTH:
            OBJ_LEVEL.bullets.remove(bullet)


def create_new_rect(velocity_x, velocity_y, life, obj_height, obj_width, type):
    global last_rect_creation_time, rectangles, ENEMY_PRODUCED, OBJ_LEVEL
    # Check if it's time to create a new rectangle
    current_time = pygame.time.get_ticks()
    if current_time - last_rect_creation_time > OBJ_LEVEL.next_enemy():
        rectangles.append(enemy.CreateEnemy(velocity_x, velocity_y, life, obj_height, obj_width, type).getEnemy())
        ENEMY_PRODUCED += 1
        last_rect_creation_time = current_time


def handle_enemy_movement():
    global MY_HEALTH, OBJ_LEVEL
    # Update and draw each rectangle
    for enemy in rectangles:
        OBJ_LEVEL.my_health += enemy.move(OBJ_LEVEL.OBJ_HEIGHT, OBJ_LEVEL.OBJ_WIDTH, OBJ_LEVEL.BULLET_HIT_SOUND)


def total_crush(my_obj):
    global TOTAL_CRUSH, TOTAL_CRUSH_TINE, OBJ_LEVEL
    if TOTAL_CRUSH:
        if LEVEL == 8 and OBJ_LEVEL.boss:
            OBJ_LEVEL.my_health = 0
        elif TOTAL_CRUSH_TINE == 0:
            OBJ_LEVEL.my_health = 0
        else:
            TOTAL_CRUSH_TINE -= 1
    else:
        for enemy in rectangles:
            if enemy.getRect().colliderect(my_obj) and enemy.getLife() > 0:
                enemy.setLife(0)
                TOTAL_CRUSH = True
                OBJ_LEVEL.play_dead_sound(enemy)

def main():
    global clock, rectangles, ENEMY_PRODUCED, MY_HEALTH, LEVEL, OBJ_LEVEL
    game_over = False
    if LEVEL == 0:
        myGame.Start_page.start(WIN)
        LEVEL = 1

    match LEVEL:
        case 1:
            OBJ_LEVEL = myGame.Level_1.Level_1()
        case 2:
            OBJ_LEVEL = myGame.Level_2.Level_2()
        case 3:
            OBJ_LEVEL = myGame.Level_3.Level_3()
        case 4:
            OBJ_LEVEL = myGame.Level_4.Level_4()
        case 5:
            OBJ_LEVEL = myGame.Level_5.Level_5()
        case 6:
            OBJ_LEVEL = myGame.Level_6.Level_6()
        case 7:
            OBJ_LEVEL = myGame.Level_7.Level_7()
        case 8:
            OBJ_LEVEL = myGame.Level_8.Level_8()

    my_obj = pygame.Rect(800, 200, OBJ_LEVEL.OBJ_WIDTH, OBJ_LEVEL.OBJ_HEIGHT)
    winner_text = ""
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(OBJ_LEVEL.bullets) < OBJ_LEVEL.MAX_BULLETS:
                    bullet = pygame.Rect(my_obj.x, my_obj.y + my_obj.height // 2 - OBJ_LEVEL.START_BULLET_DEV, OBJ_LEVEL.BULLET_WIDTH, OBJ_LEVEL.BULLET_HEIGHT)
                    OBJ_LEVEL.bullets.append(bullet)
                    OBJ_LEVEL.BULLET_FIRE_SOUND.play()


        if ENEMY_PRODUCED >= OBJ_LEVEL.MAX_ENEMY and OBJ_LEVEL.my_health > 0 and not rectangles:
            if LEVEL == 8 and not OBJ_LEVEL.boss:
                OBJ_LEVEL.BOSS_SOUND.play()
                OBJ_LEVEL.boss = True
                OBJ_LEVEL.MAX_ENEMY = 1
                OBJ_LEVEL.MAX_BULLETS = 80
                rectangles.clear()
                ENEMY_PRODUCED = 0
            else:
                winner_text = "YOU WON!!!"
                game_over = True
                clock.tick(3)
                if LEVEL == 8:
                    LEVEL = 0
                else:
                    LEVEL += 1
                break

        if OBJ_LEVEL.my_health <= 0:
            winner_text = "YOU LOST!!!"
            game_over = True
            clock.tick(3)
            LEVEL = 0
            break

        if ENEMY_PRODUCED < OBJ_LEVEL.MAX_ENEMY:
            velocity_x, velocity_y, life, obj_height, obj_width, enemyType = OBJ_LEVEL.get_enemy_details()
            create_new_rect(velocity_x, velocity_y, life, obj_width, obj_height, enemyType)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, my_obj, OBJ_LEVEL.VEL, OBJ_LEVEL.OBJ_HEIGHT, OBJ_LEVEL.OBJ_WIDTH)
        handle_enemy_movement()
        handle_bullets()
        total_crush(my_obj)
        OBJ_LEVEL.draw_window(WIN, HEALTH_FONT, my_obj, TOTAL_CRUSH, rectangles)

    if game_over:
        OBJ_LEVEL.game_over_screen(WIN, WINNER_FONT, winner_text)
        init_game()
        main()

if __name__ == '__main__':
    main()