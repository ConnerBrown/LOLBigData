import copy
import math
import tabulate
import pprint
import random
import utils
import operator
import matplotlib.pyplot as plt
import tdidt


#create TDIDT tree on train and make predictions
#for all test instances
def train_test_tree(train, test, att_indexes, att_domains, class_index):
    tree = tdidt.tdidt(train, att_indexes, att_domains, class_index)
    predictions = []
    for item in test:
        predictions.append(classify_tdidt(tree, item))
    return predictions, tree

# Classifies an instance given a tdidt tree
def classify_tdidt(tree, instance):
    if tree[0] == 'Leaf':
        return tree[1]
    else:
        i = 2
        while (instance[tree[1]] != tree[i][1]):
            i += 1
        return classify_tdidt(tree[i][2], instance)

#Create a stratified test and remainder set
def test_remainder_stratified(data, class_index):
    bins = utils.stratifiedCrossValidationBins(5, data, class_index)
    test = bins[0]
    remainder = bins[1] + bins[2]
    return test, remainder


#Construct a random forest of decision trees using N M and F
#Print the accuracy and the confusion matrix (optional)
def random_forest(N, M, F, table, attr_indexes, attr_domains, class_index, strat_index):
    random.shuffle(table)
    test, remainder = test_remainder_stratified(table, strat_index)
    boot_samples = []
    attr_subsets = []
    trees = []
    accuracies = []
    trees = []
    #setup boot straps
    for _ in range(N):
        attr_subsets.append(utils.rand_attributes(attr_indexes, F)) 
        boot = utils.bootstrap(remainder)
        valid = []
        #build validator set
        for item in remainder:
            if item not in boot:
                valid.append(item)
        boot_samples.append([boot, valid])
    
    #build trees
    for i in range(N):
            #returns predictions, tree
        pred, tree = train_test_tree(boot_samples[i][0], boot_samples[i][1], 
                                    attr_subsets[i], attr_domains, class_index)
        correct = 0
        for j in range(len(boot_samples[i][1])):
            if boot_samples[i][1][j][class_index] == pred [j]:
                correct += 1
        trees.append([tree, utils.div(correct,len(boot_samples[i][1]))])
    
    

    trees.sort(key = lambda x: x[1])
    mtrees = trees[len(trees)-M:]

    #predict and determine accuracy
    print("     grouping test set")
    minutes, groups = utils.groupBy(test, 1)
    print("     running classifier")
    accuracies = []
    overall_correct = 0
    total_instance = len(test)
    
    for count in range(len(minutes)):
        correct = 0
        for item in groups[count]:
            votes = []
            for tree in mtrees:
                votes.append(classify_tdidt(tree[0], item))
            vote = utils.majority_vote(votes)
            if item[class_index] == vote:
                correct+=1
                overall_correct += 1
        accuracies.append([minutes[count], correct/len(groups[count]), correct, len(groups[count])])

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

    return accuracies


def main():
    print('reading table')
    table = utils.readTable("LoL_clean_manual.csv")
    #remove header
    table = table[1:]
    #reduce table size
    print('Reducing table size')
    table = table[0:int(len(table)/20)]
    print('converting table numeric')
    utils.convertToNumeric(table)
    print('Reducing Range of Several Attributes')
    cut_offs = [-8000, -6000, -4000, -2000, -1000, 0, 1000, 2000, 4000, 6000, 8000]
    table = utils.discrimatize(table, 16, cut_offs)
    cut_offs = [10, 20, 30, 40, 50, 60, 75]
    table = utils.discrimatize(table, 17, cut_offs)
    table = utils.discrimatize(table, 23, cut_offs)
    cut_offs = [3, 6, 9, 12, 15, 18]
    table = utils.discrimatize(table, 20, cut_offs)
    table = utils.discrimatize(table, 26, cut_offs)
    cut_offs = [0, 3, 6, 10, 15]
    table = utils.discrimatize(table, 19, cut_offs)
    table = utils.discrimatize(table, 25, cut_offs)
    cut_offs = [0, 3, 6, 9, 12]
    table = utils.discrimatize(table, 18, cut_offs)
    table = utils.discrimatize(table, 24, cut_offs)
    cut_offs = [0, 1, 2]
    table = utils.discrimatize(table, 21, cut_offs)
    table = utils.discrimatize(table, 27, cut_offs)
    print('Shuffling')
    random.shuffle(table)
    
    print('     Instances: ', len(table))

    att_indexes = [1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                    26, 27, 28]
    domains = {
                1: [x+1 for x in range(76)],
                16: [1,2,3,4,5,6,7,8,9,10,11], 
                17: [x+1 for x in range(7)],
                18: [1,2,3,4,5],
                19: [1,2,3,4,5],
                20: [x+1 for x in range(6)],
                21: [1,2,3],
                22: [0,1,2,3],
                23: [x+1 for x in range(7)],
                24: [1,2,3,4,5],
                25: [1,2,3,4,5], 
                26: [x+1 for x in range(6)],
                27: [1,2,3],
                28: [0,1,2,3]
                }

    print('Generating Random Forest this will take some time')
    print('N = ', 30, " M = ", 7, " F = ", 2)
    accuracies = random_forest(30, 7, 2, table, att_indexes, domains, 5, 1)
    #utils.plot(accuracies, "randomforestaccuracies.png")

    

if __name__ == "__main__":
    main()