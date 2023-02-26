import random
import math

# params for the genetic algorithm
POPULATION_SIZE = 100
GENERATIONS = 200
MUTATION_RATE = 0.005
COPY_RATE = 0.25

# function to get the information from the .kp file
def read_file(filename):
   data = []
   with open(filename) as f:
      for line in f:
         data.append(list(map(str, line.strip().split(',')))) # implementation to accept strings for the label
   return data

# function to initialize a population randomly
def initialize_population():
    # create empty array
    population = []
    for i in range(POPULATION_SIZE):
        # randomly choose if each gene will be 0 or 1
        # 0 = don't include item in knapsack, 1 = include item in knapsack
        individual = ''.join(str(random.randint(0, 1)) for _ in range(len(data)))
        # add the individual to the population
        population.append(individual)
    return population

# function to calculate the fitness of an individual
def calculate_fitness(individual, weights, values, max_weight):
    # create variables to store total value and weight
    total_weight = 0
    total_value = 0
    # check each gene in an individual's genotype
    for i in range(len(individual)):
        # if an item is included in the knapsack, then add
        # that item's value and weight to the total
        if individual[i] == '1':
            total_weight += weights[i]
            total_value += values[i]
            # if the total weight is greater than the max weight, then
            # it is invalid, thus the fitness is very low
            if total_weight > max_weight:
                return -math.inf
    # if the total weight is 0, then no items are included
    if total_weight == 0:
        return -math.inf
    return total_value/total_weight


# function to generate an intermediate population
def generate_intermediate_population(population):
    fitnesses = [calculate_fitness(individual, weights, values, max_weight) for individual in population]
    total_fitness = sum(fitnesses)
    # calculate average fitness of the population
    avg = total_fitness/len(population) if total_fitness != -math.inf else 0
    # calculate the number of individuals to select from each parent
    n = [fitness/avg if avg != 0 else 0 if fitness != max(fitnesses) else 1 for fitness in fitnesses]
    # use remainder stochastic sampling to select individuals from parents
    intermediate_population = []
    for i in range(len(population)):
        # select the whole number part of n[i] individuals from parent i
        num_individuals = int(n[i])
        for j in range(num_individuals):
            intermediate_population.append(population[i])
        # randomly select one additional individual based on the fractional part of n[i]
        if random.random() < n[i] - num_individuals:
            intermediate_population.append(population[i])
    # if the intermediate population size is still smaller than the population size, randomly add individuals until it reaches the desired size
    while len(intermediate_population) < POPULATION_SIZE:
        intermediate_population.append(random.choice(population))
    return intermediate_population

# function to recombine the intermediate population
def recombine(intermediate_population):
    new_population = []
    # choose 50 pairs of parents at random
    for i in range(50):
        parent1, parent2 = random.sample(intermediate_population, 2)
        # 25% chance of copying parents directly
        if random.random() < COPY_RATE:
            child1 = parent1
            child2 = parent2
        else:
            # choose a random crossover point
            crossover_point = random.randint(1, len(parent1) - 1)
            # combine parents at crossover point
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
        # add children to new population
        new_population.append(child1)
        new_population.append(child2)
    return new_population

# function for mutation of an individual
def mutate(individual):
    # create new individual to return
    mutated_individual = ""
    # go through each gene in an individual's genotype
    for gene in individual:
        # 0.5% chance of mutation
        if random.random() < MUTATION_RATE:
            if gene == "0":
                mutated_individual += "1"
            else:
                mutated_individual += "0"
        else:
            mutated_individual += gene
    return mutated_individual

# get information from the dataset
filename = "Datasets/my-tests/test1.kp"
data = read_file(filename)

max_weight = int(data[0][1]) # gets max weight from the file
del data[0] # gets rid of first index in array containing number of lines and max weight

# gets all of the weights and puts them into an array and does the same with complementing values
weights = [sublist[1] for sublist in data]
values = [sublist[2] for sublist in data]
# converts the arrays into int arrays
weights = [int(i) for i in weights]
values = [int(i) for i in values]

# Run the genetic algorithm
# initialize starting population randomly
population = initialize_population()
best_fitness = 0
best_individual = None
# run the algorithm for 200 generations
for generation in range(GENERATIONS):
    intermediate_population = generate_intermediate_population(population)
    new_population = recombine(intermediate_population)
    for i in range(len(new_population)):
        new_population[i] = mutate(new_population[i])
    population = new_population
    # update the best individual found so far
    for individual in population:
        fitness = calculate_fitness(individual, weights, values, max_weight)
        if fitness > best_fitness:
            best_fitness = fitness
            best_individual = individual
            max_value = sum([v * int(individual[i]) for i, v in enumerate(values)])
            weight = sum([w * int(individual[i]) for i, w in enumerate(weights)])

# Print results
print("Number of Generations:", GENERATIONS)
print("Max Value:", max_value)
print("Max Weight:", weight)
print("Best Individual:", best_individual)
