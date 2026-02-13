#Importing the necessary libraries

#Data Analysis and Data Wrangling
import numpy as np
import pandas as pd

#Data Visualization
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns
#%matplotlib inline

#Setting up plot styles
#sns.set_style('whitegrid')
sns.set_context('poster') #larger fonts

import random

#Displaying all the columns in the dataset
pd.set_option('display.max_columns', None)


class Nootropics_effect():
    """Class to examine the substances that have and do not have effects on certain aspects of our lives."""
    
    def __init__ (self, data, substance, varB):
        """Initializing the attributes in the Sub_effect class"""
        self.data = data
        self.substance = substance
        self.varB = varB
    
    def negative_effect(self):
        data_varB = self.data[[self.substance, self.varB]]
        
        negative_effect = data_varB[data_varB[self.varB] < 0].reset_index(drop = True)
        
        print(f"{len(negative_effect)} substances have negative effects on {self.varB} \n")
        
        print(f"Substances that have negative effects on {self.varB} are: \n")
        for sub in negative_effect[self.substance].to_list():
            print(sub)
            
        return data_varB[data_varB[self.varB] < 0].sort_values([self.varB], ascending = False).reset_index(drop = True)
        
        
    def zero_effect(self):

        data_varB = self.data[[self.substance, self.varB]]
        
        no_effect = data_varB[data_varB[self.varB] == 0].reset_index(drop = True)
        
        print(f"{len(no_effect)} substances have no effect on {self.varB} \n")
        
        print(f"Substances that have no effect on {self.varB} are: \n")
        for sub in no_effect[self.substance].to_list():
            print(sub)
            
    
    def positive_effect(self):
        data_varB = self.data[[self.substance, self.varB]]
        
        effect = data_varB[data_varB[self.varB] > 0].sort_values([self.varB], ascending = False).reset_index(drop = True)
        
        print(f"{len(effect[self.substance].to_list())} substances have varying positive effects on {self.varB}")
        print("\nIn the order of their intensity, they are:  \n")
        
        for substance in effect[self.substance].to_list():
            print(substance)
        
        print(f'\nNOTE: Their effects are independent of each other, and the higher they are, the stronger their effect on {self.varB} \n')
        
        print(f"\n\nThe top 10 substances that have a positive effect on {self.varB} and by how much are: \n")
        
        return effect[0:10]
    
    def top10_effect(self):
        data_varB = self.data[[self.substance, self.varB]]
        
        new_data = data_varB[data_varB[self.varB] > 1].sort_values([self.varB], ascending = False).reset_index(drop = True)[0:10]
        return new_data
    
    def visualize_effect(self):
        data_varB = self.data[[self.substance, self.varB]]
        new_data = data_varB[data_varB[self.varB] > 1].sort_values([self.varB], ascending = False).reset_index(drop = True)[0:10]
        
        x = new_data[self.varB]
        y = new_data[self.substance]


        plt.figure(figsize = (12, 8))

        color_palettes = ['muted', 'bright', 'dark','Set1', 'Set2', 'Pastel1', 'Pastel2', 'Set3', 'Paired' ]
        
        sns.barplot(x=x, y=y, palette = random.choice(color_palettes), orient = 'horizontal')
        plt.title(f'Top 10 substances affecting {self.varB}', fontsize = 30)
        plt.xlabel('Intensity', fontsize = 25)
        plt.ylabel('Substances', fontsize = 25)
        plt.xticks(np.arange(0, 40, 5))

        plt.show()