#!/usr/bin/env python3
import sys

def parse(filename):
    parents = []

    roots = []
    root = []

    tree = root

    roots.append(root)

    def up():
        if len(parents) == 0:
            newroot = []
            roots.append(newroot)
            parents.append(newroot)
            
        tree = parents.pop()
        if len(line) > 2:
            tree.append(line[2:-1])

    with open(filename) as fp:
        for line in fp:
            if line[0] in "+-.<":
                action = line[0]
                if action == ".":
                    tree.append(line[2:-1])
                elif action == "+":
                    newtree = [line[2:-1]]
                    tree.append(newtree)
                    parents.append(tree)
                    tree = newtree
                elif action == "-":
                    if len(parents) == 0:
                        newroot = []
                        roots.append(newroot)
                        parents.append(newroot)
                        
                    tree = parents.pop()
                    if len(line) > 2:
                        tree.append(line[2:-1])
                elif action == "<":
                    nlevels = int(line[2:-1])
                    for _ in range(nlevels):
                        if len(parents) == 0:
                            newroot = []
                            roots.append(newroot)
                            parents.append(newroot)
                        tree = parents.pop()


    return roots


def generate_sexp(tree):
    items = []
    for node in tree:
        if isinstance(node, list):
            items.append(generate_sexp(node))
        else:
            items.append(node)

    return f"({" ".join(items)})"

roots = parse(sys.argv[1])
sexps = [generate_sexp(root) for root in roots]
print("\n".join(sexps))
