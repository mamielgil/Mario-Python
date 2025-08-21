from Enemy import Enemy
from Sprite import Sprite
import pyxel


class Enemy1(Enemy):

    def __init__(self, direction: str, x: float, y: float, lives: int, width: int, height: int):
        # We  inherit the attributes from the Enemy's mother class
        """:param direction: indicates whether the enemy moves to the right or the left
            :param x: initial x position of the enemy
            :param y: initial y position of the enemy
            :param lives: amount of lives that the enemy has
            :param width: width of the enemy
            :param height: height of the enemy """

        # This class corresponds to the turtle enemy
        super().__init__(direction, x, y, lives, width, height)
        # We establish the width to a constant values to avoid sprite problems
        self.width = 16
        self.height = 16

        # We define the lists that have the sprites of the enemy depending on their tile-map_collisions
        self.sprites_right = [Sprite(self.x, self.y, 0, 0, 32, self.width, self.height),
                              Sprite(self.x, self.y, 0, 16, 32, self.width, self.height),
                              Sprite(self.x, self.y, 0, 32, 32, self.width, self.height)]

        self.sprites_left = [Sprite(self.x, self.y, 0, 0, 32, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 16, 32, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 32, 32, -self.width, self.height)]

        # We store the knocked sprite individually to be able to use it easily
        self.knocked_sprite = Sprite(self.x, self.y, 0, 48, 32, self.width, self.height)

        # Consider dead and time attributes are going to be used to control the time that the enemy is knocked down
        self.__consider_dead = 0
        self.__time = 0
        self.lives = 1
        self.x_speed = 1

    def update(self):
        # The enemy is updated by using the update method of the mother Enemy Class and then the sprite method is
        # executed to determine the sprite that is going to be drawn
        self.update_enemy()
        draw_sprite = self.change_sprite()
        draw_sprite.draw(self.x, self.y)

    def change_sprite(self):

        if self.knocked:
            sprite = self.knocked_sprite
            if self.__consider_dead == 0:
                # we store the frame in which the enemy was downed
                self.__time = pyxel.frame_count
                self.__consider_dead += 1

            if pyxel.frame_count == self.__time + 150:
                self.knocked = False
                # We empower the Enemy after not having been hit for a while
                self.__empower()

        else:
            # If the Enemy is not knocked we execute the sprites direction method to determine the final sprite
            sprite = self.sprites_direction()

        return sprite

    def __empower(self):

        # Strengthening the enemy if it has been knocked down ,and it has not been killed
        self.x_speed = 1.5
        # We reset consider dead for it to be able to get knocked down again
        self.__consider_dead = 0
        # Change to the corresponding sprites
        self.sprites_right = [Sprite(self.x, self.y, 0, 96, 32, self.width, self.height),
                              Sprite(self.x, self.y, 0, 112, 32, self.width, self.height),
                              Sprite(self.x, self.y, 0, 128, 32, self.width, self.height)]

        self.sprites_left = [Sprite(self.x, self.y, 0, 96, 32, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 112, 32, -self.width, self.height),
                             Sprite(self.x, self.y, 0, 128, 32, -self.width, self.height)]

        self.knocked_sprite = Sprite(self.x, self.y, 0, 144, 32, self.width, self.height)