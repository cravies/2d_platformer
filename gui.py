#gui to edit game levels

from tkinter import *
import numpy as np

test_matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])

class Table:
    
    def __init__(self,window,matrix):
        self.window = window
        self.matrix = matrix
        [self.columns,self.rows] = np.shape(matrix)
        self.spacing = 20
        self.width = self.columns * self.spacing
        self.height = self.rows * self.spacing

        #create entries using list comprehension
        self.entries = [[self.make_entry(i,j) for j in range(self.columns)] for i in range(self.rows)]
        
        #create "save" button
        save = Button(window, text="Save level", command=self.save_matrix)
        save.grid(row=self.rows+1,column=0)

    def make_entry(self,i,j):
        my_entry = Entry(self.window, width=self.spacing, fg='blue', font=('Arial','16','bold'))
        my_entry.grid(row=i,column=j)
        my_entry.insert(END,self.matrix[i,j])
        return my_entry

    def save_matrix(self):
        self.result = np.zeros([self.rows,self.columns])
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.entries[i][j])
                self.result[i,j] = self.entries[i][j].get()
        print(self.result)
        np.savetxt("level.csv", self.result, delimiter=',')


window = Tk()
mytable = Table(window,test_matrix)
window.mainloop()
