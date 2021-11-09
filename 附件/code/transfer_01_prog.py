from gurobipy import *

waste_rate = [2.560700676, 1.400819674, 0.661405597, 3.498634788, 4.847985089, 1.89170451, 3.511251652, 2.122831952]

f = open("./order_Q4_for_delivery.csv", mode='r', encoding='utf-8-sig')
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
f.close()

for w in range(24):
    order_list = [0] * len(order)
    order_dict = {}
    for i in range(len(order)):
        if order[i][w] <= 6e3:
            order_list[i] = order[i][w]
        else:
            order_list[i] = 6e3
            o = order[i][w] - 6e3
            while o > 6e3:
                order_list.append(6e3)
                order_dict[len(order_list) - 1] = i
                o -= 6e3
            order_list.append(o)
            order_dict[len(order_list) - 1] = i
        order_dict[i] = i

    I_NUM = len(order_list)
    J_NUM = len(waste_rate)

    # create a model
    MODEL = Model()
    MODEL.setParam('OutputFlag', 0)

    # add variables
    x = MODEL.addVars(I_NUM, J_NUM, vtype=GRB.BINARY, name='x')
    MODEL.update()

    # set the objective
    MODEL.setObjective(quicksum(waste_rate[j] * x[i, j] * order_list[i] for i in range(I_NUM) for j in range(J_NUM)), GRB.MINIMIZE)

    # add constraints
    MODEL.addConstrs(quicksum(x[i, j] for j in range(J_NUM)) == 1 for i in range(I_NUM))
    MODEL.addConstrs(quicksum(x[i, j] * order_list[i] for i in range(I_NUM)) <= 6e3 for j in range(J_NUM))

    # optimize the model
    MODEL.optimize()

    # output
    # print(MODEL.ObjVal, end=',')
    i = 0
    j = -1
    for v in MODEL.getVars():
        if i % J_NUM == 0:
            print('')
            j += 1
            print(w + 1, order_dict[j] + 1, order_list[j], sep=',', end=',')
        print(round(v.x, 0), end=',')
        i += 1
        if j == I_NUM:
            break
