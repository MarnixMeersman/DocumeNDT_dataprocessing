from vedo import Points, show, Mesh
import numpy as np
from visualization.visualisation_functions import *



npts = 5000                  # nr. of points where the scalar value is known
coords = np.random.rand(npts, 3)
coords = get_3d_lines(get_coords()[0], get_coords()[1], 20, get_vel_as_arr())

scals = coords[:, 3]             # set equl to 3 to present v with color

pts = Points(coords[:, 0:3])
pts.pointdata["scals"] = scals

# Now interpolate the values at these points to the full Volume
# available interpolation kernels are: shepard, gaussian, voronoi, linear.
vol = pts.tovolume(kernel='voronoi', n=4)
##
surf = Mesh("./wall2_coord.obj").normalize().wireframe()
vol_surf = surf.binarize()

vol.c(["maroon","g","b"])        # set color   transfer function
vol.alpha([0.4, 0.6])            # set opacity transfer function
vol.alpha([(0.3,0.3), (0.9,0.9)]) # alternative way, by specifying (xscalar, alpha)
vol.alpha_unit(0.25)              # make the whole object less transparent (default is 1)

# replace voxels of specific range with a new value
# vol.threshold(above=0.3, below=0.4, replace=0.9)
# Note that scalar range now has changed (you may want to reapply vol.c().alpha())

# ch = CornerHistogram(vol, pos="bottom-left")

vol.add_scalarbar3d('Velocity', s=[None,1])
vol.scalarbar.rotate_x(90).pos(1.15,1,0.5)

show(vol, __doc__, axes=1, elevation=-90).close()
