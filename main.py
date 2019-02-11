import random

DEBUG = False
a, b, c, d = (0, 0, 3, 2)
x1, x2 = (0, 31)
pk, pm = (0.8, 0.2)
population_size = 6

def f(binary):
    x = binary_to_number(binary)
    return a*x**3 + b*x**2 + c*x + d

def create_starting_population(chain_size):
    return [create_one(chain_size) for x in range(population_size)]

def create_one(chain_size):
    return [random.randint(0,1) for x in range(chain_size)]

def evolve_population(population):
    selection = roulette_select(population)
    children = []
    for p in selection:
        if pk > random.random():
            father = selection[random.randint(0,len(selection)-1)]
            mother = selection[random.randint(0,len(selection)-1)]  
            half = len(father)//2
            child = father[:half] + mother[half:] 
            children.append(child)
    selection.extend(children)
    for i in range(len(selection)):
        if pm > random.random():
            selection[i] = mutate(selection[i])
    selection = sorted(selection, key=lambda x: f(x), reverse=True)
    return selection[:len(population)]

def roulette_select(population):
    fs = [f(x) for x in population] 
    total_fs = float(sum(fs))
    rel_fs = [f/total_fs for f in fs]
    probs = [sum(rel_fs[:i+1]) for i in range(len(rel_fs))]
    new_population = []
    for n in range(population_size):
        for (i, individual) in enumerate(population):
            if random.random() <= probs[i]:
                new_population.append(individual)
                break
    return new_population

def mutate(target):
    sequence = target.copy()
    r = random.randint(0,len(sequence)-1)
    if target[r] == 1:
        sequence[r] = 0
    else:
        sequence[r] = 1
    return sequence 

def get_parameteres():
    print("Type a")
    a = float(input())
    print("Type b")
    b = float(input())    
    print("Type c")
    c = float(input())
    print("Type d")
    d = float(input())
    return (a, b, c, d)

def get_probability():
    print("Insert crossover probability, i.e. 0.8")
    pk = float(input())
    print("Insert mutation probability, i.e. 0.2")
    pm = float(input())
    return (pk, pm)

def get_scope():
    print("Type first point of the local scope:")
    x1 = float(input())
    print("Type last point of the local scope")
    x2 = float(input())
    return (x1, x2) if x1 < x2 else (x2, x1)

def get_population_size():
    print("Insert population size")
    return int(input())

def get_chain_size(precision = 6):
    value = (x2 - x1) * 10**precision
    chain_size = 0
    while value >= 2**chain_size:
        chain_size+=1
    return chain_size

def binary_to_number(binary):
    out = 0
    for bit in binary:
        out = (out << 1) | bit
    return x1 + (x2 - x1) * out / (2**len(binary) - 1)


def main():
    global a, b, c, d, x1, x2, pk, pm, population_size

    if not DEBUG:
        a, b, c, d = get_parameteres()
        x1, x2 = get_scope()
        pk, pm = get_probability()
        population_size = get_population_size()

    chain_size = get_chain_size()
    maximum_generations = 1000
    max_attempts = int(0.1 * maximum_generations)
    population = create_starting_population(chain_size)
    counter = 0
    maximum = -float("inf")
    for generation in range(maximum_generations):
        print("Generation {} of {}".format(generation+1,maximum_generations))
        for i in population:        
            print("%s, f(x): %s" % (str(i), f(i)))
        if f(population[0]) > maximum:
            maximum = f(population[0])
            counter = 0
        else:
            counter+=1

        if generation == maximum_generations-1 or counter == max_attempts:
            print("Best: f({}) = {}.".format(binary_to_number(population[0]), f(population[0])))
            break
        else:
            population = evolve_population(population)    

if __name__ == "__main__":
    main()
