
import pyxel


class Sprite:

    def __init__(self, x: float, y: float, img: int, u: int, v: int, w: int, h: int):
        """:param x: x position of the sprite
        :param y: y position of the sprite
        :param img: image bank in which the sprite is stored
        :param u: u position of the sprite in the image bank
        :param v: v position of the sprite in the image bank
        :param w: width of the sprite
        :param h: height of the sprite"""

        self.x = x
        self.y = y
        self.image = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h

    def draw(self, x: float, y: float):
        # This method prints the corresponding sprite
        pyxel.blt(x, y, self.image, self.u, self.v, self.w, self.h, 0)

    @ property
    def x(self):
        return self.__x

    @ x.setter
    def x(self,posx):

        if not isinstance(posx, int) and not isinstance(posx, float):
            raise TypeError("The sprite's y position must be an integer or a float")
        else:
            self.__x = posx

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, posy):

        if not isinstance(posy, int) and not isinstance(posy, float):
            raise TypeError("The sprite's y position must be an integer or a float")
        else:
            self.__y = posy

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, image):

        if not isinstance(image, int):
            raise TypeError("The sprite's image bank must be an integer")
        elif image < 0 or image > 2:
            raise ValueError("The introduced image bank does not exist")
        else:
            self.__img = image

    @property
    def u(self):
        return self.__u

    @u.setter
    def u(self, posu):

        if not isinstance(posu, int):
            raise TypeError("The sprite's image bank must be an integer")
        elif posu < 0 or posu > 248:
            raise ValueError("The introduced u value does not exist")
        else:
            self.__u = posu

    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, posv):

        if not isinstance(posv, int):
            raise TypeError("The sprite's image bank must be an integer")
        elif posv < 0 or posv > 248:
            raise ValueError("The introduced u value does not exist")
        else:
            self.__v = posv

    @ property
    def w(self):
        return self.__w

    @ w.setter
    def w(self, width):

        if not isinstance(width, int):
            raise TypeError("The width should be an integer")

        else:
            self.__w = width

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, height):

        if not isinstance(height, int):
            raise TypeError("The height should be an integer")
        else:
            self.__h = height



