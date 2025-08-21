
from Sprite import Sprite
from Constants import Constants


class Pow:

    def __init__(self, x: float, y: float, uses: int):
        """:param x: corresponds to POW's x position
            :param y: corresponds to POW's y position
            :param uses: corresponds to the number of uses of the POW"""
        # We define the attributes of the POW including:constants class,width,height,collisions,sprites and visibility
        self.x = x
        self.y = y
        self.uses = uses
        self.constants = Constants()
        self.width = 16
        self.height = 16
        self.collision = False

        self.default = Sprite(self.x, self.y, 0, 0, 104, self.width,self.height)
        self.hit1 = Sprite(self.x, self.y, 0, 16, 104, self.width, self.height)
        self.hit2 = Sprite(self.x, self.y, 0, 32, 104, self.width, self.height)
        self.visible = True

    def pow_explosion(self):
        # The POW is allowed to be hit if it still has uses
        if self.uses != 0:
            if self.collision:
                # If it is hit it loses one use and the collision is reset to False
                self.uses -= 1
                self.collision = False
                return "Pow"

    def draw(self):
        # We draw the corresponding POW sprite in function of the remaining uses
        if self.uses > 0:
            self.visible = True
            if self.uses == 3:
                self.default.draw(self.x, self.y)
            elif self.uses == 2:
                self.hit1.draw(self.x, self.y)
            elif self.uses == 1:
                self.hit2.draw(self.x, self.y)
        else:
            # If it has no uses then it will not be shown
            self.visible = False

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x1):
        if not isinstance(x1, int):
            raise TypeError("The value must be an integer")
        if x1 > 256:
            raise ValueError("The x position must be less than the with of the screen: ", 256)
        if x1 < 0:
            raise ValueError("The value must be positive.")
        self.__x = x1

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y1):
        if not isinstance(y1, int):
            raise TypeError("The value must be an integer")
        if y1 > 256:
            raise ValueError("The y position must be less than the height of the screen:", 256)
        if y1 < 0:
            raise ValueError("The value must be positive.")
        self.__y = y1

    @property
    def uses(self):
        return self.__uses

    @uses.setter
    def uses(self, uses1):
        if not isinstance(uses1, int):
            raise TypeError("The value must be an integer")
        if uses1 < 0:
            raise TypeError("The value must be positive.")
        self.__uses = uses1

    @ property
    def visible(self):
        return self.__visible

    @ visible.setter
    def visible(self,vis):
        if not isinstance(vis,bool):
            raise TypeError("The visibility of the pow must be a boolean")
        else:
            self.__visible = vis

    @property
    def constants(self):
        return self.__constants

    @constants.setter
    def constants(self, const):
        if not isinstance(const, Constants):
            raise TypeError("The Constants for the POW must be  obtained from the Constants class")
        else:
            self.__constants = const

    @ property
    def width(self):
        return self.__width

    @ width.setter
    def width(self,w):
        if not isinstance(w, int):

            raise TypeError("The width must be an integer")

        elif w <= 0:
            raise ValueError("The width for the POW must be a positive value")
        else:
            self.__width = w

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        if not isinstance(h, int):

            raise TypeError("The height must be an integer")

        elif h <= 0:
            raise ValueError("The height for the POW must be a positive value")
        else:
            self.__height = h

    @ property
    def collision(self):
        return self.__collision

    @ collision.setter
    def collision(self,col):
        if not isinstance(col,bool):
            raise TypeError("The collision status must be a boolean")
        else:
            self.__collision = col

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, vis):
        if not isinstance(vis, bool):
            raise TypeError("The visibility of the POW must be a boolean")
        else:
            self.__visible = vis

    @ property
    def hit1(self):
        return self.__hit1

    @ hit1.setter
    def hit1(self,sprite):
        if not isinstance(sprite,Sprite):
            raise TypeError("The sprite for the pow must be from the Sprites class")
        else:
            self.__hit1 = sprite

    @property
    def hit2(self):
        return self.__hit2

    @hit2.setter
    def hit2(self, sprite):
        if not isinstance(sprite, Sprite):
            raise TypeError("The sprite for the pow must be from the Sprites class")
        else:
            self.__hit2 = sprite

    @property
    def default(self):
        return self.__default

    @default.setter
    def default(self, sprite):
        if not isinstance(sprite, Sprite):
            raise TypeError("The sprite for the pow must be from the Sprites class")
        else:
            self.__default = sprite

