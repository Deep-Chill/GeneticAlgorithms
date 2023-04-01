import random, time

import numpy as np

# np.random.seed(5)
# genetic_code = np.random.randint(0, 5, 6)

# 1 = Energy Capacity
# 2 = Speed
# 3 = Reproduction Rate
# 4 = Resource Efficiency
# 5 = Size
# 6 = Lifespan
descriptions = {1: 'Energy capacity', 2: 'Speed', 3: 'Reproduction Rate', 4: 'Resource Efficiency', 5: 'Size',
                6: 'Lifespan'}
weights = {1: 10, 2: 10, 3: 0, 4: 10, 5: 10, 6: 0}


def create_parents(size, parents_needed):
    list_of_genetic_codes = []
    list_of_genetic_codes_scores = []

    for i in range(size):
        genetic_code = np.random.randint(0, 5, 6)
        score = sum([j * weights[i + 1] for i, j in enumerate(genetic_code)])
        list_of_genetic_codes.append(list(genetic_code))
        list_of_genetic_codes_scores.append(score)

    probability_max = sum(list_of_genetic_codes_scores)
    probabilities = [i / probability_max for i in list_of_genetic_codes_scores]
    parents = np.random.choice(len(list_of_genetic_codes_scores), p=probabilities, replace=True, size=parents_needed)
    parents = [list_of_genetic_codes[i] for i in parents]
    return parents


def create_parents_from_preset_generation(generation, parents_needed):
    list_of_genetic_codes_scores = []
    for k in range(len(generation)):
        score = sum([i * weights[j + 1] for i, j in enumerate(generation[k])])
        list_of_genetic_codes_scores.append(score)
    probability_max = sum(list_of_genetic_codes_scores)
    probabilities = [i / probability_max for i in list_of_genetic_codes_scores]
    parents = np.random.choice(len(list_of_genetic_codes_scores), p=probabilities, replace=True, size=parents_needed)
    parents = [generation[i] for i in parents]
    print(parents)
    return parents


# Get 2 parents each reproductive cycle, randomly, get their children
def reproduce(parent_1_genetic_code, parent_2_genetic_code):
    child_1 = []
    child_2 = []
    for i, j in zip(parent_1_genetic_code, parent_2_genetic_code):
        gene_selection = [i, j]
        child_1_selected_gene = np.random.choice(gene_selection, size=1)
        child_2_selected_gene = np.random.choice(gene_selection, size=1)
        child_1.append(int(child_1_selected_gene))
        child_2.append(int(child_2_selected_gene))

    return child_1, child_2


random.seed(time.time())


def reproduce_2_childs_with_mutation(parent_1_genetic_code, parent_2_genetic_code):
    mutation_rate_list = [50, 1]
    child_1 = []
    child_2 = []
    a = [i for i in parent_1_genetic_code]
    b = [i for i in parent_2_genetic_code]
    for i, j in zip(parent_1_genetic_code, parent_2_genetic_code):
        gene_selection = [i, j]
        child_1_selected_gene = random.choices(gene_selection, k=1)[0]
        child_1_selection = [child_1_selected_gene, random.randint(0, 5)]
        child_1_selected_gene = random.choices(child_1_selection, weights=mutation_rate_list, k=1)[0]
        child_1.append(int(child_1_selected_gene))
        child_2_selected_gene = np.random.choice(gene_selection, size=1)[0]
        child_2_selection = [child_2_selected_gene, random.randint(0, 5)]
        child_2_selected_gene = random.choices(child_2_selection, weights=mutation_rate_list, k=1)[0]
        child_2.append(int(child_2_selected_gene))
    return child_1, child_2


# print(reproduce_2_childs_with_mutation([1, 2, 4, 3, 2], [4, 3, 4, 2, 1]))


def return_average_score_of_n_populations(generations, size_of_generation):
    children = []
    sum_children = 0
    # Why is the number of generations affecting the size of the children?
    for generation in range(generations):
        current_generation = []
        if generation == 0:
            for n in range(size_of_generation // 2):
                list_of_parents = create_parents(size_of_generation, 2)
                two_children = reproduce_2_childs_with_mutation(list_of_parents[0], list_of_parents[1])
                current_generation.append(two_children[0])
                current_generation.append(two_children[1])
            children = current_generation
        else:
            for reproduction in range(size_of_generation // 2):
                list_of_parents = create_parents_from_preset_generation(children, 2)
                # print("list_of_p:", list_of_parents)
                two_children = reproduce_2_childs_with_mutation(list_of_parents[0], list_of_parents[1])
                current_generation.append(two_children[0])
                current_generation.append(two_children[1])
            children = current_generation
            print(sum_children)
            for i in current_generation:
                sum_children += sum(i)

    return children


print(return_average_score_of_n_populations(10000, 6))


# print(create_parents(50, 2))


# print(reproduce_1_child_with_mutation('069997', '235994', mutation_rate=[10, 2]))


class Environment:
    def __init__(self, width, height, num_resources):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=np.object_)
        self.resources = np.random.randint(0, num_resources + 1, size=(width, height))
        self.creatures = np.random.randint(0, 2, size=(width, height))
        # Want to show which creatures have access to a resource
        self.lived = np.array(self.resources == self.creatures)
        self.lived_filtered = np.where(self.lived == True, 1, 0)

    def add_creature(self, creature, x, y):
        if self.grid[x, y] is None:
            self.grid[x, y] = creature
            return True
        return False

    def move_creature(self, x, y, new_x, new_y):
        if self.grid[new_x, new_y] is None:
            self.grid[new_x, new_y] = self.grid[x, y]
            self.grid[x, y] = None
            return True
        return False

    def remove_creature(self, x, y):
        self.grid[x, y] = None

    def get_resource(self, x, y):
        return self.resources[x, y]

    def consume_resource(self, x, y):
        resource = self.resources[x, y]
        self.resources[x, y] = 0
        return resource

    def get_creature(self, x, y):
        return self.creatures[x, y]


# Example usage
width, height = 10, 10
num_resources = 1

# env = Environment(width, height, num_resources)
# print("Resource grid:")
# print(env.resources)
# print("Organisms: ")
# print(env.creatures)
# print("Organisms that survived: ")
# print(env.lived_filtered)
# unique, counts = np.unique(env.lived_filtered, return_counts=True)
# print("Survived/Died, Amount ")
# print([i for i in zip(unique, counts)])
