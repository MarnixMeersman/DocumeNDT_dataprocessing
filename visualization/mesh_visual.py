from vedo import Mesh, dataurl, Plotter, Points, show, Text2D
from visualization.visualisation_functions import *
from vedo.applications import Slicer3DPlotter
import matplotlib.cm as cm
def main():
    surf = Mesh("./wall2_coord_more_downsampled.obj").normalize().wireframe()


    coords = get_3d_lines(get_coords()[0], get_coords()[1], 2000, get_vel_as_arr())
    scals = coords[:, 3]             # set equl to 3 to present v with color
    pts = Points(coords[:, 0:3])
    pts.pointdata["scals"] = scals
    vol = pts.tovolume(kernel='gaussian', n=3).smooth_gaussian(sigma=(0.25, 0.25, 0.25))
    vol_surf = surf.binarize(spacing=(0.02,0.02,0.02))
    surf.backcolor("white")
    # surf.alpha(0.95)
    pts.c('red')
    # pts.pointdata.alpha([0.4, 0.6])

    vol_surf.c('blue')
    vol_surf.alpha(0.5)            # set opacity transfer function
    # # vol.alpha([(0.3,0.3), (0.9,0.9)]) # alternative way, by specifying (xscalar, alpha)
    vol_surf.alpha_unit(0.7)              # make the whole object less transparent (default is 1)
    vol.c(["r","g","b"])        # set color   transfer function
    vol.alpha([0, 1])            # set opacity transfer function
    # vol.alpha([(0.3,0.3), (0.9,0.9)]) # alternative way, by specifying (xscalar, alpha)
    vol.alpha_unit(0.1)

    vol.add_scalarbar3d('Velocity')
    vol.scalarbar.rotate_x(90).pos(0,0,1)


    # vol = surf.binarize(spacing=(0.02,0.02,0.02))
    # vol.alpha([0,0.6]).c('blue')
    #
    # iso = vol.isosurface().color("blue5")

    plt = Plotter(N=2, axes=9)
    plt.at(0).show(pts, surf, vol_surf)
    plt.at(1).show(vol, __doc__)
    plt.interactive().close()

if __name__=="__main__":
    main()