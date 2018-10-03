#!/usr/bin/env python
__author__ = "Simon Lassourreuille"

import sys, re, math

"""
Commen utiliser : pipez les résultats du solveur dans le script. Ex :
    ./MMDP_Solver file.dpomdp -h3 --discount=0.9 | python3 ~/path/to/script/matrix-script.py
"""

# ---------------------------------------------------------------------------- #
# Récupérer la ligne de la matrice
matrix_line = ""
for line in sys.stdin:
    if line[:13] == "action policy": # la ligne qui contient la matrice
        matrix_line = line

# ---------------------------------------------------------------------------- #
# Récupérer la taille de la matrice
match = re.search('\[(\d+),(\d+)\]', matrix_line)
nb_states = int(match.group(1)) # nb lignes
nb_actions = int(match.group(2)) # nb colonnes
nb_a = int(math.sqrt(nb_actions))
nb_s = int(math.sqrt(nb_states))

matrix = [[0 for i in range(nb_actions)] for j in range(nb_states)]

# ---------------------------------------------------------------------------- #
# Récupérer la matrice
match = re.search('\(\((.*)\)\)', matrix_line)
matrix_string = match.group(1)
for i, line in enumerate(matrix_string.split('),(')):
    for j, column in enumerate(line.split(',')):
        matrix[i][j] = float(column)

# ---------------------------------------------------------------------------- #
# On affiche la matrice avec un format plus agréable

actions = ("↑","↓","←","→","•")[:nb_a]

states = []
for i in range(nb_s):
    for j in range(nb_s):
        s = list("____")
        if i != j:
            s[i] = "x"
            s[j] = "o"
        else:
            s[i] = "◉"
        states.append('(' + ''.join(s) + ')')

actions_list = [' ' * 5] + ["(" + actions[i] + " " + actions[j] + ")" for i in range(nb_a)
                                                    for j in range(nb_a)]

print(' '.join(actions_list))
print('\n'.join([states[i] + ' '.join(['{:5.3}'.format(x) for x in line]) for i, line in enumerate(matrix)]))
print()
# # Print latex
# latex_states = [''.join([x if x != '_' else '\\_' for x in s]) for s in states]
# print(' ' + ' & '.join(actions_list) + '\\\\')
# print('\n'.join([latex_states[i] + ' & ' + ' & '.join(['{:5.3}'.format(x) for x in line]) + "\\\\" for i, line in enumerate(matrix)]))

# print()

# ---------------------------------------------------------------------------- #
# On récupère les différents max
for state in range(nb_states):
    local_max = max(matrix[state])
    action = matrix[state].index(local_max)
    print("{s:2} --> {a:2} [{v}]".format(
            s = state, a = action, v=local_max
        ))

