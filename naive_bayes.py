import pandas as pd

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


def numerify_instance(instance):
    new = []
    for attribute in instance:
        try:
            new.append(float(attribute))
        except:
            new.append(attribute)
    return new


def main():
    
