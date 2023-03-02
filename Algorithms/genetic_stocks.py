import random
import time

start_time = time.time()

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

def simple_moving_average(data, genotype):
    window_size = 0
    i = 0
    for gene in genotype:
        if gene == 's':
            num = genotype[i + 1] + genotype[i + 2] + genotype[i + 3]
            window_size = int(num)
        i += 1

    # Calculates the simple moving average of the data using the specified window size
    if len(data) < window_size:
        raise ValueError("Window size cannot be larger than data size")
    
    sma = 0
    for i in range(window_size, len(data)+1):
        window = data[i-window_size:i]
        sma += (sum(window) / window_size)
    
    return sma

def exponential_moving_average(data, genotype):
    alpha = 0
    i = 0
    for gene in genotype:
        if gene == 'e':
            num = genotype[i + 1] + genotype[i + 2] + genotype[i + 3]
            alpha = 2 / int(num) + 1
        i += 1

    # Calculates the exponential moving average of the data using the specified alpha value
    ema = 0
    for i in range(1, len(data)):
        ema += ()
    
    return ema

dir = "Datasets/historical-stock-prices/"
data_strings = [dir+"AAPL-1.txt",dir+"AAPL-2.txt",dir+"AAPL-3.txt",dir+"AAPL-4.txt",dir+"AAPL-5.txt",dir+"DDS-1.txt",dir+"DDS-2.txt",dir+"DDS-3.txt",dir+"DDS-4.txt",dir+"DDS-5.txt",dir+"F-1.txt",dir+"F-2.txt",dir+"F-3.txt",dir+"F-4.txt",dir+"F-5.txt",dir+"GE-1.txt",dir+"GE-2.txt",dir+"GE-3.txt",dir+"GE-4.txt",dir+"GE-5.txt",dir+"RTX-1.txt",dir+"RTX-2.txt",dir+"RTX-3.txt",dir+"RTX-4.txt",dir+"RTX-5.txt"]
datasets = []
for d in data_strings:
    datasets.append(read_file(d))

genotype = "s050&e030&m010"

print("Simple moving average     : " + str(simple_moving_average(datasets[0], genotype)))
print("Exponential moving average: " + str(exponential_moving_average(datasets[0], genotype)))

end_time = time.time()
time_elapsed = end_time - start_time
print("\nTime elapsed: {:.1f} seconds".format(time_elapsed))