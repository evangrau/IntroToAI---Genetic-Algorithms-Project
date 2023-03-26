import random
import time
import threading

# params for the genetic algorithm
POPULATION_SIZE = 50
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

    if denominator == 0:
        return False

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

    # keep out all strategies that don't buy or sell
    if not (first_num == 0 and second_num == 0 and third_num == 0):
        # iterate through each dataset
        for dataset in datasets:
            # keep track of how many shares bought
            shares = 0
            # reset capital back to 20000
            if capital != 20000:
                diff = 20000 - capital
                gain -= diff
                capital = 20000

            # find the largest number and start from there
            index = max(first_num, second_num, third_num)
            # if all three strategies are > 0
            if first_num > 0 and second_num > 0 and third_num > 0:
                # go through the entire dataset and buy and sell as needed
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
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
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                    # only first two or third have to be true to buy
                    elif operators[0] == "&" and operators[1] == "|":
                        if (first_arg and second_arg) or third_arg:
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                    # third and first or second have to be true to buy
                    elif operators[0] == "|" and operators[1] == "&":
                        if (first_arg or second_arg) and third_arg:
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                    # any single one has to be true to buy
                    else:
                        if (first_arg or second_arg) or third_arg:
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                
                    index += 1
            # if the first and second strategies are > 0
            elif first_num > 0 and second_num > 0 and third_num == 0:
                # iterate through entire dataset
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
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
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                    # only one has to be true to buy
                    else:
                        if first_arg or second_arg:
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                
                    index += 1
            # if the first and third strategies are > 0
            elif first_num > 0 and second_num == 0 and third_num > 0:
                # iterate through entire dataset
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
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
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                    # only one has to be true to buy
                    else:
                        if first_arg or third_arg:
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                
                    index += 1
            # if the second and third strategies are > 0
            elif first_num == 0 and second_num > 0 and third_num > 0:
                # iterate through entire dataset
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
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
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                    else:
                        if second_arg or third_arg:
                            # get maximum number of shares that can be bought in one step
                            max_shares = int(capital / share_price)
                            # buy max shares
                            capital -= max_shares * share_price
                            shares += max_shares
                        else:
                            # sell all shares
                            gain += shares * share_price
                            shares -= shares
                        # if any shares are left over then sell them all at the final closing price
                        gain += shares * dataset[len(dataset) - 1]
                        shares -= shares
                
                    index += 1
            # if just the first strategy is > 0
            elif first_num > 0 and second_num == 0 and third_num == 0:
                # iterate through entire dataset
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
                    # getting the first strategy
                    if letter_order[0] == "s":
                        first_arg = simple_moving_average(dataset, index, first_num)
                    elif letter_order[0] == "e":
                        first_arg = exponential_moving_average(dataset, index, first_num)
                    else:
                        first_arg = max_rule(dataset, index, first_num)
                    # buy if true
                    if first_arg:
                        # get maximum number of shares that can be bought in one step
                        max_shares = int(capital / share_price)
                        # buy max shares
                        capital -= max_shares * share_price
                        shares += max_shares
                    else:
                        # sell all shares
                        gain += shares * share_price
                        shares -= shares
                    # if any shares are left over then sell them all at the final closing price
                    gain += shares * dataset[len(dataset) - 1]
                    shares -= shares
                
                    index += 1
            # if just the second strategy is > 0
            elif first_num == 0 and second_num > 0 and third_num == 0:
                # iterate through entire dataset
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
                    # getting the second strategy
                    if letter_order[1] == "s":
                        second_arg = simple_moving_average(dataset, index, second_num)
                    elif letter_order[1] == "e":
                        second_arg = exponential_moving_average(dataset, index, second_num)
                    else:
                        second_arg = max_rule(dataset, index, second_num)
                    # buy if true
                    if second_arg:
                        # get maximum number of shares that can be bought in one step
                        max_shares = int(capital / share_price)
                        # buy max shares
                        capital -= max_shares * share_price
                        shares += max_shares
                    else:
                        # sell all shares
                        gain += shares * share_price
                        shares -= shares
                    # if any shares are left over then sell them all at the final closing price
                    gain += shares * dataset[len(dataset) - 1]
                    shares -= shares
                
                    index += 1
            # if just the third strategy is > 0
            elif first_num == 0 and second_num == 0 and third_num > 0:
                # iterate through entire dataset
                while index < len(dataset):
                    # get current share price
                    share_price = dataset[index]
                    
                    # getting the third strategy
                    if letter_order[2] == "s":
                        third_arg = simple_moving_average(dataset, index, third_num)
                    elif letter_order[2] == "e":
                        third_arg = exponential_moving_average(dataset, index, third_num)
                    else:
                        third_arg = max_rule(dataset, index, third_num)
                    # buy if true  
                    if third_arg:
                        # get maximum number of shares that can be bought in one step
                        max_shares = int(capital / share_price)
                        # buy max shares
                        capital -= max_shares * share_price
                        shares += max_shares
                    else:
                        # sell all shares
                        gain += shares * share_price
                        shares -= shares
                    # if any shares are left over then sell them all at the final closing price
                    gain += shares * dataset[len(dataset) - 1]
                    shares -= shares
                
                    index += 1
    
    return gain if gain > 0 else 0 # return the total gain over all datasets

def initialize_population():
    # create starting array
    population = ["s010&e000&m000", "s025&e000&m000", "s000&e010&m000", "s000&e025&m000", 
                  "s000&e000&m010", "s000&e000&m025", "s043&e057&m109", "s083&e100&m036", 
                  "s011|e140|m040", "s052|e130&m024", total_best_individual]
    letters = ["s", "e", "m"]
    operators = ["&", "|"]
    while len(population) < 40:
        # create empty individual
        individual = ""
        individual += letters[random.randint(0,2)]
        for i in range(3):
            individual += str(0)
        individual += operators[random.randint(0,1)]
        individual += letters[random.randint(0,2)]
        for i in range(3):
            individual += str(0)
        individual += operators[random.randint(0,1)]
        individual += letters[random.randint(0,2)]
        for i in range(3):
            individual += str(0)
        # add the individual to the population
        population.append(individual)
    while len(population) < POPULATION_SIZE:
        # create empty individual
        individual = ""
        individual += letters[random.randint(0,2)]
        for i in range(3):
            individual += str(random.randint(0,9))
        individual += operators[random.randint(0,1)]
        individual += letters[random.randint(0,2)]
        for i in range(3):
            individual += str(random.randint(0,9))
        individual += operators[random.randint(0,1)]
        individual += letters[random.randint(0,2)]
        for i in range(3):
            individual += str(random.randint(0,9))
        # add the individual to the population
        population.append(individual)
    return population

def generate_intermediate_population(population):
    fitnesses = [fitness(individual) for individual in population]
    avg = sum(fitnesses) / len(fitnesses)
    n = [(fitness / avg) / 100000 for fitness in fitnesses] if avg != 0 else 0
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
    # choose 25 pairs of parents at random
    for i in range(25):
        parent1, parent2 = random.sample(intermediate_population, 2)
        # 20% chance of copying parents directly
        if random.random() < COPY_RATE:
            child1 = parent1
            child2 = parent2
        else:
            # choose a random crossover point
            crossover_point = random.randint(0, 13)
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
        # 1% chance of mutation
        if random.random() < MUTATION_RATE:
            if gene == "s":
                letters = ["e", "m"]
                mutated_individual += letters[random.randint(0,1)]
            elif gene == "e":
                letters = ["s", "m"]
                mutated_individual += letters[random.randint(0,1)]
            elif gene == "m":
                letters = ["s", "e"]
                mutated_individual += letters[random.randint(0,1)]
            elif gene == "&":
                mutated_individual += "|"
            elif gene == "|":
                mutated_individual += "&"
            elif gene == "0":
                numbers = ["1","2","3","4","5","6","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "1":
                numbers = ["0","2","3","4","5","6","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "2":
                numbers = ["0","1","3","4","5","6","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "3":
                numbers = ["0","1","2","4","5","6","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "4":
                numbers = ["0","1","2","3","5","6","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "5":
                numbers = ["0","1","2","3","4","6","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "6":
                numbers = ["0","1","2","3","4","5","7","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "7":
                numbers = ["0","1","2","3","4","5","6","8","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "8":
                numbers = ["0","1","2","3","4","5","6","7","9"]
                mutated_individual += numbers[random.randint(0,8)]
            elif gene == "9":
                numbers = ["0","1","2","3","4","5","6","7","8"]
                mutated_individual += numbers[random.randint(0,8)]
        else:
            mutated_individual += gene
    return mutated_individual

# function that prints the timer
def print_timer(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        print("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)), end='\r')
        time.sleep(1)

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

# keep track of best individual found over multiple runs
total_best_individual = "s003&e000|s224"
total_best_fitness = fitness(total_best_individual)

# create an event object to signal the thread to stop
stop_event = threading.Event()

# start the timer in a separate thread
start_time = time.time()
timer_thread = threading.Thread(target=print_timer, args=(start_time, stop_event))
timer_thread.start()

# initialize the initial population
population = initialize_population()

# set initial values
best_fitness_value = 0.0
best_individual = None

# run the genetic algorithm
for generation in range(GENERATIONS):
    print(f"Generation: {generation + 1}")
    intermediate_population = generate_intermediate_population(population)
    new_population = recombine(intermediate_population)
    for i in range(len(new_population)):
        new_population[i] = mutate(new_population[i])
    population = new_population
    # update the best individual found so far
    for individual in population:
        ind_fitness = fitness(individual)
        if ind_fitness > best_fitness_value:
            best_fitness_value = ind_fitness
            best_individual = individual

    print(f"Best individual this run: {best_individual}, ${best_fitness_value:.2f}")

    # update best individual over multiple runs
    if best_fitness_value > total_best_fitness:
        total_best_individual = best_individual
        total_best_fitness = best_fitness_value

    print(f"Total best individual: {total_best_individual}, ${total_best_fitness:.2f}")
    print("----------------------------------------------------")

# stop the timer thread when the program ends
stop_event.set()
timer_thread.join()

# print the final timer value
elapsed_time = time.time() - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)
print("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))