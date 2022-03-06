#!/bin/python3

import os
import pprint
import sys

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
#   |---|---|---|---|
# 4 | o | o | o | Q |
#   |---|---|---|---|
# 3 |   |   | o | o |
#   |---|---|---|---|
# 2 |   | o |   | o |
#   |---|---|---|---|
# 1 | o |   |   | o |
#   |---|---|---|---|
#     1   2   3   4  
# 
# q = (4  , 4)
#      q_r, q_c
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

def calc_unobstructed(n, c, q_pos):
    q_r = q_pos[0]
    q_c = q_pos[1]
    if c == 'n':
        return n - q_r
    elif c == 'e':
        return n - q_c
    elif c == 's':
        return q_r - 1
    elif c == 'w':
        return q_c - 1
    elif c == 'ne':
        dr = n - q_r
        dc = n - q_c
        assert dr >= 0
        assert dc >= 0
        return min(dr, dc)
    elif c == 'nw':
        dr = n - q_r
        dc = q_c - 1
        assert dr >= 0
        assert dc >= 0
        return min(dr, dc)
    elif c == 'se':
        dr = q_r - 1
        dc = n - q_c
        assert dr >= 0
        assert dc >= 0
        return min(dr, dc)
    elif c == 'sw':
        dr = q_r - 1
        dc = q_c - 1
        assert dr >= 0
        assert dc >= 0
        return min(dr, dc)

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

def queensAttack(n, k, r_q, c_q, obstacles):
    q_pos = [r_q, c_q]

    obst_by_cardinal = {}
    for c in ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']:
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

    total_moves = 0
    for (c, v) in obst_by_cardinal.items():
        if v is None:
            total_moves += calc_unobstructed(n, c, q_pos)
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
