__author__ = "Nivardo Albuquerque"
__version__ = "1.0.0"
__maintainer__ = "Nivardo Albuquerque"
__email__ = "nivardo00@gmail.com"

import numpy as np
import math
import matplotlib.pyplot as plt

plt.tight_layout()

from dataclasses import dataclass


# Uncomment this if the output is too big to be shown
# np.set_printoptions(threshold=np.inf)


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(int(self.x / other), int(self.y / other))


class Line:

    def __init__(self, starting_point, ending_point, resolution_mutiplier=1):
        self.resolution_mutiplier = resolution_mutiplier
        self.starting_point: Point = starting_point * resolution_mutiplier
        self.ending_point: Point = ending_point * resolution_mutiplier

        xs = [self.starting_point.x, self.ending_point.x]
        ys = [self.starting_point.y, self.ending_point.y]

        xs.sort()
        ys.sort()

        # Ordered limits of the line
        self._min_x, self._max_x = xs
        self._min_y, self._max_y = ys

        self._len_y = max((self.starting_point.y, self.ending_point.y))
        n = max((self._max_y, self._max_x))
        self.matrix = np.zeros((n + 1, n + 1))

    @property
    def dx(self) -> float:
        return self.ending_point.x - self.starting_point.x

    @property
    def dy(self) -> float:
        return self.ending_point.y - self.starting_point.y

    @property
    def m(self) -> float:
        return (self.dy / self.dx) if (self.dx != 0 and self.dy != 0) else np.inf

    @property
    def b(self) -> float:
        return self.ending_point.y - (self.m * self.ending_point.x)

    def calculate_x(self, y):
        # Handles horizontal lines
        if self.m == np.inf:
            return self.starting_point.x

        return (y - self.b) / self.m

    def calculate_y(self, x):
        # Handles vertical lines
        if self.m == np.inf:
            return self.starting_point.y
        return self.m * x + self.b

    def trace_line(self):
        inverse = abs(self.dx) > abs(self.dy)
        virtual_line = self.__trace_line(self.matrix, inverse)

        self.matrix = virtual_line

    def __trace_line(self, matrix, inverse: bool):
        if inverse:
            for x in range(self._min_x, self._max_x + 1):
                y = self.calculate_y(x)
                x, y = create_fragment(x, y)
                matrix[x][y] = 1
        else:
            for y in range(self._min_y, self._max_y + 1):
                x = self.calculate_x(y)
                x, y = create_fragment(x, y)
                matrix[x][y] = 1

        return matrix

    def plot(self):

        self.trace_line()
        print(self)
        print(self.matrix)
        self.__matplot_line()

    def __matplot_line(self):
        fig, ax = plt.subplots(dpi=80 * math.sqrt(self.resolution_mutiplier))
        line_matrix = self.matrix.T
        size_x, size_y = line_matrix.shape

        matrix_resolution = max((size_x, size_y))

        ax.imshow(line_matrix, aspect='equal', origin='lower', cmap='gray_r')
        major_ticks = np.arange(0, matrix_resolution, 1)

        minor_ticks = np.arange(.5, matrix_resolution, 1)

        ax.set_xticks(major_ticks)
        ax.set_yticks(major_ticks)

        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(minor_ticks, minor=True)
        ax.set_title("{} to {} - resolution {}".format(
            self.starting_point/self.resolution_mutiplier,
            self.ending_point/self.resolution_mutiplier,
            self.resolution_mutiplier
        ))
        ax.tick_params(axis='both', which='major', labelsize=int(10 / math.sqrt(self.resolution_mutiplier)))
        plt.xticks(rotation=-90)

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
            'Line info'.center(20, '='),
            self.starting_point,
            self.ending_point,
            self.dx,
            self.dy,
            self.m,
            self.b,
            '=' * 20
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
    # Increases the size of the matrix by resolution_multiplier^2
    resolution_mutiplier = 3

    p0 = Point(x=0, y=0)
    p1 = Point(x=9, y=3)

    line = Line(p0, p1, resolution_mutiplier=resolution_mutiplier)
    line.plot()

