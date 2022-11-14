# DocumeNDT_dataprocessing

The script requires you to upload matlab ".mat" files into the ./raw_data folder. Make sure the filenames have only a code-number as file name, e.g. "11.mat", as it searches for these particular names while processing.
The second step is to open main.py and adjust the parameters to your liking, at the top of the file, you should define the locations list which should corresponds to the files you just uploaded. 
Parameters to adjust include:
  - locations ID's
  - number of stickers (programm assumes 10 laserpoints per sticker)
  - Signal to Noise Ratio threshold to disregard bad quality readings
  - Variance threshold on when to trigger T1
  
 The ouput of main.py updates ./results/time_differences.csv, velocities.csv should be calculated yourself using an excelfile and the known locations of emission and reception. 
 If make_plots = True, you can find the results under ./plots. Careful, this almost doubles the processing time. A short runtime is around 5 minutes.
