import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

N = 300
n_gen = 300
percentage_elitismo = 0.02
p_cruce = 0.8
p_mutacion = 0.1
movimientos = ["arriba", "abajo", "izquierda", "derecha"]
t = {"arriba": (-1, 0), "abajo": (1, 0), "derecha": (0, 1), "izquierda": (0, -1)}
salto = 2


def cromosoma():
    instruc = []

    for i in [0, 1]:
        for j in [0, 1]:
            for k in [0, 1]:
                instruc.append(((i, j, k), random.choice(movimientos)))

    return instruc


def mutacion(individuo):
    for i in range(3):
        pos = random.randint(0, 7)

        (i, j, k), mov = individuo[pos]

        individuo[pos] = ((i, j, k), random.choice(movimientos))

    return individuo


def crossover(indiv1, indiv2):
    pos_cruce = random.randint(0, 7)

    return indiv1[:pos_cruce] + indiv2[pos_cruce:]


def sn(poblacion, maze):
    rankings = []

    for indiv in poblacion:
        rankings.append((fitness(indiv, maze), indiv))

    rankings.sort(reverse=True, key=lambda x: x[0])

    return [indiv for _, indiv in rankings[:N]]


def simular(indiv, maze):
    fila, col = (1, 0)
    cou = 0

    vis = {}

    for paso in range(500):
        # arriba, abajo, derecha
        i, j, k = maze[fila - 1][col], maze[fila + 1][col], maze[fila][col + 1]

        tupla, accion = indiv[(i * 4) + (j * 2) + (k)]
        tF, tC = t[accion]

        if col + tC < 0:
            return 0, cou

        if maze[fila + tF][col + tC] == 1:
            return 0, cou

        fila, col = fila + tF, col + tC

        if (fila, col) in vis:
            return 0, cou

        vis[(fila, col)] = True

        cou += 1

        if fila == 13 and col == 14:
            return 1, cou

    # Llega, nPasos, distanciaAlOrigen
    return 0, cou


def fitness(individuo, maze):
    llega, cou = simular(individuo, maze)

    return llega * 1000 + cou


def mostrarPasos(indiv, maze):
    pasos = [(1, 0)]
    fila, col = (1, 0)

    for paso in range(500):

        # arriba, abajo, derecha
        i, j, k = maze[fila - 1][col], maze[fila + 1][col], maze[fila][col + 1]

        tupla, accion = indiv[(i * 4) + (j * 2) + (k)]
        tF, tC = t[accion]

        if col + tC < 0:
            return pasos

        if maze[fila + tF][col + tC] == 1:
            return pasos

        fila, col = fila + tF, col + tC

        if fila == 13 and col == 14:
            return pasos

        pasos.append((fila, col))

    return pasos


def genetico(maze):
    # Crear poblacion inicial
    poblacion = []
    for i in range(N):
        poblacion.append(cromosoma())

    for i in range(n_gen):
        poblacionElite = poblacion[: int(0.2 * N)]
        nuevaPoblacion = poblacionElite

        # Mutacion
        for indiv in poblacion:
            if random.random() < p_mutacion:
                nuevaPoblacion.append(mutacion(indiv))

        # Crossover
        for j in range(20):
            for k in range(300):
                if i != k:
                    if random.random() < p_cruce:
                        nuevaPoblacion.append(crossover(poblacion[j], poblacion[k]))

        # Seleccion natural
        nuevaPoblacion = sn(nuevaPoblacion, maze)

        poblacion = nuevaPoblacion

        print(
            "GEN #"
            + str(i)
            + " = "
            + str(fitness(poblacion[0], maze))
            + " "
            + str(fitness(poblacion[200], maze))
        )

    return poblacion[0]


def display_maze(maze):
    cmap = ListedColormap(["white", "black", "green", "black"])
    plt.figure(figsize=(6, 6))
    plt.pcolor(maze[::-1], cmap=cmap, edgecolors="k", linewidths=2)
    plt.gca().set_aspect("equal")
    plt.xticks([])
    plt.yticks([])
    plt.title("Maze with Entrance and Exit")
    plt.show()


maze = np.loadtxt("./maze_case_base.txt", dtype=int)
# display_maze(maze)

best = genetico(maze)
pasos = mostrarPasos(best, maze)

nuevoMaze = maze
for i, j in pasos:
    nuevoMaze[i][j] = 2

print(nuevoMaze)

display_maze(nuevoMaze)
