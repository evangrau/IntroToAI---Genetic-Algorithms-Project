import random
import time

# params for the genetic algorithm
POPULATION_SIZE = 100
GENERATIONS = 200
MUTATION_RATE = 0.01
COPY_RATE = 0.20

# function to get daily prices from file
def read_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.strip())
    del data[0]
    del data[0]
    for i, val in enumerate(data):
        data[i] = float(val)
    return data


def simple_moving_average(data, n, s_num):
    # Calculates the simple moving average of the data using the specified window size
    if len(data) < n:
        return False # sell

    sum = 0
    i = n - s_num
    while i < n:
        sum += data[i]
        i += 1
    
    sma = sum / s_num - 1

    return data[n] > sma
    

def exponential_moving_average(data, n, e_num):
    # Calculates the exponential moving average of the data using the specified alpha value
    if len(data) < n:
        return False # sell
    
    alpha = 2 / e_num + 1
        
    numerator = 0
    denominator = 0

    i = n - e_num
    ex = 0
    while i < n:
        numerator += ((1-alpha)**ex)*data[i]
        denominator += (1-alpha)**ex
        ex += 1
        i += 1

    ema = numerator / denominator

    return data[n] > ema

def max_rule(data, n, m_num):
    if len(data) < n:
        return False
    
    max = 0
    i = n - m_num
    while i < n:
        if data[i] > max:
            max = data[i]
        i += 1

    return data[n] > max


def fitness(genotype):
    
    letter_order = [genotype[0], genotype[5], genotype[10]]
    operators = [genotype[4], genotype[9]]

    first_num = int(genotype[1:4])
    second_num = int(genotype[6:9])
    third_num = int(genotype[11:14])

    # frame = [letter_order[0], operators[0], letter_order[1], operators[1], letter_order[2]]
    # print(frame)

    capital = 20000
    gain = 0
    for dataset in datasets:
        shares = 0

        if capital != 20000:
            diff = 20000 - capital
            gain -= diff
            capital = 20000

        if (letter_order[0] == "s" and letter_order[1] == "e" and letter_order[2] == "m") and (first_num > 0 and second_num > 0 and third_num > 0):

            largest_num = max(first_num, second_num, third_num)

            while largest_num < len(dataset):

                sma = simple_moving_average(dataset, largest_num, first_num)
                ema = exponential_moving_average(dataset, largest_num, second_num)
                max_num = max_rule(dataset, largest_num, third_num)

                if operators[0] == "&" and operators[1] == "&":
                    if (sma and ema) and max_num:
                        while capital - dataset[largest_num] > 0:
                            capital -= dataset[largest_num]
                            shares += 1
                    else:
                        while shares > 0:
                            gain += dataset[largest_num]
                            shares -= 1
                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
                elif operators[0] == "&" and operators[1] == "|":
                    if (sma and ema) or max_num:
                        while capital - dataset[largest_num] > 0:
                            capital -= dataset[largest_num]
                            shares += 1
                    else:
                        while shares > 0:
                            gain += dataset[largest_num]
                            shares -= 1
                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
                elif operators[0] == "|" and operators[1] == "&":
                    if (sma or ema) and max_num:
                        while capital - dataset[largest_num] > 0:
                            capital -= dataset[largest_num]
                            shares += 1
                    else:
                        while shares > 0:
                            gain += dataset[largest_num]
                            shares -= 1
                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
                else:
                    if (sma or ema) or max_num:
                        while capital - dataset[largest_num] > 0:
                            capital -= dataset[largest_num]
                            shares += 1
                    else:
                        while shares > 0:
                            gain += dataset[largest_num]
                            shares -= 1

                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
            
                largest_num += 1
    
    return gain

# stuff for later
# # function to recombine the intermediate population
# def recombine(intermediate_population):
#     new_population = []
#     # choose 50 pairs of parents at random
#     for i in range(50):
#         parent1, parent2 = random.sample(intermediate_population, 2)
#         # 20% chance of copying parents directly
#         if random.random() < COPY_RATE:
#             child1 = parent1
#             child2 = parent2
#         else:
#             # choose a random crossover point
#             crossover_point = random.randint(1, len(genotype) - 1)
#             # combine parents at crossover point
#             child1 = parent1[:crossover_point] + parent2[crossover_point:]
#             child2 = parent2[:crossover_point] + parent1[crossover_point:]
#         # add children to new population
#         new_population.append(child1)
#         new_population.append(child2)
#     return new_population

# # function for mutation of an individual
# def mutate(individual):
#     # create new individual to return
#     mutated_individual = ""
#     # go through each gene in an individual's genotype
#     for gene in individual:
#         # 1% chance of mutation
#         if random.random() < MUTATION_RATE:
#             if gene == "s":
#                 letters = ["e", "m"]
#                 mutated_individual += letters[random.randint(0,1)]
#             elif gene == "e":
#                 letters = ["s", "m"]
#                 mutated_individual += letters[random.randint(0,1)]
#             elif gene == "m":
#                 letters = ["s", "e"]
#                 mutated_individual += letters[random.randint(0,1)]
#             elif gene == "&":
#                 mutated_individual += "|"
#             elif gene == "|":
#                 mutated_individual += "&"
#             elif gene == "0":
#                 numbers = ["1","2","3","4","5","6","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "1":
#                 numbers = ["0","2","3","4","5","6","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "2":
#                 numbers = ["0","1","3","4","5","6","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "3":
#                 numbers = ["0","1","2","4","5","6","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "4":
#                 numbers = ["0","1","2","3","5","6","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "5":
#                 numbers = ["0","1","2","3","4","6","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "6":
#                 numbers = ["0","1","2","3","4","5","7","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "7":
#                 numbers = ["0","1","2","3","4","5","6","8","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "8":
#                 numbers = ["0","1","2","3","4","5","6","7","9"]
#                 mutated_individual += numbers[random.randint(0,8)]
#             elif gene == "9":
#                 numbers = ["0","1","2","3","4","5","6","7","8"]
#                 mutated_individual += numbers[random.randint(0,8)]
#         else:
#             mutated_individual += gene
#     return mutated_individual

companies = ["AAPL", "DDS", "F", "GE", "RTX"]
dir = "Datasets/historical-stock-prices/"
dataset_strings = []

for company in companies:
    for i in range(1,6):
        dataset_strings.append(f"{dir}{company}-{i}.txt")

datasets = []
for d in dataset_strings:
    datasets.append(read_file(d))

genotype = "s050&e030&m010"

start_time = time.time()

print("Genotype: " + genotype)
print("Fitness: ${:.2f}".format(fitness(genotype)))

end_time = time.time()
time_elapsed = end_time - start_time
print("\nTime elapsed: {:.2f} seconds".format(time_elapsed))
