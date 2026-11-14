import musicpy as mp 
import random

#data = [random.random() for _ in range(10)]
data = [161.721, 161.7105, 161.7105, 161.7105, 161.7105, 161.7105, 161.7105, 161.711, 161.7146, 161.7152, 161.7255, 161.715, 161.7205, 161.7215, 161.7296, 161.7365, 161.7225, 161.7225, 161.7223, 161.7223, 161.7224, 161.7248, 161.7246, 161.7246, 161.7246, 161.7316, 161.7311, 161.7311, 161.7301, 161.7303]

maxi = max(data)
mini = min(data)
diff = maxi-mini

normalizedData = list(map(lambda x : (x-mini)/diff, data))

keykey = 0

options = [1,2,3,4,5,6,7]
def calcWeights(percentageDiff):
    weights = [1,2,2.5,3,1,3,2.5,2,1]
    if percentageDiff < 0:
        for i in range(4):
            weights[i] = weights[i]*(1-percentageDiff*2)
    elif percentageDiff > 0:
        for i in range(4):
            weights[i + 5] *= (1+percentageDiff*2)
    return weights

def createSequence(start,length):
    sequence = [start]
    for i in range(length-1):
        percentageDiff = (normalizedData[i]-normalizedData[i+1])
        weights = calcWeights(percentageDiff)
        nextChoice = random.choices([j for j in range(7)], weights=chain[sequence[i]-1])[0]
        nextNote = sequence[i] + nextChoice
        if nextNote > 7:
            nextNote -= 7
        sequence.append(nextNote)
    print(sequence)

print(data[0], calcWeights(0))
for i in range(len(data)-1):
    percentageDiff = (normalizedData[i+1]-normalizedData[i])
    print(data[i+1], calcWeights(percentageDiff))
