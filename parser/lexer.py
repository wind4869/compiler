#!/usr/bin/env python

import re

keywords = [
    'int', 'double', 'string', 'if',
    'else', 'end', 'while', 'print'
]
map_table = {}
symbols_table = {}
map_result = []
raw_result = []

fd = open('../lexer/map.txt')
for line in fd:
    map_table[line[:-3]] = line[-2]
fd.close()

regex_id = '^[A-Za-z_][\w]*$'
regex_int = '^-?[\d]+$'
regex_double = '^-?[\d]*\.[\d]+$'

linenum = 1
semaphore = 0
num_lex_error = 0

fd = open('../lexer/s.txt')
for l in fd:
    line = l[:-1].split(' ')
    count = 0
    for item in line:
        if item == '#':
            break
        if not item:
            continue
        raw_result.append(item)
        if item in keywords:
            map_result.append(map_table[item])
            if item == 'if' or item == 'while':
                semaphore -= 1
            if item == 'end':
                semaphore += 1
        elif re.match(regex_id, item):
            map_result.append('v')
            symbols_table[item] = ['v']
        elif re.match(regex_int, item):
            map_result.append('n')
        elif re.match(regex_double, item):
            map_result.append('d')
        elif item and item[0] == '\'' and item[-1] == '\'':
            map_result.append('g')
        elif item in map_table.keys():
            map_result.append(map_table[item])
        else:
            num_lex_error += 1
            for i in range(count):
                map_result.pop()
            print '>>> Unidentified symbols in line %d' % linenum
            break
        count = count + 1
    if not semaphore:
        map_result.append(' ')
    linenum = linenum + 1
fd.close()

source = ''.join(map_result)
raw_result.reverse()

if __name__ == '__main__':
    print source
    print raw_result
    print symbols_table
