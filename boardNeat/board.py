import random

import numpy as np

# reverse a matrix 


class Board():
    def __init__(self):
        #print('in init')
        self.commands = {'up':self.up, 'down':self.down,'left':self.left,'right':self.right}
        self.history = []
        self.new_game()

    def new_game(self):
        matrix = []
        for i in range(4):
            matrix.append([0]*4)
        self.matrix = matrix
        self.temp_matrix = matrix
        self.add_two()
        self.add_two()
        self.history.append(self.matrix)

    def add_two(self):
        if self.game_state() == 2:
            a = random.randint(0, 3)
            b = random.randint(0, 3)
            while self.matrix[a][b] != 0:
                a = random.randint(0, 3)
                b = random.randint(0, 3)
            self.matrix[a][b] = 2
            #self.history.append(self.matrix)

    def numZeros(self):
        num = 0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    num += 1
        return num

    def numNum(self,num):
        count = 0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == num:
                    count += 1
        return count
    def symCount(self):
        count = 0
        num_zeros = 0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[j][i]:
                    if self.matrix[i][j] != 0:
                        if i != j:
                        # print('new match')
                        # print('i is :')
                        # print(i)
                        # print('j is :')
                        # print(j)
                            count += 1
                    else:
                        num_zeros += 1
                if self.matrix[i][j] == self.matrix[3-j][3-i]:
                    if self.matrix[i][j] != 0:
                        # print('new match')
                        # print('i is :')
                        # print(i)
                        # print('j is :')
                        # print(j)
                        if i != 3-j:
                            count += 1
                    else:
                        num_zeros += 1
        return count/2

    def game_state(self):
        mat = self.matrix
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == 2048:
                    # win
                    return 1
        # check for any zero entries
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == 0:
                    # not over
                    return 2
        # check for same cells that touch each other
        for i in range(len(mat)-1):
            # intentionally reduced to check the row on the right and below
            # more elegant to use exceptions but most likely this will be their solution
            for j in range(len(mat[0])-1):
                if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                    #not over
                    return 2
        for k in range(len(mat)-1):  # to check the left/right entries on the last row
            if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
                #not over
                return 2
        for j in range(len(mat)-1):  # check up/down entries on last column
            if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
                #not over
                return 2
        #over 
        return 0
    def reverse(self):
        mat = self.matrix
        new = []
        for i in range(len(mat)):
            new.append([])
            for j in range(len(mat[0])):
                new[i].append(mat[i][len(mat[0])-j-1])    
        self.matrix = new

    def transpose(self):
        mat = self.matrix
        new = []
        for i in range(len(mat[0])):
            new.append([])
            for j in range(len(mat)):
                new[i].append(mat[j][i])
        self.matrix = new

    def cover_up(self):
        self.temp_matrix = []
        mat = self.matrix
        for j in range(4):
            partial_new = []
            for i in range(4):
                partial_new.append(0)
            self.temp_matrix.append(partial_new)
        done = False
        for i in range(4):
            count = 0
            for j in range(4):
                if mat[i][j] != 0:
                    self.temp_matrix[i][count] = mat[i][j]
                    if j != count:
                        done = True
                    count += 1
        self.matrix = self.temp_matrix
        return done

    def merge(self, done):
        mat = self.matrix
        for i in range(4):
            for j in range(3):
                if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                    mat[i][j] *= 2
                    mat[i][j+1] = 0
                    done = True
        self.matrix = mat
        return done


    def up(self):
        
        self.transpose()
        done = self.cover_up()
        done = self.merge(done)
        self.cover_up()
        self.transpose()
        if done:
            self.add_two()
            self.history.append(self.matrix)
        return done

    def down(self):
        
        self.transpose()
        self.reverse()
        done = self.cover_up()
        done = self.merge(done)
        self.cover_up()
        self.reverse()
        self.transpose()
        if done:
            self.add_two()
            self.history.append(self.matrix)
        return done

    def left(self):
        
        done = self.cover_up()
        done = self.merge(done)
        self.cover_up()
        if done:
            self.add_two()
            self.history.append(self.matrix)
        return  done    

    def right(self):
        
        self.reverse()
        done = self.cover_up()
        done = self.merge(done)
        self.cover_up()
        self.reverse()
        if done:
            self.add_two()
            self.history.append(self.matrix)

        return  done

    def follow_instr(self,inst):
        for i in range(len(inst)):
            print('in instructions')
            print(inst[i])
            self.commands[inst[i]]()



    def toString(self):
        list_as_array = np.array(self.matrix)
        print(list_as_array)

    def printHistory(self):
    	for i in range(len(self.history)):
    	    print(np.array(self.history[i]))



