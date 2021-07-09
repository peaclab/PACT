### This is a tool for generating a video for a transient result file from PACT. This tool will work with any '.cir.csv' grid file from PACT and will output a heatmap video file and a folder with individual heatmap frames for each simulation step.

# Requirements:

* Python version: 3.6.5

* Same libraries as PACT: sys, numpy, pandas, os, scipy, argparse,

* Additional Python libraries: matplotlib 2.2.0, seaborn 0.9.0, opencv-python 4.1.0.25, re, pathlib, shutil

* Users can directly install the correct version of the Python packages through the following commands:
```
pip install -r requirements.txt
```

# Usage:

```
python videogen.py [transient data file] [--fps FPS] [--overlay OVERLAY_IMAGE] [--min VMIN] [--max VMAX] [--layer LAYER] [--dpi DPI]
```     

The only required input is the transient data file. This file should have the extension '.grid.cir.csv' or '.cir.csv', but the script will still work if it was renamed. The video file and frame folder outputs will be saved to the same folder as the data file. All other inputs are optional:

* **--fps**: Default=5. Used to specify the frames-per-second value of the output video.

* **--overlay** : Default=None. Used to specify a floorplan image to overlay over the heatmap.

* **--min / --max** : Default=auto. Used to specify the min or max value (in degrees C) of the heatmap color scale. By default the script will use the min and max value from the data. Users may choose to specify both, only one, or niether of the values.

* **--layer** : Default=0. Used to specify the layer used for video generation.

* **--dpi** : Default=100. Used to modify the size of the heatmap images. By default, will use 100 dpi.

# Example
Here is a simple example with the included files:

```
python videogen.py Example_transient_data_files/IBMPower9transientheatsink_128x128.grid.cir.csv --overlay Example_overlay_images/IBMPower9.png
```
