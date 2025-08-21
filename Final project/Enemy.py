import pyxel
from Entities import Entity
from Sprite import Sprite


class Enemy(Entity):
    # This class contains all the information about the enemies

    def __init__(self, direction: str, x: float, y: float, lives: int, width: int, height: int):
        """:param direction: indicates whether the enemy moves to the right or the left
            :param x: initial x position of the enemy
            :param y: initial y position of the enemy
            :param lives: amount of lives that the enemy has
            :param width: width of the enemy
            :param height: height of the enemy"""

        super().__init__(x, y, lives, width, height)

        # We initialize the corresponding parameters: the ones mentioned above and knocked which stores if the
        # enemy has been hit and the sprites lists with the counter
        self.direction = direction
        self.x_speed = 1
        self.knocked = False
        self.sprites_right = []
        self.sprites_left = []
        self.__counter = 0

    def movefnc(self):
        # Controls the movement of the enemy. If the enemy has not been hit, it is allowed to move
        if not self.knocked:
            if self.direction == "Right":
                self.x += self.x_speed

            elif self.direction == "Left":
                self.x -= self.x_speed

            # We establish the bounds for the Enemy to avoid them leaving the screen
            if self.x <= 0 and self.direction == "Left":
                self.x = self.constants.width - self.width
                if self.y > self.constants.height - 56:
                    self.y = 16

            elif self.x + self.width > self.constants.width and self.direction == "Right":
                self.x = self.width
                if self.y > self.constants.height - 56:
                    self.y = 16

    def update_enemy(self):
        # We execute the update of the entity class that checks the collision and the fall; then we
        # execute the enemy's movement
        self.update_entity()
        self.movefnc()

    def sprites_direction(self):
        # Here we determine how the sprites will change depending on the direction toward the enemy is
        # moving by using the count attribute.We define the sprites in each of the specific enemies as
        # they will have different ones

        if self.direction == "Right":
            if self.__counter == len(self.sprites_right) - 1:
                self.__counter = 0
                sprite = self.sprites_right[self.__counter]
            else:
                if pyxel.frame_count % 10 == 0:
                    self.__counter += 1
                sprite = self.sprites_right[self.__counter]

        elif self.direction == "Left":
            if self.__counter == len(self.sprites_left) - 1:
                self.__counter = 0
                sprite = self.sprites_left[self.__counter]
            else:
                if pyxel.frame_count % 10 == 0:
                    self.__counter += 1
                sprite = self.sprites_left[self.__counter]

        return sprite

# We include the setters that control the value of the attributes
    @ property
    def direction(self):
        return self.__direction

    @ direction.setter
    def direction(self, direc):

        if not isinstance(direc, str):

            raise TypeError("The direction must be a string")
        elif direc != "Right" and direc != "Left":
            raise ValueError("The direction can only be Left or Right")
        else:
            self.__direction = direc

    @ property
    def knocked(self):
        return self.__knocked

    @ knocked.setter
    def knocked(self, knock):
        if not isinstance(knock, bool):
            raise TypeError("The knocked attribute must be a boolean")
        else:
            self.__knocked = knock

    @ property
    def sprites_right(self):
        return self.__sprites_right

    @ sprites_right.setter
    def sprites_right(self, right):
        if not isinstance(right, list):
            raise TypeError("The value for the sprites must be a list")
        else:
            for element in right:
                if not isinstance(element, Sprite):
                    raise TypeError("The element of the sprites list must be sprites objects")
            self.__sprites_right = right

    @property
    def sprites_left(self):
        return self.__sprites_left

    @sprites_left.setter
    def sprites_left(self, left):
        if not isinstance(left, list):
            raise TypeError("The value for the sprites must be a list")
        else:
            for element in left:
                if not isinstance(element, Sprite):
                    raise TypeError("The element of the sprites list must be sprites objects")
            self.__sprites_left = left

    @ property
    def x_speed(self):
        return self.__x_speed

    @ x_speed.setter
    def x_speed(self,velx):
        if not isinstance(velx,int) and not isinstance(velx, float):
            raise TypeError("The x speed for the enemies must be an integer or a float")
        elif velx >= 10 or velx <= -10:
            raise ValueError("The introduced value for the speed is too great")
        else:
            self.__x_speed = velx




