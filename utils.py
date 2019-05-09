#Utility functions
import math
import copy
import tabulate
import random
import matplotlib.pyplot as plt


#normailize columns at indexes
def normalizeColumns(table, indexes):
    colMaxes = []
    colMins = []
    for index in indexes:
        col = getColumn(table, index)
        colMaxes.append(max(col))
        colMins.append(min(col))
    for i in range(len(table)):
        for j in range(len(indexes)):
            table[i][indexes[j]] = (table[i][indexes[j]]-colMins[j]) / ((colMaxes[j]- colMins[j])*1.0)


#reads a csv file of the given name into a list
#returns said list
def readTable(filename):
    table = []
    myFile = open(filename, 'r')
    #read each line in file and append into the table
    lines = myFile.read().split('\n')
    temp = []
    row = []
    isList = False
    for line in lines:
        values = line.split(',')
        for value in values:
            if isList:

                temp.append(value)
            if '"[' in value and isList == False:
                temp.append(value)
                isList = True
            if not isList:
                row.append(value)
            if isList and ']"' in value[-2:]:
                temp.append(value)
                isList = False
                row.append(temp)
                temp = []
        table.append(row)
        row = []

    myFile.close()
    return table
	
# Converts the specified column 
def convertColToInt(table, colIndex, header):
    for i in range(header, len(table), 1):
        try:
            table[i][colIndex] = int(table[i][colIndex])
        except:
            continue

#takes a table of values and turns them into floats
#'NA' values and alpha character strings are left in the list
def convertToNumeric(table):
    #try to convert to int
    for i in range(len(table)):
        for j in range(len(table[0])):
            try:
                table[i][j] = float(table[i][j])
            except:
                continue

			
#prints a 'table' to a file
#taken from Gina's Repo
def writeTable(filename, table):
    outfile = open(filename, "w")
    for k in range(len(table)):
        for i in range(len(table[k])):
            outfile.write(str(table[k][i]))
            if i < len(table[k])-1:
                outfile.write(',')
        if k < len(table)-1:
            outfile.write('\n')
        
    
    outfile.close()
	

# @Gina's repo
def getColumn(table, column_index):
    column = []
    for row in table:
            column.append(row[column_index])

    return column
	
# @Gina's Repo
def getFrequencies(table, column_index):
    column = getColumn(table, column_index)
    values = []
    counts = []

    for value in column:
        if value not in values:
            values.append(value)
            # first time we have seen this value
            counts.append(1)
        else: # we've seen it before, the list is not sorted...
            counts[values.index(value)] += 1

    return values, counts
	
# @Gina's Repo
def groupBy(table, column_index, include_only_column_index=None):
    # first identify unique values in the column
    group_names = list(set(getColumn(table, column_index)))

    # now, we need a list of subtables
    # each subtable corresponds to a value in group_names
    # parallel arrays
    groups = [[] for name in group_names]
    for row in table:
        # which group does it belong to?
        group_by_value = row[column_index]
        index = group_names.index(group_by_value)
        if include_only_column_index is None:
            groups[index].append(row.copy()) # note: shallow copy
        else:
            groups[index].append(row[include_only_column_index])

    return group_names, groups


#generate folds for stratified cross V
def stratifiedCrossValidationBins(K, table, classIndex):
    names, values = groupBy(table, classIndex)
    bins = []
    for i in range(K):
        bins.append([])
    bindex = 0
    for i in range(len(values)):
        for j in range(len(values[i])):
            bins[bindex].append(values[i][j])
            bindex = (bindex + 1)%K

    return bins 

#convert stratified bins into train/test set
def binsToSets(bins, index):
    test = bins[index]
    train = []
    for i in range(len(bins)):
        if not i == index:
            for j in range(len(bins[i])):
                train.append(bins[i][j])
    return train, test


#divsion by 0 = 0
def div(x,y):
    if y ==0:
        return 0
    return x/y


#build a tabulated confusion martix
def build_confusion_matrix(predictions_w_actual, headers, classes, strClassFlg=False):
    #If the classes are strings they must be converted to integers
    if strClassFlg==True:
        str_classes = copy.deepcopy(classes)
        for i in range(len(classes)):
            classes[i] = i+1
        for i in range(len(predictions_w_actual)):
            for k in range(len(predictions_w_actual[i])):
                for l in range(len(predictions_w_actual[i][k])):
                    for j in range(len(str_classes)):
                        if predictions_w_actual[i][k][l] == str_classes[j]:
                            predictions_w_actual[i][k][l] = classes[j]
                        elif predictions_w_actual[i][k][l] == str_classes[j]:
                            predictions_w_actual[i][k][l] = classes[j]

    value = [0 for i in range(len(classes))]
    correct = 0
    incorrect = 0
    calue_matrix = []
    for i in range(len(classes)):
        for j in range(len(predictions_w_actual)):
            for k in range(len(predictions_w_actual[j][0])):
                #predictions are at predWA[][0] actuals at predWA[][1]
                #true, accurate prediction
                if(classes[i] == predictions_w_actual[j][0][k] 
                            == predictions_w_actual[j][1][k]):
                    value[i] += 1
                    correct += 1
                #inaccurate prediction
                elif(classes[i] == predictions_w_actual[j][1][k]):
                    value[predictions_w_actual[j][0][k]-1] += 1 
                    incorrect += 1
        #compute total
        value.append(correct + incorrect)
        #compute recog
        value.append(round(div(correct, correct + incorrect),2))
        correct = 0
        incorrect = 0
        #add class
        value.insert(0, classes[i])
        calue_matrix.append(value)
        #clear value
        value = [0 for i in range(len(classes))]
    if strClassFlg:
        for i in range(len(calue_matrix)):
            calue_matrix[i][0] = str_classes[calue_matrix[i][0]-1]
    return(tabulate.tabulate(calue_matrix, headers))

#Generate random index sub set
#@gina's repo
def rand_attributes(value_list, num_values):
    shuffled = value_list[:]
    random.shuffle(shuffled)
    return shuffled[:num_values]

#compute majority vote
def majority_vote(votes):
    lis = sorted(votes)
    prime = 0
    val = 0
    mode = lis[0]
    curr = lis[0]
    for i in range(len(lis)):
        if lis[i] == curr and i != len(lis)-1:
            prime +=1
        else:
            if prime > val:
                val = prime
                mode = curr
            curr = lis[i]
            prime = 1
    return mode

#@Gina's repo
def bootstrap(table):
    n = len(table)
    sample = []
    for _ in range(n):
        rand_index = random.randrange(0, n)
        sample.append(table[rand_index])

    return sample


#Converts raw values into categories
def discrimatize(table, column_index, cut_offs):
    for i in range(len(table)):
        for j in range(len(cut_offs)):
            if(j<(len(cut_offs)-1)):
                if(table[i][column_index]<=cut_offs[j]):
                    table[i][column_index] = j+1
                    break
            else:
                table[i][column_index] = j+1
    return table


#plot accuracies by minute
def plot(accuracies, figname):
    minute = getColumn(accuracies, 0)
    accuracy = getColumn(accuracies, 1)
    plt.figure()
    plt.scatter(minute, accuracy)
    plt.title("TDIDT Accuracy Vs. Time")
    plt.xlabel('Minute')
    plt.ylabel('Accuracy')
    plt.savefig(figname)

#partition dataset based on an attribute
def partition_instances(instances, att_index, att_domain):
    # this is a group by att_domain, not by att_values in instances
    partition = {}
    for att_value in att_domain:
        subinstances = []
        for instance in instances:
            # check if this instance has att_value at att_index
            if instance[att_index] == att_value:
                subinstances.append(instance)
        partition[att_value] = subinstances
    return partition

#checks if instances have the same attribute value
def check_all_same_att(instances, index):
    base = instances[0][index]
    for elem in instances:
        if elem[index] != base:
            return False
    return True

#checks if instances are all the same class
def check_all_same_class(instances, class_index):
    base = instances[0][class_index]
    for elem in instances:
        if elem[class_index] != base:
            return False
    return True

#attribute selection with entropy 
def select_attribute(instances, att_indexes, class_index):
    Entropy_list = {}
    for index in att_indexes:
        E_new = 0
        names, values = groupBy(instances, index)
        for val in values:
            ratios = {}
            total = 0
            for instance in val:
                if instance[class_index] not in ratios:
                    ratios[instance[class_index]] = 1
                else:
                    ratios[instance[class_index]] += 1
                total += 1
            E = 0
            for ratio in ratios:
                E += (ratios[ratio] / total) * math.log((ratios[ratio] / total), 2)
            E_new += (total / len(instances)) * -E
        Entropy_list[index] = E_new

    min_i = att_indexes[0]
    for index in att_indexes:
        if Entropy_list[index] < Entropy_list[min_i]:
            min_i = index
    return min_i
