from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World

class PlayerAI:

    def __init__(self):
        """
        Any instantiation code goes here
        """
        pass
    def fill_adjacent_to_nest(self, world, friendly_units, enemy_units):
        friendly_positions = world.get_position_to_friendly_dict()
        min_health = [0,1000000000000000000]
        for unit in friendly_units:
            if unit.last_move_result == MoveResult.NEWLY_SPAWNED: #units that are newly spawned are positioned over a nest
               # if len(friendly_units) > 8:
                    for tile in world.get_friendly_tiles_around(unit.position):
                        if not (tile.position in friendly_positions): #Checks if any of the tiles around don't have a fly
                            world.move(unit, tile.position)
                            return 0
                    for tile in world.get_friendly_tiles_around(unit.position):
                        friend = friendly_positions[tile.position] #Loops over to find the friendly tile around that has a fly with the minimum health
                        if min_health[1] > friend.health:
                            min_health = [friend, friend.health]
                    world.move(unit, (min_health[0]).position)

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
        friendly_positions = world.get_position_to_friendly_dict()
        min_health = [0,1000000000000000000]
        for unit in friendly_units:
            if unit.last_move_result == MoveResult.NEWLY_SPAWNED:
               # if len(friendly_units) > 8:
                    for tile in world.get_friendly_tiles_around(unit.position):
                        if not (tile.position in friendly_positions):
                            world.move(unit, tile.position)
                            return 0
                    for tile in world.get_friendly_tiles_around(unit.position):
                        friend = friendly_positions[tile.position]
                        if min_health[1] > friend.health:
                            min_health = [friend, friend.health]
                    world.move(unit, (min_health[0]).position)

        # every firefly attacks enemy if one tile away


        # first 8
        # 1) first 2 will get closest tile
        # 2) third will build a nest 5 tiles away
        # 3) fourth will attack enemies nests
        # 4) fifth attack weakest enemies
        # 6) sixth get closest neutral tile
        # 7) seventh attacks enemy nests
        # 8) attack enemy tiles

        # more than 8
        # check that all 8 are still alive, otherwise send replacement
        # stock up on all 4 adjacent tiles around nest




