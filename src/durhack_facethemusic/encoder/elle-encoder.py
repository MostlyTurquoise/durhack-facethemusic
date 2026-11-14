import musicpy as mp 
import random

data = [random.random() for _ in range(10)]

max = max(data)
min = min(data)

keykey = 0

options = [1,2,3,4,5,6,7]

chain = [
    [0,1,0,0,0,0,0],
    [0,0,1,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,1,0,0],
    [0,0,0,0,0,1,0],
    [0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0]
]

def createSequence(start,length):
    sequence = [start]
    for i in range(length-1):
        nextChoice = random.choices([j for j in range(7)], weights=chain[sequence[i]])[0]
        sequence.append(nextChoice)
    print(sequence)

createSequence(0,9)
