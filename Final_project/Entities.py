from Constants import Constants
from Terrain import Terrain


class Entity:
    """This class is the mother class for all the different characters, both Mario and the enemies."""

    def __init__(self, x: int, y: int, lives: int, width: int, height: int):
        """ :param x: initial x position of the entity
            :param y: initial y position of the entity
            :param lives: amount of lives that the entity has
            :param width: width of the entity
            :param height: height of the entity"""
        # we store the game's constants and the entity's width and height
        self.constants = Constants()
        self.width = width
        self.height = height
        # we store a terrain object as attribute to be able to check the collisions depending on the level.
        # Not set as private as it will be required to be changed throughout the game
        self.levels = Terrain()
        # Stores the collision of the Entity
        self.tilemap_collisions = ""
        self.difference = 0
        # Store entity's x , y position, the amount of lives and if it is falling or not and the jump status
        self.x = x
        self.y = y
        self.lives = lives
        self.falling = True
        self.jumping = False

    def falling_fnc(self):
        # If the enemy is allowed to fall we subtract the y position
        if self.falling:
            self.y += 4

    def update_entity(self):
        # we update the entity checking its collision with the tile-map and
        # executing the falling method if it is possible
        self.collisions_check()
        self.falling_fnc()

    def checkcollisions_y(self, x: float, y: float, width: int, height: int):

        """:param x: x  position of the entity that is having its collision checked
            :param y: y position of the entity
            :param width: width of the entity
            :param height: height of the entity"""

        # The x and y position of the entities must be divided by eight to  adjust it to
        # the tile-map coordinates(32 X 32) and be able to analyze the corresponding tiles

        x_initial = int(x // 8)
        y_initial = int(y // 8)

        # We follow the same process by taking the x and y considering the height and width
        x_final = int((x + width) // 8)
        y_final = int((y + height) // 8)
        result = ""

        # We use a for loop to determine if any pixel of the entity coincides with a specific tile

        for y_ in range(y_initial, y_final + 1):
            for x_ in range(x_initial, x_final + 1):
                # Store the tile corresponding to the x_ and y_ that are being analyzed
                current_tile = self.levels.get_tile(self.constants.level,
                                                      x_, y_ - 1)
                # Check if it is on the ground or on the floor by taking different tiles
                if current_tile in self.levels.objects_collisions:
                    result = "Roof"

                current_tile = self.levels.get_tile(self.constants.level,
                                                      x_, y_)
                if current_tile in self.levels.objects_collisions:
                    result = "Floor"
        return result

    def check_collisions_x(self, x: float, y: float, width: int, height: int):
        # Follow the same process that in the other method. The only
        # difference is that now we are studying the wall collisions

        """:param x: x  position of the entity that is having its collision checked
        :param y: y position of the entity
        :param width: width of the entity
        :param height: height of the entity"""

        x_initial = int(x // 8)
        y_initial = int(y // 8)
        x_final = int((x + width + 1) // 8)
        y_final = int((y + height - 1) // 8)
        result = ""

        for y_ in range(y_initial, y_final + 1):
            for x_ in range(x_initial, x_final + 1):

                current_tile = self.levels.get_tile(self.constants.level,
                                                    x_ + 1, y_)
                if current_tile == self.levels.pipe or current_tile == self.levels.brick:
                    result = "Right"

                current_tile = self.levels.get_tile(self.constants.level, x_ - 1, y_)
                if current_tile == self.levels.pipe or current_tile == self.levels.brick:
                    result = "Left"
        return result

    def collisions_check(self):
        # We mix the collisions of the x and y-axis and control the entity depending on the detected collision
        check_y = self.checkcollisions_y(self.x, self.y, self.width, self.height)
        check_x = self.check_collisions_x(self.x, self.y, self.width, self.height)
        self.tilemap_collisions = ""
        # We store the corresponding collision in an attribute to be able to use it later(tilemap_collisions)

        if check_y == "Floor":
            # If the entity is on the floor falling is cancelled ,and we allow the entity to jump again
            self.tilemap_collisions = "Floor"
            self.difference = 0
            self.falling = False
            self.jumping = False

        elif check_y == "Roof":
            # if the entity is on the roof then we force the entity to fall
            self.tilemap_collisions = "Roof"
            self.falling = True
            self.difference = 0
            self.jumping = False

        else:
            self.falling = True

        if check_x == "Right":
            self.tilemap_collisions = "Right"

        elif check_x == "Left":
            self.tilemap_collisions = "Left"

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        if not isinstance(width,int):
            raise TypeError("The width of the entity must be an integer")
        elif width <= 0:
            raise ValueError("The width should be a positive value")
        else:
            self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if not isinstance(height, int):
            raise TypeError("The width of the entity must be an integer")
        elif height <= 0:
            raise ValueError("The width should be a positive value")
        else:
            self.__height = height

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self,posx):
        if isinstance(posx, int) or isinstance(posx,float):
            self.__x = posx
        else:
            raise TypeError("The introduced value for the x position is incorrect")

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, posy):
        if isinstance(posy, int) or isinstance(posy, float):
            self.__y = posy
        else:
            raise TypeError("The introduced value for the x position is incorrect")

    @ property
    def lives(self):
        return self.__lives

    @ lives.setter
    def lives(self, health):
        if not isinstance(health, int):
            raise TypeError("The lives of the entity must be an integer")

        else:
            self.__lives = health

    @ property
    def falling(self):
        return self.__falling

    @falling.setter
    def falling(self,fall):
        if not isinstance(fall, bool):
            raise TypeError("The falling value of the Entity must be a boolean")
        else:
            self.__falling = fall

    @ property
    def tilemap_collisions(self):
        return self.__tilemap_collisions

    @tilemap_collisions.setter
    def tilemap_collisions(self,col):
        if not isinstance(col,str):
            raise TypeError("The collision of the entity must be a string")

        elif col != "Floor" and col!= "Roof" and col!="Right" and col!= "Left" and col != "":
            raise ValueError("The collision value for the Entity is incorrect")
        else:
            self.__tilemap_collisions = col

    @ property
    def difference(self):
        return self.__difference

    @ difference.setter
    def difference(self,dif):
        if not isinstance(dif,int) and not isinstance(dif,float):
            raise TypeError("The difference attribute should be a number")
        elif dif < 0:
            raise ValueError("The difference attribute cannot be negative")
        else:
            self.__difference = dif

    @ property
    def jumping(self):
        return self.__jumping

    @ jumping.setter
    def jumping(self,leap):
        if not isinstance(leap,bool):
            raise TypeError("The jumping status must be a boolean")
        else:
            self.__jumping = leap

    @ property
    def constants(self):
        return self.__constants

    @ constants.setter
    def constants(self, const):
        if not isinstance(const, Constants):
            raise TypeError("The Constants for an Entity must be obtained from the Constants class")
        else:
            self.__constants = const
