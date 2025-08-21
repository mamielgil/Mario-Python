import pyxel
from Constants import Constants
from Mario import Mario
from Terrain import Terrain
import random
from Coin import Coin
from Enemy1 import Enemy1
from Enemy2 import Enemy2
from Enemy3 import Enemy3
from Pow import Pow


class Game:

    # This class contains the main methods to execute the game as well as the collision of some fundamental objects
    def __init__(self):
        # we store the in-game constants,the Mario, the terrain and the pow
        self.__constants = Constants()
        self.__mario = Mario(self.__constants.width / 2, self.__constants.height - 36, 3, 16, 24)
        self.__terrain = Terrain()
        self.__pow = Pow(128, 132, 3)

        # We store the corresponding lists and counters to control the amount of elements spawned. Set them as private
        # as we want them to be read only in the main program
        self.__coins_list = []
        self.__coins_spawned = 0
        self.__enemies_list = []
        self.__enemies_spawned = 0
        self.__enemies_killed = 0
        # we execute the game with the constants class values and load the sprites
        pyxel.init(self.__constants.width, self.__constants.height, title="Mario Bros", fps=self.__constants.fps)
        pyxel.load("./assets/Sprites.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        # There will be enemies generated only on the four established levels

        if 0 <= self.__constants.level < 4:
            self.__enemies_list = self.__enemies_hit_tube()
            enemies_col, self.__enemies_list = self.__mario.enemies_kill_knocked(self.__enemies_list)

        else:
            enemies_col = False

        # we update Mario
        self.__mario.update()

        # We check if the POW has been hit
        self.__pow_activation()

        # We check if any of the coins have been hit from below and also the collisions with Mario
        self.__coins_list = self.__coins_hit_tube()
        coin_points, self.__coins_list = self.__mario.collision_coins(self.__coins_list)

        if enemies_col:
            # If a collision has been detected the corresponding amount of points will be added
            self.__constants.points += 500
            # We keep count of the amount of enemies that have been killed
            self.__enemies_killed += 1

        if coin_points:
            # Add points if Mario has got a coin
            self.__constants.points += 100

        if self.__mario.lives == 0:
            # If mario loses all its lives the game is reset
            self.__reset()

    def draw(self):
        # we draw the level and the enemies and coins(entities).We also check if it is required to change of level
        pyxel.cls(self.__constants.backcolor)
        self.level()
        self.__change_level()
        self.__mario.draw()
        self.__load_entity()
        # Show the points that the player has
        pyxel.text(30, 10, "Points: " + str(self.__constants.points), 10)

    def level(self):
        # This method draws the corresponding level and manages the ending of the game
        self.__terrain.draw(self.__constants.level)
        if self.__terrain.reward_counter == 0:
            # When the counter of the coin level ends the initial screen is shown ,and we reset all parameters
            self.__constants.level = 5
            self.__reset()
            self.__pow.x = 128
            self.__pow.y = 132
            self.__coins_list.clear()
        if self.__constants.level == 5 and self.__constants.points != 0:
            pyxel.text(60, 168, "CONGRATULATIONS!, YOUR FINAL SCORE WAS:" + str(self.__constants.points), 10)

    # We require to generate the coins once the levels has been initialized
    # as well as its collisions with Mario

    def __determine_coins(self, level: int):
        # This method is in charge of generating the coins that are going to be spawned in the map
        """:param level: level that is being analyzed"""
        level_n = level
        if 0 <= level_n < 4:
            spawn1 = (16, 16)
            spawn2 = (16, 232)
            spawn_list = [spawn1, spawn2]
            coin_generated1 = Coin(spawn_list[0][0], spawn_list[0][1], 16, 16, 1, True)
            coin_generated2 = Coin(spawn_list[1][0], spawn_list[1][1], 16, 16, 1, True)
            return coin_generated1, coin_generated2

    def __generate_coins(self, level: int):
        # This method takes the generated coins from the determine coins methods and takes randomly one of them to give
        # more variety to the spawn

        """:param level: level in which the coins are going to be generated"""
        level_n = level
        coin_generated1, coin_generated2 = self.__determine_coins(level_n)
        if pyxel.frame_count % 100 == 0 and self.__coins_spawned < 15:

            # if a certain time is reached and 15 coins has still not been generated on that level then another one
            # will be generated
            self.__coins_spawned += 1
            random_n = random.randint(0, 1)
            if random_n == 1:

                coin_generated1.constants.level = self.__constants.level
                self.__coins_list.append(coin_generated1)
            else:
                coin_generated2.constants.level = self.__constants.level
                self.__coins_list.append(coin_generated2)
        # Return the coins list with the new generated coins
        return self.__coins_list

    def __determine_enemy(self, level: int):
        """:param level: level that is going to be analyzed"""
        # This method sets the enemies that are going to be spawned depending on the level
        level_n = level
        spawn1 = (224, 8)
        spawn2 = (24, 8)
        spawn_list = [spawn1, spawn2]

        if level_n == 0:
            # In the first level only turtles will be generated
            enemy_generated1 = Enemy1("Left", spawn_list[0][0], spawn_list[0][1], 1, 16, 16)
            enemy_generated2 = Enemy1("Right", spawn_list[1][0], spawn_list[1][1], 1, 16, 16)

        elif level_n == 1:
            # In the second level we only generate crabs
            enemy_generated1 = Enemy2("Left", spawn_list[0][0], spawn_list[0][1], 2, 16, 16)
            enemy_generated2 = Enemy2("Right", spawn_list[1][0], spawn_list[1][1], 2, 16, 16)

        elif level_n == 2:
            # In the third level we only generate flies
            spawn2 = (16, 16)
            spawn1 = (224, 16)
            spawn_list = [spawn1, spawn2]
            enemy_generated1 = Enemy3("Left", spawn_list[0][0], spawn_list[0][1], 1, 16, 16)
            enemy_generated2 = Enemy3("Right", spawn_list[1][0], spawn_list[1][1], 1, 16, 16)

        elif level_n == 3:
            spawn1 = (24, 8)
            spawn2 = (224, 8)
            spawn_list = [spawn1, spawn2]
            random_num = random.randint(0, 2)
            # In the last level we randomly generate enemies depending on a random number
            if random_num == 0:
                enemy_generated1 = Enemy3("Right", spawn_list[0][0], spawn_list[0][1], 1, 16, 16)
                enemy_generated2 = Enemy2("Left", spawn_list[1][0], spawn_list[1][1], 2, 16, 16)
            elif random_num == 1:
                enemy_generated1 = Enemy1("Right", spawn_list[0][0], spawn_list[0][1], 1, 16, 16)
                enemy_generated2 = Enemy2("Left", spawn_list[1][0], spawn_list[1][1], 2, 16, 16)
            else:
                enemy_generated1 = Enemy1("Right", spawn_list[0][0], spawn_list[0][1], 1, 16, 16)
                enemy_generated2 = Enemy3("Left", spawn_list[1][0], spawn_list[1][1], 1, 16, 16)
        else:
            # if it is another level, for example the ending or the beginning screen then no enemies will be generated
            enemy_generated1 = 0
            enemy_generated2 = 0
            # Store the two enemies that have been selected to be generated
        return enemy_generated1, enemy_generated2

    def __generate_enemies(self, level: int):
        """:param level: level in which the enemies are going to be generated"""
        # This method takes the enemies that have been selected in the determine enemy method and
        # stores them in the final list
        level_n = level
        enemy_generated1, enemy_generated2 = self.__determine_enemy(level_n)

        if pyxel.frame_count % 150 == 0 and self.__enemies_spawned < 31 and self.__constants.level < 4:
            # Check that the enemies that have been printed are smaller than 30 and that we are in a valid level
            self.__enemies_spawned += 1
            random_n = random.randint(0, 1)
            # We randomly select one of the enemies that were previous generated to be the one that spawns
            if random_n == 1:
                # We guarantee that each enemy generated works with the
                # level that has been generated
                enemy_generated1.constants.level = self.__constants.level
                self.__enemies_list.append(enemy_generated1)
            else:
                enemy_generated2.constants.level = self.__constants.level
                self.__enemies_list.append(enemy_generated2)

        # return final enemy list
        return self.__enemies_list

    def __enemies_hit_tube(self):
        # This method checks if any of the enemies of the map has been hit by a pipe
        for counter in range(len(self.__enemies_list)):
            verified = False
            # We first check that Mario has hit a tube
            tube_hit = self.__mario.tube_hit(self.__enemies_list[counter].x, self.__enemies_list[counter].y)
            if tube_hit:
                # If the tube has been hit and the enemy was knocked then it stands up and if it was not knocked then
                # it gets knocked.We use the verify variable to avoid fulfilling both conditions at the same time

                if self.__enemies_list[counter].knocked:
                    verified = True
                    self.__enemies_list[counter].knocked = False

                if self.__enemies_list[counter].lives <= 1 and not verified:
                    self.__enemies_list[counter].knocked = True
                self.__enemies_list[counter].lives -= 1
            else:
                # If mario did not hit a tube but the enemy is knocked then we will determine when the enemy is going to
                # stand up again and get empowered
                if self.__enemies_list[counter].knocked:
                    self.__enemies_list[counter].change_sprite()

        return self.__enemies_list

    def __coins_hit_tube(self):
        # This method eliminates the coins that Mario has hit with the tube

        delete = 0
        for counter in range(len(self.__coins_list)):
            # We check if Mario has hit a pipe
            tube_hit = self.__mario.tube_hit(self.__coins_list[counter - delete].x,
                                             self.__coins_list[counter - delete].y)
            if tube_hit:
                # If mario has hit a pipe we delete the corresponding element from the list ,and we add one to delete
                # which corrects the index that is being analyzed after an element has been deleted
                self.__coins_list.pop(counter - delete)
                delete += 1
                self.__constants.points += 100

        return self.__coins_list

    def __load_entity(self):
        # This method updates all the entities that are in the map
        if self.__constants.level < 4:
            # We obtain the list of enemies and coins
            generated_coins = self.__generate_coins(self.__constants.level)
            generated_enemies = self.__generate_enemies(self.__constants.level)

            for counter in range(len(generated_enemies)):
                # we update each of the enemies of the map which also includes the drawing aspect
                generated_enemies[counter].update()

            for counter in range(len(generated_coins)):
                # All the map coins are updated and drawn
                generated_coins[counter].draw()
                generated_coins[counter].update()
        else:
            for counter in range(len(self.__coins_list)):
                # In the case that we are not in an enemy level, only the coins will be updated
                self.__coins_list[counter].draw()
                self.__coins_list[counter].update()
        # We draw the pow block
        self.__pow.draw()

    def __reset(self):
        # This method is used to reset all the in-game parameters after the game has ended or the player has lost
        if self.__mario.lives == 0:
            # If the player loses it loses all its points and we reset the lives
            self.__mario.lives = 3
            self.__constants.points = 0
        # we empty all the lists and set all the spawn and killed attributes to 0
        self.__enemies_list.clear()
        self.__coins_list.clear()
        self.__enemies_spawned = 0
        self.__enemies_killed = 0
        self.__coins_spawned = 0
        # we generate Mario on the initial position
        self.__mario = Mario(self.__constants.width / 2, self.__constants.height - 36, 3, 16, 24)
        # We update Mario's level
        self.__mario.constants.level = self.__constants.level
        # We update the Pow's uses and set the final countdown to 20(final level)
        self.__pow.uses = 3
        self.__terrain.reward_counter = 20

    def __pow_activation(self):
        # Checks if Mario has hit the POW if the POW block is in the map
        if self.__pow.visible:

            self.__pow.collision = self.__mario.pow_collision(self.__pow.x, self.__pow.y, self.__pow.width,
                                                              self.__pow.height)
            pow_check = self.__pow.pow_explosion()
            # If mario has hit the POW we analyze each of the enemies that are on the map and check if they are
            # on the ground.
            if pow_check == "Pow":
                for counter in range(len(self.__enemies_list)):
                    enemy = self.__enemies_list[counter]
                    # We store the collision value of each of the enemies
                    floor_check = enemy.checkcollisions_y(enemy.x, enemy.y, enemy.width, enemy.height)

                    # If they are on the floor, they get knocked
                    if floor_check == "Floor":
                        self.__enemies_list[counter].knocked = True
                        self.__enemies_list[counter].lives = 0

    def __change_level(self):
        # This method controls the change of level and resets all the parameters to the corresponding default values

        if self.__constants.level == 5 and self.__pow.uses == 0:
            self.__constants.level = 0
            self.__constants.points = 0
            self.__reset()
            terrain = Terrain()
            terrain.constants.level = 0
            self.__pow.x = 120
            self.__pow.y = 60

        if self.__enemies_killed >= 5 and self.__constants.level == 0:
            self.__constants.level = 1
            self.__reset()
            terrain = Terrain()
            terrain.constants.level = 1
            self.__pow.x = 112
            self.__pow.y = 104

        elif self.__enemies_killed >= 5 and self.__constants.level == 1:
            self.__constants.level = 2
            self.__reset()
            terrain = Terrain()
            terrain.constants.level = 2
            self.__pow.x = 120
            self.__pow.y = 104

        elif self.__enemies_killed >= 5 and self.__constants.level == 2:
            self.__constants.level = 3
            self.__reset()
            terrain = Terrain()
            terrain.constants.level = 3
            self.__pow.x = 120
            self.__pow.y = 124

        elif self.__enemies_killed >= 5 and self.__constants.level == 3:
            self.__constants.level = 4
            self.__reset()
            self.__pow.uses = 0
            # If the player finishes the game we show them the final reward
            self.__generate_final_reward()

    def __generate_final_reward(self):
        # This method generated the static coins from the final level
        static_coins = []
        # To be able to work with tiles we need to divide by eight  to work with the tiles coordinates
        y_final = self.__constants.height // 8
        x_final = self.__constants.width // 8
        for y in range(0, y_final):

            for x in range(0, x_final, 2):
                # We perform a for loop to print a coin only on the tiles that correspond to ground level
                get_tile = self.__terrain.get_tile(self.__constants.level, x, y + 1)

                if get_tile == self.__terrain.pipe or get_tile == self.__terrain.brick:
                    generated = Coin(x * 8, y * 8 - 8, 16, 16, 1, False)
                    static_coins.append(generated)
            # We store the coins generated
            self.__coins_list = static_coins


# As all attributes are private they do not require setters
