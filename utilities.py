import math

import numpy as np


def get_dist(pos_a, pos_b):
    return math.sqrt((pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2)


def aim_ahead(delta, vr, muzzle_v):
    a = vr @ vr - muzzle_v ** 2
    b = 2 * vr @ vr
    c = delta @ delta

    desc = b ** 2 - 4 * a * c
    if desc > 0:
        return 2 * c / (math.sqrt(desc) - b)
    else:
        return None


def lead_target(start, target, muzzle_v):
    vr = np.array(target.velocity)
    delta = np.array(target.position) - np.array(start)
    delta_time = aim_ahead(delta, vr, muzzle_v)
    if delta_time is None:
        return None
    aim_point = np.array(target.position) + vr * delta_time
    return aim_point.tolist()
