#!/usr/bin/env python2.7

from first import v_and_t, productions, first_set
collection = []
goto_table = []

# Get the first set of a mixture of
# variables and terimals


def GetFirstSet(s):
    i = -1
    result = []
    xfirst = ['#']
    n = len(s) - 1
    while '#' in xfirst and i < n:
        i = i + 1
        xfirst = first_set[s[i]]
        temp = xfirst[:]
        if '#' in temp:
            temp.remove('#')
        result.extend(temp)
    if '#' in xfirst and i == n:
        result.append('#')
    return list(set(result))

# Print one item-set in a smart way


def PrintIterms(items):
    for i in range(len(items)):
        key = items[i][0]
        index = items[i][1]
        dotpos = items[i][2]
        symbol = items[i][3]

        temp = productions[key][index]
        temp = temp[0:dotpos] + '.' + temp[dotpos:]
        print '\n'.join(['[%s->%s, %s]' % (key, temp, symbol)])

# Figuring the closure of one item-set


def Closure(items):
    i = 0
    while i < len(items):
        key = items[i][0]
        index = items[i][1]
        dotpos = items[i][2]
        symbol = items[i][3]
        if dotpos == len(productions[key][index]):
            return items
        for k in productions.keys():
            if k == productions[key][index][dotpos]:
                temp = []
                beta = productions[key][index][dotpos + 1:]
                temp.extend(GetFirstSet(beta + symbol))
                for j in range(len(productions[k])):
                    for symbol in temp:
                        if (k, j, 0, symbol) not in items:
                            items.append((k, j, 0, symbol))
        i = i + 1
    return items

# Figuring the next item-set
# that current item-set will
# goto on input vort


def Goto(items, vort):
    to_items = []

    for item in items:
        key = item[0]
        index = item[1]
        dotpos = item[2]
        symbol = item[3]
        if dotpos < len(productions[key][index]):
            if vort == productions[key][index][dotpos]:
                to_items.append((key, index, dotpos + 1, symbol))

    return Closure(to_items)

# Get the collection of all item-sets


def Iterms(start_items):
    i = 0
    global collection, goto_table
    collection = [Closure(start_items)]
    while i < len(collection):
        for vort in v_and_t:
            to_items = Goto(collection[i], vort)
            if to_items:
                if to_items not in collection:
                    collection.append(to_items)
                j = collection.index(to_items)
                goto_table.append((i, vort, j))
        i = i + 1

start_items = [('L', 0, 0, '$')]
Iterms(start_items)

if __name__ == '__main__':
    for i in range(len(collection)):
        print 'I-%d:' % i
        PrintIterms(collection[i])
