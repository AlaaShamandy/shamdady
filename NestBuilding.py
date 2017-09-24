from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World
from enum import Enum

class NestStatus(Enum):
    inProgress = 0
    notBuilding = 1

class PlayerAI:

    def __init__(self):
        """
            Any instantiation code goes here
            """
        self.centeredTilePosition = ()
        self.nests = 1
        self.nestStatus = NestStatus.notBuilding # status of nests
        self.tilesToCover = [] #tiles to cover to build nest
        self.nestBuilderUuid = 0


    def buildNest(self,world, friendly_unit):
        print(friendly_unit.position)
        # get friendly nests
        closest_nest = world.get_closest_friendly_nest_from(friendly_unit.position, None)

        if ((closest_nest[0] - friendly_unit.position[0]) >= 5 or (closest_nest[0] - friendly_unit.position[0]) <= -5) or ((closest_nest[1] - friendly_unit.position[1]) >= 5 or (closest_nest[1] - friendly_unit.position[1]) <= -5): # enough space to build another nest


            if (self.nestStatus == NestStatus.notBuilding):


                self.nestStatus = NestStatus.inProgress

                # closest place to build nest
                self.centeredTilePosition = world.get_closest_neutral_tile_from(friendly_unit.position, None).position
                tiles_around = world.get_tiles_around(self.centeredTilePosition)
                print("centered tile position: ", self.centeredTilePosition)



                self.tilesToCover = sorted([tile.position for tile in tiles_around.values()])


            # mark first tile
            if self.tilesToCover:

                print(self.tilesToCover)


                world.move(friendly_unit, self.tilesToCover[0])

                index = 1

                while friendly_unit.get_next_move_target() == self.centeredTilePosition and index >= 1:
                    world.move(friendly_unit, self.tilesToCover[index])
                    index=1


                if not self.tilesToCover: # done with building nests
                    self.nests = 1
                for position in self.tilesToCover:
                    if  world.get_tile_at(position).is_friendly():
                        self.tilesToCover.remove(position)




        else:
            # do something
            neutral_position = world.get_closest_neutral_tile_from(friendly_unit.position, None)
            world.move(friendly_unit, neutral_position.position)



    def do_move(self, world, friendly_units, enemy_units):
        """
            This method will get called every turn.

            :param world: World object reflecting current game state
            :param friendly_units: list of FriendlyUnit objects
            :param enemy_units: list of EnemyUnit objects
            """
        # Fly away to freedom, daring fireflies
        # Build thou nests
        # Grow, become stronger
        # Take over the world


        # every firefly attacks enemy if one tile away



        if len(world.get_friendly_nest_positions()) == 1:
            if self.nestBuilderUuid: # first time assigning a builder

                builder = world.get_unit(self.nestBuilderUuid)
                if builder: # making sure still alive
                    self.buildNest(world,builder )
                else:
                    self.nestBuilderUuid = 0

            else:
#                if len(friendly_units) >= 3:

                    self.nestBuilderUuid = friendly_units[0].uuid
                    self.buildNest(world, friendly_units[0])
