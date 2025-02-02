#!/usr/bin/python

# Copyright (c) 2014 University of California, Davis
#
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import yaml

nodes = {}
edges = {}
art2symbol = {"equals":"==",
                  "is_included_in":"<",
                  "includes":">",
                  "overlaps":"><"}
def add_edge(s,t,label):
    edge = {}
    edge.update({"s" : s})
    edge.update({"t" : t})
    edge.update({"label" : label})
    edges.update({s + "_" + t : edge})
def add_node(concept, group):
    node = {}
    node.update({"concept": concept})
    node.update({"group": group})
    if group!="none":
        nodes.update({group + "." + concept: node})
    else:
        nodes.update({concept: node})
art = []
dictionary = {}  # group number and list of nodes in the group
f = open("in.txt", "r")
for line in f.readlines():
    if line.startswith("taxonomy"):
        groups = []
        g = line.split(" ")[1]
    if line.startswith("("):
        groups.append(line[1:-2].split(" "))
    if line =="\n":
        dictionary.update({g : groups})
    if line.startswith("["):
        art.append (line[1:-2])
for key, attr in dictionary.items():
    for value in attr:
        parent = value.pop(0)
        add_node(parent, key)
        for v in value:
            add_node(v, key)
            add_edge(key + "." + v, key + "." + parent, "isa")
for a in art:
    a = a.replace("3sum", "sum")
    a = a.replace ("4sum", "sum")
    a = a.replace("3diff", "diff")
    a = a.replace ("4diff", "diff")
    if "{" in a:
        start = a.split(" {")[0]
        end = a.split("} ")[-1]
        ops = a.split("{", 1)[1].split("}")[0].split(" ")
        label = art2symbol[ops [0]]
        for i in range(1,len(ops)):
            label = label + " OR " + art2symbol[ops[i]]
        add_edge(start, end, label)
    else:
        if any(l in a for l in ["lsum", "ldiff"]):
            if "lsum" in a:
                l = "lsum"
                op = "+"
            else:
                l = "ldiff"
                op = "-"
            plus = a.split(" " + l)[-1][-1] + op
            add_node(plus, "none")
            add_edge(plus, a.split(" " + l + " ")[-1], "out")
            for i in range(0,len(a.split(" " + l)[0].split(" "))):
                add_edge(a.split(" " + l)[0].split(" ")[i], plus, "in")
        elif any(l in a for l in ["rsum", "rdiff"]):
            if "rsum" in a:
                l = "rsum"
                op = "+"
            else:
                l= "rdiff"
                op = "-"
            plus = a.split(" " + l)[0][-1] + op
            add_node(plus, "none")
            add_edge(plus, a.split(" " + l + " ")[0], "out")
            for i in range(1,len(a.split(" " + l)[-1].split(" "))):
                add_edge(a.split(" " + l)[-1].split(" ")[i], plus,"in")
        else:
            label = art2symbol[a.split(" ")[1]]
            add_edge(a.split(" ")[0], a.split(" ")[2], label)
f.close()
with open("out.yaml", "w") as outfile:
    outfile.write(yaml.safe_dump(nodes, default_flow_style=False))
    outfile.write(yaml.safe_dump(edges, default_flow_style=False))
