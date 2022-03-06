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

n_m = (1, 0)
e_m = (0, 1)
s_m = (-1, 0)
w_m = (0, -1)
ne_m = (1, 1)
nw_m = (1, -1)
se_m = (-1, 1)
sw_m = (-1, -1)
motions = [n_m, ne_m, nw_m, s_m, se_m, sw_m, e_m, w_m]

def ensure_border_pos(n, m, pos):
    pos_r = pos[0]
    pos_c = pos[1]
    n_1 = n + 1
    print('ensure_border_pos: n: {} m: {} pos: {}'.format(n, m, pprint.pformat(pos)))
    if (pos_r == 0 or pos_r == n_1):
        return pos
    elif (pos_c == 0 or pos_c == n_1):
        return pos
    else:
        return [pos_r + m[0], pos_c + m[1]]

def add_starting_obstacles(n, q_pos, obst):
    q_r = q_pos[0]
    q_c = q_pos[1]
    
    n2 = n // 2

    n_o = [n + 1, q_c]
    obst.append(n_o)

    s_o = [0, q_c]
    obst.append(s_o)

    e_o = [q_c, n + 1]
    obst.append(e_o)

    w_o = [q_c, 0]
    obst.append(w_o)

    ne_o = [q_r + n2, q_c + n2]
    obst.append(ensure_border_pos(n, ne_m, ne_o))

    nw_o = [q_r + n2, q_c - n2]
    obst.append(ensure_border_pos(n, nw_m, nw_o))

    se_o = [q_r - n2, q_c + n2]
    obst.append(ensure_border_pos(n, se_m, se_o))

    sw_o = [q_r - n2, q_c - n2]
    obst.append(ensure_border_pos(n, sw_m, sw_o))

    return obst

def is_valid_pos(n, pos):
    r = pos[0]
    c = pos[1]
    return r >= 1 and c >= 1 and r <= n and c <= n

def queensAttack(n, k, r_q, c_q, obstacles):
    q_pos = [r_q, c_q]
    obst = add_starting_obstacles(n, q_pos, obstacles)

    total_moves = 0
    print('q_pos: {}'.format(pprint.pformat(q_pos)))
    print('obst: {}'.format(pprint.pformat(obst)))
    # for m in motions:
    #     m_obst = obst_by_m.get(m, [])
    #     # print('m: {}'.format(pprint.pformat(m)))
    #     # print('m_obst: {}'.format(pprint.pformat(m_obst)))
    #     total_moves += calc_moves(n, m_obst, q_pos, m)
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
