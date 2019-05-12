import copy # for deepcopy
import itertools # for getting all permutations
import time
def findNumberComplete(lst):
    if len(lst) == 0:
        return 0

    time = lst[0][0] # begin time of first element
    res = 0

    for i in lst:
        curB, curD, curP = i

        if time + curP <= curD: # can complete the job in time
            res += 1
            time += curP

    return res
        
def solveNaieve(lst): # lst is sorted
    allPer = list(itertools.permutations(lst))
    ans = 0

    for i in allPer:
        maxNo = findNumberComplete(i)
        ans = max(ans, maxNo)

    return ans

# greedy algorithm that takes the element with the shortest time
def solveAlgo1(to_process):
    # always take the element with shortest time
    return to_process[0]
    
# greedy algorithm that takes the element with the first deadline 
def solveAlgo2(to_process):
    temp = None
    for i in to_process:
        if temp is None or temp[1] > i[1]:
            temp = i
    return temp

# best algorithm
def solveAlgo3(to_process, time): # sorting O(nlogn) + O(n^2) = O(n^2)
    # sort by deadline
    to_process = sorted(to_process, key = lambda x: x[1])
    res = 0 #index that we need to return 
    mn = 0
    for i in range(0, len(to_process)):
        cnt = 0
        t = time
        for j in range(i, len(to_process)):
            cur = to_process[j]
            if time + cur[2] <= cur[1]:
                cnt += 1
                time += cur[2]
            else:
                if cnt > mn:
                    mn = cnt
                    res = i
    return to_process[res]

def solveAlgo4(to_process, time): # O(nlogn))
    # sort by deadline
    to_process = sorted(to_process, key = lambda x: x[1])
    res = 0 #index that we need to return 
    cnt = 0
    start, end = 0, 0
    while start < len(to_process):
        count = 0
        while end < len(to_process):
            cur = to_process[end]
            if time + cur[2] <= cur[1]:
                time += cur[2]
                count += 1
                end += 1
            else:
                break
        if count < cnt:
            cnt = count
            res = start
        time -= to_process[start][2] # removing the processing time of start
        start += 1
    return to_process[res]

def solveBasic(lst): # list is sorted based of begin time
    time = 0
    number_processed = 0
    previous_processed = None
    last_begin_time = lst[len(lst) - 1][0]
    to_process = [] # lst that will store all the elements that we need to proecess

    while time < last_begin_time and len(to_process) != 0:
        if previous_processed is None:
            previous_processed = time
            while lst[0][0] == time:
                to_process.append(lst.pop(0))
        else:
            while lst[0][0] <= time and lst[0][0] >= previous_processed and lst[0][1] > time:
                to_process.append(lst.pop(0))
            previous_processed = time
        
        if len(to_process) == 0:
            break
        else:
            processedItem = solveAlgo4(to_process, time) # returns the processed item
            number_processed += 1
            # update time
            time += processedItem[2]
            # removing all in processedItem that has time > deadline
            temp = []
            for i in to_process:
                if time < i[1]: # remove if already past deadline (or add if not here)
                    temp.append(i)
            to_process = temp

    # now we must finish processeing the to_process
    while len(to_process) != 0:
        processedItem = solveAlgo3(to_process, time)
        number_processed += 1
        # update time
        time += processedItem[2]
        # removing all in processedItem that has time > deadline
        temp = []
        for i in to_process:
            if time < i[1]:
                temp.append(i)
        to_process = temp

    return number_processed


def main(): # this deals with all the preprocessing required to run code.
    n = int(input()) # number of processes
    allProcesses = []
    for i in range(n):
        b, d, p = list(map(int, input().split(' ')))
        # b is begin time, d is due date and p is processing time
        allProcesses.append([b, d, p])
    
    # Now sorting based on begin time.
    # This is done cause we want to simulate a streaming algorithm
    # Every time we go through a loop we can have a iterator that
    # keeps track of "time" and can be enqued when begin time is met
    allProcesses = sorted(allProcesses, key = lambda x: x[0])
    
    s = time.time()
    ans = solveBasic(copy.deepcopy(allProcesses))
    #ans = solveNaieve(copy.deepcopy(allProcesses))
    e = time.time()
    #ans = solveBasic(copy.deepcopy(allProcesses))
    print("time taken is {}".format(e - s))

main()
