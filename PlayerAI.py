from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World

class PlayerAI:

    def __init__(self):
        """
        Any instantiation code goes here
        """
        self.doers = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    def fill_adjacent_to_nest(self, world, friendly_units):
        friendly_positions = world.get_position_to_friendly_dict()
        min_health = [0,1000000000000000000]
        for unit in friendly_units:

#            # Attack enemy if one tile away
# TODO need to do something with them or else they will do nothing
            closest_enemy = world.get_closest_enemy_from(unit.position, None)
            if (abs(closest_enemy.position[0] - unit.position[0]) == 1) and (abs(closest_enemy.position[1] - unit.position[1]) == 1):
                neighbors = list(world.get_neighbours(unit.position).values())
                if closest_enemy.position in neighbors:
                    world.move(unit, closest_enemy.position)
#                    self.doers.append(unit.uuid) #continue attacking in next calls of do_move
                    #continue







            if unit and  (unit.last_move_result == MoveResult.NEWLY_SPAWNED or unit.position == world.get_closest_friendly_nest_from(unit.position, None)): #units that are newly spawned are positioned over a nest
               # if len(friendly_units) > 8:
                    for tile in world.get_friendly_tiles_around(unit.position):
                        if not (tile.position in friendly_positions): #Checks if any of the tiles around don't have a fly : README : FRIENDLY_POSITIONS IS A DICTIONARY WITH THE LOCATION OF ALL FRIENDLY UNITS (CHECK ITS DECLARATION) SO IT DOES WHAT IT'S SUPPOSED TO DO
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
        for doer in self.doers: # mark place of dead doers
            if (doer != -1) and (not world.get_unit(doer)):
                self.doers[self.doers.index(doer)] = -1

        index = len(friendly_units) - 1
        while -1 in self.doers and index >= 0: # substituting dead flies with highest healths.
            if friendly_units[index].uuid not in self.doers:
                self.doers[self.doers.index(-1)] = friendly_units[index].uuid
            index -= 1


        friendly_units_copy = friendly_units[:]
        for index in range(len(self.doers)):
            unit = world.get_unit(self.doers[index])

            if unit:




                # Attack enemy if one tile away
                closest_enemy = world.get_closest_enemy_from(unit.position, None)
                if (abs(closest_enemy.position[0] - unit.position[0]) == 1) or (abs(closest_enemy.position[1] - unit.position[1]) == 1):
                    neighbors = list(world.get_neighbours(unit.position).values())
                    if closest_enemy.position in neighbors:
                        world.move(unit, closest_enemy.position)
                        continue


                if index < 4: #Collect closest tile
                    closest_tile = world.get_closest_capturable_tile_from(unit.position, None)
                    world.move(unit, closest_tile.position)
                elif index < 5: #will be buildNest later, for now it collect closest tile
                    closest_tile = world.get_closest_capturable_tile_from(unit.position, None)
                    world.move(unit, closest_tile.position)
                elif index < 6: #make attack nests only if we are winning by 20 points, otherwise collect closest tile
                    if (len(world.get_friendly_tiles()) - len(world.get_enemy_tiles()) >= 20):
                        enemy_nest_position = world.get_closest_enemy_nest_from(unit.position, None)
                        world.move(unit, enemy_nest_position)
                    else:
                        closest_tile = world.get_closest_capturable_tile_from(unit.position, None)
                        world.move(unit, closest_tile.position)

                elif index < 7: #attack enemy flies TODO CHECK IF THE ENEMY IS RIGHT NEXT TO A NEST CUZ IF SO IT DEFEATS THE GOAL OF ATTAKCING ONLY IF WE'RE WINNING
                    closest_enemy = world.get_closest_enemy_from(unit.position, None)
                    world.move(unit, closest_enemy.position)
                elif unit and index < 8: #Go after neutral tile, if none go after enemy tiles
                    closest_neutral_tile = world.get_closest_neutral_tile_from(unit.position, None)
                    if (closest_neutral_tile):
                        world.move(unit, closest_neutral_tile.position)
                    else:
                        enemy_tile = world.get_closest_capturable_tile_from(unit.position, None)
                        if (enemy_tile):
                            world.move(unit, enemy_tile.position)
                elif index < 13: #make attack nests only if we are winning by 20 points, otherwise collect closest tile #TODO MAKE IT SO THAT ONLY APPLIES IF IT'S THE LAST NEST
                    if (len(world.get_friendly_tiles()) - len(world.get_enemy_tiles()) >= 20):
                        enemy_nest_position = world.get_closest_enemy_nest_from(unit.position, None)
                        world.move(unit, enemy_nest_position)
                    else:
                        closest_tile = world.get_closest_capturable_tile_from(unit.position, None)
                        world.move(unit, closest_tile.position)
                else: #attacks enemy tiles
                    closest_tile = world.get_closest_enemy_tile_from(unit.position, None)
                    world.move(unit, closest_tile.position)

                # remove from friendly_units
                if (unit in friendly_units_copy):
                    friendly_units_copy.remove(unit)





        self.fill_adjacent_to_nest(world, friendly_units_copy)

        for unit in friendly_units:

            if unit.get_next_move_type() == MoveType.REST or unit.last_move_result in [MoveResult.MOVE_INVALID, MoveResult.BLOCKED_BY_NEST, MoveResult.BLOCKED_BY_WALL]:
                closest_nest = world.get_closest_friendly_nest_from(unit.position, None)
                if  (abs(closest_nest[0] - unit.position[0]) > 1) or  (abs(closest_nest[1] - unit.position[1]) > 1):
                    print("Yamaa")
                    closest_tile = world.get_closest_capturable_tile_from(unit.position, None)
                    world.move(unit, closest_tile.position)
                elif (world.get_tile_at(unit.position)).is_permanently_owned():
                    print("tabla")
                    closest_tile = world.get_closest_enemy_nest_from(unit.position, None)
                    world.move(unit, closest_tile)




        # every firefly attacks enemy if one tile away


        # first 8
        # 1) first 2 will get closest tile
        # 2) third will build a nest 5 tiles away
        # 3) fourth will attack enemies nests
        # 4) fifth attack weakest enemies
        # 6) sixth get closest neutral tile, if none go after nests.
        # 7) seventh attacks enemy nests
        # 8) attack enemy tiles

        # more than 8
        # check that all 8 are still alive, otherwise send replacement
        # stock up on all 4 adjacent tiles around nest




