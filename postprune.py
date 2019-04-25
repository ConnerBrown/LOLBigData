
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

def main():
    cancer = read_table('wisconsin.txt')
    convert_to_numeric(cancer)

if __name__ == "__main__":
    main()