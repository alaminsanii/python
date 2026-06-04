tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]


def printTable(tableData):

    # Create list of zeros
    colWidths = [0] * len(tableData)

    # Find longest word in each inner list
    for i in range(len(tableData)):
        for word in tableData[i]:

            if len(word) > colWidths[i]:
                print(len(word), colWidths[i])
                colWidths[i] = len(word)
                

    # Print the table
    for row in range(len(tableData[0])):
        
        for col in range(len(tableData)):
            print(col)
            print(tableData[col][row].rjust(colWidths[col]), end=' ')
        print()


printTable(tableData)