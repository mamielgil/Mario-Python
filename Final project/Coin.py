"Created by Miguel Amiel Gil"

import pyxel
from Entities import Entity
from Constants import Constants
from Sprite import Sprite


class Coin(Entity):
    # This class stores all the required information for the coin object

    def __init__(self,  x: float,  y: float,  width: int,  height: int,  lives: int, motion: bool):
        """ :param x: initial x position of the coin
            :param y: initial y position
            :param lives: number of lives of the coin
            :param width: width of the coin
            :param height: height of the coin
            :param motion: determines if the created coin is going to move or not"""

        super().__init__(x, y, lives,width, height)

        # We define the coin's size and include the constants class
        self.constants = Constants()
        self.height = 16
        self.width = 16
        self.speed = 4
        # Counter is an attribute used to control the coin's sprite
        self.__counter = 0
        self.__motion = motion

        # We define the sprites of the coin and store them in a list to be able to change them
        self.sprite_list = [Sprite(self.x, self.y, 0, 32, 88, self.width, self.height),
                            Sprite(self.x, self.y, 0, 16, 88, self.width, self.height),
                            Sprite(self.x, self.y, 0, 0, 88, self.width, self.height),
                            Sprite(self.x, self.y, 0, 48, 88, self.width, self.height)]

    def update(self):
        # We check the collision inherited from the Entity class
        self.collisions_check()
        # If motion is true then the corresponding methods from the Entity class allow the coin to move
        if self.__motion:
            self.__move()
            self.falling_fnc()

        # We establish the limits of the screen for the coin to not let them exit the gaming screen
        if self.x <= 0:
            self.x = self.constants.width - self.width
            if self.y > self.constants.height - 56:
                self.y = 16

        elif self.x + self.width > self.constants.width:
            self.x = self.width
            if self.y > self.constants.height - 56:
                self.y = 16

    def draw(self):
        # We use counter as an index to draw the sprite of the coin by changing its value per frame
        if self.__counter + 1 == len(self.sprite_list):
            self.__counter = 0
        if pyxel.frame_count % 10 == 0:
            self.__counter += 1

        self.sprite_list[self.__counter].draw(self.x, self.y)

    def __move(self):
        # We establish the motion of the coin
        if pyxel.frame_count % 5 == 0:
            self.x += self.speed
