# VisualPACT
### VisualPACT is a tool for generating a video for a transient result file from PACT. This tool will work with any '.cir.csv' grid file from PACT and will output a heatmap .avi video file and a folder with individual heatmap images for each simulation step.

# Requirements:

* Python version: 3.6.5

* Same libraries as PACT: sys, numpy, pandas, os, argparse

* Additional Python libraries: matplotlib 2.2.0, seaborn 0.9.0, opencv-python 4.1.0.25, re, pathlib, shutil

* Users can directly install the correct version of the Python packages through the following commands:
```
pip install -r requirements.txt
```

# Usage:

```
python VisualPACT.py [transient data file] [--fps FPS] [--overlay OVERLAY_IMAGE] [--min TMIN] [--max TMAX] [--layer LAYER] [--dpi DPI]
```     

The only required input is the transient data file.

* The **transient data file** should have the extension '.grid.cir.csv' or '.cir.csv', but the script will still work if it was renamed. The video file and frame folder outputs will be saved to the same folder as the data file. The first row of the transient data file must be a header containing the names of all the columns of the data. Aside from the "TIME" column, all column names will have the format "V(NODE{layer}\_{row}\_{column})" (e.g. "V(NODE0\_0\_0)").

All other inputs are optional:

* **--fps**: (Default=5) Used to specify the framerate of the output video. Each simulation time step is represented by a single heatmap image/frame. Users may want to adjust the fps based on the simulation step size and total simulation time.

* **--overlay** : (Default=None) Used to specify a floorplan image to overlay over the heatmap. (The visualize_floorplan.py script in the [Hotspot](https://github.com/uvahotspot/HotSpot) repo may be used to generate an image from a Hotspot flp file)

* **--min / --max** : (Default=auto) Used to specify the min or max value (in degrees C) of the heatmap color scale. By default the script will use the min and max value from the data. Users may choose to specify both, only one, or niether of the values.

* **--layer** : (Default=0.) Used to specify the chip layer used for video generation. For single layer chips, layer 0 is the processor layer and layer 1 is the cooling package layer. For chips with multiple layers, this can be used to make a separate video for a specific chip layer. Check the main PACT [README](https://github.com/peaclab/PACT) for more information.

* **--dpi** : (Default=100.) Used to modify the size of the heatmap images. By default, will use 100 dpi.

When designing an overlay image, it is reccomended to use thick lines, as thin lines may not show up at lower DPI settings. Otherwise, the DPI flag can be used to increase the resolution and size of the video file.

# Example
Here are some examples that work with the included files:

```
python VisualPACT.py Example_transient_data_files/IBMPower9transientheatsink_128x128.grid.cir.csv --overlay Example_overlay_images/IBMPower9.png
```
```
python VisualPACT.py Example_transient_data_files/IBMPower9transientnopackage_128x128.grid.cir.csv --fps 20 --min 40 --overlay Example_overlay_images/IBMPower9.png 
```
```
python VisualPACT.py ../Example_command_line/example.cir.csv
```
The script will print out information such as the grid resolution, video file and image folder path, and the min and max values of the colorbar. If the script runs correctly, the output should look like this:
```
python VisualPACT.py Example_transient_data_files/IBMPower9transientheatsink_128x128.grid.cir.csv --overlay Example_overlay_images/IBMPower9.png
IBMPower9transientheatsink_128x128
128 x 128
video path: <Path to PACT folder>/VisualPACT/Example_transient_data_files/IBMPower9transientheatsink_128x128.avi
image folder path: <Path to PACT folder>/VisualPACT/Example_transient_data_files/IBMPower9transientheatsink_128x128_frames/
vmin: 45.0         
vmax: 58.710000000000036
Done.                  
```
IBMPower9transientheatsink_128x128.avi:

![IBMPower9transientheatsink_128x128 (1)](https://user-images.githubusercontent.com/12175631/125837775-d0e5aa7a-a29e-4a1e-9e15-b8379312034f.gif)

If the script is run twice with the same transient file path, the previous video data will be replaced. To save previous video files, users can rename or move the files.
