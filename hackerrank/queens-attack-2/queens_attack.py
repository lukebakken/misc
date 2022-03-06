#!/bin/python3

import os
import pprint
import sys

#
# Complete the 'queensAttack' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER k
#  3. INTEGER r_q
#  4. INTEGER c_q
#  5. 2D_INTEGER_ARRAY obstacles
#
# int n: the number of rows and columns in the board
# nt k: the number of obstacles on the board
# int r_q: the row number of the queen's position - 1 based
# int c_q: the column number of the queen's position - 1 based
# int obstacles[k][2]: each element is a list of integers, the row and column of an obstacle
#
#   |---|---|---|---|---|
# 5 |   | o | o | o | x |
#   |---|---|---|---|---|
# 4 |   | x | Q | o | o |
#   |---|---|---|---|---|
# 3 |   | o | o | o |   |
#   |---|---|---|---|---|
# 2 | o |   | x |   | o |
#   |---|---|---|---|---|
# 1 |   |   |   |   |   |
#   |---|---|---|---|---|
#     1   2   3   4   5
# 
# q = (4  , 3)
#      q_r, q_c
#
# starting obstacles:
# n = (6, 3) = (n + 1, q_c)
# s = (0, 3) = (0, q_c)
# e = (4, 6) = (q_c, n + 1)
# w = (4, 0) = (q_c, 0)
#
# ne = (6, 5) = (q_r + (floor(n / 2)), q_c + (floor(n / 2)))
#      then check position to see if it's a "border". If not, move one more
#      by adding ne_m
# nw = (7, 0) = (q_r + (floor(n / 2)), q_c - (floor(n / 2)))
# se = (1, 6) = (q_r - (floor(n / 2)), q_c + (floor(n / 2)))
# sw = (1, 0) = (q_r - (floor(n / 2)), q_c - (floor(n / 2)))
#
# calculating q_pos to pos moves
# 
# (4, 3) to (1, 6)
# (abs(1 - 4), abs(6 - 3))
# (3, 3) 3 // 3 == 1, so on a diagonal
# 3 - 1 = 2 moves "in between"
#
# (4, 3) to (2, 3)
# (abs(2 - 4), abs(3 - 3))
# (2, 0) - if r or c is 0, straight dist
# 2 - 1 = 1 move "in between"
#

n_m = (1, 0)
e_m = (0, 1)
s_m = (-1, 0)
w_m = (0, -1)
ne_m = (1, 1)
nw_m = (1, -1)
se_m = (-1, 1)
sw_m = (-1, -1)

cardinals = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']

def calc_unobstructed(n, c, q_pos):
    q_r = q_pos[0]
    q_c = q_pos[1]
    if c == 'n':
        return n - q_r
    if c == 'e':
        return n - q_c
    if c == 's':
        return q_r - 1
    if c == 'w':
        return q_c - 1
    if c == 'ne':
        dr = n - q_r
        dc = n - q_c
        v = min(dr, dc) + 1
        ne_pos = (q_r + v, q_c + v)
        return calc_pos(q_pos, ne_pos)
    if c == 'nw':
        dr = n - q_r
        dc = q_c - 1
        v = min(dr, dc) + 1
        nw_pos = (q_r + v, q_c + v)
        return calc_pos(q_pos, nw_pos)
    if c == 'se':
        dr = n - q_r
        dc = q_c - 1
        v = min(dr, dc) + 1
        nw_pos = (q_r + v, q_c + v)
        return calc_pos(q_pos, nw_pos)
    if c == 'sw':
        return FOO

def calc_pos(q_pos, pos):
    q_r = q_pos[0]
    q_c = q_pos[1]
    pos_r = pos[0]
    pos_c = pos[1]

    # pos is n of queen, straight line
    if pos_c == q_c and pos_r > q_r:
        n_dist = pos_r - q_r
        assert n_dist > 0
        return ('n', n_dist - 1)

    # pos is e of queen, straight line
    elif pos_r == q_r and pos_c > q_c:
        e_dist = pos_c - q_c
        assert e_dist > 0
        return ('e', e_dist - 1)

    # pos is s of queen, straight line
    elif pos_c == q_c and pos_r < q_r:
        s_dist = q_r - pos_r
        assert s_dist > 0
        return ('s', s_dist - 1)

    # pos is w of queen, straight line
    elif pos_r == q_r and pos_c < q_c:
        w_dist = q_c - pos_c
        assert w_dist > 0
        return ('w', w_dist - 1)

    # pos is ne of queen on diagonal
    elif pos_c > q_c and pos_r > q_r:
        dr = abs(pos_r - q_r)
        dc = abs(pos_c - q_c)
        if dr == dc:
            return ('ne', dr - 1)

    # pos is nw of queen on diagonal
    elif pos_c < q_c and pos_r > q_r:
        dr = abs(pos_r - q_r)
        dc = abs(pos_c - q_c)
        if dr == dc:
            return ('nw', dr - 1)

    # pos is se of queen on diagonal
    elif pos_c > q_c and pos_r < q_r:
        dr = abs(pos_r - q_r)
        dc = abs(pos_c - q_c)
        if dr == dc:
            return ('se', dr - 1)

    # pos is sw of queen on diagonal
    elif pos_c < q_c and pos_r < q_r:
        dr = abs(pos_r - q_r)
        dc = abs(pos_c - q_c)
        if dr == dc:
            return ('sw', dr - 1)

    else:
        return None


# def ensure_border_pos(n, m, pos):
#     pos_r = pos[0]
#     pos_c = pos[1]
#     n_1 = n + 1
#     if (pos_r == 0 or pos_r == n_1):
#         return pos
#     elif (pos_c == 0 or pos_c == n_1):
#         return pos
#     else:
#         return [pos_r + m[0], pos_c + m[1]]
# 
# def add_starting_obstacles(n, q_pos, obst):
#     q_r = q_pos[0]
#     q_c = q_pos[1]
#     
#     n2 = n // 2
# 
#     n_o = [n + 1, q_c]
#     obst.append(n_o)
# 
#     s_o = [0, q_c]
#     obst.append(s_o)
# 
#     e_o = [q_r, n + 1]
#     obst.append(e_o)
# 
#     w_o = [q_r, 0]
#     obst.append(w_o)
# 
#     ne_o = [q_r + n2, q_c + n2]
#     obst.append(ensure_border_pos(n, ne_m, ne_o))
# 
#     nw_o = [q_r + n2, q_c - n2]
#     obst.append(ensure_border_pos(n, nw_m, nw_o))
# 
#     se_o = [q_r - n2, q_c + n2]
#     obst.append(ensure_border_pos(n, se_m, se_o))
# 
#     sw_o = [q_r - n2, q_c - n2]
#     obst.append(ensure_border_pos(n, sw_m, sw_o))
# 
#     return obst

def queensAttack(n, k, r_q, c_q, obstacles):
    q_pos = [r_q, c_q]
    # obst = add_starting_obstacles(n, q_pos, obstacles)

    total_moves = 0
    print('q_pos: {}'.format(pprint.pformat(q_pos)))
    print('obstacles: {}'.format(pprint.pformat(obstacles)))

    obst_by_cardinal = {}
    for c in cardinals:
        obst_by_cardinal[c] = None

    for o in obstacles:
        c_pos = calc_pos(q_pos, o)
        if c_pos is None:
            continue
        c = c_pos[0]
        dist = c_pos[1]
        curr_saved_pos = obst_by_cardinal[c]
        if curr_saved_pos is None:
            obst_by_cardinal[c] = (o, dist)
        else:
            curr_dist = curr_saved_pos[1]
            if dist < curr_dist:
                obst_by_cardinal[c] = (o, dist)

    print('obst_by_cardinal: {}'.format(pprint.pformat(obst_by_cardinal)))

    for (c, v) in obst_by_cardinal.items():
        if v is None:
            total_items += calc_unobstructed(n, c, q_pos)
        else:
            total_moves += v[1]

    return total_moves

if __name__ == '__main__':
    n = 0
    k = 0
    r_q = 0
    c_q = 0
    obstacles = []

    with open(sys.argv[1]) as f:
        first_multiple_input = f.readline().rstrip().split()
        n = int(first_multiple_input[0])
        k = int(first_multiple_input[1])
        second_multiple_input = f.readline().rstrip().split()
        r_q = int(second_multiple_input[0])
        c_q = int(second_multiple_input[1])
        for _ in range(k):
            obstacles.append(list(map(int, f.readline().rstrip().split())))

    result = queensAttack(n, k, r_q, c_q, obstacles)
    print(result)
