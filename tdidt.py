import utils
import math
import operator
import random
import pprint
import matplotlib.pyplot as plt

def classify_tdidt(tree, instance):
    if tree[0] == 'Leaf':
        return tree[1]
    else:
        i = 2
        while (instance[tree[1]] != tree[i][1]):
            i += 1
        return classify_tdidt(tree[i][2], instance)

def calculate_error(f, N, z):
    root = ((f / N) - ((f**2)/N) + ((z**2)/(4*(N**2))))**(1/2)
    top = (f + ((z**2)/(2*N)) + (z * root))
    bottom = 1 + ((z**2)/N)
    e = top / bottom
    return e

def update_count(tree, instance, class_index):
    if tree[0] == 'Leaf':
        if tree[1] == instance[class_index]:
            tree[2] += 1
        else:
            tree[3] += 1
    else:
        i = 2
        while (instance[tree[1]] != tree[i][1]):
            i += 1
        return update_count(tree[i][2], instance, class_index)


def has_all_leaves(node):
    for branch in node[2:]:
        if branch[2][0] != 'Leaf':
            return False
    return True


def same_rules(node):
    rules = set()
    for branch in node[2:]:
        rules.add(branch[2][1])
    if len(rules) == 1:
        return True
    else:
        return False


def prune(tree, confidence):
    if tree[0] == 'Leaf':
        return False, tree
    else:
        all_leaves = has_all_leaves(tree)
        if all_leaves:
            successes, fails = get_stats(tree)
            e_node = calculate_error((fails / (successes + fails)), (successes + fails), confidence)
            same_rule = same_rules(tree)
            if same_rule:
                rule = tree[2][2][1]
                tree = ['Leaf', rule, successes, fails, e_node]
                return True, tree
            else:
                N_total = 0
                e_total = 0
                for leaf in tree[2:]:
                    N_total += leaf[2][2] + leaf[2][3]
                    e_total += (leaf[2][4]) * (leaf[2][2] + leaf[2][3])
                e_average = e_total / N_total
                if e_node < e_average:
                    class0 = tree[2][2][1]
                    class1 = ""
                    class0_votes = 0
                    class1_votes = 0
                    for leaf in tree[2:]:
                        if leaf[2][1] == class0:
                            class0_votes += leaf[2][2]
                            class1_votes += leaf[2][3]
                        else:
                            class1 = leaf[2][1]
                            class1_votes += leaf[2][2]
                            class0_votes += leaf[2][3]
                    if class0_votes > class1_votes:
                        e_actual = calculate_error((class1_votes/(class0_votes + class1_votes)), (class0_votes + class1_votes), confidence)
                        tree = ['Leaf', class0, class0_votes, class1_votes, e_actual]
                    else:
                        e_actual = calculate_error((class0_votes/(class0_votes + class1_votes)), (class0_votes + class1_votes), confidence)
                        tree = ['Leaf', class1, class1_votes, class0_votes, e_actual]
                    return True, tree
                else:
                    return False, tree
        else:
            pruned = False
            for i in range(len(tree[2:])):
                a = prune(tree[i+2][2], confidence)
                if a == None:
                    continue
                else:
                    pruned_n= a[0]
                    tree[i+2][2] = a[1]
                pruned = pruned or pruned_n
            if pruned:
                return False, tree
                

def get_stats(tree):
    if tree[0] == 'Leaf':
        return tree[2], tree[3]
    else:
        successes = 0
        fails = 0
        for branch in tree[2:]:
            success_n, fail_n = get_stats(branch[2])
            successes += success_n
            fails += fail_n
        return successes, fails


def update_errors(tree, z):
    if tree[0] == 'Leaf':
        N = tree[2] + tree[3]
        f = tree[3] / N
        e = calculate_error(f, N, z)
        tree[4] = e
    else:
        for branch in tree[2:]:
            update_errors(branch[2], z)

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

def train_test_tree(tree, train, test, att_indexes, att_domains, class_index):
    predictions = []
    for item in test:
        predictions.append(classify_tdidt(tree, item))
    return predictions

def plot(accuracies):
    minute = utils.getColumn(accuracies, 0)
    accuracy = utils.getColumn(accuracies, 1)
    plt.figure()
    plt.scatter(minute, accuracy)
    plt.title("TDIDT Accuracy Vs. Time")
    plt.xlabel('Minute')
    plt.ylabel('Accuracy')
    plt.show()



def main():
    print('reading table')
    table = utils.readTable("LoL_clean_manual.csv")
    #remove header
    table = table[1:]
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
    print('Shuffling and Reducing')
    random.shuffle(table)
    table = table[0:int(len(table)/1.5)]
    print('     Instances: ', len(table))
    print('Stratisfying')

    bins = utils.stratifiedCrossValidationBins(3, table, 1)
    train1, test1 = utils.binsToSets(bins, 0)
    print('Building tree with ', len(train1), ' instances')
    att_indexes = [17, 18, 19, 20, 21, 22, 23, 24, 25,
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

    tree = tdidt(train1, att_indexes, domains, 5)
    pprint.pprint(tree)
    print("Testing by the minute, this will take some time")
    print("     grouping test set")
    minutes, groups = utils.groupBy(test1, 1)
    print("     running classifier")
    accuracies = []
    overall_correct = 0
    total_instance = 0
    #TDIDT
    
    for count in range(len(minutes)):
        predictions = train_test_tree(tree, train1, groups[count], att_indexes, domains, 5)
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
        print('Minute: ', item[0])
        print('     Accuracy: ', item[1])
        print('     Correct: ', item[2])
        print('     Instances: ', item[3])
        print()
        count+=1
    print("Overll Accurracy: ", overall_correct/total_instance)
    print("Instances: ", total_instance)
    print("Correct: ", overall_correct)

    plot(accuracies)

    print('Pruning tree')
    print('     calculating stats')
    for instance in train1:
        update_count(tree, instance, 5)
    
    update_errors(tree, 0.7)
    print("     Pruning")
    prune(tree, 0.7) 
    print("Pruned Tree: ")
    pprint.pprint(tree)

    print("Testing by the minute, this will take some time")
    print("     grouping test set")
    minutes, groups = utils.groupBy(test1, 1)
    print("     running classifier")
    accuracies = []
    overall_correct = 0
    total_instance = 0

    for count in range(len(minutes)):
        predictions = train_test_tree(tree, train1, groups[count], att_indexes, domains, 5)
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
        print('Minute: ', item[0])
        print('     Accuracy: ', item[1])
        print('     Correct: ', item[2])
        print('     Instances: ', item[3])
        print()
        count+=1
    print("Overll Accurracy: ", overall_correct/total_instance)
    print("Instances: ", total_instance)
    print("Correct: ", overall_correct)

    plot(accuracies)

if __name__ == "__main__":
    main()