import pandas as pd
import utils
import random
import matplotlib.pyplot as plt

def calculate_priors(data, index, classes):
    counts = {}
    total = 0
    for label in classes:
        counts[label] = 0
    for instance in data:
        counts[instance[index]] += 1
        total += 1
    probabilities = []
    for label in classes:
        probabilities.append(counts[label] / total)
    return probabilities

def calculate_posteriors(data, attributeIndex, attribute, classIndex, classLabels):
    conditionalCounts = {}
    counts = {}
    for label in classLabels:
        counts[label] = 0
        conditionalCounts[label] = 0
    for instance in data:
        counts[instance[classIndex]] += 1
        if instance[attributeIndex] == attribute:
            conditionalCounts[instance[classIndex]] += 1
    probabilities = []
    for label in classLabels:
        if counts[label] == 0:
            probabilities.append(0)
        else:
            probabilities.append(conditionalCounts[label] / counts[label])
    return probabilities

def naive_bayes_classify(train, classIndex, classLabels, test):
    classProbabilities = []
    for val in classLabels:
        classProbabilities.append(0)
    priors = calculate_priors(train, classIndex, classLabels)
    for i in range(len(classProbabilities)):
        classProbabilities[i] += priors[i]
    for i in range(len(test)):
        if i == classIndex:
            continue
        else:
            attribute = test[i]
            posteriors = calculate_posteriors(train, i, attribute, classIndex, classLabels)
            for i in range(len(posteriors)):
                classProbabilities[i] *= posteriors[i]
    maxP = 0
    index = 0
    for i in range(len(classProbabilities)):
        if classProbabilities[i] > maxP:
            maxP = classProbabilities[i]
            index = i
    return classLabels[index]

def plot(accuracies):
    minute = utils.getColumn(accuracies, 0)
    accuracy = utils.getColumn(accuracies, 1)
    plt.figure()
    plt.scatter(minute, accuracy)
    plt.title("Naive Bayes Accuracy Vs. Time")
    plt.xlabel('Minute')
    plt.ylabel('Accuracy')
    plt.show()


def main():
    df = pd.read_csv("LoL_clean_manual.csv")
    df = df[["Minute", "gamelength", "bResult", "bKills", "bTowers", "bInhibs", "bBarons", "bDragons", "bHeralds", "rKills", "rTowers", "rInhibs", "rBarons", "rDragons", "rHeralds"]]
    data = df.values.tolist()
    random.shuffle(data)
    bins = utils.stratifiedCrossValidationBins(5, data[:int(len(data)/10)], 0)
    test = bins[0]
    train = []
    for bin in bins[1:]:
        train += bin


    print("Testing by the minute, this will take some time")
    print("     grouping test set")
    minutes, groups = utils.groupBy(test, 0)
    print("     running classifier")
    accuracies = []
    overall_correct = 0
    total_instance = 0

    for count in range(len(minutes)):
        predictions = [naive_bayes_classify(train, 2, [0,1], instance) for instance in groups[count]]
        correct = 0
        total_instance += len(predictions)
        for i in range(len(predictions)):
            if predictions[i] == groups[count][i][2]:
                correct += 1
                overall_correct += 1
        accuracies.append([minutes[count], correct/len(predictions), correct, len(predictions)])



    print("Sorting accuracies")
    accuracies.sort(key=lambda x: x[0])
    count = 0
    for item in accuracies:
        print('Minute: ', item[0])
        print('     Accuracy: ', item[1])
        print('     Correct: ', item[2])
        print('     Instances: ', item[3])
        print()
        count+=1
    print("Overll Accurracy: ", overall_correct/total_instance)
    print("Instances: ", total_instance)
    print("Correct: ", overall_correct)

    


main()




