#!/usr/bin/env python3
import sys
from pprint import pprint

def mkatom(atom, linum):
    return {
        "atom": atom,
        "linum": linum
    }

def mkdz(dz, linum):
    return {
        "dz": dz,
        "linum": linum,
    }


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
        linum = 0
        for line in fp:
            linum += 1
            if line[0] in "+-.<":
                action = line[0]
                atom = line[2:-1]
                if action == ".":
                    tree.append(mkatom(atom, linum))
                elif action == "+":
                    newtree = [mkatom(atom, linum)]
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
                        tree.append(mkatom(atom, linum))
                elif action == "<":
                    nlevels = int(atom)
                    for _ in range(nlevels):
                        if len(parents) == 0:
                            newroot = []
                            roots.append(newroot)
                            parents.append(newroot)
                        tree = parents.pop()
            elif len(line) > 1:
                tree.append(mkdz(line, linum))


    return roots

def get_max_linum(root):
    max_linum = 0
    for node in root:
        if isinstance(node, list):
            max_linum = max(max_linum, get_max_linum(node)) 
        else:
            max_linum = max(max_linum, node['linum']) 
    return max_linum


def generate_dagzet(root, nzeros, parent=None, filename=None):
    def node_name(node, label='atom'):
        return f"{str(node['linum']).zfill(nzeros)}_{node[label]}"
   
    prev = None
    for node in root:
        if isinstance(node, list):
            if prev:
                co = f"co {node_name(node[0])} {node_name(prev)}"
                print(co)
            generate_dagzet(node, nzeros, parent=node[0])
        else:
            if "dz" in node:
                print(node['dz'])
                # if filename and node['dz'][:2] == "nn":
                #     metanode = f"meta/{node['linum']}"
                #     print(f"co $ {metanode}")
                #     nn = f"nn {metanode}"
                #     fr = f"fr {filename} {node['linum']}"
                #     print(nn)
                #     print(fr)

                continue
            nn = f"nn {node_name(node)}"
            ln = f"ln {node['atom']}"
            co = None
            if parent and parent is not node:
                co = f"co $ {node_name(parent)}"

            print(nn)
            print(ln)
            if co:
                print(co)
            if filename:
                fr = f"fr {filename} {node['linum']}"
                print(fr)
            prev = node

filename = sys.argv[1]
roots = parse(filename)

for root in roots:
    nzeros = len(str(get_max_linum(root)))
    generate_dagzet(root, nzeros, filename=filename)
