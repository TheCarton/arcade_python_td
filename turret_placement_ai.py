import utilities
import math


def closest_wall_to_pos(pos, walls):
    closest_wall = None
    best_dist = None
    for wall in walls:
        if closest_wall is None:
            closest_wall = wall
        new_dist = utilities.get_dist(wall.position, pos)
        if best_dist is None:
            best_dist = new_dist
        if new_dist < best_dist:
            best_dist = new_dist
    return closest_wall, best_dist


def closest_path_to_pos(path, pos):
    closest_path = None
    best_dist = None
    for p in path:
        if closest_path is None:
            closest_path = p
        new_dist = utilities.get_dist(p, pos)
        if best_dist is None:
            best_dist = new_dist
        if new_dist < best_dist:
            best_dist = new_dist
    return closest_path, best_dist


def filter_out_of_range(path, walls, max_range):
    r = []
    for wall in walls:
        c = closest_path_to_pos(path, wall.position)
        if c[1] < max_range:
            r.append(wall)
    return r


def min_total_distance(path, walls, max_range):
    best_wall = None
    best_dist = None
    placement_locs = filter_out_of_range(path, walls, max_range)

    for loc in placement_locs:
        if best_wall is None:
            best_wall = loc
        dist = 0
        for p in path:
            dist += utilities.get_dist(loc.position, p)
        if best_dist is None:
            best_dist = dist
        elif dist < best_dist:
            best_dist = dist
            best_wall = loc

    return best_wall


def diff_slow(slow_path, fast_path, walls, max_range):
    placement_walls = []
    for wall in walls:
        c = closest_path_to_pos(fast_path, wall.position)
        if c[1] > max_range:
            placement_walls.append(wall)
    return min(placement_walls, key=lambda e: utilities.get_dist(e.position, slow_path[0]))
