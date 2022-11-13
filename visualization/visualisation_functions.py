import numpy as np
import matplotlib.pyplot as plt

# get a user defined dense array of points between two points in 3D space, n = density
def get_line_3d(x0, y0, z0, x1, y1, z1, n):
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    zs = np.linspace(z0, z1, n)

    list = []
    list.append(xs)
    list.append(ys)
    list.append(zs)

    matrix = np.array(list).T

    return matrix

# line = get_line_3d(0, 0, 0, 1, 1, 1, 100)
# print(line)
#
#
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(line[0], line[1], line[2])
# plt.show()