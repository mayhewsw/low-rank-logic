#!/usr/bin/python
import sys
import xml.etree.cElementTree as ET
import collections

# should be kbp2013_test_.....
infile = sys.argv[1]

tree = ET.parse(infile)
root = tree.getroot()

with open("../../../data/out/latest/predict.txt") as f:
    predictions = f.readlines()

ans = {}
threshold = 0.80

tp = 0
fp = 0
fn = 0
tn = 0
    
for line in predictions:
    sline = line.strip().split("\t")
    rel = sline[-2]
    args = sline[1]
    arg1 = args.split("|")[0]
    arg2 = args.split("|")[1]
    score = float(sline[0])

    key = rel + ":" + arg1 + ":" + arg2

    if score > threshold:
        pred = "YES"
    else:
        pred = "NO"
    
    ans[key] = pred

    
# each prediction line looks like:
# score arg1|arg2 relna relation

# can just compare these against entailment file.

    
d = {}
mismatches = 0

# gather data
for child in root:
    at = child.attrib
    key = "REL$" + at["entity_type"] + ":" + at["attribute"]
    entailment = at["entailment"]
    entity = child[0].text.strip()
    value = child[1].text.strip()
    doc = child[2].text.strip()
    # key for dict is:
    # rel+entity+value

    k = key+":"+entity+":"+value+":"+doc

    if k in d and d[k] != entailment:
        mismatches += 1
        
    d[k] = entailment
    
    if k in ans:
        pred = ans[k]
    else:
        pred = "NO"

    gold = entailment
    if gold == "YES":
        if pred is "YES":
            tp += 1
        else:
            fn += 1
    else:
        if pred is "YES":
            fp += 1
        else:
            tn += 1


recall = tp / float(tp+fn)
precision = tp / float(tp + fp)
f1 = 2*recall*precision / (recall + precision)
        
print "Precision: ", precision
print "Recall: ", recall
print "F1: ", f1

print "Total: ", tp+fp+tn+fn    
print "Mismatches: ", mismatches    

    

