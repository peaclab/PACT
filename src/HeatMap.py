import seaborn as sns
import matplotlib.pyplot as plt

#Up to which layer do you want the heat map
def createHeatMap(np_array, num_layers):
    fig, ax = plt.subplots(num_layers,1)
    heat_map =[]
    #print(type(heat_map))
    for layer in range(num_layers+1):
        heat_map= heat_map + [sns.heatmap(np_array[layer],cmap="coolwarm")]
    return (heat_map,num_layers)
