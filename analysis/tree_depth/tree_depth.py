"""Calculates the mean difference between the depth of the sentence in the
gold standard parses and the prediced model parses"""
import numpy as np

# get the gold standard tree depths from the gold standard parses
GOLD_DEPTH = []
for line in open("gold_parses_tree_depth.txt", "r"):
    line = line.strip()
    max_depth = 0
    n_open = 0
    n_closed = 0
    # maximum depth = maximum difference between open and closed parentheses counts
    for char in line:
        if char == "(":
            n_open += 1
        if char == ")":
            n_closed += 1
        if n_open - n_closed > max_depth:
            max_depth = n_open - n_closed
    GOLD_DEPTH.append(max_depth)

# get the test sentence depths
TEST_DEPTH = []
sent_num = -1
sentences = {}
for line in open("bllip_tree_depth.txt", "r"):
    line = line.split("\t")
    # we take this to be the border between two sets of particle parses and weights
    if len(line) < 2:
        sent_num += 1
        # if we have collected a set of particle parses, sort them by probability and take the most probable
        if sentences:
            line = [k for k, v in sorted(sentences.items(), key=lambda x : x[1])][-1]
            max_depth = 0
            n_open = 0
            n_closed = 0
            # calculate the depth of the most probable parse as we did for the gold standard ones
            for char in line:
                if char == "(":
                    n_open += 1
                if char == ")":
                    n_closed += 1
                if n_open - n_closed > max_depth:
                    max_depth = n_open - n_closed
            TEST_DEPTH.append(max_depth)
        sentences = {}
    # if we haven't reached a break yet, store the particle and its weight
    else:
        sentences[line[0]] = float(line[1])

#calculate the differences between the gold and test depth
DIFFERENCES = np.asarray([GOLD_DEPTH[i]-TEST_DEPTH[i] for i in range(len(GOLD_DEPTH))])

print(f"On average, gold parses are {np.mean(DIFFERENCES)} deeper than predicted parses (stderr = {np.std(DIFFERENCES)/np.sqrt(len(DIFFERENCES))})")


