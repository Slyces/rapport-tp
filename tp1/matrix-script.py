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

def color(x):
    c = "\033[94m" # color
    e = "\033[0m" # endline
    return c + x + e

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

actions_list = [' ' * 6] + ["(" + actions[i] + " " + actions[j] + ")" for i in range(nb_a)
                                                    for j in range(nb_a)]

formated_str = [[' ' for j in range(nb_actions + 1)] for i in range(nb_states + 1)]
formated_str[0] = [action for action in actions_list]
for i in range(nb_states):
    formated_str[i + 1][0] = states[i]
    for j in range(nb_actions):
        val = '{:5.3}'.format(matrix[i][j])
        formated_str[i + 1][j + 1] = color(val) if matrix[i][j] == max(matrix[i]) else val
print('\n'.join([' '.join(line) for line in formated_str]))
print()

# --------------------------- affichage pour latex --------------------------- #
def latexcolor(x):
    return "\\textcolor{blue}{" + x + "}"

# Print latex
latex_states = [''.join([x if x != '_' else '\\_' for x in s]) for s in states]
formated_str = [[' ' for j in range(nb_actions + 1)] for i in range(nb_states + 1)]
formated_str[0] = [action for action in actions_list]
for i in range(nb_states):
    formated_str[i + 1][0] = latex_states[i]
    for j in range(nb_actions):
        val = '{:5.3}'.format(matrix[i][j])
        formated_str[i + 1][j + 1] = latexcolor(val) if matrix[i][j] == max(matrix[i]) else val
print('\\\\ \n'.join([' & '.join(line[:6] + line[-5:]) for line in formated_str]))
print()
# print(' ' + ' & '.join(actions_list) + '\\\\')
# print('\n'.join([latex_states[i] + ' & ' + ' & '.join([(latexcolor('{:10.3}')
    # if x == max(matrix[i]) else '{:10.3}').format(x)
    # for x in line]) + "\\\\" for (i, line) in enumerate(matrix)]))

# print()

# ---------------------------------------------------------------------------- #
# On récupère les différents max
for state in range(nb_states):
    line = matrix[state]
    local_max = max(line)
    actions_index = tuple([i for (i,x) in enumerate(line) if x == local_max])
    # actions_str = ' ; '.join(['{} {}'.format(x, actions_list[1:][x]) for x in actions_index])
    actions_str = ';'.join(['{}'.format(actions_list[1:][x]) for x in actions_index])
    print("{s:2} --> {a} [{v}]".format(
            s = states[state], a = actions_str, v=local_max
        ))

