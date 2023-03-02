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


def simple_moving_average(data, window_size, actual_price):
    # Calculates the simple moving average of the data using the specified window size
    if len(data) < window_size:
        return False # sell

    sma = []
    for i in range(window_size, len(data)+1):
        window = data[i-window_size:i]
        sma.append(sum(window) / window_size)
    
    sma_average = sum(sma) / len(sma)
    return actual_price > sma_average
    

def exponential_moving_average(data, alpha, window_size):
    # Calculates the exponential moving average of the data using the specified alpha value
    ema = [data[0]]
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1 - alpha) * ema[-1])
    
    if len(data) < window_size:
        return False
    
    for i in range(window_size, len(data)):
        if data[i] > ema[i-window_size]:
            return True
    
    return False

def max_rule(data, n):
    if len(data) < n:
        return False
    
    max_price = max(data[:n])
    return data[-1] > max_price


def fitness(genotype):
    
    letter_order = []
    operators = [genotype[4], genotype[9]]

    alpha = 0
    i = 0
    s_num = 0
    e_num = 0
    m_num = 0
    for gene in genotype:
        if gene == "s":
            num = genotype[i + 1] + genotype[i + 2] + genotype[i + 3]
            s_num = int(num)
            if s_num > 0:
                letter_order.append("s")        
        elif gene == "e":
            num = genotype[i + 1] + genotype[i + 2] + genotype[i + 3]
            e_num = int(num)
            if e_num > 0:
                alpha = 2 / e_num + 1
                letter_order.append("e")
        elif gene == "m":
            num = genotype[i + 1] + genotype[i + 2] + genotype[i + 3]
            m_num = int(num)
            if m_num > 0:
                letter_order.append("m")
        i += 1

    print(letter_order)
    print(operators)

    capital = 20000
    gain = 0
    for dataset in datasets:
        if capital != 20000:
            diff = 20000 - capital
            gain -= diff
            capital = 20000
        if s_num > 0:
            sma = simple_moving_average(dataset, s_num, s_num)
            print("Simple moving average     : " + str(sma))
        if e_num > 0:
            ema = exponential_moving_average(dataset, alpha, int(e_num))
            print("Exponential moving average: " + str(ema))
        if m_num > 0:
            max = max_rule(dataset, m_num)
            print("Max rule                  : " + str(max))

        first = False
        second = False
        if letter_order[0] == "s":
            if letter_order[1] == "e":
                if operators[0] == "&":
                    first = sma and ema
                else:
                    first = sma or ema
                second = max
            else:
                if operators[0] == "&":
                    first = sma and max
                else:
                    first = sma or max
                second = ema
        elif letter_order[0] == "e":
            if letter_order[1] == "s":
                if operators[0] == "&":
                    first = sma and ema
                else:
                    first = sma or ema
                second = max
            else:
                if operators[0] == "&":
                    first = ema and max
                else:
                    first = ema or max
                second = sma
        else:
            if letter_order[1] == "e":
                if operators[0] == "&":
                    first = max and ema
                else:
                    first = max or ema
                second = sma
            else:
                if operators[0] == "&":
                    first = max and ema
                else:
                    first = max or ema
                second = sma

        if operators[1] == "&":
            if first and second:
                print("Buy")
            else:
                print("Sell")
        else:
            if first or second:
                print("Buy")
            else:
                print("Sell")

        print("---------------------------------")

# function to recombine the intermediate population
def recombine(intermediate_population):
    new_population = []
    # choose 50 pairs of parents at random
    for i in range(50):
        parent1, parent2 = random.sample(intermediate_population, 2)
        # 20% chance of copying parents directly
        if random.random() < COPY_RATE:
            child1 = parent1
            child2 = parent2
        else:
            # choose a random crossover point
            crossover_point = random.randint(1, len(genotype) - 1)
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

dir = "Datasets/historical-stock-prices/"
data_strings = [dir+"AAPL-1.txt",dir+"AAPL-2.txt",dir+"AAPL-3.txt",dir+"AAPL-4.txt",dir+"AAPL-5.txt",dir+"DDS-1.txt",dir+"DDS-2.txt",dir+"DDS-3.txt",dir+"DDS-4.txt",dir+"DDS-5.txt",dir+"F-1.txt",dir+"F-2.txt",dir+"F-3.txt",dir+"F-4.txt",dir+"F-5.txt",dir+"GE-1.txt",dir+"GE-2.txt",dir+"GE-3.txt",dir+"GE-4.txt",dir+"GE-5.txt",dir+"RTX-1.txt",dir+"RTX-2.txt",dir+"RTX-3.txt",dir+"RTX-4.txt",dir+"RTX-5.txt"]
datasets = []
for d in data_strings:
    datasets.append(read_file(d))

genotype = "s050&e030&m010"

start_time = time.time()

fitness(genotype)

end_time = time.time()
time_elapsed = end_time - start_time
print("\nTime elapsed: {:.1f} seconds".format(time_elapsed))
