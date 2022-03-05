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

def is_valid_pos(n, pos):
    r = pos[0]
    c = pos[1]
    return r >= 1 and c >= 1 and r <= n and c <= n

def is_blocked(obst, pos):
    return pos in obst

def calc_moves(n, obst, cur_pos, m):
    moves = 0
    while True:
        next_pos = (cur_pos[0] + m[0], cur_pos[1] + m[1])
        if is_valid_pos(n, next_pos):
            if is_blocked(obst, next_pos):
                break
            else:
                # print('valid  pos: {}'.format(pprint.pformat(next_pos)))
                moves += 1
            cur_pos = next_pos
        else:
            break
    return moves

def obst_for_m(q_pos, m, obst):
    q_r = q_pos[0]
    q_c = q_pos[1]
    m_r = m[0]
    m_c = m[1]

    if m_r == 0:
        # this is a straight-line e or w motion
        # the only obstacles that can apply have the same
        # row value as the queen
        return [(o_r, o_c) for (o_r, o_c) in obst if o_r == q_r]

    if m_c == 0:
        # this is a straight-line n or s motion
        # the only obstacles that can apply have the same
        # column value as the queen
        return [(o_r, o_c) for (o_r, o_c) in obst if o_c == q_c]

    if m_r == 1 and m_c == 1:
        # ne obstacles
        return [(o_r, o_c) for (o_r, o_c) in obst if o_c >= q_c and o_r >= q_r]

    if m_r == 1 and m_c == -1:
        # nw obstacles
        return [(o_r, o_c) for (o_r, o_c) in obst if o_c <= q_c and o_r >= q_r]

    if m_r == -1 and m_c == 1:
        # se obstacles
        return [(o_r, o_c) for (o_r, o_c) in obst if o_c >= q_c and o_r <= q_r]

    if m_r == -1 and m_c == -1:
        # sw obstacles
        return [(o_r, o_c) for (o_r, o_c) in obst if o_c <= q_c and o_r <= q_r]

    raise RuntimeError('obst_for_m unreachable')

def queensAttack(n, k, r_q, c_q, obstacles):
    obst = list(map(tuple, obstacles))
    q_pos = (r_q, c_q)
    n_m = (1, 0)
    e_m = (0, 1)
    s_m = (-1, 0)
    w_m = (0, -1)
    ne_m = (1, 1)
    nw_m = (1, -1)
    se_m = (-1, 1)
    sw_m = (-1, -1)
    motions = [n_m, ne_m, nw_m, s_m, se_m, sw_m, e_m, w_m]
    total_moves = 0
    # print('q_pos: {}'.format(pprint.pformat(q_pos)))
    for m in motions:
        m_obst = obst_for_m(q_pos, m, obst)
        # print('m: {}'.format(pprint.pformat(m)))
        # print('m_obst: {}'.format(pprint.pformat(m_obst)))
        total_moves += calc_moves(n, m_obst, q_pos, m)
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
