"""

"""

__author__ = "Nivardo Albuquerque"
__version__ = "1.0.0"
__maintainer__ = "Nivardo Albuquerque"
__email__ = "nivardo00@gmail.com"

import math
from dataclasses import dataclass
import matplotlib.pyplot as plt

import numpy as np

# Uncomment this if the output is too big to be shown
# np.set_printoptions(threshold=np.inf)


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Grid:

    def __init__(self, starting_point, ending_point):
        self.starting_point: Point = starting_point
        self.ending_point: Point = ending_point

        len_x = max((starting_point.x, ending_point.x))
        len_y = max((starting_point.y, ending_point.y))

        n = max((len_x, len_y))

        self.matrix = np.zeros((len_x + 1, len_y + 1))

    @property
    def dx(self) -> float:
        return self.ending_point.x - self.starting_point.x

    @property
    def dy(self) -> float:
        return self.ending_point.y - self.starting_point.y

    @property
    def m(self) -> float:
        return self.dy / self.dx

    @property
    def b(self) -> float:
        return self.ending_point.y - (self.m * self.ending_point.x)

    def calculate_x(self, y):
        return (y - self.b) / self.m

    def calculate_y(self, x):
        return self.m * x + self.b

    def trace_line(self):
        inverse = self.dx > self.dy

        virtual_grid = self.__trace_line(self.matrix, inverse)

        self.matrix = virtual_grid

    def __trace_line(self, matrix, inverse: bool):
        x_lim, y_lim = matrix.shape
        if inverse:
            for x in range(x_lim):
                y = self.calculate_y(x)
                x, y = create_fragment(x, y)
                matrix[x][y] = 1
        else:
            for y in range(y_lim):
                x = self.calculate_x(y)
                x, y = create_fragment(x, y)
                matrix[x][y] = 1

        return matrix

    def plot_grid(self):
        self.trace_line()
        print(self)
        print(self.matrix)
        self.__matplot_grid()

    def __matplot_grid(self):
        fig, ax = plt.subplots()
        grid_matrix = self.matrix.T
        size_x, size_y = grid_matrix.shape

        matrix_resolution = max((size_x, size_y))

        ax.imshow(grid_matrix, aspect='equal', origin='lower', cmap='gray_r')
        major_ticks = np.arange(0, matrix_resolution, 1)

        minor_ticks = np.arange(.5, matrix_resolution, 1)

        ax.set_xticks(major_ticks)
        ax.set_yticks(major_ticks)

        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(minor_ticks, minor=True)

        ax.grid(color='black', linestyle='-', linewidth=.1, which='minor')
        plt.show()

    def __str__(self):
        return """{}
    Starting point = {}
    Ending point = {}
    
    dx = {}
    dy = {}
    
    m = {}
    b = {}           
{}
        """.format(
            'Line info'.center(20,'='),
            self.starting_point,
            self.ending_point,
            self.dx,
            self.dy,
            self.m,
            self.b,
            '='*20
        )


def create_fragment(x, y):
    x_m = math.floor(x)
    y_m = math.floor(y)

    # We won't use the center of the interval to represent the pixel to
    # to make things easier on the representative matrix.

    # x_p = x_m + 0.5
    # y_p = y_m + 0.5

    return x_m, y_m


if __name__ == '__main__':
    p0 = Point(x=0, y=0)
    p1 = Point(x=100, y=100)

    grid = Grid(p0, p1)
    grid.plot_grid()
