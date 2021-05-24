import numpy as np

from board import Board

def find_index(array):
    s = np.array(array)
    sort_index = np.argsort(s)
    return sort_index

def pick_two(array):
    max_value = max(array)
    max_index = array.index(max_value)
    cpy_arry = [array[i] for i in range(len(array))]
    cpy_arry.sort()
    nex_value = cpy_arry[-2]
    nex_index = array.index(nex_value)

    return max_index, nex_index

a = Board()

a.matrix = [[1,2,3,4],[2,1,3,3],[2,3,0,0],[2,1,3,5]]
b = Board()
b.matrix =[[1,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]]
b.matrix =[[1,1,0,1],[1,0,0,1],[0,0,0,1],[0,1,1,0]]

b.toString()
print(b.symCount())
# arr = [1,2,-3,0,.5]

# arr2 = [.5,.3,-.1,-3,0]


# a,b = pick_two(arr)

# c,d = pick_two(arr2)
# print(a)
# print(b)
# print(c)
# print(d)

# print(find_index(arr))
# print(find_index(arr2))


