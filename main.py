import random

import numpy as np

np.random.seed(4)
genetic_code = np.random.randint(0, 5, 6)

# 1 = Energy Capacity
# 2 = Speed
# 3 = Reproduction Rate
# 4 = Resource Efficiency
# 5 = Size
# 6 = Lifespan

weights = {1: 2, 2: 1.5, 3: 0, 4: 2, 5: 2, 6: 0}


def create_population(size):
    list_of_genetic_codes = []
    list_of_genetic_codes_scores = []

    for i in range(size):
        genetic_code = np.random.randint(0, 5, 6)
        score = sum([j * weights[i + 1] for i, j in enumerate(genetic_code)])
        list_of_genetic_codes.append(list(genetic_code))
        list_of_genetic_codes_scores.append(score)
    print(list_of_genetic_codes)
    print(list_of_genetic_codes_scores)
    children = random.choices(list_of_genetic_codes, weights=list_of_genetic_codes_scores, k=3)
    print(children)


create_population(5)


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
