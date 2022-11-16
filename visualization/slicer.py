from vedo import Mesh, dataurl, Plotter, Points, show, Text2D
from visualization.visualisation_functions import *
from vedo.applications import Slicer3DPlotter
import matplotlib.cm as cm


def main():

    coords = get_3d_lines(get_coords()[0], get_coords()[1], 1000, get_vel_as_arr())
    scals = coords[:, 3]             # set equl to 3 to present v with color
    pts = Points(coords[:, 0:3])
    pts.pointdata["scals"] = scals
    vol = pts.tovolume(kernel='gaussian', n=3).smooth_gaussian(sigma=(0.25, 0.25, 0.25))





    vol.c(["r","g","b"])        # set color   transfer function
    vol.alpha([0, 1])            # set opacity transfer function
    vol.alpha_unit(0.1)



    slice = Slicer3DPlotter(
        vol,
        bg="black",
        bg2="white",
        cmaps=("jet_r", "Spectral_r", "gist_ncar_r", "hot_r", "bone_r"),
        use_slider3d=False,
        draggable=False,
        show_histo=True
    )
    plt.show(slice)

if __name__ == "__main__":
    main()
