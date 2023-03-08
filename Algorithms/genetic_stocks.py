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
            data.append(line.strip()) # get each line and put it in the array
    del data[0] # get rid of company name
    del data[0] # get rid of time period
    for i, val in enumerate(data): # change each value to floats
        data[i] = float(val)
    return data

# function to calculate the SMA
def simple_moving_average(data, n, s_num):
    # if the value we are starting from is greater than
    # the last day in the file, then we sell
    if len(data) < n:
        return False # sell

    sum = 0
    i = n - s_num
    while i < n: # sum up values over the past n days
        sum += data[i]
        i += 1
    
    sma = sum / s_num - 1 # sma based on the given formula

    return data[n] > sma # return whether or not the current price is greater than the sma
    
# function to find the EMA
def exponential_moving_average(data, n, e_num):
    # if the value we are starting from is greater than
    # the last day in the file, then we sell
    if len(data) < n:
        return False # sell
    
    alpha = 2 / e_num + 1 # calculating alpha based on the given formula
        
    numerator = 0
    denominator = 0

    i = n - e_num
    ex = 0
    while i < n: # calculating the numerator and denominator for the ema based on the given formula
        numerator += ((1-alpha)**ex)*data[i]
        denominator += (1-alpha)**ex
        ex += 1
        i += 1

    ema = numerator / denominator # ema based on given formula

    return data[n] > ema # return whether or not the current price is greater than the ema

# function to find the MAX
def max_rule(data, n, m_num):
    # if the value we are starting from is greater than
    # the last day in the file, then we sell
    if len(data) < n:
        return False # sell
    
    max = 0
    i = n - m_num
    while i < n: # find the max value over the past n days
        if data[i] > max:
            max = data[i]
        i += 1

    return data[n] > max # return whether or not the current price is greater than the max

# function to find the fitness of a given individual/genotype
def fitness(genotype):
    
    # get the order of the letters/functions to be called
    letter_order = [genotype[0], genotype[5], genotype[10]]
    # get the order of the operators
    operators = [genotype[4], genotype[9]]

    # get the number of days meant for each function
    first_num = int(genotype[1:4])
    second_num = int(genotype[6:9])
    third_num = int(genotype[11:14])

    # set initial values for capital and gain
    capital = 20000
    gain = 0
    # iterate through each dataset
    for dataset in datasets:
        # keep track of how many shares bought
        shares = 0
        # reset capital back to 20000
        if capital != 20000:
            diff = 20000 - capital
            gain -= diff
            capital = 20000
        # keep out all strategies that don't buy or sell
        if not (first_num == 0 and second_num == 0 and third_num == 0):
            # if all three strategies are > 0
            if first_num > 0 and second_num > 0 and third_num > 0:
                # find the largest number and start from there
                index = max(first_num, second_num, third_num)
                # go through the entire dataset and buy and sell as needed
                while index < len(dataset):
                    
                    # getting the first strategy
                    if letter_order[0] == "s":
                        first_arg = simple_moving_average(dataset, index, first_num)
                    elif letter_order[0] == "e":
                        first_arg = exponential_moving_average(dataset, index, first_num)
                    else:
                        first_arg = max_rule(dataset, index, first_num)
                    # getting the second strategy
                    if letter_order[1] == "s":
                        second_arg = simple_moving_average(dataset, index, second_num)
                    elif letter_order[1] == "e":
                        second_arg = exponential_moving_average(dataset, index, second_num)
                    else:
                        second_arg = max_rule(dataset, index, second_num)
                    # getting the third strategy
                    if letter_order[2] == "s":
                        third_arg = simple_moving_average(dataset, index, third_num)
                    elif letter_order[2] == "e":
                        third_arg = exponential_moving_average(dataset, index, third_num)
                    else:
                        third_arg = max_rule(dataset, index, third_num)
                    # if both operators are & then all 3 have to be true to buy
                    if operators[0] == "&" and operators[1] == "&":
                        if (first_arg and second_arg) and third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                    # only first two or third have to be true to buy
                    elif operators[0] == "&" and operators[1] == "|":
                        if (first_arg and second_arg) or third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                    # third and first or second have to be true to buy
                    elif operators[0] == "|" and operators[1] == "&":
                        if (first_arg or second_arg) and third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                    # any single one has to be true to buy
                    else:
                        if (first_arg or second_arg) or third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                
                    index += 1
            # if the first and second strategies are > 0
            elif first_num > 0 and second_num > 0 and third_num == 0:
                # find largest and start from there
                index = max(first_num, second_num)
                # iterate through entire dataset
                while index < len(dataset):
                    
                    # getting the first strategy
                    if letter_order[0] == "s":
                        first_arg = simple_moving_average(dataset, index, first_num)
                    elif letter_order[0] == "e":
                        first_arg = exponential_moving_average(dataset, index, first_num)
                    else:
                        first_arg = max_rule(dataset, index, first_num)
                    # getting the second strategy
                    if letter_order[1] == "s":
                        second_arg = simple_moving_average(dataset, index, second_num)
                    elif letter_order[1] == "e":
                        second_arg = exponential_moving_average(dataset, index, second_num)
                    else:
                        second_arg = max_rule(dataset, index, second_num)
                    # both have to be true to buy
                    if operators[0] == "&":
                        if first_arg and second_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                    # only one has to be true to buy
                    else:
                        if first_arg or second_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                
                    index += 1
            # if the first and third strategies are > 0
            elif first_num > 0 and second_num == 0 and third_num > 0:
                # find largest and start from there
                index = max(first_num, third_num)
                # iterate through entire dataset
                while index < len(dataset):
                    
                    # getting the first strategy
                    if letter_order[0] == "s":
                        first_arg = simple_moving_average(dataset, index, first_num)
                    elif letter_order[0] == "e":
                        first_arg = exponential_moving_average(dataset, index, first_num)
                    else:
                        first_arg = max_rule(dataset, index, first_num)
                    # getting the third strategy
                    if letter_order[2] == "s":
                        third_arg = simple_moving_average(dataset, index, third_num)
                    elif letter_order[2] == "e":
                        third_arg = exponential_moving_average(dataset, index, third_num)
                    else:
                        third_arg = max_rule(dataset, index, third_num)
                    # both have to be true to buy
                    if operators[1] == "&":
                        if first_arg and third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                    # only one has to be true to buy
                    else:
                        if first_arg or third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                
                    index += 1
            # if the second and third strategies are > 0
            elif first_num == 0 and second_num > 0 and third_num > 0:
                # find largest and start from there
                index = max(second_num, third_num)
                # iterate through entire dataset
                while index < len(dataset):
                    
                    # getting the second strategy
                    if letter_order[1] == "s":
                        second_arg = simple_moving_average(dataset, index, second_num)
                    elif letter_order[1] == "e":
                        second_arg = exponential_moving_average(dataset, index, second_num)
                    else:
                        second_arg = max_rule(dataset, index, second_num)
                    # getting the third strategy
                    if letter_order[2] == "s":
                        third_arg = simple_moving_average(dataset, index, third_num)
                    elif letter_order[2] == "e":
                        third_arg = exponential_moving_average(dataset, index, third_num)
                    else:
                        third_arg = max_rule(dataset, index, third_num)

                    if operators[1] == "&":
                        if second_arg and third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                    else:
                        if second_arg or third_arg:
                            # buy as many shares as possible
                            while capital - dataset[index] > 0:
                                capital -= dataset[index]
                                shares += 1
                        else:
                            # sell all shares
                            while shares > 0:
                                gain += dataset[index]
                                shares -= 1
                        # if any shares are left over then sell them all at the final closing price
                        while shares > 0:
                            gain += dataset[len(dataset) - 1]
                            shares -= 1
                
                    index += 1
            # if just the first strategy is > 0
            elif first_num > 0 and second_num == 0 and third_num == 0:
                # start at 1st
                index = first_num
                # iterate through entire dataset
                while index < len(dataset):
                    
                    # getting the first strategy
                    if letter_order[0] == "s":
                        first_arg = simple_moving_average(dataset, index, first_num)
                    elif letter_order[0] == "e":
                        first_arg = exponential_moving_average(dataset, index, first_num)
                    else:
                        first_arg = max_rule(dataset, index, first_num)
                    # buy if true
                    if first_arg:
                        # buy as many shares as possible
                        while capital - dataset[index] > 0:
                            capital -= dataset[index]
                            shares += 1
                    # sell otherwise
                    else:
                        # sell all shares
                        while shares > 0:
                            gain += dataset[index]
                            shares -= 1
                    # if any shares are left over then sell them all at the final closing price
                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
                
                    index += 1
            # if just the second strategy is > 0
            elif first_num == 0 and second_num > 0 and third_num == 0:
                # start at 2nd
                index = second_num
                # iterate through entire dataset
                while index < len(dataset):
                    
                    # getting the second strategy
                    if letter_order[1] == "s":
                        second_arg = simple_moving_average(dataset, index, second_num)
                    elif letter_order[1] == "e":
                        second_arg = exponential_moving_average(dataset, index, second_num)
                    else:
                        second_arg = max_rule(dataset, index, second_num)
                    # buy if true
                    if second_arg:
                        # buy as many shares as possible
                        while capital - dataset[index] > 0:
                            capital -= dataset[index]
                            shares += 1
                    # sell otherwise
                    else:
                        # sell all shares
                        while shares > 0:
                            gain += dataset[index]
                            shares -= 1
                    # if any shares are left over then sell them all at the final closing price
                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
                
                    index += 1
            # if just the third strategy is > 0
            elif first_num == 0 and second_num == 0 and third_num > 0:
                # start at 3rd
                index = third_num
                # iterate through entire dataset
                while index < len(dataset):
                    
                    # getting the third strategy
                    if letter_order[2] == "s":
                        third_arg = simple_moving_average(dataset, index, third_num)
                    elif letter_order[2] == "e":
                        third_arg = exponential_moving_average(dataset, index, third_num)
                    else:
                        third_arg = max_rule(dataset, index, third_num)
                    # buy if true  
                    if third_arg:
                        # buy as many shares as possible
                        while capital - dataset[index] > 0:
                            capital -= dataset[index]
                            shares += 1
                    # sell otherwise
                    else:
                        # sell all shares
                        while shares > 0:
                            gain += dataset[index]
                            shares -= 1
                    # if any shares are left over then sell them all at the final closing price
                    while shares > 0:
                        gain += dataset[len(dataset) - 1]
                        shares -= 1
                
                    index += 1
    
    return gain # return the total gain over all datasets

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

# getting data from each dataset
companies = ["AAPL", "DDS", "F", "GE", "RTX"]
dir = "Datasets/historical-stock-prices/"
dataset_strings = []

for company in companies:
    for i in range(1,6):
        dataset_strings.append(f"{dir}{company}-{i}.txt")

datasets = []
for d in dataset_strings:
    datasets.append(read_file(d))

# setting test genotype
# genotypes = []
genotype = "s050&e030&m010"

start_time = time.time()

print("Genotype: " + genotype)
print("Fitness: ${:.2f}".format(fitness(genotype)))

end_time = time.time()
time_elapsed = end_time - start_time
print("Time elapsed: {:.2f} seconds".format(time_elapsed))
