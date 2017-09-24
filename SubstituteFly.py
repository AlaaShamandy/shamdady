from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World

#Bug : in closed map run, units_by_age lost track of a live firefly and it just remained idle there
#Possible sol: after looping all in units_by_age check top say 5 healthiest in friendly_units, if they're not in units_by_age add them to the 8th index (friendly units is sorted by health so just check last 5 elements)

class PlayerAI:
    global units_by_age # a global list containing units in order of oldest to youngest
    units_by_age = []

    def __init__(self):
        """
        Any instantiation code goes here
        """
        pass
    def fill_adjacent_to_nest(self, world, friendly_units):
        friendly_positions = world.get_position_to_friendly_dict()
        min_health = [0,1000000000000000000]
        for unit in friendly_units:
            if unit and  unit.last_move_result == MoveResult.NEWLY_SPAWNED: #units that are newly spawned are positioned over a nest
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
        global units_by_age
        for unit in friendly_units:
            if unit and unit.last_move_result == MoveResult.NEWLY_SPAWNED:
                units_by_age.append(unit.uuid)
        for i in range(len(units_by_age)): #len of friendly_units and units_by_age is supposed to be the same yet there's a lag of 3 turns for replacement of dead flies
            if i < 8:
                #From this point on refer to unit as uni cuz somehow before defining it, it was reading another variable called unit
                if i < 2:
                    if world.get_unit(units_by_age[i]) != None: #Checks that the unit isn't dead
                        uni = world.get_unit(units_by_age[i])
                        pos = world.get_closest_capturable_tile_from(uni.position, None)
                        world.move(uni, pos.position)
                    else:
                        if len(units_by_age) > 8: # if we're here we replace it with the oldest fly without a task then we pop it to avoid dupicates, depending on when you read this the number might not be 8 due to testing purposes
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
                elif i <3:
                    if world.get_unit(units_by_age[i]) != None:
                        #Integrating NestBuilding at the end cuz it's too long and need to read through it first, for now the 3rd just collects tiles too
                        uni = world.get_unit(units_by_age[i])
                        pos = world.get_closest_capturable_tile_from(uni.position, None)
                        world.move(uni, pos.position)
                    else:
                        if len(units_by_age) > 8:
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
                elif i<4:
                    if world.get_unit(units_by_age[i]) != None:
                        uni = world.get_unit(units_by_age[i])
                        pos = world.get_closest_enemy_nest_from(uni.position, None)
                        world.move(uni, pos)
                    else:
                        if len(units_by_age) > 8:
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
                elif i<5:
                    if world.get_unit(units_by_age[i]) != None:
                        uni = world.get_unit(units_by_age[i])
                        closest_enemy = world.get_closest_enemy_from(uni.position, None)
                        world.move(uni, closest_enemy.position)
                    else:
                        if len(units_by_age) > 8:
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
                elif i<6: #doesn't go after nests yet, plus it's probably better off just going after non neutral tiles
                     if world.get_unit(units_by_age[i]) != None:
                        uni = world.get_unit(units_by_age[i])
                        pos = world.get_closest_neutral_tile_from(uni.position, None)
                        world.move(uni, pos.position)
                     else:
                        if len(units_by_age) > 8:
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
                elif i<7:
                    if world.get_unit(units_by_age[i]) != None:
                        uni = world.get_unit(units_by_age[i])
                        pos = world.get_closest_enemy_nest_from(uni.position, None)
                        world.move(uni, pos)
                    else:
                        if len(units_by_age) > 8:
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
                else:
                    if world.get_unit(units_by_age[i]) != None:
                        uni = world.get_unit(units_by_age[i])
                        pos = world.get_closest_enemy_tile_from(uni.position, None)
                        world.move(uni, pos.position)
                    else:
                        if len(units_by_age) > 8:
                            units_by_age[i] = units_by_age[8]
                            units_by_age.pop(8)
            else:
                nesters = [world.get_unit(u) for u in units_by_age[8:]] #gets the remaining unprocessed flies
                PlayerAI.fill_adjacent_to_nest(self,world, nesters)









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




