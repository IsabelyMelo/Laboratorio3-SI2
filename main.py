import random
import math
import matplotlib.pyplot as plt
import networkx as nx

random.seed(32)

Ncidades = 8
cidades = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(Ncidades)}

# tamanho da população (entre 40 e 120)
POP_SIZE = 100
# número máximo de gerações (entre 150 e 400)
NUM_GENERATIONS = 200
# k da seleção por torneio (entre 2 e 4)
TOURNAMENT_SIZE = 3
# taxa de crossover (~80%)
CROSSOVER_RATE = 0.8
# taxa de mutação (2%, entre 1% e 5%)
MUTATION_RATE = 0.02
# número de indivíduos preservados por elitismo
ELITE_SIZE = 2
# critério opcional de parada por estagnação
NO_IMPROVEMENT_LIMIT = 50

# Funções auxiliares do TSP
def distance(city1, city2):
    x1, y1 = cidades[city1]
    x2, y2 = cidades[city2]
    return math.hypot(x2 - x1, y2 - y1)

def tour_length(tour):
    length = 0.0
    for i in range(len(tour)):
        city_from = tour[i]
        city_to = tour[(i + 1) % len(tour)]
        length += distance(city_from, city_to)
    return length

def fitness(tour):
    return 1.0 / tour_length(tour)

def create_individual():
    tour = list(cidades.keys())
    random.shuffle(tour)
    return tour

def create_population(size):
    return [create_individual() for _ in range(size)]

def fill_child(child, other_parent, size, b):
    idx = (b + 1) % size
    parent_idx = (b + 1) % size
    while None in child:
        gene = other_parent[parent_idx]
        if gene not in child:
            child[idx] = gene
            idx = (idx + 1) % size
        parent_idx = (parent_idx + 1) % size
    return child

# Operador de selecao por torneio
def tournament_selection(population, k):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: tour_length(ind))
    return selected[0]

# Operador de crossover
def order_crossover(parent1, parent2):
    if random.random() > CROSSOVER_RATE:
        return parent1[:], parent2[:]

    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))

    child1 = [None] * size
    child2 = [None] * size

    child1[a:b + 1] = parent1[a:b + 1]
    child2[a:b + 1] = parent2[a:b + 1]

    child1 = fill_child(child1, parent2, size, b)
    child2 = fill_child(child2, parent1, size, b)

    return child1, child2

# Operador de mutacao
def swap_mutation(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]

# Gera uma nova populacao
def evolve_population(population):
    population.sort(key=lambda ind: tour_length(ind))

    new_population = population[:ELITE_SIZE]

    # selecao por torneio
    while len(new_population) < POP_SIZE:
        parent1 = tournament_selection(population, TOURNAMENT_SIZE)
        parent2 = tournament_selection(population, TOURNAMENT_SIZE)

        child1, child2 = order_crossover(parent1, parent2)

        swap_mutation(child1)
        swap_mutation(child2)

        new_population.append(child1)
        if len(new_population) < POP_SIZE:
            new_population.append(child2)

    return new_population

# Executa o algoritmo genetico completo er egistra o melhor individuo por geracao
def run_ga():
    population = create_population(POP_SIZE)
    best_per_gen = []
    best_individual = None
    best_distance = float('inf')
    no_improvement = 0

    for gen in range(NUM_GENERATIONS):
        population.sort(key=lambda ind: tour_length(ind))
        current_best = population[0]
        current_distance = tour_length(current_best)
        best_per_gen.append(current_distance)

        if current_distance < best_distance:
            best_distance = current_distance
            best_individual = current_best[:]
            no_improvement = 0
        else:
            no_improvement += 1

        if NO_IMPROVEMENT_LIMIT is not None and no_improvement >= NO_IMPROVEMENT_LIMIT:
            print(f"Parando na geração {gen} por falta de melhoria.")
            break

        population = evolve_population(population)

    population.sort(key=lambda ind: tour_length(ind))
    current_best = population[0]
    current_distance = tour_length(current_best)
    if current_distance < best_distance:
        best_distance = current_distance
        best_individual = current_best[:]
        best_per_gen.append(current_distance)

    return best_individual, best_distance, best_per_gen

best_tour, best_dist, history = run_ga()

print("Coordenadas das cidades:")
for city, coord in cidades.items():
    print(f"Cidade {city}: {coord}")

print("\nMelhor rota encontrada:")
print(best_tour)
print(f"Melhor distância total: {best_dist:.4f}")

# Graficos
G = nx.Graph()
for node, pos in cidades.items():
    G.add_node(node, pos=pos)

for i in range(len(best_tour)):
    u = best_tour[i]
    v = best_tour[(i + 1) % len(best_tour)]
    G.add_edge(u, v)

fig, ax = plt.subplots(figsize=(6, 6))
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, ax=ax)

ax.set_axis_on()
ax.tick_params(left=True, bottom=True, labelleft=False, labelbottom=False)

ax.set_title(
    f"Melhor rota encontrada\n"
    f"Distância total: {best_dist:.4f}"
)

plt.tight_layout()
plt.show()

plt.figure()
plt.plot(history)
plt.xlabel("Geração")
plt.ylabel("Melhor distância")
plt.title("Evolução da melhor distância por geração")
plt.tight_layout()
plt.show()