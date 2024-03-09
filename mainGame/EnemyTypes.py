import random
import pygame
WIDTH, HEIGHT = 900, 500


class CreateEnemy:
    def __init__(self, velocity_x, velocity_y, life, obj_height, obj_width, type):
        match type:
            case 0:
                self.enemy = Enemy(velocity_x, velocity_y, life, obj_height, obj_width)
            case 1:
                self.enemy = EnemyZigzag(velocity_x, velocity_y, life, obj_height, obj_width)
            case 2:
                self.enemy = EnemySprinter(velocity_x, velocity_y, life, obj_height, obj_width)
            case 3:
                self.enemy = EnemyStop(velocity_x, velocity_y, life, obj_height, obj_width)
            case _:
                None

    def getEnemy(self):
        return self.enemy



class Enemy:
    def __init__(self, velocity_x, velocity_y, life, obj_height, obj_width):
        x = random.randint(0 - obj_height, 0)
        y = random.randint(0, HEIGHT - obj_width)
        self.__rect = pygame.Rect(x, y, obj_width, obj_height)
        self.__velocity_x = velocity_x
        self.__velocity_y = velocity_y
        self.__life = life

    def getRect(self):
        return self.__rect

    def setX(self, x):
        self.__rect.x = x

    def setY(self, y):
        self.__rect.y = y

    def getX(self):
        return self.__rect.x

    def getY(self):
        return self.__rect.y

    def getVelX(self):
        return self.__velocity_x

    def getVelY(self):
        return self.__velocity_y

    def setVelX(self, vel):
        self.__velocity_x = vel

    def setVelY(self, vel):
        self.__velocity_y = vel

    def setLife(self, life):
        self.__life = life

    def getLife(self):
        return self.__life

    def move(self, obj_height, obj_width, BULLET_HIT_SOUND):
        health = 0
        if self.getX() + obj_width >= WIDTH:
            if self.getLife() > 0:
                health -= 1
                BULLET_HIT_SOUND.play()
                self.setLife(0)
        if (self.getY() + self.getVelY() + obj_height >= HEIGHT and self.getY() > 0) or (self.getY() - self.getVelY() <= 0 and self.getY() < 0):
            if self.getY() > HEIGHT:
                self.setY(HEIGHT - obj_height)
            elif self.getY() < 0:
                self.setY(0)
            self.setVelY((-1) * self.getVelY())

        # Move the rectangle
        else:
            self.setX((self.getX() + self.getVelX()))
            self.setY((self.getY() + self.getVelY()))
        return health

class EnemyZigzag(Enemy):
    def __init__(self, velocity_x, velocity_y, life, obj_height, obj_width):
        super().__init__(velocity_x, velocity_y, life, obj_height, obj_width)
        self.devY = 1
        self.counter = 0

    def move(self, obj_height, obj_width, BULLET_HIT_SOUND):
        health = 0
        if self.getX() + obj_width >= WIDTH:
            if self.getLife() > 0:
                health -= 1
                BULLET_HIT_SOUND.play()
                self.setLife(0)
        if (self.getY() + self.getVelY() + obj_height >= HEIGHT and self.getY() > 0) or (self.getY() - self.getVelY() <= 0 and self.getY() < 0):
            if self.getY() + obj_height > HEIGHT:
                self.setY(HEIGHT - obj_height)
            elif self.getY() < 0:
                self.setY(0)
            self.setVelY((-1) * self.getVelY())

        # Move the rectangle
        else:
            self.setX((self.getX() + self.getVelX()))
            self.setY((self.getY() + (self.getVelY() * self.devY)))


            if self.counter == 20:
                if self.devY == 1:
                    self.devY = -1
                else:
                    self.devY = 1
                self.counter = 0
            self.counter += 1
        return health

class EnemySprinter(Enemy):
    def __init__(self, velocity_x, velocity_y, life, obj_height, obj_width):
        super().__init__(velocity_x, velocity_y, life, obj_height, obj_width)


    def move(self, obj_height, obj_width, BULLET_HIT_SOUND):
        health = 0
        if self.getX() + obj_width >= WIDTH:
            if self.getLife() > 0:
                health -= 1
                BULLET_HIT_SOUND.play()
                self.setLife(0)
        if (self.getY() + self.getVelY() + obj_height >= HEIGHT and self.getY() > 0) or (self.getY() - self.getVelY() <= 0 and self.getY() < 0):
            if self.getY() > HEIGHT:
                self.setY(HEIGHT - obj_height)
            elif self.getY() < 0:
                self.setY(0)
            self.setVelY((-1) * self.getVelY())

        # Move the rectangle
        else:
            x = random.randint(1, 500)
            if x == 5:
                self.setX((self.getX() + (self.getVelX() * 50)))
            else:
                self.setX((self.getX() + self.getVelX()))
            self.setY((self.getY() + self.getVelY()))
        return health

class EnemyStop(Enemy):
    def __init__(self, velocity_x, velocity_y, life, obj_height, obj_width):
        super().__init__(velocity_x, velocity_y, life, obj_height, obj_width)
        self.counter = 0


    def move(self, obj_height, obj_width, BULLET_HIT_SOUND):
        health = 0
        if self.getX() + obj_width >= WIDTH:
            if self.getLife() > 0:
                health -= 1
                BULLET_HIT_SOUND.play()
                self.setLife(0)
        if (self.getY() + self.getVelY() + obj_height >= HEIGHT and self.getY() > 0) or (self.getY() - self.getVelY() <= 0 and self.getY() < 0):
            if self.getY() > HEIGHT:
                self.setY(HEIGHT - obj_height)
            elif self.getY() < 0:
                self.setY(0)
            self.setVelY((-1) * self.getVelY())

        # Move the rectangle
        else:
            r = 23
            if self.counter == 0:
                r = random.randint(1, 80)
            if r != 23:
                self.setX((self.getX() + self.getVelX()))
            else:
                self.counter += 1
                if self.counter == 40:
                    self.counter = 0
            self.setY((self.getY() + self.getVelY()))
        return health



