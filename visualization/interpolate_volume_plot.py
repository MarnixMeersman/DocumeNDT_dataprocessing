from vedo import Points, show
import numpy as np
from visualization.visualisation_functions import get_line_3d

# prepare added matrices
matrices = []
for i in range(9):
    for j in range(9):
        matrix = get_line_3d(0, 0, 0, 90, (i+1)*10, (j+1)*10, 2)
        matrices.append(matrix)
coords = np.reshape(matrices, (-1, 3))
print(coords)

npts = 500                      # nr. of points where the scalar value is known
# coords = np.random.rand(npts, 3)
# print(coords)# range is [0, 1]
scals = coords[:, 2]             # let the scalar be the z of the point itself

pts = Points(coords)
pts.pointdata["scals"] = scals

# Now interpolate the values at these points to the full Volume
# available interpolation kernels are: shepard, gaussian, voronoi, linear.
vol = pts.tovolume(kernel='shepard', n=4, dims = (90,90,90))

vol.c(["maroon","g","b"])        # set color   transfer function
vol.alpha([0.3, 0.9])            # set opacity transfer function
# vol.alpha([(0.3,0.3), (0.9,0.9)]) # alternative way, by specifying (xscalar, alpha)
vol.alpha_unit(0.9)              # make the whole object less transparent (default is 1)

# replace voxels of specific range with a new value
# vol.threshold(above=0.3, below=0.4, replace=0.9)
# Note that scalar range now has changed (you may want to reapply vol.c().alpha())

# ch = CornerHistogram(vol, pos="bottom-left")

vol.add_scalarbar3d('Velocity', s=[None,1])
vol.scalarbar.rotate_x(90).pos(1.15,1,0.5)

show(pts, vol, __doc__, axes=1, elevation=-90).close()
