import matplotlib.pyplot as plt 
import csv 
import numpy as np
import seaborn as sns
import os
from pathlib import Path



GRID_INDEX = 0
CELLS_INDEX = 2
AGGLOMERATION_INDEX = 3
AGENTS_INDEX = 4
MAX_INDEX = 5


home_directory = Path.home()

current_directory = os.getcwd()


def read_parameters(input_filename, output_filename, index):

    """
        Reads parameters from input and output CSV files.

    """
    x = []
    y = []
    y1 = []
    y2 = []

    with open(f"{input_filename}",'r') as inputfile: 
        with open(f"{output_filename}",'r') as outputfile:  
            inputlines = csv.reader(inputfile, delimiter=',') 
            outputlines = csv.reader(outputfile, delimiter=',') 

            #skip the header line
            next(inputlines)
      

            # Read each row from input file
            for inputline in inputlines:
            
                x.append(float(inputline[index])) 
            
            # Read each row from output file
            for outputline in outputlines:
            
                y.append(float(outputline[0])) 
                y1.append(float(outputline[1])) 
                y2.append(float(outputline[2])) 

    return  x, y, y1, y2



def plot_time(x, y, subfolder, xlabel, filename):

    
    """
        Plots the time performance as a function of input size.

    """

    plt.figure(figsize=(15,6))
    plt.plot(x, y, color = 'b', label = "Time (seconds)") 
  
    plt.xticks(rotation = 25) 
    plt.xlabel(f"{xlabel}") 
    plt.ylabel('Time') 
    plt.title('Time complexity', fontsize = 15) 
    plt.grid() 
    plt.legend() 
 
    subfolder_path = subfolder+"_fig"
    os.makedirs(subfolder_path, exist_ok=True)
    file_path = os.path.join(subfolder_path, 'time__'+filename+'.pdf')
    plt.savefig(file_path)

    #plt.show()
    plt.clf()

          
def plot_space(x, y1, subfolder, xlabel, filename):   

    """

        Plots the space performance as a function of input size. 
        
    """
     
    plt.figure(figsize=(15,6))
    plt.plot(x, y1, color = 'b', label = "Memory (byte)") 
  
    plt.xticks(rotation = 25) 
    plt.xlabel(f"{xlabel}") 
    plt.ylabel('Memory occupied') 
    plt.title('Space complexity (byte)', fontsize = 15) 
    plt.grid() 
    plt.legend() 
 
    subfolder_path = subfolder+"_fig"
    os.makedirs(subfolder_path, exist_ok=True)
    file_path = os.path.join(subfolder_path, 'space__'+filename+'.pdf')
    plt.savefig(file_path)


    #plt.show()
    plt.clf()

  

          
def plot_peak(x, y2, subfolder, xlabel, filename):  

    
    """
       Plots peak memory usage as a function of input size.
        
    """
   
    plt.figure(figsize=(15,6))
    plt.plot(x, y2, color = 'b', label = "Memory (byte)") 
  
    plt.xticks(rotation = 25) 
    plt.xlabel(f"{xlabel}") 
    plt.ylabel('Memory occupied') 
    plt.title('Space complexity (byte)', fontsize = 15) 
    plt.grid() 
    plt.legend() 
 
    
    subfolder_path = subfolder+"_fig"
    os.makedirs(subfolder_path, exist_ok=True)
    file_path = os.path.join(subfolder_path, 'peak__'+filename+'.pdf')
    plt.savefig(file_path)


    #plt.show()
    plt.clf()


current_directory = os.getcwd()

############################ grid implemented using an array #############################

subfolder = "grid"
subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs-grid_array'
file_input = os.path.join(subfolder_path_current, 'inputs.csv')

file_output = os.path.join(subfolder_path_current, output_name +".csv")
x_label = "Input size (grid dimensions)"




x, y, y1, y2 = read_parameters(file_input, file_output, GRID_INDEX)


plot_time(x, y, subfolder_path_current, x_label, output_name)

plot_space(x, y1, subfolder_path_current, x_label, output_name)

plot_peak(x, y2, subfolder_path_current, x_label, output_name)





############################ agents measures 50 x 50 #############################
subfolder = "agents"
subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs-agents_array_50_50'
file_input = os.path.join(subfolder_path_current, 'inputs-agents_50_50.csv')

file_output = os.path.join(subfolder_path_current, output_name + '.csv')
x_label = "Input size (number of agents)"


x, y, y1, y2 = read_parameters(file_input, file_output, AGENTS_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)




subfolder = "agents"
subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs_agents_array_100_50'
file_input = os.path.join(subfolder_path_current, 'inputs-agents_100_50.csv')

file_output = os.path.join(subfolder_path_current, output_name + '.csv')
x_label = "Input size (number of agents)"


x, y, y1, y2 = read_parameters(file_input, file_output, AGENTS_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)

############################ max measures 30 x 20 #############################

current_directory = os.getcwd()
subfolder = "max_grid"
subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs-max_30_20'
file_input = os.path.join(subfolder_path_current, 'inputs-max_30_20.csv')

file_output = os.path.join(subfolder_path_current, output_name+'.csv')
x_label = "Input size (max) in a 30 x 20 grid"


x, y, y1, y2 = read_parameters(file_input, file_output, MAX_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)

############################ max measures 100 x 50 #############################

output_name = 'outputs-max_100_50'
file_input = os.path.join(subfolder_path_current, 'inputs-max_100_50.csv')

file_output = os.path.join(subfolder_path_current, output_name+ '.csv')
x_label = "Input size (max) in a grid 100 x 50"


x, y, y1, y2 = read_parameters(file_input, file_output, MAX_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)




############################ agglomeration measures 100 x 50#############################

output_name = 'outputs-agglomeration'


subfolder = "agglomeration"
subfolder_path_current = os.path.join(current_directory, subfolder)


file_input = os.path.join(subfolder_path_current, 'inputs-agglomeration_100_50.csv')

file_output = os.path.join(subfolder_path_current, output_name +".csv")
x_label = "Input size (agglomeration factor) in a grid 100 x 50"



x, y, y1, y2 = read_parameters(file_input, file_output, AGGLOMERATION_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)



############################ agglomeration measures 50 x 50#############################


output_name = 'outputs-agglomeration_50_50'
file_input = os.path.join(subfolder_path_current, 'inputs-agglomeration_50_50.csv')

file_output = os.path.join(subfolder_path_current, output_name +".csv")
x_label = "Input size (agglomeration factor) in a grid 50 x 50"




x, y, y1, y2 = read_parameters(file_input, file_output, AGGLOMERATION_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)

############################ cells measures 50 x 50#############################
subfolder = "cells"
subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs_new_array__cells_50_50'
file_input = os.path.join(subfolder_path_current, 'inputs-cells_50_50.csv')

file_output = os.path.join(subfolder_path_current, output_name +".csv")
x_label = "Input size (percentage of traversable cells) in a grid 50 x 50"




x, y, y1, y2 = read_parameters(file_input, file_output, CELLS_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)

############################ cells measures 100 x 50#############################


output_name = 'outputs_new_array__cells_100_50'
file_input = os.path.join(subfolder_path_current, 'inputs-cells_100_50.csv')

file_output = os.path.join(subfolder_path_current, output_name +".csv")
x_label = "Input size (percentage of traversable cells) in a grid 100 x 50"




x, y, y1, y2 = read_parameters(file_input, file_output, CELLS_INDEX)


plot_time(x, y, subfolder, x_label, output_name)

plot_space(x, y1, subfolder, x_label, output_name)

plot_peak(x, y2, subfolder, x_label, output_name)


############################ agents in a 100 x 50 grid implemented with dictonary #############################
folder = "dictionary"
subfolder_path_current = os.path.join(current_directory, folder)


subfolder = "agents"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)

#subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs_agents_dict_100_50_2'
file_input = os.path.join(subsubfolder_path, 'inputs-agents_100_50.csv')

file_output = os.path.join(subsubfolder_path, output_name + '.csv')
x_label = "Input size (number of agents) in a grid 100 x 50"


x, y, y1, y2 = read_parameters(file_input, file_output, AGENTS_INDEX)
new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)

plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)

############################ agents in a 50 x 50 grid implemented with dictonary #############################

##file in cui gli agenti sono implentati con dictionary
folder = "dictionary"
subfolder_path_current = os.path.join(current_directory, folder)


subfolder = "agents"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)

#subfolder_path_current = os.path.join(current_directory, subfolder)

output_name = 'outputs-agents_dictionary_50_50'
file_input = os.path.join(subsubfolder_path, 'inputs-agents_50_50.csv')

file_output = os.path.join(subsubfolder_path, output_name + '.csv')
x_label = "Input size (number of agents) in a grid 50 x 50"


x, y, y1, y2 = read_parameters(file_input, file_output, AGENTS_INDEX)
new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)


plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)



############################ cells measures 50 x 50 implemented with dictonary #############################

subfolder = "cells"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)


output_name = 'outputs-dict-cells_50_50'
file_input = os.path.join(subsubfolder_path, 'inputs-cells_50_50.csv')

file_output = os.path.join(subsubfolder_path, output_name +".csv")
x_label = "Input size (percentage of traversable cells) in a grid 50 x 50"




x, y, y1, y2 = read_parameters(file_input, file_output, CELLS_INDEX)

new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)


plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)

############################ cells measures 100 x 50 implemented with dictonary #############################

output_name = 'outputs-dict-cells_100_50'
file_input = os.path.join(subsubfolder_path, 'inputs-cells_100_50.csv')

file_output = os.path.join(subsubfolder_path, output_name +".csv")
x_label = "Input size (percentage of traversable cells) in a grid 100 x 50"




x, y, y1, y2 = read_parameters(file_input, file_output, CELLS_INDEX)

new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)

plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)


############################ grid measures implemented with dictonary ##########################


folder = "dictionary"
subfolder_path_current = os.path.join(current_directory, folder)


subfolder = "grid"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)

output_name = 'outputs_grid_dict'
file_input = os.path.join(subsubfolder_path, 'inputs.csv')

file_output = os.path.join(subsubfolder_path, output_name +".csv")
x_label = "Input size (grid dimensions)"




x, y, y1, y2 = read_parameters(file_input, file_output, GRID_INDEX)
new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)

plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)

############################ max measures implemented with dictonary 30 x 20 ##########################



folder = "dictionary"
subfolder_path_current = os.path.join(current_directory, folder)


subfolder = "max"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)

output_name = 'outputs-max-dict_30_20'
file_input = os.path.join(subsubfolder_path, 'inputs-max_30_20.csv')

file_output = os.path.join(subsubfolder_path, output_name +".csv")
x_label = "Input size (max value) in a grid 30 x 20"


new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)


x, y, y1, y2 = read_parameters(file_input, file_output, MAX_INDEX)


plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)



############################ agglomeration measures implemented with dictonary 50 x 50 ##########################


folder = "dictionary"
subfolder_path_current = os.path.join(current_directory, folder)


subfolder = "agglomeration"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)

output_name = 'outputs_new_dict__agglomeration_50_50'
file_input = os.path.join(subsubfolder_path, 'inputs-agglomeration_50_50.csv')

file_output = os.path.join(subsubfolder_path, output_name +".csv")
x_label = "Input size (agglomeration)"

new_subfolder_path= os.path.join(subfolder_path_current +'_fig', subfolder)



x, y, y1, y2 = read_parameters(file_input, file_output, AGGLOMERATION_INDEX)


plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)

############################ agglomeration measures implemented with dictonary 100 x 50 ##########################



folder = "dictionary"
subfolder_path_current = os.path.join(current_directory, folder)


subfolder = "agglomeration"
subsubfolder_path = os.path.join(subfolder_path_current, subfolder)

output_name = 'outputs_new_dict__agglomeration_100_50'
file_input = os.path.join(subsubfolder_path, 'inputs-agglomeration_100_50.csv')

file_output = os.path.join(subsubfolder_path, output_name +".csv")
x_label = "Input size (agglomeration) in a grid 100 x 50"


x, y, y1, y2 = read_parameters(file_input, file_output, AGGLOMERATION_INDEX)

new_subfolder_path= os.path.join(subfolder_path_current  + '_fig', subfolder )


plot_time(x, y, new_subfolder_path, x_label, output_name)

plot_space(x, y1, new_subfolder_path, x_label, output_name)

plot_peak(x, y2, new_subfolder_path, x_label, output_name)