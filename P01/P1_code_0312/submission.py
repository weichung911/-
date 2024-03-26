import json
import os
import sys
import graderUtil
from itertools import product
import random

# a dict stores the final result
task_result = {
    "ini_cost": -1,
    "best_cost": -1,
    "locations": []
} 

#######################################################################
# read task file content
task_file = sys.argv[1]
task_content = graderUtil.load_task_file(task_file)
if task_content:
    print(task_content)
# BEGIN_YOUR_CODE
# split data 
search_type = task_content[0]

grids = list(map(int, task_content[1].split(",")))

playgroungs_info = task_content[2].split('|')
playgroungs_nums = playgroungs_info[0]
playgroungs_info = playgroungs_info[1:]
playgroungs_info_list = [list(map(int, coord.split(","))) for coord in playgroungs_info]

restroom_info = task_content[3].split('|')
restroom_num = restroom_info[0]

restarts_time = -1
if search_type == '1' :
    restroom_info = -1
    try:
        restarts_time = (grids[0]*grids[1] - (int(playgroungs_nums)+3))*int(restroom_num)
        if len(task_content) >= 5:
            restarts_time = task_content[4]
    except NameError:
        pass  # 如果 task_content 未定义，忽略异常
else:
    restroom_info = restroom_info[1:]
    restroom_info_list = [list(map(int, coord.split(","))) for coord in restroom_info]
#^^^^
    
## function
def distence(restroom,playground):
    dis_x = abs(restroom[0]-playground[0])
    dis_y = abs(restroom[1]-playground[1])
    return dis_x + dis_y

def cost(restroom_list):
    cost = 0
    tmp = []
    for i in playgroungs_info_list:
        for restroom in restroom_list:
            tmp.append(distence(restroom,i))
        cost += min(tmp)
        tmp = []
    return cost

def cartesian_product(lists):
    return [list(items) for items in product(*lists)]

def remove_duplicate_lists(lists):
    result = []
    seen = []
    for sublist in lists:
        for i in sublist:
            if i not in seen:
                seen.append(i)
            else:
                break 
        if len(sublist) == len(seen):
            result.append(sublist)
        seen = []
    return result

def move(restroom):
    tmp = []
    tmp.append(restroom)
    right = [restroom[0]+1]+[restroom[1]]
    if [0,0]<= right and right <= grids:
        if right not in playgroungs_info_list:
            tmp.append(right)
    left = [restroom[0]-1]+[restroom[1]]
    if [0,0]<= left and left <= grids:
        if left not in playgroungs_info_list:
            tmp.append(left)
    up = [restroom[0]]+[restroom[1]+1]
    if [0,0]<= up and up <= grids:
        if up not in playgroungs_info_list:
            tmp.append(up)
    down = [restroom[0]]+[restroom[1]-1]
    if [0,0]<= down and down <= grids:
        if down not in playgroungs_info_list:
            tmp.append(down)
    return tmp

def generate_neighbors(restroom_list):
    tmp = []
    for i in restroom_list:
        tmp.append(move(i))
    return cartesian_product(tmp)

def hill_climbing(cost, restroom_list):
    ans = restroom_list
    while True:
        neighbors = generate_neighbors(ans)

        neighbors = remove_duplicate_lists(neighbors)

        best_neighbor = min(neighbors, key=cost)

        if cost(best_neighbor) >= cost(ans):
            return ans
        ans = best_neighbor

def generate_restroom_list(length, restarts_time):
    random_list = []
    restroom_list = []
    for _ in range(restarts_time):
        while True:
            random_list = []
            for _ in range(length):
                while True:
                    x = random.randint(0, grids[0])
                    y = random.randint(0, grids[1])
                    if [x,y] not in playgroungs_info_list and [x,y] not in random_list:
                        random_list.append([x, y])
                        break
            if random_list not in restroom_list:
                restroom_list.append(random_list)
                break
    return restroom_list

def random_restart_hill_climbing(cost, restroom_nums, restarts_time):
    tmp = []
    restroom_list = generate_restroom_list(restroom_nums,restarts_time)

    for i in range(restarts_time):
        ans = hill_climbing(cost,restroom_list[i])
        tmp.append(ans)
    
    return min(tmp, key=cost)
# ^^^^^

## main

locations = [[0,1],[1,2]]
if search_type == '0':
    task_result["ini_cost"] = cost(restroom_info_list)
    locations = hill_climbing(cost,restroom_info_list)
    best_cost = cost(locations)

if search_type == '1':
    locations = random_restart_hill_climbing(cost,int(restroom_num),int(restarts_time))
    best_cost = cost(locations)

task_result["best_cost"] = best_cost
task_result["locations"] = locations

##^^^^^^


# END_YOUR_CODE
#######################################################################

# output your final result
print(json.dumps(task_result))