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
        for unit in friendly_units:
            path = world.get_shortest_path(unit.position,
                                           world.get_closest_capturable_tile_from(unit.position, None).position,
                                           None)
            if path: world.move(unit, path[0])

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
            



