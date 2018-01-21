"""
Halite bot (DesBot) created by Desmin Little.

V1 Strategy: A mix of defence, offence, and exploration
1. Generate a list of nearby entities.
2. If the entity is a planet and not owned, dock or move toward it to dock
3. If the entity is a ship and it is docked, attack it
"""
import hlt
import logging
from collections import OrderedDict

# GAME START
game = hlt.Game("DesBot-V1")

owned_planets = []

logging.info("Starting DesBot-V1!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    for ship in game_map.get_me().all_ships():
        if ship.docking_status == ship.DockingStatus.DOCKED:
            continue

        closest_entities = OrderedDict(sorted(game_map.nearby_entities_by_distance(ship).items(), key=lambda t: t[0]))

        for distance in closest_entities:
            entity = closest_entities[distance][0]
            if isinstance(entity, hlt.entity.Planet):
                if not entity.is_owned() or (entity.is_owned() and entity.owner != game_map.get_me()):
                    if ship.can_dock(entity):
                        command_queue.append(ship.dock(entity))
                        break
                    else:
                        navigate_command = ship.navigate(ship.closest_point_to(entity), game_map,
                                                         speed=int(hlt.constants.MAX_SPEED * .80))
                        if navigate_command:
                            command_queue.append(navigate_command)
                            break
            if isinstance(entity, hlt.entity.Ship):
                if entity.owner != game_map.get_me():
                    if entity.docking_status == entity.DockingStatus.DOCKED:
                        attack_command = ship.navigate(ship.closest_point_to(entity), game_map,
                                                       speed=int(hlt.constants.MAX_SPEED * .9))
                        if attack_command:
                            command_queue.append(attack_command)
                            break

    game.send_command_queue(command_queue)

    '''closest_empty_planets = [closest_entities[distance][0] for distance in closest_entities if isinstance(closest_entities[distance][0], hlt.entity.Planet) and closest_entities[distance][0] not in owned_planets]

        if len(closest_empty_planets) > 0:
            chosen_planet = closest_empty_planets[0]

            if ship.can_dock(chosen_planet):
                command_queue.append(ship.dock(chosen_planet))
                owned_planets.append(chosen_planet)
            else:
                navigate_command = ship.navigate(ship.closest_point_to(chosen_planet), game_map, speed=int(hlt.constants.MAX_SPEED*.80))
                if navigate_command:
                    command_queue.append(navigate_command)'''
