import random
weights = [10, 10, 10, 10, 10, 0, 0, 0, 0, 0]
class Individual:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = self.compute_fitness()

    def compute_fitness(self):
        return sum(gene * weight for gene, weight in zip(self.genes, weights))

    def mate(self, partner):
        child_genes = []
        for g1, g2 in zip(self.genes, partner.genes):
            child_genes.append(g1 if random.random() < 0.5 else g2)

            # Mutation
            if random.random() < 0.01:
                child_genes[-1] = random.randint(min_gene_value, max_gene_value)

        return Individual(child_genes)

def create_population(population_size, gene_count, min_gene_value, max_gene_value):
    return [Individual([random.randint(min_gene_value, max_gene_value) * random.choice([0, 1]) for _ in range(gene_count)]) for _ in range(population_size)]

def select_parents(population, n):
    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[:n]

def create_children(parents, n):
    children = []
    for _ in range(n):
        parent1, parent2 = random.choices(parents, weights=[x.fitness for x in parents], k=2)
        child = parent1.mate(parent2)
        children.append(child)
    return children

def simulate_generations(population_size, gene_count, min_gene_value, max_gene_value, parent_count, generations, print_every):
    population = create_population(population_size, gene_count, min_gene_value, max_gene_value)

    for i in range(generations):
        parents = select_parents(population, parent_count)
        children = create_children(parents, population_size - parent_count)
        population = parents + children
        if i % print_every == 0:
            print("Generation:", i)
            population.sort(key=lambda x: x.fitness, reverse=True)
            for individual in population:
                print("Genes:", individual.genes, "Fitness:", individual.fitness)

    return population

population_size = 50
gene_count = 10
min_gene_value = 1
max_gene_value = 10
parent_count = 25
generations = 100
print_every = 1

final_population = simulate_generations(population_size, gene_count, min_gene_value, max_gene_value, parent_count, generations, print_every)
final_population.sort(key=lambda x: x.fitness, reverse=True)

print("Final generation:")
for individual in final_population:
    print("Genes:", individual.genes, "Fitness:", individual.fitness)
