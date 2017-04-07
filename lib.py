import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors
import random


class lib(object):

    def __init__(self):
        self.colors = [mcolors.BASE_COLORS]
        for item in mcolors.CSS4_COLORS:
            self.colors.append(item)

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def choose_countries(self, d):
        # This is how to choose countries for the INFANT MORTALITY
        chosen_countries = []
        for country in d:
            chosen_countries.append(country)
        return chosen_countries

    def display(self, c, d):
        for i, country in enumerate(c):
            x = np.array([item[0] for item in d[country]])
            y = np.array([item[1] for item in d[country]])
            try:
                plt.scatter(x, y, color=random.choice(self.colors))
            except Exception as e:
                print e
                break
        plt.show()
