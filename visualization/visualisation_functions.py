import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import array

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def get_coords():
    print("\n *** MAKE SURE ALL FILES IN ./visualization/emission_reception_velocities ARE UPDATED *** ")
    print(" ***                             ESPECIALLY ./velocities.csv                          ***")
    e = pd.read_csv('./emission_reception_velocities/emission.csv', header=None, delimiter=",").to_numpy()
    r = pd.read_csv('./emission_reception_velocities/reception.csv', header=None, delimiter=",").to_numpy()
    return e, r

def get_vel_as_arr():
    v = pd.read_csv('./emission_reception_velocities/velocities.csv', header=None, delimiter=",").to_numpy()
    return v.flatten()

def quick_plot_coords(e_matrix, r_matrix):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(e_matrix[:,0], e_matrix[:,1], e_matrix[:,2], c = 'green')
    ax.scatter(r_matrix[:,0], r_matrix[:,1], r_matrix[:,2], c = 'red')
    for e_row in e_matrix:
        for r_row in r_matrix:
            x, y, z = [
                [e_row[0], r_row[0]],
                [e_row[1], r_row[1]],
                [e_row[2], r_row[2]]
            ]


            ax.plot(x, y, z, c= 'blue', linewidth=0.25)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
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

def get_3d_lines(e_matrix, r_matrix, npoints, v_1D_arr):
    v_1D_arr = NormalizeData(v_1D_arr)
    coords = np.array([])
    i = 0
    for e_row in e_matrix:
        for r_row in r_matrix:
            d = np.sqrt((e_row[0]-r_row[0])**2 + (e_row[1]-r_row[1])**2 + (e_row[2]-r_row[2])**2)
            xs = np.linspace(e_row[0], r_row[0], int(npoints/d)).ravel()*2.5
            ys = np.linspace(e_row[1], r_row[1], int(npoints/d)).ravel()*2.4
            zs = np.linspace(e_row[2], r_row[2], int(npoints/d)).ravel()*4 - 0.75
            vs = np.ones(int(npoints/d)) * v_1D_arr[i]
            minimatrix = np.array([
                xs, ys, zs, vs
            ]).T
            coords = np.append(coords, minimatrix)
            i += 1
    # coords = coords.ravel().ravel()
    coords = np.reshape(coords, (-1, 4))
    print("Data Size: ", np.shape(coords))
    return coords

# quick_plot_coords(get_coords()[0], get_coords()[1])
# get_3d_lines(get_coords()[0], get_coords()[1], 8000, get_vel_as_arr())
