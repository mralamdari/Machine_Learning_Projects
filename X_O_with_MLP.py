import tkinter  # This module helps us to create the GUI of the programimport tkinter  # This module helps us to create the GUI of the program
import numpy as np
from tkinter import messagebox



class Artificial_Neural_Network:
    def __init__(self, size):
        # +1 for bias node in all layers except output layer ############### this is a place to save bias
        self.sizes = [item + 1 for item in size[:-1]] + [size[-1]]
        self.number_of_layers = len(self.sizes)
        self.activation = [np.ones((x, 1)) for x in self.sizes]
        self.weight = [np.random.randn(x, y) for x, y in zip(self.sizes[1:], self.sizes[:-1])]
        self.cost = [np.zeros((x, y)) for x, y in zip(self.sizes[1:], self.sizes[:-1])]

    @staticmethod
    def sigmoid(x):
        return np.tanh(x)

    @staticmethod
    def prime_sigmoid(y):
        return 1.0 - y ** 2

    def update(self, inputs):
        tem = self.sigmoid(inputs)
        self.activation[0] = tem.reshape(len(tem), 1)
        for i in range(len(self.weight)):
            self.activation[i + 1] = self.sigmoid(np.dot(self.weight[i], self.activation[i]))
        return self.activation[-1]

    def backpropagate(self, targets, alpha, M):
        deltas = list()
        output_err = targets - self.activation[-1]
        delta = self.prime_sigmoid(self.activation[-1]) * output_err
        deltas.append(delta)
        for i in range(1, len(self.weight) + 1):
            error = np.dot(np.transpose(self.weight[-i]), delta)
            delta = self.prime_sigmoid(self.activation[-i - 1]) * error
            deltas.append(np.transpose(delta))

        for j in range(1, len(self.weight) + 1):
            change = np.transpose(np.dot(self.activation[-j - 1], deltas[j - 1]))
            self.weight[-j] += alpha * change + M * self.cost[-j]
            self.cost[-j] = change
            

        return sum(0.5 * (targets - self.activation[-1]) ** 2)

    def train(self, patterns, iterations=2000, alpha=0.5, M=0.1):
        # alpha: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[:-2] + [1]  # to add bias
                targets = p[-1]
                self.update(inputs)
                error = error + self.backpropagate(targets, alpha, M)
            if i % 100 == 0:
                print('error %-.5f' % error)
        return self.activation[-2]

class SecondPage:
    
    def __init__(self):
        pass
    
    def get_data(self, Gotten_Array, letter):
        my_arr = [-1 if i == 0 else i for i in Gotten_Array] #[w1,...w25] , we add b at end when we use 
        my_arr.append(1)  
        if letter == "":  # no written data === > test
            self.MLP(Gotten_Array)
        elif letter.upper() == "X":  # Learn X
            my_arr.append(1)# [w1,...w25,b,y]
            with open("./Learnings_database.csv", "a+") as Learnings_database:
                Learnings_database.write(",".join(str(i) for i in my_arr) + "\n")
            messagebox.showwarning("Successful", "We Stored Your Sample!!!")

        elif letter.upper() == "O":  # Learn O
            my_arr.append(-1)# [w1,...w25,b,y]
            with open("./Learnings_database.csv", "a+") as Learnings_database:
                Learnings_database.write(",".join(str(i) for i in my_arr) + "\n")
            messagebox.showwarning("Successful", "We Stored Your Sample!!!")

        else:
            # Show Error message
            messagebox.showwarning("Fail", "Sorry, You must enter only on letter")
        
    
    def MLP(self, data):

        sep_learned_data = []
        with open("Formula.csv") as Formula:  # this file saves created formulas numbers
            my_formula = Formula.read()

        if len(my_formula) == 0:  # don't have a formula so create it
            with open("./Learnings_database.csv") as Learnings_database:  # this file saves created Examples
                learned_data = Learnings_database.readlines()
            index=0
            for i in learned_data:  # create usable data
                TEMP = [float(z) for z in i.split(',')[:-1]]
                TEMP.append(1 if i.split(',')[-1] == "1\n" else -1)
                sep_learned_data.append(TEMP)
                index += 1
            network = Artificial_Neural_Network([24, 16, 32, 26, 1])
            
            trained_weights = network.train(sep_learned_data)

            with open("./Formula.csv", "a+") as Formula:
                Formula.write(",".join(str(i[0]) for i in trained_weights))
            return trained_weights       
        
        else:
            summ = 0
            # use my_formula to test your roject
            for i, j in zip(my_formula.split(',')[:-1], data):
                summ += float(i) * float(j)
            print(summ)    
            if summ > 0:
                messagebox.askretrycancel("Successful", "It IS  X")
            elif summ < 0:
                messagebox.askretrycancel("Successful", "It IS  O")
            else:
                messagebox.askretrycancel("Fail", "Sorry couldn\'t detect it ")

second_page_window = tkinter.Tk()
second_page_window.title("Character Detector Page")
# We Define the variables we want to get from the gui
GLetter = tkinter.StringVar()
v_1, v_2, v_3, v_4, v_5 = tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()
v_6, v_7, v_8, v_9, v_10 = tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()
v_11, v_12, v_13, v_14, v_15 = tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()
v_16, v_17, v_18, v_19, v_20 = tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()
v_21, v_22, v_23, v_24, v_25 = tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()

# # # Define all variables in a list to iterate throw them easily
arr = [v_1, v_2, v_3, v_4, v_5, v_6, v_7, v_8, v_9, v_10, v_11, v_12, v_13, v_14, v_15, v_16, v_17, v_18, v_19, v_20,v_21, v_22, v_23, v_24, v_25]
index = 0
for i in range(1, 6):
    for j in range(1, 6):
        tkinter.Checkbutton(second_page_window, text="", variable=arr[index], height=2, width=2).grid(row=i, column=j)
        index += 1

l_1 = tkinter.Label(second_page_window, text="Please select your pattern", background="gold")
l_1.grid(row=0, column=1, columnspan=5)

e_1 = tkinter.Entry(second_page_window, text="", textvariable=GLetter, width=20, background="pink")
e_1.grid(row=6, column=1, columnspan=2)

b_1 = tkinter.Button(second_page_window, text="Start", command=lambda:SecondPage().get_data([i.get() for i in arr], GLetter.get()), width=20, background="blue")
b_1.grid(row=6, column=4, columnspan=2)

b_1 = tkinter.Button(second_page_window, text="Exit", command=second_page_window.quit, width=45, background="red")
b_1.grid(row=7, column=1, columnspan=5)

second_page_window.mainloop()