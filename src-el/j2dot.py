import json
import random
from collections import defaultdict

nodes = defaultdict(list)
edges = {}
cluster = {}

# parse the stylesheet file
def readStyleSheet(stylefile):
    global styles
    with open(stylefile) as style_file:    
        styles = json.load(style_file)

def parse(datafile, output):
    f= open(output,"w")
    f.write("digraph{\n")
    with open('data.json') as data_file:    
        data = json.load(data_file)
        f.write('rankdir=' + styles["Graph"]["rankdir"] + '\n')
        f.write('labelloc=' + styles["Graph"]["labelloc"] + '\n')
        f.write('labeljust=' + styles["Graph"]["labeljust"] + '\n')
        f.write('fontsize=' + styles["Graph"]["fontsize"] + '\n')
        f.write('label="' + styles["Graph"]["label"] + '"\n')
        # seperate different node, edge, cluster, ... objects
        for item, attr in data.iteritems():
            if data[item]["type"] == "node":
                nodes[data[item]['group']].append(data[item]["concept"])
            elif data[item]["type"] == "edge":
                edges[item] = attr
            elif data[item]["type"] == "cluster":
                cluster[item]= attr
    for n in nodes:
        f.write('node[shape="' +styles[n]["shape"] + '", style="' +styles[n]["style"] + '", color="' + styles[n]["color"] + '", fillcolor="' + styles[n]["fillcolor"] +'"]' +'\n')
        for g in nodes[n]:
            if n!= "common":
               f.write('"'+ n + "." + g + '"\n')
            else:
               f.write(g + '\n')           
    for key, value in cluster.iteritems():
       r = lambda: random.randint(0,255)
       color = "#" + hex(r())[2:] + hex(r())[2:] + hex(r())[2:]
       f.write('subgraph cluster' + str(random.randint(0,100)) + '{\n')
       f.write('label=""\n')
       f.write('color="' + color + '"\n')
       c = cluster[key]['s'].split(",")
       for i in range(0, len(c)):
           f.write('"' + c[i] + '"\n')
       f.write('}\n')
       f.write('edge[style="' + styles["lsum"]["style"] + '", color="' + color + '", penwidth="' + cluster[key]["w"] + '"]' +'\n')
       f.write('"' + c[1] + '" -> "' + cluster[key]['t'] + '" [label="' + cluster[key]["l"] + '"]\n')
    for key, value in edges.iteritems():
        if edges[key]["l"] in styles:
            edge = edges[key]["l"]
        else:
            edge = "default"
        color = styles[edge]["color"] 
        f.write('edge[style="' + styles[edge]["style"] + '", color="' + color + '", penwidth="' + edges[key]["w"] + '"]' +'\n')
        f.write('"' + edges[key]["s"] + '" -> "' + edges[key]["t"] + '"')
        if edges[key]["l"] != "isa":
            f.write(' [label="' + edges[key]["l"] + '"]')
        f.write('\n')
    f.write('}')            
    f.close()         

readStyleSheet('stylesheet.json')
parse('data.json', 'out.dot')










