![Ontwerp zonder titel-1](https://user-images.githubusercontent.com/57674797/203540981-e0793f43-e972-47eb-a662-410762a034ef.jpeg)
_This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No 101030275_

Latest release:  <a href="https://zenodo.org/badge/latestdoi/565529865"><img src="https://zenodo.org/badge/565529865.svg" alt="DOI"></a>
# DocumeNDT_dataprocessing

## Quick Start
First copy this repository to your pc running the following in your python terminal (Python 3.9 recommended)
```
git clone https://github.com/MarnixMeersman/DocumeNDT_dataprocessing
```

Then install al required libraries using: (if prophet gives you errors, dont worry, it is only required for machine learning time series predictions and not a vital library in order to run the rest)
```
pip install -r requirements.txt
```


Then proceed with reading this README. Have fun!

## Data Processing
The script requires you to upload matlab ".mat" files into the ./raw_data folder. Make sure the filenames have only a code-number as file name, e.g. "11.mat", as it searches for these particular names while processing.
The second step is to open main.py and adjust the parameters to your liking, at the top of the file, you should define the locations list which should corresponds to the files you just uploaded. 
Parameters to adjust include:
  - locations ID's
  - number of stickers (programm assumes 10 laserpoints per sticker)
  - Signal to Noise Ratio threshold to disregard bad quality readings
  - Variance threshold on when to trigger T1
  
 The ouput of main.py updates ./results/time_differences.csv, velocities.csv should be calculated yourself using an excelfile and the known locations of emission and reception. 
 If make_plots = True, you can find the results under ./plots. Careful, this almost doubles the processing time. A short runtime is around 5 minutes. Here a visual overview of main.py:
 
<img width="1512" alt="SCR-20221121-dzt" src="https://user-images.githubusercontent.com/57674797/203034779-757c3c58-5ad0-48df-947e-db9577fdab2b.png">

### Manual Checker: manual_checker.py
To manually check any of the waveforms, use manual_checker.py as shown below. Adjustment to T0 or T1 can be made using the GUI. Clicking on the legend allows you to view and hide different tranformations and signals. 

![ezgif-3 com-gif-maker](https://user-images.githubusercontent.com/57674797/203036614-0ac37bae-9c6e-494c-8c88-1f40d58daa07.gif)

## Visualizing your results
In order to visualize your results, go to the ./visualization folder. Make sure that you update your ./visualization/emission_reception_velocities folder since it uses only these values. So UPDATE MANUALLY this folder. Below a video showing how to use the interface:

!!!In addition for 3d visualizations, please upload a DOWNSAMPLED .obj file for the object. Also, the scaling might be off sometimes, try exporting in mm instead of meters. You can shift and scale the obj file playing with the scaling and shifteing operators for each axis in line 62, 63 and 64 of visualisation_function.py !!!
### 3D Slicer Filer: slicer.py
Allows you to take sections of the interpolated volume using the slicers in X, Y and Z. Button in the top left allows for different color mappings. The histogram represents the distribution over the WHOLE volume. Therefore in doesn't change when playing with the sliders. 

![ezgif-2 com-gif-maker](https://user-images.githubusercontent.com/57674797/203033455-35437852-9549-4133-be0d-5769828edbd7.gif)

### 3D Visulation File: mesh_visual.py
It allows your for an interactive way to see side my side the interpolated volume and the the dimensional object containing the rays that pass-through your volume (requires an .obj file)
![Screen Recording 2022-11-21 at 11](https://user-images.githubusercontent.com/57674797/203034542-47a0f97e-d631-41d4-b4f2-9e9eb7da2332.gif)


# License
DocumeNDT_dataprocessing is available under the CC0 license. See the LICENSE file for more info.
