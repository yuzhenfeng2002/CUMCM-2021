from gurobipy import *

waste_rate = [2.560700676, 1.400819674, 0.661405597, 3.498634788, 4.847985089, 1.89170451, 3.511251652, 2.122831952]

f = open("./order_Q3_for_delivery.csv", mode='r', encoding='utf-8-sig')
csv = f.readlines()
data = csv
order = []
for row in data:
    d = row[:-1].split(',')
    try:
        d = list(map(int, d))
        order.append(d)
    except:
        print(d)
# print(len(order), len(order[0]))
f.close()

# define the constants
I_NUM = len(order)
J_NUM = len(waste_rate)
DEMAND_Q = 2.82e4

for week in range(24):

    # create a model
    MODEL = Model()
    MODEL.setParam('OutputFlag', 0)

    # add variables
    x = MODEL.addVars(I_NUM, J_NUM, lb=0, vtype=GRB.INTEGER, name='x')

    MODEL.update()

    # set the objective
    MODEL.setObjective(quicksum(waste_rate[j] * x[i, j] for i in range(I_NUM) for j in range(J_NUM)), GRB.MINIMIZE)
    # MODEL.setObjective(quicksum(s[j] for j in range(J_NUM)), GRB.MINIMIZE)

    # add constraints
    MODEL.addConstrs(quicksum(x[i, j] for j in range(J_NUM)) == order[i][week] for i in range(I_NUM))
    MODEL.addConstrs(quicksum(x[i, j] for i in range(I_NUM)) <= 6e3 for j in range(J_NUM))

    # optimize the model
    MODEL.optimize()

    # output

    print(MODEL.ObjVal, end=',')
    # i = j = 0
    # for v in MODEL.getVars():
    #     if round(v.x, 0) > 0:
    #         print(v)
