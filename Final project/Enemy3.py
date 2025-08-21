
from Enemy import Enemy
from Sprite import Sprite
import pyxel


class Enemy3(Enemy):

    def __init__(self, direction: str, x: float, y: float, lives: int, width: int, height: int):
        """:param direction: indicates whether the enemy moves to the right or the left
            :param x: initial x position of the enemy
            :param y: initial y position of the enemy
            :param lives: amount of lives that the enemy has
            :param width: width of the enemy
            :param height: height of the enemy """

        super().__init__(direction, x, y, lives, width, height)
        # We establish the width to a constant values to avoid sprite problems
        self.width = 16
        self.height = 16

        # We define the lists that have the sprites of the enemy depending on their tile-map_collisions
        self.sprites_right = [Sprite(self.x, self.y, 0, 0, 64, self.width, self.height),
                              Sprite(self.x, self.y, 0, 16, 64, self.width, self.height),
                              Sprite(self.x, self.y, 0, 32, 64, self.width, self.height),
                              Sprite(self.x, self.y, 0, 48, 64, self.width, self.height)]

        self.sprites_left = [Sprite(self.x, self.y, 0, 0, 64, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 16, 64, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 32, 64, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 48, 64, -self.width, self.height)]

        # We store the knocked sprite individually to be able to use it easily
        self.knocked_sprite = Sprite(self.x, self.y, 0, 64, 64, self.width, self.height)
        self.x_speed = 1.25

        # These parameters are going to be used for the fly to be able to jump
        # Jumping speed
        self.jump_speed = 36
        # Stores if the enemy is in the jumping state
        self.jumping = False
        # Stores how much the enemy still has to jump
        self.difference = 0
        # Controls the time rate at which the fly jumps
        self.__jumping_counter = 0
        # stores the y in which the fly started the jump
        self.__previous_y = 0

        # To control that the variable time is only established the first time that the Enemy is knocked down so
        # you can control the time that the enemy is downed
        self.__consider_dead = 0
        self.__time = 0

    def update(self):
        # We allowed the enemy to jump if it is not knocked
        if not self.knocked:
            self.move3fnc()
        draw_sprite = self.change_sprite()
        draw_sprite.draw(self.x, self.y)

    def change_sprite(self):
        # calculate operations regarding the sprite that is going to be drawn
        if self.knocked:
            sprite = self.knocked_sprite
            if self.__consider_dead == 0:
                # we store the frame in which the enemy was downed
                self.__time = pyxel.frame_count
                self.__consider_dead += 1

            if pyxel.frame_count == self.__time + 150:
                self.knocked = False
                # We  strengthen the enemy if it has not been killed after a certain amount of time
                self.__empower()

        else:
            # if the enemy is not knocked, the sprite is determined  executing the sprites direction method
            sprite = self.sprites_direction()

        return sprite

    def __empower(self):
        # Strengthening the enemy if it has been knocked down ,and it has not been killed
        self.x_speed = 1.5
        # We reset consider dead for it to be able to get knocked down again
        self.__consider_dead = 0

    def move3fnc(self):
        # Firstly collisions from the Entity mother class are checked
        self.collisions_check()
        # Executed if the enemy is still jumping, or it has been one second since it was on the ground
        if self.__jumping_counter == 30 or self.jumping or self.falling:
            self.movefnc()
            if not self.jumping and not self.falling:
                # if it is not jumping then we start the jumping  process,storing the initial y and setting time to 0
                self.jumping = True
                self.__previous_y = self.y
                self.__jumping_counter = 0

            if self.jumping and not self.difference >= self.jump_speed:
                # the enemy is still jumping ,and it has not reached the established maximum height
                self.y -= 4
                self.difference = abs(self.y - self.__previous_y)

            if self.difference >= self.jump_speed:
                # when it has reached the peak then the enemy stops jumping and starts falling
                self.falling = True
                self.jumping = False
                self.difference = 0
            if not self.jumping:
                self.falling_fnc()
        else:
            # we add one to the counter to count the time in which the enemy has been on the ground
            self.__jumping_counter += 1
