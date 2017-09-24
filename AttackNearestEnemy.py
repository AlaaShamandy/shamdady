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

        for unit in friendly_units:
            closest_enemy = world.get_closest_enemy_from(unit.position, None)

            if (abs(closest_enemy.position[0] - unit.position[0]) == 1) or (abs(closest_enemy.position[1] - unit.position[1])) == 1:
                neighbors = list(world.get_neighbours(unit.position).values())
                if closest_enemy.position in neighbors:
                    world.move(unit, closest_enemy.position)




