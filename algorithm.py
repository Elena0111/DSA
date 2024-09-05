from Grid import Grid_Obj

from queue import PriorityQueue
from time import time
import math as m
import csv
import os



ini_file = "seeds.ini"
inputfile = ''
outputfile = ''




def minimum_distance(node: list[int, int], end: list[int, int]):

        """ 
            Calculates the Euclidian distance between two given points.

        """

        return m.sqrt(m.pow(end[0] - node[0], 2) + m.pow(end[1] - node[1], 2))


def diagonal_distance(node, goal):

        
        """ 
            Calculates the Diagonal distance between two given points.

        """
        
        dx = abs(node[1] - goal[1])
        dy = abs(node[0] - goal[0])
        return 1 * (dx + dy) + (m.sqrt(2) - 2 * 1) * min(dx, dy)




def find_state(state, queue):

    """ 
        Checks if a state is present in the queue 

    """
    result = False

    for i in range(len(queue.queue)):
        element=queue.queue[i]
        if element == state:
            result = True
    return result

def find_node(state, closed):

    """ 
        Checks if a node is present in the queue 

    """
    while closed.empty():
        if state == closed.get()[0]:
            node = state[0]
            return node

    return None


def get_cost_to_node(next_state, cost_to_node, open, closed):

    """ 
       Initializes the cost of the unexplored nodes

    """
     
    if not find_state(next_state, open) and not find_state(next_state, closed):

        return float('inf')
    
    else:

        return cost_to_node[tuple(next_state)]


def vprint(text, verbose):
    
    """ 
      Prints the given text if the verbose mode is enabled

    """
    if verbose: 
        print(text)


def find_prev_position(agent, t):

     
    """ 
      Returns the previous position of a wait state, that is the position in the path before the wait state

    """

    # all the temporal istants before the wait state
    lower_values = [value for value in agent.keys() if value < t]

    #the one immediately before the wait state
    return max(lower_values)

def getAgentPositionsFromArray(agent, t):

    """ 
      Get the position of the time t in the agent path implemented as an array

    """

    if len(agent) > t:
        position= agent[t]
        prev_position= agent[t-1]
    else:

        #if the agent is in his goal position already

        position= agent[len(agent)-1]
        prev_position= agent[len(agent)-2]

    return position, prev_position



def getAgentPositionFromDictionary(agent, t):
    """ 
      Get the position of the time t in the agent path implemented as dictionary

    """
         
    if t not in agent.keys():

        # This means that it is a wait state or already in his goal position, therefore we need to return the previous position in the path

        key =find_prev_position(agent, t)
        position = agent[key]
        
    else:
        position= agent[t]
        
    return position


def reachGoal(start, goal, grid, max, agents, mosse_wait, verbose):

    """
    Implementation of the A* algorithm for finding the shortest path between two points.

    """

   

    parent_node = {}    # dictionary that contains the parent of each node in the shortest path
    cost_to_node = {}    # dictionary that contains the cost to get to each node in the shortest path

    # A state consists of the vertex coordinates and time

    state_start=tuple([tuple(start), 0])

    parent_node[tuple(state_start)] = None    # The start node has no parent

    cost_to_node[tuple(state_start)] = 0    # The cost to get to the start node is 0

   
    t=0
    traversable = False

    """
    The frontier is implemented as a priority queue with the priority being the cost to get to the node + the heuristic.
    Every time we pop a node from the frontier, we are guaranteed that it is the one with the lowest cost to get to it.

    """
    open = PriorityQueue()


    closed = PriorityQueue()

    #Put the start node into the frontier, with the f score. In this case it corresponds to the heuristic function

    open.put((diagonal_distance(goal, start), state_start), 0)      # Add the start node to the frontier
    
    while not open.empty():  # Continue searching while there are nodes to explore

        current_state = tuple(open.get()[1])    # Retrieve the state with the lowest cost to reach
       
        closed.put(current_state) 
        
        current_node = current_state[0]

        # If the current node is the goal, we have found the shortest path

        if current_node == tuple(goal):
            
            return reconstruct_path(grid, parent_node, cost_to_node, start,current_state, mosse_wait,verbose)

        t = t+1
        
        neighbors=grid.neighbors(current_node)
        
        if t < max:
            
            

            for next_node in neighbors:    # checks all the neighbors of the current node, Adv[v]
                
                next_state=[next_node, t]

            
                found= find_state(tuple(next_state), closed)

                if found==False:
                    traversable= True

                #checks that there are no collisions with other agents

                for agent in agents:

                    #these should be uncommented when using an array
                    
                    #position = getAgentPositionFromDictionary(agent, t)
                    #prev_position = getAgentPositionFromDictionary(agent, t-1)

                    #if the agent is in his goal position
                    position, prev_position = getAgentPositionsFromArray(agent, t)

                    if  position==next_node or (position==current_node and prev_position==next_node):
                        traversable = False
                        break # we need just one collision for it not to be traversable


                if traversable == True:

                # cost to get to the node = cost to get to the parent in the previous time + cost to go 

                    new_cost = cost_to_node[tuple(current_state)] + grid.get_weight_value(current_node, next_node)
            
                

                # verifies that the current node hasn't already been considered or that it has a lower cost  

                    if new_cost < get_cost_to_node(next_state, cost_to_node, open, closed) or tuple(next_node) not in cost_to_node: 

                    # In this case, it adds a new entry in cost_to_node, inserts the node into the frontier, and updates its predecessor

                        cost_to_node[tuple(next_state)] = new_cost
                        parent_node[tuple(next_state)] = current_state
                        
                    find=find_state(tuple(next_state), open)

                    if find==False:
                        
                        priority = new_cost + diagonal_distance(goal, next_node)    # priority = cost to get to the node + heuristic
                     
                        open.put((priority, next_state))
                       
    
                
    #vprint(f"Mosse wait {mosse_wait}", verbose)
    vprint(f"Numero di stati espansi {closed.qsize()}", verbose)
   
    return None, None, None 

def fill_nodes(nodes, mosse_wait):

    """
        Fill the nodes array with the positions corresponding to the wait states

    """


    for i in range(len(nodes)):
        if nodes[i] == 0:
            nodes[i] = nodes[i-1] 
            
            mosse_wait = mosse_wait +1
      
    return nodes, mosse_wait      

def wait_counter(nodes, lenght):

    """
        Counts the wait states in a path implemented as a dictionary

    """
    wait = 0
    for i in range(lenght):
        if i not in nodes.keys():
            wait += 1
    return wait


def reconstruct_path(grid, parent_node, cost_to_node, start, goal, mosse_wait, verbose):

    """
    Reconstructs the shortest path between the start and goal positions of the given grid,
   
    """

    # getting the start and goal positions

    
    start_state=tuple([tuple(start), 0])

    # drawing the path starting from the goal node and going backwards to the start

    current_state = goal
    lenght= current_state[1]
   

    nodes=[0 for i in range(lenght+1)]
    
    #nodes = {}
    
    nodes[lenght] = goal[0]
   
    while parent_node[current_state] != start_state:
        
        current_state = parent_node[current_state]    # going to the predecessor of the current node
       
        nodes[current_state[1]] = current_state[0]
         
    
    
    nodes[0]=start_state[0]

    # If we are implementing the paths as arrays, we need to fill the arrays with positions correspoinding to wait states

    nodes, mosse_wait = fill_nodes(nodes, mosse_wait)

    # This method is used in order to count the wait states if we don't implement the paths as arrays

    #mosse_wait = wait_counter(nodes, lenght) 

    
    vprint(f"Lunghezza del cammino minimo: {lenght}", verbose)
    vprint(f"Cost del cammino minimo: {cost_to_node[tuple(goal)]}", verbose)
    vprint(f"Mosse wait {mosse_wait }", verbose)
    return cost_to_node[tuple(goal)], nodes, mosse_wait


