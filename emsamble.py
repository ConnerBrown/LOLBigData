import copy
import math
import tabulate
import pprint
import random
import utils
import operator


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


def check_all_same_att(instances, index):
    base = instances[0][index]
    for elem in instances:
        if elem[index] != base:
            return False
    return True

def check_all_same_class(instances, class_index):
    base = instances[0][class_index]
    for elem in instances:
        if elem[class_index] != base:
            return False
    return True

def select_attribute(instances, att_indexes, class_index):
    Entropy_list = {}
    for index in att_indexes:
        E_new = 0
        names, values = utils.groupBy(instances, index)
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

def handle_clash(instances, class_index):
    votes = {}
    for instance in instances:
        if instance[class_index] not in votes:
            votes[instance[class_index]] = 1
        else:
            votes[instance[class_index]] += 1
    # Referenced from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_x = sorted(votes.items(), reverse=True, key=operator.itemgetter(1))
    return ["Leaf", sorted_x[0][0], 0, 0, 0]


def tdidt(instances, att_indexes, att_domains, class_index):
    if check_all_same_class(instances, class_index):
        return ["Leaf", instances[0][class_index], 0, 0, 0]
    if att_indexes == []:
        return handle_clash(instances, class_index)
    index = select_attribute(instances, att_indexes, class_index)
    new_indexes = att_indexes[:]
    new_indexes.remove(index)
    if check_all_same_att(instances, index):
        return tdidt(instances, new_indexes, att_domains, class_index)
    else:
        tree = ["Attribute", index]
        partitions = partition_instances(instances, index, att_domains[index])
        for val in partitions:
            if (partitions[val] == []):
                return handle_clash(instances, class_index)
            tree.append(["Value", val, tdidt(partitions[val], new_indexes, att_domains, class_index)])
        return tree


#create TDIDT tree on train and make predictions
#for all test instances
def train_test_tree(train, test, att_indexes, att_domains, class_index):
    tree = tdidt(train, att_indexes, att_domains, class_index)
    predictions = []
    for item in test:
        predictions.append(classify_tdidt(tree, item))
    return predictions, tree

#divsion by 0 = 0
def div(x,y):
    if y ==0:
        return 0
    return x/y


def classify_tdidt(tree, instance):
    if tree[0] == 'Leaf':
        return tree[1]
    else:
        i = 2
        while (instance[tree[1]] != tree[i][1]):
            i += 1
        return classify_tdidt(tree[i][2], instance)


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

#generate folds for stratified cross V
def stratified_cross_validation_bins(K, table, classIndex):
    names, values = utils.groupBy(table, classIndex)
    bins = []
    for i in range(K):
        bins.append([])
    bindex = 0
    for i in range(len(values)):
        for j in range(len(values[i])):
            bins[bindex].append(values[i][j])
            bindex = (bindex + 1)%K

    return bins 


#Create a stratified test and remainder set
def test_remainder_stratified(data, class_index):
    bins = stratified_cross_validation_bins(3, data, class_index)
    test = bins[0]
    remainder = bins[1] + bins[2]
    return test, remainder

#@Gina's repo
def bootstrap(table):
    n = len(table)
    sample = []
    for _ in range(n):
        rand_index = random.randrange(0, n)
        sample.append(table[rand_index])

    return sample

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

#Construct a random forest of decision trees using N M and F
#Print the accuracy and the confusion matrix (optional)
def random_forest(N, M, F, table, attr_indexes, attr_domains, class_index):
    random.shuffle(table)
    test, remainder = test_remainder_stratified(table, class_index)
    boot_samples = []
    attr_subsets = []
    trees = []
    predictions = []
    accuracies = []
    trees = []
    #setup boot straps
    for _ in range(N):
        attr_subsets.append(rand_attributes(attr_indexes, F)) 
        boot = bootstrap(remainder)
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
        trees.append([tree, div(correct,len(boot_samples[i][1]))])
    
    

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
            vote = majority_vote(votes)
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
    table = discrimatize(table, 16, cut_offs)
    cut_offs = [10, 20, 30, 40, 50, 60, 75]
    table = discrimatize(table, 17, cut_offs)
    table = discrimatize(table, 23, cut_offs)
    cut_offs = [3, 6, 9, 12, 15, 18]
    table = discrimatize(table, 20, cut_offs)
    table = discrimatize(table, 26, cut_offs)
    cut_offs = [0, 3, 6, 10, 15]
    table = discrimatize(table, 19, cut_offs)
    table = discrimatize(table, 25, cut_offs)
    cut_offs = [0, 3, 6, 9, 12]
    table = discrimatize(table, 18, cut_offs)
    table = discrimatize(table, 24, cut_offs)
    cut_offs = [0, 1, 2]
    table = discrimatize(table, 21, cut_offs)
    table = discrimatize(table, 27, cut_offs)
    print('Shuffling')
    random.shuffle(table)
    
    print('     Instances: ', len(table))

    att_indexes = [ 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
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
    print('N = ', 50, " M = ", 5, " F = ", 3)
    random_forest(50, 5, 3, table, att_indexes, domains, 5)

    

if __name__ == "__main__":
    main()