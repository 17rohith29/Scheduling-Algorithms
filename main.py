import copy # for deepcopy
import itertools # for getting all permutations

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

def solveBasic(lst): # list is sorted based of begin time
    time = 0
    number_processed = 0
    previous_processed = None
    last_begin_time = lst[len(lst) - 1][0]
    to_process = [] # lst that will store all the elements that we need to proecess

    while time < last_begin_time:
        if previous_processed is None:
            previous_processed = time
            while lst[0][0] == time:
                to_process.append(lst.pop(0))
        else:
            while lst[0][0] <= time and lst[0][0] >= previous_processed:
                to_process.append(lst.pop(0))
            previous_processed = time
            
        processedItem = solveAlgo1(to_process)
        number_processed += 1
        # update time
        time += processedItem[2]
        # removing all in processedItem that has time > deadline
        temp = []
        for i in to_process:
            if time < i[1]:
                temp.append(i)
        to_process = temp

    # now we must finish processeing the to_process
    while len(to_process) != 0:
        processedItem = solveAlgo1(to_process)
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

    ans = solveNaieve(copy.deepcopy(allProcesses))
    # ans = solveBasic(copy.deepcopy(allProcesses))
    print("The Best set of jobs has number {}".format(ans))
main()
