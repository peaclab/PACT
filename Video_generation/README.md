This is a tool for generating a video file from transient PACT results. This tool will work with any '.cir.csv' grid file from PACT and
 will output an avi video heatmap from the data as well as the individual frames from the video. 

Requirements: Python version: > 3.6.5
 Requires same libraries as PACT,
 Additional python Libraries: matplotlib, seaborn, cv2, re, pathlib, shutil 

How to use:
usage: videogen.py transient_data_file fps
                   [-h] [--overlay OVERLAY_IMAGE] [--min VMIN] [--max VMAX]
                   [--layer LAYER]
                   
transient_data_file : The first required input is the path to the transiend data file. The video and frame folder outputs will
 be placed in the same folder as the data file. This file should have the extension '.grid.cir.csv' or '.cir.csv', but it 
 should still work if the file was renamed.

fps: The second input is the frames-per-second value of the output video. For a 100 frame video, 5 fps may be a good starting point.

--overlay : This flag can be used to specify a floorplan image to overlay over the trasient heatmap images. The script will automatically
 resize the image to fit the aspect ratio of the data's grid resolution. For the 'agg' backend, the script works when the overlay_height is 
 set to 370 pixels, but this may need to be adjusted depending on your system.

--min / --max : These flags can be used to specify the range for the heatmap scale in degrees Celcius. By default, the script will just get
 the min and max values from the data file, but --min or --max can be used to limit this range. The user may choose to specify neither, one,
 or both flags.

--layer : This flag can be used to specify the layer to use for the video generation. By default, the script will use layer 0.

-h, --help : shows usage


Example: python videogen.py /projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/IBM_Power9/results/Power9/IBMPower9transientheatsink_100x100.grid.cir.csv 5 --overlay IBMPower9.png 


transient files:
/projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/IBM_Power9/results/Power9/IBMPower9transientheatsink_100x100.grid.cir.csv
/projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/IBM_Power9/results/Power9/IBMPower9transientheatsink_275x253.grid.cir.csv
/projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/IBM_Power9/results/Power9/IBMPower9transientnopackage_100x100.grid.cir.csv
/projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/OpenRoad/results/Pico/Pico95_128x128.grid.cir.csv
/projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/Example_command_line/example.cir.csv
/projectnb/peaclab-cri-cooling/PACT_Carlton/PACT/Example/results/20mm/MyToolRun_htc_1e5_NonUniformPD_50_500Wcm2_80x80.cir.csv
