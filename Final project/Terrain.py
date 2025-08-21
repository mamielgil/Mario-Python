"Created by Miguel Amiel Gil"
import pyxel
from Constants import Constants


class Terrain:

    def __init__(self):
        # We define as attributes the constants object and the counter for the ending level
        self.constants = Constants()
        self.reward_counter = 20

    def get_tile(self, n_tilemap: int, tile_x: float, tile_y: float):

        # This method returns the position of a certain tile. This position
        # is shown in coordinates corresponding to the image bank of the
        # tile-map
        return pyxel.tilemaps[n_tilemap].pget(tile_x, tile_y)

    def draw(self, level: int):
        """:param level: level that is going to be drawn"""
        level_n = level
        # We print the tile-map
        pyxel.bltm(0, 0, level_n, 0, 0, self.constants.width, self.constants.height)

        self.constants = Constants()
        # We check if any of the tiles need to be changed due to having been hit
        self.__change_tile_hit(level_n)

        if level_n == 4:
            # Text shown in the last level
            pyxel.text(88, 208, "CONGRATULATIONS!", 12)
            pyxel.text(160, 208, "Time remaining:" + str(self.reward_counter), 12)

            if pyxel.frame_count % self.constants.fps == 0:
                # Performs a counter of 20 seconds for the final screen
                self.reward_counter -= 1

        elif level_n == 5:
            # In the initial screen this text is shown
            pyxel.text(72, 208, "JUMP ON THE POW 3 TIMES TO START!", 12)

    def __change_tile_hit(self, level: int):

        """:param level: level that is going to be drawn"""
        # This method is used to be able to change the tiles that have been hit by Mario when trying to kill an enemy
        level_n = level

        # Convert the entity's position into tile-map coordinates
        x_final = self.constants.width // 8
        y_final = self.constants.height // 8

        if pyxel.frame_count % 30 == 0:
            # After a certain amount of time the tiles that were changed due to Mario's hit are reestablished
            for counter in range(0, x_final):

                for number in range(0, y_final):
                    tile = self.get_tile(level_n, counter, number)
                    if tile == self.pipe_hit1:
                        pyxel.tilemaps[level_n].pset(counter, number,self.background)

                    if tile == self.pipe_hit2 or tile == self.pipe_hit3 or tile == self.pipe_hit4:
                        pyxel.tilemaps[level_n].pset(counter, number, self.pipe)

    # We set the tuples with the tile positions as only-read attributes as they must not be changed
    @ property
    def brick(self):
        return 6, 13

    @property
    def pipe(self):
        return 9, 13

    @property
    def pipe_hit1(self):
        return 7, 15

    @property
    def pipe_hit2(self):
        return 7, 16

    @property
    def pipe_hit3(self):
        return 6, 16

    @property
    def pipe_hit4(self):
        return 8, 16

    @ property
    def revive_platform(self):
        return 0, 16

    @property
    def objects_collisions(self):
        return (self.brick, self.pipe, self.pipe_hit1, self.pipe_hit2,
                self.pipe_hit3,self.pipe_hit4,self.revive_platform)

    @property
    def background(self):
        return 0, 0

    @property
    def constants(self):
        return self.__constants

    @constants.setter
    def constants(self, const):
        if not isinstance(const, Constants):
            raise TypeError("The Constants for the terrain must be obtained from the Constants class")
        else:
            self.__constants = const

    @ property
    def reward_counter(self):
        return self.__reward_counter

    @ reward_counter.setter
    def reward_counter(self,count):
        if not isinstance(count, int):
            raise TypeError("The reward counter must be an integer")

        elif count < 0:
            raise ValueError("The reward counter must be positive")
        else:
            self.__reward_counter = count