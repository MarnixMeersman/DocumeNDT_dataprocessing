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


# Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged legally invalid or ineffective under applicable law, such
partial invalidity or ineffectiveness shall not invalidate the remainder
of the License, and in such case Affirmer hereby affirms that he or she
will not (i) exercise any of his or her remaining Copyright and Related
Rights in the Work or (ii) assert any associated claims and causes of
action with respect to the Work, in either case contrary to Affirmer's
express Statement of Purpose.

4. Limitations and Disclaimers.

 a. No trademark or patent rights held by Affirmer are waived, abandoned,
    surrendered, licensed or otherwise affected by this document.
 b. Affirmer offers the Work as-is and makes no representations or
    warranties of any kind concerning the Work, express, implied,
    statutory or otherwise, including without limitation warranties of
    title, merchantability, fitness for a particular purpose, non
    infringement, or the absence of latent or other defects, accuracy, or
    the present or absence of errors, whether or not discoverable, all to
    the greatest extent permissible under applicable law.
 c. Affirmer disclaims responsibility for clearing rights of other persons
    that may apply to the Work or any use thereof, including without
    limitation any person's Copyright and Related Rights in the Work.
    Further, Affirmer disclaims responsibility for obtaining any necessary
    consents, permissions or other rights required for any use of the
    Work.
 d. Affirmer understands and acknowledges that Creative Commons is not a
    party to this document and has no duty or obligation with respect to
    this CC0 or use of the Work.


