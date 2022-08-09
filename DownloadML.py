import gdown
import os
url = "https://drive.google.com/u/0/uc?id=1RUiWwh-QwoA9dr1XTI_MsCUVilMPsZdw&export=download"
output = "MLModels.tar.gz"
gdown.download(url, output)
os.system("tar -xvf MLModels.tar.gz")
