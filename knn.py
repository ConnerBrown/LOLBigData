import utils
import math
import operator
import random

            
#compute Distance
def KNNDistance(val1, val2, indexes):
    diffsSquared = []
    for index in indexes:
        diffsSquared.append((val1[index]-val2[index])**2)
    return math.sqrt(sum(diffsSquared))

#compute knn classification
def KNNClassification(training, K, value, indexes, classIndex):
    distances = []
    currIndex = 0
    for item in training:
        distances.append([currIndex, KNNDistance(item, value, indexes)])
        currIndex += 1
    distances.sort(key=operator.itemgetter(1))
    #Ignores own point that is in training (distance would be 0)
    #Note duplicate cars where removed in PA1
    #we will assume that no remaining instances have the same
    ##of cylinders, weight or acceleration
    distances = distances[1:K+1]
    counts = {}
    for d in distances:
        classs = training[d[0]][classIndex]
        if(classs in counts.keys()):
            counts[classs] = counts[classs] + 1
        else:
            counts[classs] = 1
    most = -1
    classification = -1
    for key in list(counts.keys()):
        if(counts[key] > most):
            most = counts[key]
            classification = key
    return classification

#preform KNN classification
def KNN(training, K, testing, indexes, classIndex):
    predictions = []
    for item in testing:
        classification = KNNClassification(training, K, item, indexes, classIndex)
        predictions.append(classification)
    
    return predictions


def main():
    print('reading table')
    table = utils.readTable("LoL_clean.csv")
    #remove header
    table = table[1:]
    print('converting columns to numeric')
    utils.convertColToInt(table, 16, False)
    utils.convertColToInt(table, 1, False)
    print('Normalizing gold diff and minute')
    utils.normalizeColumns(table, [1, 16])
    print('Shuffling and reducing')
    random.shuffle(table)
    table = table[0:int(len(table)/15)]
    print('     Instances: ', len(table))
    print('Stratisfying')
    bins = utils.stratifiedCrossValidationBins(5, table, 5)
    train1, test1 = utils.binsToSets(bins, 0)
    train2, test2 = utils.binsToSets(bins, 1)
    '''
    print('Preforming knn on train1')
    predictions = KNN(train1, 5, test1, [1, 16], 5)
    print('Computing accuracy')
    correct = 0
    for i in range(len(predictions)):
        if predictions[i] == test1[i][5]:
            correct += 1
    print("     accurracy: ", correct/len(predictions))
    '''
    
    print("Testing by the minute")
    print("     grouping test set")
    minutes, groups = utils.groupBy(test1, 1)
    
    accuracies = []
    for count in range(len(minutes)):
        print('-')
        predictions = KNN(train1, 5, groups[count], [1, 16], 5)
        correct = 0
        for i in range(len(predictions)):
            if predictions[i] == groups[count][i][5]:
                correct += 1
        accuracies.append([minutes[count], correct/len(predictions), correct, len(predictions)])

    print("Sorting accuracies")
    accuracies.sort(key=lambda x: x[0])
    count = 0
    for item in accuracies:
        print('Minute: ', count)
        print('     Accuracy: ', item[1])
        print('     Correct: ', item[2])
        print('     Instances: ', item[3])
        print()
        count+=1
    

if __name__ == "__main__":
    main()