import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 11
GAME_HEIGHT = 11

#### Put class definitions here ####
class Character(GameElement):
    IMAGE = "Girl"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = False

    def interact(self, player):
        GAME_BOARD.draw_msg("Congratulations! You win!")

class BlueGem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("you just acquired a blue gem! You have %d blue gems!" %(len(player.inventory)))

class GreenGem(GameElement):
    IMAGE = "GreenGem"
    SOLID = False

    def interact(self, player):
        print PLAYER.x, PLAYER.y

        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(0, 0, PLAYER)
        print PLAYER.x, PLAYER.y

        GAME_BOARD.draw_msg("You touched a reset gem and have been moved to the start.")

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    ###Directions
    GAME_BOARD.draw_msg("Reach the treasure chest to win the game!")

    ###Player
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 1, PLAYER)
    print PLAYER

    ###Obstacles
    rock_positions  = [
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
    rocks[-1].SOLID = False

    tall_tree_positions = [
        ]

    tall_trees = []
    for pos in tall_tree_positions:
        tree = TallTree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        tall_trees.append(tree)

    for character in game_map:
        if character == T:
            tree = TallTree()
            GAME_BOARD.register(tree)
            GAME_BOARD.set_el()
        

    ####Gems
    bluegem1 = BlueGem()
    GAME_BOARD.register(bluegem1)
    GAME_BOARD.set_el(3, 1, bluegem1)

    resetgem1 = GreenGem()
    GAME_BOARD.register(resetgem1)
    GAME_BOARD.set_el(4, 4, resetgem1)

    ####PRIZE
    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(10, 9, chest)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"

    elif KEYBOARD[key.DOWN]:
        direction = "down"

    elif KEYBOARD[key.LEFT]:
        direction = "left"

    elif KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]


        #block players from moving off of the board
        if (next_x) >= GAME_WIDTH:
            next_x -= 1
        elif (next_x) < 0:
            next_x = 0
        if (next_y) >= GAME_HEIGHT:
            next_y -= 1
        elif (next_y) < 0:
            next_y = 0

        #figure out if there is a game element in the square you are moving to
        existing_el = GAME_BOARD.get_el(next_x, next_y)

        #if there is nothing there, or if the thing there is not solid
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
        #if there is something there, interact with it.
        if existing_el:
            existing_el.interact(PLAYER)


