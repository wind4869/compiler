#!/usr/bin/env python2.7

first_set = {}
productions = {}
variables = []
terminals = []
v_and_t = []  # the set of all variables and terminals

# Recursive function for figuring first set of
# one vort(variable or terminal)


def first(vort):
    if vort in terminals:
        return [vort]
    firstv = []
    for i in range(len(productions[vort])):
        j = -1
        xfirst = ['#']
        n = len(productions[vort][i]) - 1
        while '#' in xfirst and j < n:
            j = j + 1
            xfirst = first(productions[vort][i][j])
            temp = xfirst[:]
            if '#' in temp and len(temp) > 1:
                temp.remove('#')
            firstv.extend(temp)
        if '#' in xfirst and j == n:
            firstv.append('#')
    return list(set(firstv))

fd = open('../cfg/p.txt')
for line in fd:
    productions[line[0]] = line[3:-1].split('|')
fd.close()
fd = open('../cfg/t.txt')
for line in fd:
    terminals = line[:-1].split(' ')
fd.close()
fd = open('../cfg/v.txt')
for line in fd:
    variables = line[:-1].split(' ')
fd.close()

# Eliminate left recursion
extra_variables = []
for vi in variables:
    for vj in variables[:variables.index(vi)]:
        for bodyi in productions[vi]:
            if bodyi[0] == vj:
                gamma = bodyi[1:]
                productions[vi].remove(bodyi)
                for bodyj in productions[vj]:
                    productions[vi].append(bodyj + gamma)
    recursive = False
    for bodyi in productions[vi]:
        if bodyi[0] == vi:
            recursive = True
            break
    if recursive:
        i = 0
        n = productions[vi]
        new_var = vi.lower()
        extra_variables.append(new_var)
        productions[new_var] = ['#']
        for i in range(len(productions[vi])):
            bodyi = productions[vi][0]
            if bodyi[0] == vi:
                alpha = bodyi[1:]
                productions[new_var].append(alpha + new_var)
            else:
                productions[vi].append(bodyi + new_var)
            productions[vi].remove(bodyi)

# Get first set of all variables and terminals
# except extra variables
v_and_t = variables + terminals
variables += extra_variables
for elem in v_and_t:
    first_set[elem] = first(elem)

# Reload variables and productions
variables = []
new_productions = productions  # productions without left recursion
productions = {}

fd = open('../cfg/v.txt')
for line in fd:
    variables = line[:-1].split(' ')
fd.close()
fd = open('../cfg/p.txt')
for line in fd:
    productions[line[0]] = line[3:-1].split('|')
fd.close()

if __name__ == '__main__':
    print '-----productions without left recursion-----'
    for k, v in new_productions.items():
        print '%s->%s' % (k, '|'.join(v))
    print '-----first set of all terminals and variables-----'
    print "\n".join(['first(%s) = %s' % (k, v) for k, v in first_set.items()])
