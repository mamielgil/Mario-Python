
import pyxel
from Sprite import Sprite
from Entities import Entity
from Terrain import Terrain


class Mario(Entity):

    def __init__(self, x: int, y: int, lives: int, width: int, height: int):
        """:param x: initial x position of Mario
            :param y: initial y position of Mario
            :param lives: amount of lives that Mario has
            :param width: width of Mario
            :param height: height of  Mario"""

        super().__init__(x, y, lives, width, height)
        # We define the number of lives for Mario and its x and y speed as well as the collisions
        self.lives = 3
        self.speed_x = 2
        self.speed_y = 72
        self.tilemap_collisions = ""
        self.__IE_collisions = ""

        # This Mario attributes are used to create the jump of  the character
        self.jumping = False
        self.__previous_y = self.y
        self.difference = 0

        # Here we define the different sprites that Mario will use
        self.__sprite_static_right = Sprite(self.x, self.y, 0, 0, 8,
                                            self.width, self.height)
        self.__sprite_jumping_left = Sprite(self.x, self.y, 0, 64, 8, -self.width, self.height)
        self.__sprite_jumping_right = Sprite(self.x, self.y, 0, 64, 8, self.width, self.height)

        self.__sprite_left = [Sprite(self.x, self.y, 0, 16, 8, -self.width, self.height),
                              Sprite(self.x, self.y, 0, 32, 8, -self.width, self.height),
                              Sprite(self.x, self.y, 0, 48, 8, -self.width, self.height),
                              Sprite(self.x, self.y, 0, 0, 8, -self.width, self.height)]

        self.__sprite_right = [Sprite(self.x, self.y, 0, 16, 8, self.width, self.height),
                               Sprite(self.x, self.y, 0, 32, 8, self.width, self.height),
                               Sprite(self.x, self.y, 0, 48, 8, self.width, self.height),
                               self.__sprite_static_right]
        self.__counter = 0

        # We create this direction attribute to know to which side Mario is moving and being able to change its sprite
        self.__direction = ""

        # Final sprite is the attribute that stores at each moment the
        # sprite that Mario will carry depending on the tilemap_collisions that he is
        # following

        self.__final_sprite = self.__sprite_static_right

    def update(self):
        # Every frame the tilemap_collisions and collision methods are checked as well as Mario's movement
        self.change_sprite()
        self.collisions_check()
        self.__jump()
        self.__move()
        self.__control_movement()

    def draw(self):
        # we show on the screen the number of Mario's lives and calculate the sprite that will be shown
        self.__final_sprite.draw(self.x, self.y)
        for lives in range(self.lives):
            pyxel.blt(160 + 8 * lives, 8, 0, 8, 0, 8, 8)

    def __move(self):
        self.__direction = ""
        # We establish the different conditions for Mario's movement in function of the user's input and the collisions

        if ((pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT)) and
                (self.tilemap_collisions != "Left") and self.__IE_collisions != "Left"):

            # If Mario is not colliding with the pow or with a wall it is allowed to move to the left
            self.x -= self.speed_x

            # We indicate that Mario is moving to the left for the sprite
            self.__direction = "L"

            if self.jumping or self.falling:
                # If Mario is falling or jumping the sprite will be updated
                self.__final_sprite = self.__sprite_jumping_left

        if ((pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT)) and
                self.tilemap_collisions != "Right" and self.__IE_collisions != "Right"):

            # If Mario is not colliding with the pow or with a wall it is allowed to move to the right
            self.x += self.speed_x
            # We indicate that Mario is moving to the right
            self.__direction = "R"

            if self.jumping or self.falling:

                # If Mario is falling or jumping the sprite will be updated
                self.__final_sprite = self.__sprite_jumping_right

    def __control_movement(self):
        # We control that Mario is not able to exit the screen
        if self.x + self.width > self.constants.width:

            self.x = self.width
        elif self.x < 0:

            self.x = self.constants.width - self.width

    def __jump(self):
        # This methof is in charge of executing Mario's jump
        if ((pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP)) and
                (self.difference == 0 and not self.jumping) and not
                self.falling):

            # If Mario is not jumping or falling then if the user will be able to jump
            self.jumping = True
            self.falling = True

            # Save the original y position in case that the player wants to jump on the same y
            self.__previous_y = self.y
            self.__final_sprite = self.__sprite_jumping_right

        if self.difference < self.speed_y and self.jumping is True:

            # Mario will keep going up until the difference corresponds to the established y speed
            self.y -= 4
            self.difference = abs(self.y - self.__previous_y)

        if self.difference == self.speed_y:

            # If Mario has reached the peak then stops jumping
            self.jumping = False

        if not self.jumping:

            # If the jumping has stopped then Mario will fall
            self.falling_fnc()

    def collision_coins(self, coins_list: list):
        """:param coins_list: corresponds to the list of coins that are in the level"""

        # This method checks the collision between Mario and the coins
        # We store the width and height of Mario
        w = self.width
        h = self.height

        # We create a list that stores the indexes of the coins that are going to be deleted
        del_index = []

        # delete corrects the index that is being analyzed after having eliminated a coin
        delete = 0
        collisions = False

        x_initial = self.x
        # We store the x and y of Mario both the initial and the final(considering height and width)
        x_final = self.x + w - 1
        y_final = self.y + h // 2
        for counter in range(len(coins_list)):
            result = "NO"
            coin = coins_list[counter]

            # We check the several conditions that would correspond to a coin collision
            if ((coin.x + coin.width > x_initial > coin.x) and
                    (y_final > coin.y and y_final + h // 2 <= coin.y + coin.height)):

                result = "Coin"

            elif ((coin.x < x_final < coin.x + coin.width)
                  and (y_final > coin.y and y_final + h // 2 <= coin.y + coin.height)):

                result = "Coin"

            if result == "Coin":
                # If a coin has been detected then the index of that coin is stored and the collision is set to True
                del_index.append(counter)
                collisions = True

        if len(del_index) > 0:
            for element in del_index:
                # We take all the indexes that were a collision and delete them from the coins list.
                coins_list.pop(element - delete)
                delete += 1

        # We return the collision status and the coins list
        return collisions, coins_list

    def enemies_kill_knocked(self, enemies_list: list):
        """:param enemies_list: list containing the enemies of the level"""
        # This method is used to check if Mario has collided with a knocked enemy
        w = self.width
        h = self.height
        # Follow same process that with the coins
        del_index = []
        delete = 0
        collisions = False

        x_initial = self.x

        x_final = self.x + w - 1
        y_final = self.y + h // 2
        for counter in range(len(enemies_list)):
            result = "NO"

            # Check several conditions with the enemies to detect the collision
            enemy = enemies_list[counter]

            if ((enemy.x + enemy.width > x_initial > enemy.x) and
                    (y_final > enemy.y and y_final + h // 2 <= enemy.y + enemy.height)):

                if enemy.knocked:
                    result = "Enemy"
                else:
                    self.lives -= 1
                    self.y = 8
                    self.x = 120

            elif ((enemy.x < x_final < enemy.x +
                   enemy.width) and (y_final > enemy.y and y_final + h // 2 <= enemy.y + enemy.height)):

                if enemy.knocked:
                    result = "Enemy"
                else:
                    self.lives -= 1
                    self.y = 8
                    self.x = 120

            if result == "Enemy":

                # We store the index position in which the enemy that was hit is if and only if the enemy has one
                # life remaining if not we subtract one from it
                if enemy.lives <= 0:
                    del_index.append(counter)
                    collisions = True

        if len(del_index) > 0:
            for element in del_index:
                # Those enemies that were hit and had one life are eliminated. We use the delete variable to adjust the
                # index to the correct position that needs to be analyzed after having deleted element from the list
                enemies_list.pop(element - delete)
                delete += 1

        # We return the enemies list and the collision status
        return collisions, enemies_list

    def pow_collision(self, x: float, y: float, width: int, height: int):
        """:param x: POW's x position
            :param y: POW's y position
            :param width: POW's width
            :param height: POW's height"""

        # This method detects if Mario has activated the POW block
        collision = False

        # We store Mario's x and y position both initial and final
        x_initial = x
        y_initial = y
        x_final = x + width
        y_final = y + height
        self.__IE_collisions = ""

        # We check the several conditions to see if Mario has collided with the POW
        if self.y == y_final:
            if x_initial - 16 <= self.x <= x_final:
                self.falling = True
                self.difference = 0
                self.jumping = False

            if x_initial - 8 <= self.x <= x_final - 4:
                collision = True
                self.falling = True
                self.difference = 0
                self.jumping = False

        if x_initial - 4 <= self.x + self.width <= x_initial:
            if y_initial <= self.y + 12 <= y_final:
                self.__IE_collisions = "Right"
        if x_final <= self.x <= x_final + 4:
            if y_initial <= self.y + 12 <= y_final:
                self.__IE_collisions = "Left"

        return collision

    def change_sprite(self):
        # Depending on how Mario is moving we establish one list of sprites

        if not self.jumping and not self.falling:
            select = ""
            if self.__direction == "R":
                select = self.__sprite_right
            elif self.__direction == "L":
                select = self.__sprite_left

            if self.__direction == "R" or self.__direction == "L":

                if pyxel.frame_count % 1 == 0:
                    self.__counter += 1

                if self.__counter + 1 == len(select):
                    # The counter attribute allows to change the index of the sprites list
                    self.__counter = 0
                self.__final_sprite = select[self.__counter]
            else:
                self.__final_sprite = self.__sprite_static_right

    def tube_hit(self, x: float, y: float):
        # This method is used to check if Mario is hitting an enemy below a pipe
        posx = x
        posy = y

        # We store the x and y position as well as the Terrain class to analyze the corresponding tiles
        terrain_check1 = Terrain()

        # We check if Mario collapses with the tile associated to its position
        terrain_check2 = terrain_check1.get_tile(self.constants.level, self.x // 8, (self.y - 10) // 8)
        collision = False
        if posx - self.width <= self.x <= posx + self.width:

            if (self.y - self.height >= posy and self.y < posy + self.width + 16
                    and terrain_check2 == terrain_check1.pipe):

                # We store the tile positions in coordinates of the tile-map
                # to be able to change the sprite
                save_x = self.x // 8
                save_x2 = (self.x - 8) // 8
                save_x3 = (self.x + 8) // 8
                save_y = (self.y - 10) // 8
                save_y2 = (self.y - 18) // 8
                collision = True

                # We change the corresponding tiles of the pipe  to the hit status

                tile_left = terrain_check1.get_tile(self.constants.level, save_x2, save_y)
                tile_right = terrain_check1.get_tile(self.constants.level, save_x3, save_y)
                pyxel.tilemaps[self.constants.level].pset(save_x, save_y, terrain_check1.pipe_hit2)
                pyxel.tilemaps[self.constants.level].pset(save_x, save_y2, terrain_check1.pipe_hit1)

                # Checking that the tile that will be changed does not correspond to the background tile(black)
                if tile_left != terrain_check1.background:
                    pyxel.tilemaps[self.constants.level].pset(save_x2, save_y, terrain_check1.pipe_hit3)

                if tile_right != terrain_check1.background:
                    pyxel.tilemaps[self.constants.level].pset(save_x3, save_y, terrain_check1.pipe_hit4)
            else:
                # We return the collision value
                collision = False
        return collision

    # Here we have the setters that control the value of the different attributes that Mario has.Most of the setters are
    # defined in the entities mother class

    @property
    def speed_y(self):
        return self.__speed_y

    @speed_y.setter
    def speed_y(self, speed_y):
        if not isinstance(speed_y, int) and not isinstance(speed_y, float):

            raise TypeError("The y speed must be a number")
        elif speed_y % 4 != 0:

            raise ValueError("The y speed must be a multiple of 4")
        elif speed_y <= 0:

            raise ValueError("The y speed must be a positive number")
        else:
            self.__speed_y = speed_y

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, health):
        if not isinstance(health, int):
            raise TypeError("The number of lives for Mario must be an integer bigger than 0")
        elif health < 0:
            raise ValueError("The number of lives for Mario must a positive integer")
        else:
            self.__lives = health

    @property
    def speed_x(self):
        return self.__speed_x

    @speed_x.setter
    def speed_x(self, speed_x):
        if not isinstance(speed_x, int) and not isinstance(speed_x, float):

            raise TypeError("The y speed must be a number")
        elif speed_x <= 0:
            raise ValueError("The x speed must be positive")
        else:
            self.__speed_x = speed_x
