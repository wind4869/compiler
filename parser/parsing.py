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
quarternary = []
counter = 0

for item in source_block:
    if not item:
        source_block.remove(item)
source_block.pop()

for block in source_block:
    p = 0
    block += '$'
    terminal = block[0]
    state_stack = [0]
    symbol_stack = []
    raw_stack = []
    back_stack = []
    while_stack = []
    print 'state_stack\tsymbol_stack\tinput\taction'

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
            print '%r\t%r\t%s\ts' % (state_stack, symbol_stack, block[p:])

            if terminal == 'w':
                print 'shot'
                back_stack.append('w')
                while_stack.append(counter)
            elif terminal == 'l':
                quarternary[back_stack.pop()][3] = counter + 1
                quarternary.insert(counter, ['goto', '', '', -1])
                back_stack.append(counter)
                counter += 1
            elif terminal == '\\':
                num_quarternary = back_stack.pop()
                quarternary[num_quarternary][3] = counter
                if back_stack:
                    judge = back_stack.pop()
                    if judge == 'w':
                        quarternary.insert(counter, [
                                           'goto', '', '', while_stack.pop()])
                        quarternary[num_quarternary][3] += 1
                        counter += 1
                    else:
                        back_stack.append(judge)

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
                quarternary.insert(counter, [temp[
                                   1], temp[0], temp[2], temp_var])
                counter += 1
                temp_var = 't'
            elif key in ['P', 'C', 'F', 'O'] or selector == ('T', 2) or selector == ('E', 2):
                if selector == ('F', 0):
                    temp = temp[1:2]
                raw_stack.extend(temp)
            elif key == 'B':
                raw_stack.append('B')
                quarternary.insert(counter, [temp[
                                   1], temp[0], temp[2], counter + 2])
                quarternary.insert(counter + 1, ['goto', '', '', -1])
                back_stack.append(counter + 1)
                counter += 2
            elif key == 'S' and index in [1, 2, 3, 7, 8]:
                raw_stack.append('S')
                if index == 1:
                    quarternary.insert(counter, ['=', temp[3], '', temp[1]])
                elif index in [2, 3]:
                    quarternary.insert(counter, ['=', temp[2], '', temp[0]])
                elif index in [7, 8]:
                    quarternary.insert(counter, ['print', temp[1], '', ''])
                counter += 1
            else:
                raw_stack.append(key)

            print '%r\t%r\t%s\tr' % (state_stack, symbol_stack, block[p:])
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

for i in range(len(quarternary)):
    print '%d - %r' % (i, quarternary[i])
print '----------#_# The Quarternaries Are Above----------'
