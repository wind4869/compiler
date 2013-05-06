#!/usr/bin/env python2.7

from first import variables, terminals, productions
from items import collection, goto_table

action_table = []

# Get the state j that
# state i will goto
# on input vort


def Goto(i, vort):
    for item in goto_table:
        if i == item[0] and vort == item[1]:
            return item[2]
    return -1

# Build the action_table
for i in range(len(collection)):
    for item in collection[i]:
        key = item[0]
        index = item[1]
        dotpos = item[2]
        symbol = item[3]
        if dotpos < len(productions[key][index]):
            vort = productions[key][index][dotpos]
            if vort in terminals:
                j = Goto(i, vort)
                if (i, vort, 's', j) not in action_table:
                    action_table.append((i, vort, 's', j))
        elif key != 'L':
            action_table.append((i, symbol, 'r', key, index))
        else:
            action_table.append((i, '$', 'a'))

fd = open('../table/action.txt', 'w')
for item in action_table:
    fd.write(str(item) + '\n')
fd.close()

fd = open('../table/goto.txt', 'w')
for item in goto_table:
    fd.write(str(item) + '\n')
fd.close()

if __name__ == '__main__':
    print '---------------ACTION--------------'
    for item in action_table:
        print item
    print '----------------GOTO----------------'
    for item in goto_table:
        if item[1] in variables:
            print item
