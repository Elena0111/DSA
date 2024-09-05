from queue import PriorityQueue
#import math as m
import random 
from PIL import Image
import math as m
import numpy as np


class Grid_Obj():

    def __init__(self, width, height, traversable_percent, agglomeration_factor, random):

        """
        Instantiate a grid object for the given parameters.

        """
        
        self.width=width
        self.height=height
         
        self.obstacle_percents = 1 - traversable_percent

        #if we implement the grid as an array of obstacles

        self.grid=[]  

        #if we implement the grid as a matrix
        #self.grid=[[ -1 for i in range(self.width) ] for j in range(self.height) ]  

        #this is used to show the grid

        self.matrix_string=[ [ -1 for i in range(self.width) ] for j in range(self.height) ]  

        self.agglomeration_factor = agglomeration_factor
       
        self.build_grid(random)
        
        

    def checkBorders(self, move):

        """
            Checks if a coordinate position is between the grid height and width

        """

        if move[0] <= self.height-1 and move[0] >= 0 and move[1] <= self.width-1 and move[1] >= 0:

            return True
        
        else:

            return False

  
    
    def checkMove(self, move):
        
        """
            Check if the new position is inside the grid 

        """
        
        if self.checkBorders(move): 

            return True
        else:
            return False
    
    

    def pickmove(self,pos):
         
        """
            Selects a random allowed move in an adjacent position or the same position

        """

        move=[-1,-1]  
        while True:
            n = random.randint(1, 4) 

            # Top move
            if n == 1:
                move = [pos[0], pos[1]+1]

            # Bottom move
            elif n == 2:
                move = [pos[0], pos[1]-1]

            # Right move
            elif n == 3:
                new_y=pos[0]+1
                new_x=pos[1]
                move = [new_y, new_x]

            # Left move
            elif n == 4:
                move = [pos[0]-1, pos[1]]


            if self.checkMove(move):
                return move


   

    def build_obstacles(self, dim_agglomerato, random):

           
        """
            Selects the obstacles positions

        """


        # First position 
        x = random.randint(1, self.width-1)
        y = random.randint(1, self.height-1)

        pos = [0 for i in range(2)]
        pos[0]=y
        pos[1]=x

        # Add obstacle to the grid
         
        self.grid.append(tuple(pos))
        for i in range(int(dim_agglomerato-1)): #dim_agglomerato-1
            
            next_pos=self.pickmove(pos)

            #if we are using the matrix 
            #self.grid[next_pos[0]][next_pos[1]]=0

            #if we are using an array of obstacles

            self.grid.append(tuple(next_pos))
            
            pos=next_pos





    def build_grid(self, random):

        """
            Creates the grid obstacles

        """

        # Total number of cells in the grid

        cells = self.width * self.height

        # Obstacle cells

        obstacles = float(cells) * self.obstacle_percents
        
        # Agglomerate dimension

        dim_agglomerato = np.ceil(float(obstacles) * self.agglomeration_factor )

        # Number of agglomerates

        n_agglomerati = np.ceil(obstacles / dim_agglomerato)
        

        #if we are using the matrix 
        #self.grid[self.start_pos[0]][self.start_pos[1]]=1
      

        # Creates the agglomerates

        for i in range(int(n_agglomerati) - 1): 
            self.build_obstacles(int(dim_agglomerato), random)  

        last = obstacles - dim_agglomerato * (n_agglomerati - 1)

        self.build_obstacles(last, random)
      



    def get_start_pos(self):

        """
            Helper function to get the start position

        """
        return self.start_pos

    def get_goal_pos(self):

        """
            Helper function to get the goal position

        """
        return self.goal_pos


    def print_grid(self):

        """
            Prints the grid

        """
        for i in range(self.height-1):

            for j in range(self.width-1):

                print(self.grid[i][j])



    def get_weight_value(self, node, end):

        """
            Computes the weight between two nodes. If the nodes are the same, the weight is equal to 1.

        """


        if end==node:
            return 1
        else:
            return m.sqrt(m.pow(end[0] - node[0], 2) + m.pow(end[1] - node[1], 2))
    



    def check_agents_nodes(self, node, paths):
         
        """
            Checks if a node is present in an agent path.

        """

        found = False
        for i in range(len(paths)):
            
            if paths[i] == node:

                found = True
                break
        return found


    def initialise_positions(self, paths, random):
        """
            Initialises the positions of the start and end goal, making sure there are no collisions

        """
       
        
        start_y = random.randint(1,self.height - 1)
        start_x = random.randint(1,self.width - 1)
        
        start_pos = [start_y,start_x]
        
        
        # Checks if the start position selected corresponds to one of the agents start. In this case, it keeps selecting a new position

        while self.check_agents_nodes(start_pos, paths):
            start_y = random.randint(1,self.height - 1)
            start_x = random.randint(1,self.width - 1)
            start_pos = [start_y,start_x]

        goal_y = random.randint(1,self.height - 1)
        goal_x = random.randint(1,self.width - 1)

        goal_pos = [goal_y, goal_x]

        # Checks if the goal position selected is the start position or if it corresponds to one of the agents goals. 
        # In this case, we keep selecting a new position

        while start_pos == goal_pos or self.check_agents_nodes(goal_pos, paths):

            goal_y = random.randint(1,self.height - 1)
            goal_x = random.randint(1,self.width - 1)
            goal_pos = [goal_y, goal_x]
        
        return start_pos, goal_pos
    

    def substitute_values(self, value, x, y):

        """
        Replaces the values of the coordinates provided in the string grid

        """


        if value in self.grid:
           
            str_value = ' #  '
        else:
            str_value = ' . '

        if self.matrix_string[y][x] not in [' S ',' G ','C','1','2','3','4','5','6', '#']:
              
             
            self.matrix_string[y][x] = str_value
        


    def substitute_start_node(self, start_pos):

        """
            Sets the start position character at 'start_pos' in 'matrix_string'

        """
        self.matrix_string[start_pos[0]][start_pos[1]] = ' S '


    def substitute_goal_node(self, goal_pos):

        """
            Sets the start position character at 'goal_pos' in 'matrix_string'

        """
        
        
        self.matrix_string[goal_pos[0]][goal_pos[1]] = ' G '


    def replace_initial_values(self,start_pos, goal_pos):

        """
            Set the goal position to be displayed on the grid

        """

        self.substitute_start_node(start_pos)
        self.substitute_goal_node(goal_pos)

    def neighbors(self, pos: list[int, int]):

        """
        Finds the neighbors of a given node that are walkable, i.e. not obstacles and within the borders.

        """

        neighbors = []

        # South, north, west and east neighbors of the current node
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)]:    
           
        
            # Computing the x and y coordinates of the next node
            next_node = (pos[0] + new_position[0], pos[1] + new_position[1])
    
            # Checking if the next node is out of bounds. If it is, then step to the next neighbor
            if not self.checkBorders(next_node) or next_node in self.grid:
        
                continue

                                         
            # Checking if the next node is a wall
            
            neighbors.append(next_node)

        return neighbors

    
    def show_map(self, filename, start, goal):

        """
        Creates the grid as an image and shows it, then it saves the .png file.
    
        """

     

        # Define width and height of image
        width = self.width
        height = self.height

       
        # Scale of the image

        scale = 80

        # Create an image
        image = Image.new('RGB', (width * scale, height * scale),
                          (255, 255, 0))

        pixels = image.load()

        # Assigns a different colour for each different element on the grid: obstacles, agents
        
        colors = {

            '#': (115, 100, 215),  
            ' . ': (240, 240, 240),  
            ' S ': (36, 36, 36),  
            ' G ': (36, 36, 36),  
            'C' : (36, 36, 36),   
              
            '1': (96, 96, 96),   
            '2': (0, 204, 0),   
              
            '3': (255, 0, 255),  
            '4': (0, 128, 255),   
            '5': (81, 33, 107),    
            '6': (166, 166, 166),  
            '7': (255, 165, 0),   
            '8': (255, 0, 0),      
            '9': (0, 255, 255),    
        } 
            
        # Replace the start and goal positions as a value corresponding to the black color     
        self.replace_initial_values(start, goal)

        # Process the image and set the color of each pixel for every position
        for y in range(height):
            for x in range(width):

                pos = [0 for i in range(2)]
                pos[0]=y
                pos[1]=x

                self.substitute_values(pos, x, y)
                value= self.matrix_string[y][x] 
                if value not in colors :
                    continue
                for i in range(scale):
                    for j in range(scale):
                       
                        pixels[x * scale + i,
                               y * scale + j] = colors[self.matrix_string[y][x]]
   
        image.putpixel
        image.show()
        image.save(filename)
        
       


    def set_cell_value(self, pos, value):

        """
        Helper function to set the value of the cell at pos to the passed value  

        """
        
        self.matrix_string[pos[0]][pos[1]] = value
        