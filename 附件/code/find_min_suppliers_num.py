from gurobipy import *

f = open("./supply_capacity_max.csv", mode='r', encoding='utf-8-sig')
csv = f.readlines()
data = csv
capacity = []
for row in data:
    d = row[:-1].split(',')[:-1]
    try:
        d = list(map(int, d))
        capacity.append(d)
    except:
        print(d)
# print(len(capacity), len(capacity[0]))
f.close()

f = open("./demand_per_m3.csv", mode='r', encoding='utf-8-sig')
csv = f.read()
demand = csv.split(',')
demand = list(map(float, demand))
# print(demand)

# define the constants
I_NUM = 402
J_NUM = 24
DEMAND_Q = 2.82e4
MAX = 1e5

# create a model
MODEL = Model()
# MODEL.setParam('OutputFlag', 0)

# add variables
x = MODEL.addVars(I_NUM, vtype=GRB.BINARY, name='x')
s = MODEL.addVars(J_NUM, lb=-GRB.INFINITY, name='s')
MODEL.update()

# set the objective
MODEL.setObjective(quicksum(x[i] for i in range(I_NUM)), GRB.MINIMIZE)
# MODEL.setObjective(quicksum(s[j] for j in range(J_NUM)), GRB.MINIMIZE)

# add constraints
MODEL.addConstrs(quicksum(quicksum(capacity[i][j] / demand[i] * x[i] for i in range(I_NUM)) for j in range(k)) + s[k - 1] == DEMAND_Q * k for k in range(1, J_NUM + 1))
MODEL.addConstrs(s[j] <= 0 for j in range(J_NUM))

# optimize the model
MODEL.optimize()

# output
for v in MODEL.getVars():
    if round(v.x, 0) == 1:
        print(v.index + 1, end=',')
