import utils
import math
import operator
import random
import matplotlib.pyplot as plt
            
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

#plots accuracies by minute
def plot(accuracies, figname):
    minute = utils.getColumn(accuracies, 0)
    accuracy = utils.getColumn(accuracies, 1)
    plt.figure()
    plt.scatter(minute, accuracy)
    plt.title("KNN Accuracy Vs. Time")
    plt.xlabel('Minute')
    plt.ylabel('Accuracy')
    plt.savefig(figname)

def main():
    print('reading table')
    table = utils.readTable("LoL_clean_manual.csv")
    #remove header
    table = table[1:]
    print('converting columns to numeric')
    utils.convertColToInt(table, 16, False)
    utils.convertColToInt(table, 1, False)
    #make histogram
    minutes = utils.getColumn(table, 1)
    plt.figure()
    plt.hist(minutes, bins=max(minutes), histtype='step')
    plt.title("Minute Histogram")
    plt.xlabel("Minute")
    plt.ylabel("Games")
    plt.savefig("minutes_histogram.png")
    print('Normalizing gold diff and minute')
    utils.normalizeColumns(table, [1, 16])
    print('Shuffling and reducing')
    random.shuffle(table)
        #use 1/15 the total data set
    table = table[0:int(len(table)/15)]
    print('     Instances: ', len(table))
    print('Stratisfying')
    bins = utils.stratifiedCrossValidationBins(5, table, 1)
    train1, test1 = utils.binsToSets(bins, 0)
    
    print("Testing by the minute, this will take some time")
    print("     grouping test set")
    minutes, groups = utils.groupBy(test1, 1)
    print("     running classifier")
    accuracies = []
    overall_correct = 0
    total_instance = 0
    for count in range(len(minutes)):
        predictions = KNN(train1, 5, groups[count], [1, 16], 5)
        correct = 0
        total_instance += len(predictions)
        for i in range(len(predictions)):
            if predictions[i] == groups[count][i][5]:
                correct += 1
                overall_correct += 1
        accuracies.append([minutes[count], correct/len(predictions), correct, len(predictions)])

    print("Sorting accuracies")
    accuracies.sort(key=lambda x: x[0])
    count = 0
    for item in accuracies:
        print('Minute: ', round(item[0], 3))
        print('     Accuracy: ', item[1])
        print('     Correct: ', item[2])
        print('     Instances: ', item[3])
        print()
        count+=1
    print("Overall Accurracy: ", overall_correct/total_instance)
    print("Instances: ", total_instance)
    print("Correct: ", overall_correct)
    #plot(accuracies, "KNN_accuracies.png")

if __name__ == "__main__":
    main()