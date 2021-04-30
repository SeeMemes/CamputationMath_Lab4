import math
import numpy as np
import matplotlib.pyplot as plt
from termcolor import cprint
from tabulate import tabulate


##############################
#       MATRIX LOGIC         #
##############################

def get_matrix():
    new_matrix = []
    answer = int(input())
    if answer == 1:
        rows = int(input())
        if rows != 1:
            for i in range(rows):
                a = []
                for j in range(rows + 1):
                    a.append(float(input()))
                new_matrix.append(a)
            print(new_matrix)
            return new_matrix
        else:
            return get_matrix()
    elif answer == 0:
        with open(filename) as f:
            matrix_from_file = [list(map(float, row.split())) for row in f.readlines()]
        print_matrix(matrix_from_file)
        return matrix_from_file
    else:
        return get_matrix()


def print_matrix(input_matrix):
    cprint(tabulate(input_matrix,
                    tablefmt="fancy_grid", floatfmt="2.5f"), 'cyan')


def double_matrix(a):
    x0 = (a[0][2] * a[1][1] - a[0][1] * a[1][2]) / (a[0][0] * a[1][1] - a[0][1] * a[0][1])
    x1 = (a[0][0] * a[1][2] - a[0][2] * a[1][0]) / (a[0][0] * a[1][1] - a[0][1] * a[0][1])
    return [x0, x1]


def tripple_matrix(a):
    d = a[0][0] * a[1][1] * a[2][2] + a[1][0] * a[2][1] * a[0][2] + a[0][1] * a[1][2] * a[2][0] - \
        a[2][0] * a[1][1] * a[0][2] - a[2][1] * a[1][2] * a[0][0] - a[1][0] * a[0][1] * a[2][2]
    d1 = a[0][3] * a[1][1] * a[2][2] + a[1][3] * a[2][1] * a[0][2] + a[0][1] * a[1][2] * a[2][3] - \
         a[2][3] * a[1][1] * a[0][2] - a[2][1] * a[1][2] * a[0][3] - a[1][3] * a[0][1] * a[2][2]
    d2 = a[0][0] * a[1][3] * a[2][2] + a[1][0] * a[2][3] * a[0][2] + a[0][3] * a[1][2] * a[2][0] - \
         a[2][0] * a[1][3] * a[0][2] - a[2][3] * a[1][2] * a[0][0] - a[1][0] * a[0][3] * a[2][2]
    d3 = a[0][0] * a[1][1] * a[2][3] + a[1][0] * a[2][1] * a[0][3] + a[0][1] * a[1][3] * a[2][0] - \
         a[2][0] * a[1][1] * a[0][3] - a[2][1] * a[1][3] * a[0][0] - a[1][0] * a[0][1] * a[2][3]
    x0 = d1 / d
    x1 = d2 / d
    x2 = d3 / d
    return [x0, x1, x2]


##############################
#       APPROXIMATION        #
##############################

def lineal(input_xy):
    x = input_xy[0]
    y = input_xy[1]
    sx = 0
    sxx = 0
    sy = 0
    sxy = 0
    for i in range(len(x)):
        sx += x[i]
        sxx += x[i] ** 2
        sy += y[i]
        sxy += x[i] * y[i]
    n = len(x)
    answer_matrix = double_matrix([[sxx, sx, sxy], [sx, n, sy]])
    cprint('\n\tLINEAR: y = ' + str(answer_matrix[0]) + ' * x + ' + str(answer_matrix[1]), 'green', attrs=['bold'])
    s = 0
    for i in range(len(x)):
        s += (answer_matrix[0] * x[i] + answer_matrix[1] - y[i]) ** 2
    cprint('\t\tМера отклонения: ' + str(s), 'green')
    cprint('\t\tСреднеквадратичное отклонение: ' + str(math.sqrt(s / len(x))), 'green')
    up = 0
    sum_of_lineal_func = 0
    squares = 0
    for i in range(len(x)):
        up += (y[i] - (answer_matrix[0] * x[i] + answer_matrix[1])) ** 2
        sum_of_lineal_func += answer_matrix[0] * x[i] + answer_matrix[1]
        squares += (answer_matrix[0] * x[i] + answer_matrix[1]) ** 2
    cprint('\t\tДостоверность аппроксимации: ' + str(1 - (up / (squares - (sum_of_lineal_func ** 2) / len(x)))), \
           'green')
    answer_matrix.append(math.sqrt(s / len(x)))
    return answer_matrix


def square(input_xy):
    x = input_xy[0]
    y = input_xy[1]
    sx = 0
    sxx = 0
    sxxx = 0
    sxxxx = 0
    sy = 0
    sxy = 0
    sxxy = 0
    for i in range(len(x)):
        sx += x[i]
        sxx += x[i] ** 2
        sxxx += x[i] ** 3
        sxxxx += x[i] ** 4
        sy += y[i]
        sxy += x[i] * y[i]
        sxxy += x[i] ** 2 * y[i]
    param_matrix = [[len(x), sx, sxx, sy], [sx, sxx, sxxx, sxy], [sxx, sxxx, sxxxx, sxxy]]
    answer_matrix = tripple_matrix(param_matrix)
    cprint('\n\tSQUARE: y = ' + str(answer_matrix[0]) + ' + ' + str(answer_matrix[1]) + ' * x + ' + str(
        answer_matrix[2]) + ' * x ^ 2', 'green', attrs=['bold'])
    s = 0
    for i in range(len(x)):
        s += (answer_matrix[0] + answer_matrix[1] * x[i] + answer_matrix[2] * x[i] ** 2 - y[i]) ** 2
    cprint('\t\tМера отклонения: ' + str(s), 'green')
    cprint('\t\tСреднеквадратичное отклонение: ' + str(math.sqrt(s / len(x))), 'green')
    up = 0
    sum_of_lineal_func = 0
    squares = 0
    for i in range(len(x)):
        up += (y[i] - (answer_matrix[0] + answer_matrix[1] * x[i] + answer_matrix[2] * x[i] ** 2)) ** 2
        sum_of_lineal_func += answer_matrix[0] + answer_matrix[1] * x[i] + answer_matrix[2] * x[i] ** 2
        squares += (answer_matrix[0] + answer_matrix[1] * x[i] + answer_matrix[2] * x[i] ** 2) ** 2
    cprint('\t\tДостоверность аппроксимации: ' + str(1 - (up / (squares - (sum_of_lineal_func ** 2) / len(x)))),
           'green')
    answer_matrix.append(math.sqrt(s / len(x)))
    return answer_matrix


def exponent(input_xy):
    x = input_xy[0]
    y = input_xy[1]
    sx = 0
    sxx = 0
    sy = 0
    sxy = 0
    for i in range(len(x)):
        if y[i] > 0:
            sx += x[i]
            sxx += x[i] ** 2
            sy += math.log(y[i], math.e)
            sxy += x[i] * math.log(y[i], math.e)
        else:
            cprint('\n\tEXPONENT method can\'t be used', 'red', attrs=['bold'])
            return
    param_matrix = [[len(x), sx, sy], [sx, sxx, sxy]]
    answer_matrix = double_matrix(param_matrix)
    cprint('\n\tEXPONENT: y = ' + str(math.e ** answer_matrix[0]) + ' * e ^ ( ' + str(answer_matrix[1]) + ' * x )',
           'green', attrs=['bold'])
    s = 0
    for i in range(len(x)):
        s += ((math.e ** answer_matrix[0] * math.e ** (answer_matrix[1] * x[i])) - y[i]) ** 2
    cprint('\t\tМера отклонения: ' + str(s), 'green')
    cprint('\t\tСреднеквадратичное отклонение: ' + str(math.sqrt(s / len(x))), 'green')
    up = 0
    sum_of_lineal_func = 0
    squares = 0
    for i in range(len(x)):
        up += (y[i] - (math.e ** answer_matrix[0] * math.e ** (answer_matrix[1] * x[i]))) ** 2
        sum_of_lineal_func += (math.e ** answer_matrix[0] * math.e ** (answer_matrix[1] * x[i]))
        squares += (math.e ** answer_matrix[0] * math.e ** (answer_matrix[1] * x[i])) ** 2
    cprint('\t\tДостоверность аппроксимации: ' + str(1 - (up / (squares - (sum_of_lineal_func ** 2) / len(x)))),
           'green')
    answer_matrix.append(math.sqrt(s / len(x)))
    return answer_matrix


def degree(input_xy):
    x = input_xy[0]
    y = input_xy[1]
    sx = 0
    sxx = 0
    sy = 0
    sxy = 0
    for i in range(len(x)):
        if y[i] > 0 and x[i] > 0:
            sx += math.log(x[i], math.e)
            sxx += math.log(x[i], math.e) ** 2
            sy += math.log(y[i], math.e)
            sxy += math.log(x[i], math.e) * math.log(y[i], math.e)
        else:
            cprint('\n\tDEGREE method can\'t be used', 'red', attrs=['bold'])
            return
    param_matrix = [[len(x), sx, sy], [sx, sxx, sxy]]
    answer_matrix = double_matrix(param_matrix)
    cprint('\n\tDEGREE: y = ' + str(math.e ** answer_matrix[0]) + ' * x ^ ( ' + str(answer_matrix[1]) + ' )', 'green',
           attrs=['bold'])
    s = 0
    for i in range(len(x)):
        s += ((math.e ** answer_matrix[0] * x[i] ** (answer_matrix[1])) - y[i]) ** 2
    cprint('\t\tМера отклонения: ' + str(s), 'green')
    cprint('\t\tСреднеквадратичное отклонение: ' + str(math.sqrt(s / len(x))), 'green')
    up = 0
    sum_of_lineal_func = 0
    squares = 0
    for i in range(len(x)):
        up += (y[i] - (math.e ** answer_matrix[0] * x[i] ** (answer_matrix[1]))) ** 2
        sum_of_lineal_func += (math.e ** answer_matrix[0] * x[i] ** (answer_matrix[1]))
        squares += (math.e ** answer_matrix[0] * x[i] ** (answer_matrix[1])) ** 2
    cprint('\t\tДостоверность аппроксимации: ' + str(1 - (up / (squares - (sum_of_lineal_func ** 2) / len(x)))),
           'green')
    answer_matrix.append(math.sqrt(s / len(x)))
    return answer_matrix


def log(input_xy):
    x = input_xy[0]
    y = input_xy[1]
    sx = 0
    sxx = 0
    sy = 0
    sxy = 0
    for i in range(len(x)):
        if x[i] > 0:
            sx += math.log(x[i], math.e)
            sxx += math.log(x[i], math.e) ** 2
            sy += y[i]
            sxy += math.log(x[i], math.e) * y[i]
        else:
            cprint('\n\tLOGARIFM method can\'t be used', 'red', attrs=['bold'])
            return
    param_matrix = [[len(x), sx, sy], [sx, sxx, sxy]]
    answer_matrix = double_matrix(param_matrix)
    cprint('\n\tLOGARITHM: y = ' + str(answer_matrix[1]) + ' * ln(x) + ' + str(answer_matrix[0]), 'green',
           attrs=['bold'])
    s = 0
    for i in range(len(x)):
        s += ((answer_matrix[1] * math.log(x[i], math.e) + answer_matrix[0]) - y[i]) ** 2
    cprint('\t\tМера отклонения: ' + str(s), 'green')
    cprint('\t\tСреднеквадратичное отклонение: ' + str(math.sqrt(s / len(x))), 'green')
    up = 0
    sum_of_lineal_func = 0
    squares = 0
    for i in range(len(x)):
        up += (y[i] - (answer_matrix[1] * math.log(x[i], math.e) + answer_matrix[0])) ** 2
        sum_of_lineal_func += (answer_matrix[1] * math.log(x[i], math.e) + answer_matrix[0])
        squares += (answer_matrix[1] * math.log(x[i], math.e) + answer_matrix[0]) ** 2
    cprint('\t\tДостоверность аппроксимации: ' + str(1 - (up / (squares - (sum_of_lineal_func ** 2) / len(x)))),
           'green')
    answer_matrix.append(math.sqrt(s / len(x)))
    return answer_matrix


def print_table(input_xy, linealM, squareM, exponentM, degreeM, logM):
    new_table = []
    x = input_xy[0]
    y = input_xy[1]
    for i in range(len(x)):
        if exponentM is None and logM is None:
            new_table.append([i + 1, x[i], y[i], linealM[0] * x[i] + linealM[1],
                              squareM[0] + squareM[1] * x[i] + squareM[2] * x[i] ** 2])
        elif exponentM is None:
            new_table.append([i + 1, x[i], y[i], linealM[0] * x[i] + linealM[1],
                              squareM[0] + squareM[1] * x[i] + squareM[2] * x[i] ** 2,
                              logM[1] * math.log(x[i], math.e) + logM[0]])
        elif logM is None:
            new_table.append([i + 1, x[i], y[i], linealM[0] * x[i] + linealM[1],
                              squareM[0] + squareM[1] * x[i] + squareM[2] * x[i] ** 2,
                              math.e ** exponentM[0] * math.e ** (exponentM[1] * x[i])])
        else:
            new_table.append([i + 1, x[i], y[i], linealM[0] * x[i] + linealM[1],
                              squareM[0] + squareM[1] * x[i] + squareM[2] * x[i] ** 2,
                              math.e ** exponentM[0] * math.e ** (exponentM[1] * x[i]),
                              math.e ** degreeM[0] * x[i] ** (degreeM[1]),
                              logM[1] * math.log(x[i], math.e) + logM[0]])
    print('\nTable:')
    if exponentM is None and logM is None:
        cprint(tabulate(new_table, headers=["№", "x", "f(x)", "LIN", "SQR"],
                        tablefmt="fancy_grid", floatfmt="2.5f"), 'cyan')
    elif exponentM is None:
        cprint(tabulate(new_table, headers=["№", "x", "f(x)", "LIN", "SQR", "LOG"],
                        tablefmt="fancy_grid", floatfmt="2.5f"), 'cyan')
    elif logM is None:
        cprint(tabulate(new_table, headers=["№", "x", "f(x)", "LIN", "SQR", "EXP"],
                        tablefmt="fancy_grid", floatfmt="2.5f"), 'cyan')
    else:
        cprint(tabulate(new_table, headers=["№", "x", "f(x)", "LIN", "SQR", "EXP", "DEG", "LOG"],
                        tablefmt="fancy_grid", floatfmt="2.5f"), 'cyan')


def choose_best_approximation(linealM, squareM, exponentM, degreeM, logM):
    print('\nBest approximation:\n')

    if exponentM is None and logM is None:
        min_sqr = min(linealM[2], squareM[3])
    elif exponentM is None:
        min_sqr = min(linealM[2], squareM[3], logM[2])
    elif logM is None:
        min_sqr = min(linealM[2], squareM[3], exponentM[2])
    else:
        min_sqr = min(linealM[2], squareM[3], exponentM[2], degreeM[2],
                      logM[2])

    if min_sqr == linealM[2]:
        cprint('\tLINEAR: y = ' + str(linealM[0]) + ' * x + ' + str(linealM[1]), 'green', attrs=['bold'])
    elif min_sqr == squareM[3]:
        cprint('\tSQUARE: y = ' + str(squareM[0]) + ' + ' + str(squareM[1]) + ' * x + ' + str(
            squareM[2]) + ' * x ^ 2', 'green', attrs=['bold'])
    elif exponentM is not None and min_sqr == exponentM[2]:
        cprint('\tEXPONENT: y = ' + str(math.e ** exponentM[0]) + ' * e ^ ( ' + str(
            exponentM[1]) + ' * x )', 'green', attrs=['bold'])
    elif logM is not None and min_sqr == logM[2]:
        cprint('\tLOGARIFM: y = ' + str(logM[1]) + ' * ln(x) + ' + str(logM[0]), 'green', attrs=['bold'])
    elif min_sqr == degreeM[2]:
        cprint('\tDEGREE: y = ' + str(math.e ** degreeM[0]) + ' * x ^ ( ' + str(
            degreeM[1]) + ' )', 'green', attrs=['bold'])


def create_graph(input_xy, linealM, squareM, exponentM, degreeM, logM):
    ax = plt.gca()
    plt.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    minimum = input_xy[0][0]
    maximum = input_xy[0][-1]
    x = np.linspace(minimum - ((maximum - minimum) / 20), maximum + ((maximum - minimum) / 20), 100)
    plt.title('y = f(x)')
    plt.plot(x, linealM[0] * x + linealM[1], color="g", linewidth=1, label='LIN')
    plt.plot(x, squareM[0] + squareM[1] * x + squareM[2] * x ** 2, color="b",
             linewidth=1, label='SQR')
    if exponentM is not None:
        plt.plot(x, math.e ** exponentM[0] * math.e ** (exponentM[1] * x), color="c",
                 linewidth=1, label='EXP')
    if degreeM is not None:
        plt.plot(x, math.e ** degreeM[0] * x ** (degreeM[1]), color="m", linewidth=1,
                 label='DEG')
    if logM is not None:
        plt.plot(x, logM[1] * np.log(x) + logM[0], color="y", linewidth=1, label='LOG')
    plt.plot(x, 0 * x, color="black", linewidth=1)
    for i in range(len(input_xy[0])):
        plt.scatter(input_xy[0][i], input_xy[1][i], color="r", s=30)
    plt.legend()
    plt.show()
    fig, axs = plt.subplots(5, sharex=True, sharey=True)
    fig.suptitle('y = f(x)')
    axs[0].plot(x, linealM[0] * x + linealM[1], color="g", linewidth=1, label='LIN')
    axs[1].plot(x, squareM[0] + squareM[1] * x + squareM[2] * x ** 2, color="b", linewidth=1, label='SQR')
    if exponentM is not None:
        axs[2].plot(x, math.e ** exponentM[0] * math.e ** (exponentM[1] * x), color="c", linewidth=1, label='EXP')
    if degreeM is not None:
        axs[3].plot(x, math.e ** degreeM[0] * x ** (degreeM[1]), color="m", linewidth=1, label='DEG')
    if logM is not None:
        axs[4].plot(x, logM[1] * np.log(x) + logM[0], color="y", linewidth=1, label='LOG')
    for i in range(5):
        axs[i].spines['top'].set_visible(False)
        axs[i].spines['right'].set_visible(False)
        axs[i].grid()
        if not ((i == 2 and exponentM is None) or (i == 3 and degreeM is None) or (
                i == 4 and logM is None)):
            axs[i].legend()
            for j in range(len(input_xy[0])):
                axs[i].scatter(input_xy[0][j], input_xy[1][j], color="r", s=20)
    plt.show()
    del x


##############################
#     PROGRAM BEGINNING      #
##############################

print('Напишите название файла: ')
filename = input()
with open(filename) as f:
    xy = [list(map(float, row.split())) for row in f.readlines()]
    xy[0].insert(0, "X")
    xy[1].insert(0, "Y")
print('\nFunction:')
print_matrix(xy)
xy[0].pop(0)
xy[1].pop(0)
print('\nApproximation functions:')
lineal_matrix = lineal(xy)
square_matrix = square(xy)
exponent_matrix = exponent(xy)
degree_matrix = degree(xy)
log_matrix = log(xy)
print_table(xy, lineal_matrix, square_matrix, exponent_matrix, degree_matrix, log_matrix)
choose_best_approximation(lineal_matrix, square_matrix, exponent_matrix, degree_matrix, log_matrix)
create_graph(xy, lineal_matrix, square_matrix, exponent_matrix, degree_matrix, log_matrix)
