import math
import random
from IPython.display import display
import pandas as pd

"""
Defining Constants
"""

x_val = ['1110010000', '0001001101', '1010100001',
         '1001000110', '1100011000', '0011100101']
y_val = ['1100100000', '0011100111', '0111001000',
         '1000010100', '1011100011', '0011111000']
fx = []
Fx = []
population = []

ll = 0
ul = 6
bits = 10

"""
Fitness function: Returns the fitness value.
Optional boolean parameter exist for specifying maximization or minimization problem
"""
def rastrigin_function(x, y, maximisation):
  f_x = pow(x*x+y-11, 2)+pow(x+y*y-7, 2)
  if maximisation:
    F_x = f_x
  else:
    F_x = 1 / (1 + f_x)
  return round(f_x, 5), round(F_x, 5)

"""
Decoding function: Binary decoding of the given chromosomes
"""
def binary_decoding(xb, ll, ul, no_of_bits):
   xd = int(str(xb), 2)
   xi = ll + (ul-ll) * (xd/(pow(2, no_of_bits)-1))
   return round(xi, 5)

def printTable(print_set):
    df = pd.DataFrame(print_set)
    display(df)

"""
Selection function: Selection procedure for the GA
"""
def selection(population, objective, fitness):
    cummulative = []
    random_number = []
    new_population = []

    s = 0
    probability = []
    for i in range(len(fitness)):
        p = fitness[i] / sum(fitness)
        probability.append(p)

    for i in range(len(fitness)):
        s = s + probability[i]
        cummulative.append(s)
    '''for i in range(len(fitness)):
        random_number.append(random())'''
    random_number = ['0.472', '0.108', '0.723', '0.536', '0.931', '0.972']
    s_no_new = []
    for i in range(len(fitness)):
        for j in range(len(fitness)):
            if cummulative[j] > float(random_number[i]):
                new_population.append(population[j])
                s_no_new.append(j+1)
                break
    print_set = {"population": population, "objective": objective, "fitness": fitness, "probability": probability, "cummulative": cummulative, "random_number": random_number,
                 "new_population": new_population, "new_population_sequence_number": s_no_new}
    print("Selection : \n")
    printTable(print_set)
    return print_set


"""
Crossover function: Crossover procedure for the GA
"""
def crossover(chromosome, pc):

    random_number = []
    random_number = ['0.717', '0.363', '0.817']
    '''for i in range(len(chromosome)/2):
    random_number.append(random())'''
    isCrossover = []
    crossoverChromosome = []
    j = 0
    for i in range(0, len(chromosome), 2):
        if float(random_number[j]) < pc:

            chromosome1 = list(chromosome[i][0] + chromosome[i][1])
            chromosome2 = list(chromosome[i+1][0] + chromosome[i+1][1])
            length = len(chromosome1)
            #cross_site = random.randint(0,len(chromosome1)-1)
            cross_site = 9
            isCrossover.append("Yes")
            for i in range(cross_site, length):
                chromosome1[i], chromosome2[i] = chromosome2[i], chromosome1[i]
            chromosome1 = "".join(chromosome1)
            chromosome2 = "".join(chromosome2)
            crossoverChromosome.append((chromosome1[:10], chromosome1[10:]))
            crossoverChromosome.append((chromosome2[:10], chromosome2[10:]))

        else:
            isCrossover.append("No")
        j = j + 1
    print("\nCrossover :\n")
    print(crossoverChromosome)
    return crossoverChromosome


"""
Mutation function: Mutation procedure for the GA
"""
def mutation(chromosome, pm):

    random_number = []
    random_number = ['0.189', '0.607', '0.192', '0.386', '0.001', '0.413']
    '''for i in range(len(chromosome)/2):
    random_number.append(random())'''

    isMutation = []
    mutatedChromosome = []
    for i in range(0, len(chromosome)):
        if float(random_number[i]) < pm:
            isMutation.append(True)
            mutated_Chromosome = chromosome[i][0] + chromosome[i][1]
            #randomNumber = random.randint(0,len(mutated_Chromosome)-1)

            randomNumber = 10

            if mutated_Chromosome[randomNumber] == "0":
                mutated_Chromosome = list(mutated_Chromosome)
                mutated_Chromosome[randomNumber] = '1'
            else:
                mutated_Chromosome = list(mutated_Chromosome)
                mutated_Chromosome[randomNumber] = '0'

            mutated_Chromosome = "".join(mutated_Chromosome)
            mutatedChromosome.append(
                (mutated_Chromosome[:10], mutated_Chromosome[10:]))
        else:
           isMutation.append(False)
           mutatedChromosome.append(("null", "null"))
           #mutatedChromosome = chromosome
    print_set = {"Population": chromosome,
                 "Is-Mutation": isMutation, "OffSpring": mutatedChromosome}
    print("\nMutation :\n")
    printTable(print_set)
    return print_set


"""
General Genetic Algorithm

S1.[Start] Generate random population of n chromosomes
S2.[Fitness] Evaluate the fitness F(x) of each chromosome x in the population
S3.[New Population] Create a new population by repeating the following
steps until the new population is complete
    a. [Selection] Select 2 parent chromosomes according to fitness (the
    better fitness, the bigger chance to be selected)
    b. [Cross-over] With a cross-over probability (Pc ) cross-over the parents to
    form new children
    c. [Mutation] With a mutation probability (Pm) mutate new offspring at a
    locus
    d. [Accept] Place new offspring(s) in population
S4. [Replace] Use generated population for a further run
S5. [Test] If the end condition is satisfied, stop and return the best solution in
run.
S6. [Loop] Go to S2.

"""
def gentic_algorithm(population, fx, Fx):
    for i in range(0, 6):
        new_population = []
        selection_output = selection(population, fx, Fx)
        crossover_output = crossover(selection_output["new_population"], 0.8)
        mutation_output = mutation(selection_output["new_population"], 0.05)

        for chromosome in selection_output['new_population']:
            x = binary_decoding(chromosome[0], ll, ul, bits)
            y = binary_decoding(chromosome[1], ll, ul, bits)
            new_population.append((chromosome, rastrigin_function(x, y, False)[1]))
        for chromosome in crossover_output:
            x = binary_decoding(chromosome[0], ll, ul, bits)
            y = binary_decoding(chromosome[1], ll, ul, bits)
            new_population.append((chromosome, rastrigin_function(x, y, False)[1]))
        for chromosome in mutation_output['OffSpring']:
            if chromosome[0] != 'null' and chromosome[1] != 'null':
                x = binary_decoding(chromosome[0], ll, ul, bits)
                y = binary_decoding(chromosome[1], ll, ul, bits)
                new_population.append(
                    (chromosome, rastrigin_function(x, y, False)[1]))

        new_population = list(sorted(new_population, key=lambda item: item[1], reverse=True))[:6]
        try:
            population = [chromosomes[0] for chromosomes in new_population]
            print("New Population: \n", population)
            fx = [], Fx = []
            for i in range(len(population)):
                x = binary_decoding(population[i][0], ll, ul, bits)
                y = binary_decoding(population[i][1], ll, ul, bits)
                ox, Ox = rastrigin_function(x, y, False)
                population.append((x_val[i], y_val[i]))
                fx.append(ox)
                Fx.append(Ox)
        except:
            print("Unable to fetch top 6! Finalizing with the existing population")
            exit()

if __name__ == '__main__':
    for i in range(len(x_val)):
        x = binary_decoding(x_val[i], ll, ul, bits)
        y = binary_decoding(y_val[i], ll, ul, bits)
        ox, Ox = rastrigin_function(x, y, False)
        population.append((x_val[i], y_val[i]))
        fx.append(ox)
        Fx.append(Ox)
    gentic_algorithm(population, fx, Fx)
