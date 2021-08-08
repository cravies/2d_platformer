#gui to edit game levels
"""
key: 
    0 = nothing
    1 = gravel
    2 = dirt
    3 = grass
"""

from tkinter import *
import numpy as np

screen_width = 1400
screen_height = 800
tile_size = 50

test_matrix = np.zeros([int(screen_height/tile_size), int(screen_width/tile_size)],dtype='int')

class Table:
    
    def __init__(self,window,matrix):
        self.window = window
        self.matrix = matrix
        [self.rows,self.columns] = np.shape(matrix)
        self.spacing = 5
        self.width = self.columns * self.spacing
        self.height = self.rows * self.spacing
        self.name = "mymatrix.csv"

        #create entries using list comprehension
        self.entries = [[self.make_entry(i,j) for j in range(self.columns)] for i in range(self.rows)]
        
        #create "save" button
        self.save = Button(window, text="Save file", command=self.save_matrix, font=('Arial', '16', 'bold'))
        self.save.grid(row=self.rows+1,column=0,columnspan=3)

        #set level matrix name
        self.file_name = Entry(self.window, width=self.spacing * 3, fg='red', font=('Arial', '16', 'bold'))
        self.file_name.grid(row=self.rows+1,column=3,columnspan=3)
        self.file_name.insert(END,"file name")

        #colour grid as if it were the level
        self.grid_colour = Button(window, text="Colour grid", command=self.colour_grid, font=('Arial', '16', 'bold'))
        self.grid_colour.grid(row=self.rows+1, column=6, columnspan=6)

    def make_entry(self,i,j):
        my_entry = Entry(self.window, width=self.spacing, fg='blue', font=('Arial','16','bold'))
        my_entry.grid(row=i,column=j)
        my_entry.insert(END,self.matrix[i,j])
        return my_entry

    def colour_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                entry = int(self.entries[i][j].get())
                print(entry)
                if (entry==0):
                    print("its zero")
                elif (entry==1):
                    self.entries[i][j]['bg'] = "GRAY"
                elif (entry==2):
                    self.entries[i][j]['bg'] = "BROWN"
                elif (entry==3):
                    self.entries[i][j]['bg'] = "GREEN"
                else:
                    print("ERROR: entry should be 0,1,2 or 3")

    def save_matrix(self):
        #get matrix name from file_name field
        self.name = self.file_name.get()
        self.result = np.zeros([self.rows,self.columns])
        #update matrix from table entries
        for i in range(self.rows):
            for j in range(self.columns):
                self.result[i,j] = self.entries[i][j].get()
        print(self.result)
        #save as a csv file
        np.savetxt(self.name, self.result, delimiter=',')


window = Tk()
mytable = Table(window,test_matrix)
window.mainloop()
