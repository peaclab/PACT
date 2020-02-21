import seaborn as sns
import matplotlib.pyplot as plt

createHeatMap(np_array, num_layers):
    if num_layers == 1:
        heat_map = sns.heatmap(np_array)
        plt.show()
