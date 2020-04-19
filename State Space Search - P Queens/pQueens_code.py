
# coding: utf-8

# In[5]:


import numpy as np
import time as t
from heapq import nlargest
st = t.time()

input_lines = np.asarray([input_line.rstrip('\n') for input_line in open('input.txt')])
n = input_lines[0].astype(int)
p = input_lines[1].astype(int)
s = input_lines[2].astype(int)

activity_pt_grid = np.zeros((n,n))
city_area = np.zeros((n,n))

for each_coordinate in range(3,input_lines.size):
    coordinate = input_lines[each_coordinate].split(',')
    x = int(coordinate[0])
    y = int(coordinate[1])
    activity_pt_grid[x][y] = activity_pt_grid[x][y] + 1
    
col_max = activity_pt_grid.max(0)
col_sum = np.zeros(n)
for i in range(0,n):
    for k in range(i,n):
        col_sum[i] = col_sum[i]+ col_max[k]

heuristic_check = np.zeros((p+1,n+1))
for i in range(0,n+1):
    for k in range(0,p+1):
        heuristic_check[k][i]=sum(nlargest(k,col_max[i:]))      
        
def place_officer(city_area, current, n,p):
    global g 
    global maximum 
    if p==0:
        maintain_state(city_area)
        return
    if(n-current<p):
        return 
    if(n-current>p):
        if(g+heuristic_check[p][current+1]>maximum):
            place_officer(city_area,current+1,n,p)
    for i in range(n):
        if check_conflict(city_area, i, current, n):
            city_area[i][current] = 1
            g = g + activity_pt_grid[i][current]
            if(g+heuristic_check[p-1][current+1]>maximum):
                place_officer(city_area,current+1,n,p-1)
            city_area[i][current] = 0
            g = g - activity_pt_grid[i][current]

def maintain_state(city_area):
    global maximised_activity 
    global maximum 
    x = np.where(city_area==1)
    y = np.asarray(x).T
    for i in range(p):
        M=y[i][0]
        N=y[i][1]
        maximised_activity = activity_pt_grid[M][N] + maximised_activity
    if(maximised_activity>maximum):
        maximum = maximised_activity
    maximised_activity=0

def check_conflict(city_area, i, current, n):
    l, k = i, current
    while k >= 0 and l >= 0:
        if city_area[l][k] == 1:
            return False
        k=k-1
        l=l-1
    
    o, p = i ,current
    while p>=0 and o < n:
        if city_area[o][p] == 1:
            return False
        p=p-1
        o=o+1

    for k in range(current):
        if city_area[i][k] == 1:
            return False  
    return True

g = 0 
maximised_activity = 0 
maximum = 0 
place_officer(city_area, 0, n, p)
maximum = int(maximum)


with open('output.txt','w') as f:
    f.write(str(maximum))

