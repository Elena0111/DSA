from Grid import Grid_Obj
from queue import PriorityQueue
from time import time
from jinja2 import Template
import os
import random
import algorithm
import math as m
import csv
import sys, getopt
import tracemalloc
import gc
import re

ini_file = "seeds.ini"


def write_results(outputfile, time_result, space_result):
    """
        Creates the .csv output file

    """
    with open(f"{outputfile}.csv", mode='a', newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        output_writer.writerow([time_result, space_result[0], space_result[1]])
        

def init_files(argv):

    """
        Reads the parameters from the command line if present, otherwise use the default parameters
    
    """
        


    inputfile = None
    outputfile = "default"

    try:
        opts, _ = getopt.getopt(argv,"hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        sys.exit()

       

    for opt, arg in opts:
        if opt == '-h':
            print ('algorithm.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            
            inputfile = arg
        elif opt in ("-o", "--ofile"):
           
            outputfile = arg
       
    return inputfile, outputfile




def read_seeds(file):
    
    """
        Reads seeds from the seeds.ini file to initialise the random number generator
    
    """
        
    
    values = []
    with open(file, 'r') as f:
        for line in f:
            values.append(line.strip())
     
    return values



def read_parameters(filename):

    """
        Reads the parameters from the input csv file

    """
    j=0
 
    parameters = {} 

    with open(f"{filename}", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            parameter=[]

            # height 
            parameter.append(int(row[0]))

            # width
            parameter.append(int(row[1]))

            # percentage of traversable cells
            parameter.append(float(row[2]))

            # agglomeration factor
            parameter.append(float(row[3]))

            # number of agents
            parameter.append(int(row[4]))
            
            # max value
            parameter.append(int(row[5]))

            parameters[j]=parameter
            j=j+1
        
    return parameters



def write_summary(results_file, parameter, cost, agent1, mosse_wait, start1, goal1, paths, max, elapsed_time, allocated_mem, enumerate):
    
    """
        Writes the parameters and additional information in the summary file

    """
     
    template_str = """
\n\nGrid height: {{ parameter[0] }}
Grid width: {{ parameter[1] }}
Traversable cells percentages: {{ parameter[2] }}
Agglomeration factor: {{ parameter[3] }}

Gli agenti sono stati generati con l'algoritmo ReachGoal
Agents: {{ paths }}
Numero di agenti: {{ parameter[4] }}

{% for i, path in enumerate(paths) %}
Agent {{ i }}
Path: {{ path }}
Path length: {{ path|length }}
{% endfor %}

Init: {{ start1 }}
Goal: {{ goal1 }}
Max: {{ max }}
{% if cost is none %}
Failure
{% else %}
Path: {{ agent1 }}
Mosse wait: {{ mosse_wait }}
Cost to reach the goal: {{ cost }}
{% endif %}
Time: {{ elapsed_time }}
Current occupied memory: {{ allocated_mem[0] }}
Peak occupied memory: {{ allocated_mem[1] }}
Heuristic: diagonal distance
"""

    template = Template(template_str)
    output = template.render(
        enumerate = enumerate,
        parameter=parameter,
        paths=paths,
        start1=start1,
        goal1=goal1,
        agent1=agent1,
        mosse_wait=mosse_wait,
        cost=cost,
        max=max,
        elapsed_time=elapsed_time,
        allocated_mem=allocated_mem
    )

    
    file_name = results_file.replace('/', '_')
    with open(file_name, 'a') as file:
        file.write(output)
    

def color_grid(grid, paths, entry_agent):

    """
        Changes the grid value to print the grid

    """
    i=0

    for pos in grid.grid:    
        grid.set_cell_value(pos, "#")

    
    for agent in paths:
                
            for node in agent:
                grid.set_cell_value(node, str(i))
              
            i=i+1

    if entry_agent is not None:
        for node in entry_agent:
          
            grid.set_cell_value(node, "C")
        
    
    return grid

def checkMax(max, parameter, max_path):
   
    """
       Checks if the max value exceeds the maximum allowed value

    """
   

    if max > (parameter[0] * parameter[1] * parameter[2])+max_path:
        print("Max exceeds the maximum value")
        return True
   


def main(argv):
    
    
    inputfile, outputfile = init_files(argv)

    if inputfile != None and outputfile != None:
        results_file = "results" + inputfile + ".txt"

        parameters = read_parameters(inputfile)
    else:
        parameters = {}
        print("Using default parameters")

        # Prints the results in the file

        results_file = "results.txt"
        n_executions = 3
        for i in range(n_executions):
            parameters[i]=[10, 8, 0.8,  0.5, 3, 50]
    t=0

    max_path = 0

    # Execution for each instance

    for parameter in parameters.values():
        


        seeds = read_seeds(ini_file)
       
        random.seed(seeds[0])

        # Initialize the grid with the first seed

        grid = Grid_Obj(parameter[0], parameter[1], parameter[2], parameter[3], random)
   

       
        # Create start and goal positions for the first agent
            
        start, goal = grid.initialise_positions([], random)
        
        """Predefined agents values
        agents = [[[0,1], [2,1], [3,2], [4,2], [5,2]], #yellow
        [[1,3], [1,4], [1,5], [1,6], [1,7]], #green
        [[8,1], [7,2], [6,3], [6,4]], #light blue
        ]
        """
        # Number of agents
            
        paths=[]
       
       
        # Repeat the Reachgoal algorithm to create the agents paths

        n_agents = parameter[4]

        max = parameter[5]

        if checkMax(max, parameter, 0):
            continue

        for i in range(n_agents):
               
            _ , agent, mosse_wait = algorithm.reachGoal(start, goal, grid, max, paths, 0, False) # calling the A* algorithm
          
            # Repeats the algorithm until it finds a path to the goal

            while agent==None:

                start, goal = grid.initialise_positions(paths, random)
                _, agent, mosse_wait = algorithm.reachGoal(start, goal, grid, max, paths, 0, False) # calling the A* algorithm
                    
         
           
            if max > max_path: max_path = max 
            checkMax(max, parameter, max_path)

            paths.append(agent)
            j = i+1
            random.seed(seeds[j])

           


   

    
        # The last seed is used for the entry agent

        random.seed(seeds[n_agents])
       
        entry_agent_start, entry_agent_goal = grid.initialise_positions(paths, random)
    
        start = time()
        
        tracemalloc.start()

        print(f"\n\nExecuting the algorithm for the entry agent with {n_agents} agents")
      
        #Algorithm execution 
        cost, entry_agent_path, mosse_wait = algorithm.reachGoal(entry_agent_start, entry_agent_goal, grid, max, paths, 0, True)
        
        
        
        elapsed_time = time() - start
        

        time_interval = tracemalloc.get_traced_memory()
        tracemalloc.stop() 
        
        gc.collect()  # garbage collector to free memory

        write_summary(results_file, parameter, cost, entry_agent_path, mosse_wait, entry_agent_start, entry_agent_goal, paths, max, elapsed_time, time_interval, enumerate=enumerate)
        write_results(outputfile, elapsed_time, time_interval)
       
      
        #grid = color_grid(grid, paths, entry_agent_path)

        #grid.show_grid(f"final_path{t}.png", entry_agent_start, entry_agent_goal) 
        t = t+1








if __name__ == "__main__":
    main(sys.argv[1:])