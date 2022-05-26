from math import radians, cos, sin, asin, sqrt

import numpy as np
import pandas as pd
import random


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


class City:
    def __init__(self, lon, lat, id):
        self.lon = lon
        self.lat = lat
        self.id = id

    def distance(self, city):
        distance = haversine(self.lon, self.lat, city.lon, city.lat)
        return distance

    def __repr__(self):
        return "(" + str(self.lon) + "," + str(self.lat) + ")"


class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def route_distance(self):
        if self.distance == 0:
            path_distance = 0
            for i in range(0, len(self.route)):
                from_city = self.route[i]
                to_city = None
                if i + 1 < len(self.route):
                    to_city = self.route[i + 1]
                else:
                    to_city = self.route[0]
                path_distance += from_city.distance(to_city)
            self.distance = path_distance
        return self.distance

    def route_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())
        return self.fitness


def create_route(city_list):
    route = random.sample(city_list, len(city_list))
    return route


def initial_population(pop_size, city_list):
    population = []

    for i in range(0, pop_size):
        population.append(create_route(city_list))
    return population


def rank_routes(population):
    fitness_results = {}
    for i in range(0, len(population)):
        fitness_results[i] = Fitness(population[i])
    return sorted(fitness_results.items(), key=lambda x: x[1].route_fitness(), reverse=True)


def selection(pop_ranked, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array(list(map(lambda x: (x[0], x[1].route_fitness()), pop_ranked))), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[i][0])
    for i in range(0, len(pop_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(0, len(pop_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(pop_ranked[i][0])
                break
    return selection_results


def mating_pool(population, selection_results):
    matingpool = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        matingpool.append(population[index])
    return matingpool


def breed(parent1, parent2):
    child = []
    child_p1 = []
    child_p2 = []

    gene_a = int(random.random() * len(parent1))
    gene_b = int(random.random() * len(parent1))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        child_p1.append(parent1[i])

    child_p2 = [item for item in parent2 if item not in child_p1]

    child = child_p1 + child_p2
    return child


def breed_population(matingpool, elite_size):
    children = []
    length = len(matingpool) - elite_size
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, elite_size):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swap_with]

            individual[swapped] = city2
            individual[swap_with] = city1
    return individual


def mutate_population(population, mutation_rate):
    mutated_pop = []

    for ind in range(0, len(population)):
        mutated_ind = mutate(population[ind], mutation_rate)
        mutated_pop.append(mutated_ind)
    return mutated_pop


def next_generation(current_gen, elite_size, mutation_rate):
    pop_ranked = rank_routes(current_gen)
    selection_results = selection(pop_ranked, elite_size)
    matingpool = mating_pool(current_gen, selection_results)
    children = breed_population(matingpool, elite_size)
    next_gen = mutate_population(children, mutation_rate)
    return next_gen


def genetic_algorithm(population, pop_size, elite_size, mutation_rate, generations):
    pop = initial_population(pop_size, population)
    print("Initial distance: " + str(1 / rank_routes(pop)[0][1].route_fitness()))

    for i in range(0, generations):
        pop = next_generation(pop, elite_size, mutation_rate)

    rank = rank_routes(pop)
    print("Final distance: " + str(1 / rank[0][1].route_fitness()))
    best_route_index = rank[0][0]
    best_route = pop[best_route_index]
    return best_route, rank[0][1].route_distance()


# cities = [
#     {"coordinate": [59.51558758306887, 48.16863948273658], "name": "Waypoint 1", "id": "1"},
#     {"coordinate": [8.890580430511505, 23.314839367161525], "name": "Waypoint 2", "id": "2"},
#     {"coordinate": [101.8905847220459, 23.658768645568983], "name": "Waypoint 3", "id": "3"},
#     {"coordinate": [102.45307613897705, -13.390168290108448], "name": "Waypoint 4", "id": "4"},
#     {"coordinate": [29.515580430511505, -10.823785838014572], "name": "Waypoint 5", "id": "5"},
#     {"coordinate": [61.20307613897708, 26.376925103513457], "name": "Waypoint 6", "id": "6"}
# ]
#
# cityList = []
#
# for i in range(0, len(cities)):
#     cityList.append(City(id=cities[i]["id"], lon=cities[i]["coordinate"][0], lat=cities[i]["coordinate"][1]))
#
# iteration_map = {
#     4: 100,
#     8: 170,
#     12: 400,
#     25: 900
# }
#
# num_of_generation = iteration_map[max([i for i in iteration_map.keys() if i < len(cities)])]
#
# print(list(map(lambda x: x.id, genetic_algorithm(population=cityList, pop_size=100, elite_size=20, mutation_rate=0.01, generations=num_of_generation))))
