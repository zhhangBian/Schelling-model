import matplotlib.pyplot as plt
import random
import copy

import numpy as np
from matplotlib.colors import ListedColormap


class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold):
        self.width = width
        self.height = height

        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold

        self.house_board = {(i, j): 0 for i in range(self.height) for j in range(self.width)}

        house_position_list = [(i, j) for i in range(self.height) for j in range(self.width)]
        random.shuffle(house_position_list)
        empty_house_num = int(self.empty_ratio * (self.height * self.width))
        self.empty_house_position_list = house_position_list[:empty_house_num]
        self.not_empty_house_list = house_position_list[empty_house_num:]

        for pos in self.not_empty_house_list:
            self.house_board[pos] = (pos[0] + pos[1]) % 2 + 1

    def is_unsatisfied(self, pos):
        race = self.house_board[pos]
        pos_x = pos[0]
        pos_y = pos[1]
        count_similar = 0
        count_different = 0

        step = [-1, 0, 1]
        for dx in step:
            for dy in step:
                if dx == 0 and dy == 0:
                    continue
                x = pos_x + dx
                y = pos_y + dy
                if (0 <= x < self.width and 0 <= y < self.height and
                        (x, y) not in self.empty_house_position_list):
                    if self.house_board[(x, y)] == race:
                        count_similar += 1
                    else:
                        count_different += 1

        if count_similar == 0 and count_different == 0:
            return False
        else:
            return float(count_similar) / (count_similar + count_different) < self.similarity_threshold

    def simulate(self, num):
        for i in range(num):
            old_house_board = copy.deepcopy(self.house_board)
            old_not_empty_house_list = copy.deepcopy(self.not_empty_house_list)

            for pos in old_not_empty_house_list:
                if self.is_unsatisfied(pos):
                    race = old_house_board[pos]
                    empty_pos = random.choice(self.empty_house_position_list)
                    self.house_board[empty_pos] = race
                    self.house_board[pos] = 0

                    self.empty_house_position_list.remove(empty_pos)
                    self.not_empty_house_list.append(empty_pos)
                    self.not_empty_house_list.remove(pos)
                    self.empty_house_position_list.append(pos)

    def plot(self, title):
        colors = {0: 'white', 1: 'red', 2: 'blue'}

        grid = np.zeros((self.height, self.width), dtype=int)

        for pos, race in self.house_board.items():
            grid[pos[0], pos[1]] = race

        plt.figure(figsize=(8, 8))
        plt.title(title)
        plt.xticks([])
        plt.yticks([])

        plt.imshow(grid, cmap=ListedColormap(list(colors.values())))
        plt.savefig(title)
        plt.close()

    def calculate_similarity(self):
        similarity = []
        for pos in self.not_empty_house_list:
            count_similar = 0
            count_different = 0
            race = self.house_board[pos]
            pos_x = pos[0]
            pos_y = pos[1]

            step = [-1, 0, 1]
            for dx in step:
                for dy in step:
                    if dx == 0 and dy == 0:
                        continue

                    x = pos_x + dx
                    y = pos_y + dy

                    if ((0 <= x < self.width) and (0 <= y < self.height) and
                            ((x, y) not in self.empty_house_position_list)):
                        if self.house_board[(x, y)] == race:
                            count_similar += 1
                        else:
                            count_different += 1

            try:
                similarity.append(float(count_similar) / (count_similar + count_different))
            except ZeroDivisionError:
                similarity.append(1)

        return sum(similarity) / len(similarity)


def main():
    schelling = Schelling(50, 50, 0.1, 0.7)
    schelling.plot('initial')
    print("finish init")

    for i in range(20):
        schelling.simulate(1)
        schelling.plot("simulate " + str(i))
        print("finish "+str(i))


if __name__ == "__main__":
    main()
