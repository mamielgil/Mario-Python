
class Constants:
    # We create this two variables as class variables to be able to be changed for the all the classes in which they
    # are going to be used

    def __init__(self):
        # Variables that are going to store the points for Mario and the level in which he is
        # Are going to be used in the rest of objects of the game
        self.level = 5
        self.points = 0

    # We establish the rest of attributes as only read attributes as we do not want them to be changed
    @ property
    def width(self):
        return 256

    @ property
    def height(self):
        return 256

    @ property
    def backcolor(self):
        return 0

    @ property
    def fps(self):
        return 30

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self,points_num):
        if type(points_num) != int:
            raise TypeError("The points for the player must be an integer number")
        else:
            self.__points = points_num

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level_n):
        if not isinstance(level_n, int):
            raise TypeError("The level you are working with must be an integer number")
        elif level_n < 0:
            raise ValueError("The level must be a positive integer number")
        else:
            self.__level = level_n




