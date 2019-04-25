import math
import operator
import copy
import random
import pprint
from tabulate import tabulate


#takes a table of values and turns them into floats
#'NA' values and alpha character strings are left in the list
def convert_to_numeric(table):
    #try to convert to int
    for i in range(len(table)):
        for j in range(len(table[0])):
            try:
                table[i][j] = float(table[i][j])
            except:
                continue

#reads a csv file of the given name into a list
#returns said list
def read_table(filename):
    table = []
    myFile = open(filename, 'r')
    #read each line in file and append into the table
    lines = myFile.read().split('\n')
    for line in lines:
        values = line.split(',')
        table.append(values)
    myFile.close()
    return table


# @Gina's Repo
def group_by(table, column_index, include_only_column_index=None):
    # first identify unique values in the column
    group_names = sorted(list(set(get_column(table, column_index))))

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


# takes a table and a column index
# returns a column at index where values are converted to numeric
def get_column(table, column_index):
    column = []
    for item in table:
        column.append(item[column_index])
    return column

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
        names, values = group_by(instances, index)
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
    return ["Leaf", sorted_x[0][0]]

def tdidt(instances, att_indexes, att_domains, class_index):
    if check_all_same_class(instances, class_index):
        print("Returning Leaf, all same class")
        return ["Leaf", instances[0][class_index]]
    if att_indexes == []:
        return handle_clash(instances, class_index)
    index = select_attribute(instances, att_indexes, class_index)
    new_indexes = att_indexes[:]
    new_indexes.remove(index)
    if check_all_same_att(instances, index):
        print('Calling 1:')
        print('with attributes: ', new_indexes)
        return tdidt(instances, new_indexes, att_domains, class_index)
    else:
        tree = ["Attribute", index]
        partitions = partition_instances(instances, index, att_domains[index])
        for val in partitions:
            if (partitions[val] == []):
                return handle_clash(instances, class_index)
            print('Calling 2:')
            pprint.pprint(tree)
            print('with attributes: ', new_indexes)
            print('with partition: ', val)
            tree.append(["Value", val, tdidt(partitions[val], new_indexes, att_domains, class_index)])
        return tree

def classify_tdidt(tree, instance):
    if tree[0] == 'Leaf':
        return tree[1]
    else:
        i = 2
        while (instance[tree[1]] != tree[i][1]):
            i += 1
        return classify_tdidt(tree[i][2], instance)

def main():
    titanic = read_table('titanic.txt')
    convert_to_numeric(titanic)
    attr_indexes = [0,1,2]
    att_domains = {0: ["crew", "first", "second", "third"], 
                1: ["adult", "child"],
                2: ["male", "female"]}
    class_index = 3
    random.shuffle(titanic)
    test = titanic[:int(len(titanic)/3)]
    train = titanic[int(len(titanic)/3):]
    tree = tdidt(train, attr_indexes, att_domains, class_index)
    print()
    print()
    print()
    print()
    pprint.pprint(tree)


if __name__ == "__main__":
    main()
