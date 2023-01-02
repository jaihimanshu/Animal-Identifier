import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import datetime
from PIL import Image
from natsort import os_sorted

#Change the parameters as per user's choice
save_path = 'C:/Users/himan/OneDrive/Desktop/IDC409/Project2/'
times=100
Generations=200
Cross_over_prob=0.6
Mutation_prob=[0.05]

now = datetime.now()
todaysDate = now.strftime("%d-%m-%Y_%H-%M-%S")
os.mkdir(f"{save_path}Results/{todaysDate}")
choice=0 
fun=["Pearson Correlation"]
Population_size=times*len(os.listdir(f"{save_path}Processed_animals/"))
animaln=os_sorted(os.listdir(f"{save_path}Processed_animals/"))
animalno=[]
for i,u in enumerate(animaln):
    animalno.append(len(os.listdir(f"{save_path}Processed_animals/{animaln[i]}")))