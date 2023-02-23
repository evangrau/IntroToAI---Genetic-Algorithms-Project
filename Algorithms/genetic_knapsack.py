import random

# Define the parameters
POPULATION_SIZE = 100
GENERATIONS = 200
MUTATION_RATE = 0.005
RECOMBINATION_RATE = 0.5

# Define the knapsack problem parameters
values = [10, 5, 15, 7, 6, 18, 3]
weights = [2, 3, 5, 4, 2, 6, 1]
capacity = 12

# Define the fitness function
def fitness(individual):
    total_value = sum([values[i] for i in range(len(individual)) if individual[i] == 1])
    total_weight = sum([weights[i] for i in range(len(individual)) if individual[i] == 1])
    if total_weight > capacity:
        return 0
    return total_value / total_weight

# Define the remainder stochastic sampling function
def remainder_stochastic_sampling(fitness_values, k):
    intermediate_population = []
    sum_fitness = sum(fitness_values)
    p = [fitness_values[i] / sum_fitness for i in range(len(fitness_values))]
    counts = [int(POPULATION_SIZE * p[i]) for i in range(len(p))]
    remainder = POPULATION_SIZE - sum(counts)
    for i in range(remainder):
        counts[i] += 1
    for i in range(len(counts)):
        intermediate_population.extend([i] * counts[i])
    return [random.choice(intermediate_population) for i in range(k)]

# Define the recombination function
def recombine(parent1, parent2):
    if random.random() < RECOMBINATION_RATE:
        crossover_point = random.randint(0, len(parent1)-1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        child1 = parent1
        child2 = parent2
    return child1, child2

# Define the mutation function
def mutate(individual):
    mutated = False
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
            mutated = True
    if not mutated:
        index = random.randint(0, len(individual)-1)
        individual[index] = 1 - individual[index]
    return individual

# Initialize the population randomly
population = [[random.randint(0, 1) for i in range(len(values))] for j in range(POPULATION_SIZE)]

# Run the genetic algorithm
for generation in range(GENERATIONS):
    # Calculate the fitness of each individual
    fitness_values = [fitness(individual) for individual in population]

    # Select parents using remainder stochastic sampling
    intermediate_population = remainder_stochastic_sampling(fitness_values, int(RECOMBINATION_RATE * POPULATION_SIZE))

    # Recombine parents
    new_population = []
    for i in range(int(RECOMBINATION_RATE * POPULATION_SIZE // 2)):
        parent1 = population[intermediate_population[random.randint(0, len(intermediate_population)-1)]]
        parent2 = population[intermediate_population[random.randint(0, len(intermediate_population)-1)]]
        child1, child2 = recombine(parent1, parent2)
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))

    # Copy parents with 25% probability
    for i in range(int(POPULATION_SIZE * 0.25)):
        new_population.append(population[random.randint(0, POPULATION_SIZE-1)])

    # Replace the old population with the new population
    population = new_population

# Find the individual with the highest fitness value
best_individual = population[0]
best_fitness = fitness(best_individual)
for individual in population:
    if fitness(individual) > best_fitness:
        best_individual = individual
        best_fitness = fitness(individual)

# Print the best solution
print("Best solution found:")
print("Knapsack contents: ", end="")
for i in range(len(best_individual)):
    if best_individual[i] == 1:
        print(f"{i+1} ", end="")

print(f"\nTotal value: {sum([values[i] for i in range(len(best_individual)) if best_individual[i] == 1])}")
print(f"Total weight: {sum([weights[i] for i in range(len(best_individual)) if best_individual[i] == 1])}")
print(f"Fitness value: {best_fitness}")
