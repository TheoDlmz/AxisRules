import numpy as np 

import sys
import gurobipy as gp
from gurobipy import GRB

nb_voters = -1
nb_cand = -1
coefs = []
l_voters = []

def read_file(file_name):
	global nb_cand
	global nb_voters
	global coefs
	global l_voters

	f = open(file_name, "r")

	nb_cand = int(f.readline())
	nb_voters = int(f.readline())

	line = f.readline()

	while line:
		line_split = line.split(" ")

		for i in range(len(line_split)):
			line_split[i] = int(line_split[i])-1
		coefs += [int(line[0])]
		#print(line_split, l_voters)
		l_voters += [line_split[1:]]
		line = f.readline()

read_file("irv_2_ft.csv")
#print(nb_voters, nb_cand, coefs, l_voters)

print("coefs: ", coefs)

m = gp.Model("mip1")
x = m.addMVar((nb_cand,nb_cand), vtype=GRB.BINARY)
z = m.addMVar((nb_voters, nb_cand, nb_cand), vtype=GRB.BINARY)

expr = gp.LinExpr()

for i in range(nb_voters):
	for j in range(nb_cand):
		for k in range(nb_cand):
			expr += coefs[i]*z[i][j][k]

m.setObjective(expr)

for i in range(nb_cand):
	for j in range(i+1, nb_cand):
		m.addConstr(x[i][j] + x[j][i] == 1)

for i in range(nb_cand):
	for j in range(nb_cand):
		for k in range(nb_cand):
			if i != j and i != k and j != k:
				m.addConstr(x[i][j] - x[i][k] - x[k][j] >= -1)

for v in range(nb_voters):
	top_v = l_voters[v][0]
	#print(top_v, l_voters[v])

	for i in range(nb_cand):
		for j in range(i+1, nb_cand):
			v_i = l_voters[v][i]
			v_j = l_voters[v][j]

			m.addConstr(z[v][v_i][v_j] - x[top_v][v_j] - x[v_j][v_i] >= -1)
			m.addConstr(z[v][v_i][v_j] - x[v_j][top_v] - x[v_i][v_j] >= -1)
m.optimize()

sol = []

for i in range(nb_cand):
	s = ""
	s_sol = []
	for j in range(nb_cand):
		s+= str(int(x[i][j].X))+" "
		s_sol.append(int(x[i][j].X))
	print(s)
	sol += [s_sol]

print(sol)

l_rangs = []

for i in range(len(sol)):
	s = 0

	for j in range(len(sol[i])):
		s += sol[i][j]

	l_rangs += [s]


for i in range(len(l_rangs)):
	print(l_rangs.index(i))