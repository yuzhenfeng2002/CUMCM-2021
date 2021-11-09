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

target = [108, 131, 139, 140, 151, 201, 229, 275, 307, 308, 329, 330, 340, 348, 361, 395]
f = open("./demand_per_m3.csv", mode='r', encoding='utf-8-sig')
csv = f.read()
demand = csv.split(',')
demand = list(map(float, demand))


def map_from_demand_to_price(d):
    if d == 0.6:
        return 1.2
    if d == 0.66:
        return 1.1
    if d == 0.72:
        return 1


price = list(map(map_from_demand_to_price, demand))

# define the constants
I_NUM = 16
J_NUM = 24
DEMAND_Q = 2.82e4

# create a model
MODEL = Model()
# MODEL.setParam('OutputFlag', 0)

# add variables
x = MODEL.addVars(I_NUM, J_NUM, lb=0, vtype=GRB.INTEGER, name='x')
s = MODEL.addVars(J_NUM, lb=-GRB.INFINITY, name='s')
MODEL.update()

# set the objective
MODEL.setObjective(quicksum(price[target[i] - 1] * x[i, j] for i in range(I_NUM) for j in range(J_NUM)), GRB.MINIMIZE)
# MODEL.setObjective(quicksum(s[j] for j in range(J_NUM)), GRB.MINIMIZE)

# add constraints
MODEL.addConstrs(quicksum(quicksum(x[i, j] / demand[target[i] - 1] for i in range(I_NUM)) for j in range(k))
                 + s[k - 1] >= DEMAND_Q * k for k in range(1, J_NUM + 1))
# MODEL.addConstrs(quicksum(capacity[target[i] - 1][j] * x[i, j] / demand[target[i] - 1] for i in range(I_NUM)) >= DEMAND_Q / 2 for j in range(J_NUM))
MODEL.addConstrs(x[i, j] <= capacity[target[i] - 1][j] for i in range(I_NUM) for j in range(J_NUM))
# MODEL.addConstrs(x[i, j] <= 6000 for i in range(I_NUM) for j in range(J_NUM))
MODEL.addConstrs(s[j] <= 0 for j in range(J_NUM))

# optimize the model
MODEL.optimize()

# output
i = j = 0
for v in MODEL.getVars():
    print(round(v.x, 0), end=',')
    i += 1
    if i % J_NUM == 0:
        print('')
        j += 1
    if j == I_NUM:
        break
