# DocumeNDT_dataprocessing

The script requires you to upload matlab ".mat" files into the ./raw_data folder. Make sure the filenames have only a code-number as file name, e.g. "11.mat", as it searches for these particular names while processing.
The second step is to open main.py and adjust the parameters to your liking, at the top of the file, you should define the locations list which should corresponds to the files you just uploaded. 
Parameters to adjust include:
  - locations ID's
  - number of stickers (programm assumes 10 laserpoints per sticker)
  - Signal to Noise Ratio threshold to disregard bad quality readings
  - Variance threshold on when to trigger T1
  
 The ouput of main.py updates ./results/time_differences.csv, velocities.csv should be calculated yourself using an excelfile and the known locations of emission and reception. 
 If make_plots = True, you can find the results under ./plots. Careful, this almost doubles the processing time. A short runtime is around 5 minutes. Here a visual overview:
 
<img width="1512" alt="SCR-20221121-dzt" src="https://user-images.githubusercontent.com/57674797/203034779-757c3c58-5ad0-48df-947e-db9577fdab2b.png">
 
To manually check any of the waveforms, use manual_checker.py as shown below. Adjustment to T0 or T1 can be made using the GUI.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/57674797/203011903-475c887e-d0fa-4c18-9d5a-56650cf11c93.gif)

In order to visualize your results, go to the ./visualization folder. Make sure that you update your ./visualization/emission_reception_velocities folder since it uses only these values. So UPDATE MANUALLY this folder. Below a video showing how to use the interface:

!!!In addition for 3d visualizations, please upload a DOWNSAMPLED .obj file for the object. Also, the scaling might be off sometimes, try exporting in mm instead of meters. You can shift and scale the obj file playing with the scaling and shifteing operators for each axis in line 62, 63 and 64 of visualisation_function.py !!!

![ezgif-2 com-gif-maker](https://user-images.githubusercontent.com/57674797/203033455-35437852-9549-4133-be0d-5769828edbd7.gif)

![Screen Recording 2022-11-21 at 11](https://user-images.githubusercontent.com/57674797/203034542-47a0f97e-d631-41d4-b4f2-9e9eb7da2332.gif)





