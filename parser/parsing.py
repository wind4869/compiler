#!/usr/bin/env python2.7

from lexer import source, raw_result, num_lex_error
from table import action_table, Goto
from first import productions

# Figuring out and return the
# action that parsing will do
# on input terminal in current
# state state


def Action(state, terminal):
    for item in action_table:
        if item[0] == state and item[1] == terminal:
            return item[2:]
    return -1

source_block = source.split(' ')
num_parse_error = 0
temp_num = 0
temp_var = 't'
quaternary = []

for item in source_block:
    if not item:
        source_block.remove(item)

for block in source_block:
    p = 0
    block += '$'
    terminal = block[0]
    state_stack = [0]
    symbol_stack = []
    raw_stack = []
    print 'state_stack\tsymbol_stack\traw_stack\tinput\taction'

    # Do parsing for each block
    while True:
        state = state_stack.pop()
        state_stack.append(state)
        action = Action(state, terminal)
        if action == -1:
            num_parse_error += 1
            print '>>> error1'
            break
        if action[0] == 's':
            state_stack.append(action[1])
            symbol_stack.append(terminal)
            raw_stack.append(raw_result.pop())
            print '%r\t%r\t%r\t%s\ts' % (state_stack, symbol_stack, raw_stack, block[p:])
            p = p + 1
            terminal = block[p]
        elif action[0] == 'r':
            key = action[1]
            index = action[2]
            temp = []
            for i in range(len(productions[key][index])):
                state_stack.pop()
                symbol_stack.pop()
                temp.append(raw_stack.pop())

            state = state_stack.pop()
            state_stack.append(state)
            state_stack.append(Goto(state, key))
            symbol_stack.append(key)

            temp.reverse()
            selector = action[1:3]
            if selector == ('E', 0) or selector == ('E', 1) or\
                    selector == ('T', 0) or selector == ('T', 1):
                temp_num += 1
                temp_var += str(temp_num)
                raw_stack.append(temp_var)
                quaternary.append((temp[1], temp[0], temp[2], temp_var))
                temp_var = 't'
            elif key == 'F' or selector == ('T', 2) or selector == ('E', 2):
                if selector == ('F', 0):
                    temp = temp[1:2]
                raw_stack.extend(temp)
            elif selector == ('S', 2):
                quaternary.append(('=', temp[2], '', temp[0]))

            print '%r\t%r\t%r\t%s\tr' % (state_stack, symbol_stack, raw_stack, block[p:])
            print '>>> use productions:%s->%s' % (key, productions[key][index])
        elif action[0] == 'a':
            print '>>> finish parsing'
            break
        else:
            num_parse_error += 1
            print '>>> error2'
            break
num_error = num_lex_error + num_parse_error
if num_error:
    print '----------@_@ FAILED WITH %d ERRORS----------' % num_error
else:
    print '----------^_^ SUCCEEDED WITH %d ERRORS----------' % num_error

for item in quaternary:
    print item
print '----------#_# The Quaternaries Are Above----------'
