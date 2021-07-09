"""Analyses Errors at the single particle MVRR sentences"""

import json, math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#provides information about the regions under consideration
REGION_DATA = {
        1 : "Start",
        2 : "Noun",
        3 : "Ambiguous verb",
        4 : "RC contents",
        5 : "Disambiguator",
        6 : "End"
    }

# load in the meta data about the sentences from the JSON files
META_DATA = []
mvrr_json = json.load(open("../mvrr_analysis/mvrr.json"))
for item in mvrr_json["items"]:
    for sub_item in item["conditions"]:
        META_DATA.append(sub_item)

# dictionary to store information about the sentences
AVERAGED_DICT = {}

for i in range(10):
    sentence_number = 0
    OVERALL_DICT = {}
    for line in open(f"bllip_particle/single-particle-{i+1}.txt"):
    #for line in open("single_particle.txt", "r"):
        if line.strip() and line.split()[0] != "Running":
            line = line.strip().split()
            region_index = 0
            # store information based on the current condition
            condition_name = META_DATA[sentence_number]["condition_name"]
            if condition_name not in OVERALL_DICT:
                OVERALL_DICT[condition_name] = {}
            regions = META_DATA[sentence_number]["regions"]
            # a stack to store the current open NT, padded with an extra in the case of a prematurely closed NT
            curr_open_nt = ["NULL"]
            for word in line:
                # open NT
                if "(" in word:
                    curr_open_nt.append(word)
                else:
                    # if we have closed an NT, then we need to pop the NT off the stack
                    subtract = word.count(")")
                    word = word.replace(")", "")
                    # update the information for the current condition
                    if  regions[region_index]["content"] and regions[region_index]["content"].split()[-1] == word:
                        region_number = regions[region_index]["region_number"]
                        if region_number not in OVERALL_DICT[condition_name]:
                            OVERALL_DICT[condition_name][region_number] = {}
                        if curr_open_nt[-1] not in OVERALL_DICT[condition_name][region_number]:
                            OVERALL_DICT[condition_name][region_number][curr_open_nt[-1]] = 1
                        else:
                            OVERALL_DICT[condition_name][region_number][curr_open_nt[-1]] += 1
                        region_index += 1
                        if region_index == len(regions):
                            break

                    # pop off all of the closed NTs from the stack
                    if subtract:
                        while subtract:
                            del curr_open_nt[-1]
                            subtract -= 1

            sentence_number += 1

    # append the values for averaging
    for key in OVERALL_DICT:
        if key not in AVERAGED_DICT:
            AVERAGED_DICT[key] = {}
        for region_number in OVERALL_DICT[key]:
            if region_number not in AVERAGED_DICT[key]:
                AVERAGED_DICT[key][region_number] = {}
            for nt in OVERALL_DICT[key][region_number]:
                if nt not in AVERAGED_DICT[key][region_number]:
                    AVERAGED_DICT[key][region_number][nt] = []
                AVERAGED_DICT[key][region_number][nt].append(OVERALL_DICT[key][region_number][nt])




# average and plot the values
OVERALL_DICT = {}
for key in AVERAGED_DICT:
    OVERALL_DICT[key] = {}
    for region_number in AVERAGED_DICT[key]:
        if region_number not in OVERALL_DICT[key]:
            OVERALL_DICT[key][region_number] = {}
        for nt in AVERAGED_DICT[key][region_number]:
            OVERALL_DICT[key][region_number][nt] = np.mean(np.asarray(AVERAGED_DICT[key][region_number][nt]))

def my_pct(pct):
    return f"{pct :.1f}%" if pct > 3 else ""

# plot the pie charts for each of the four cases
for i in [5]:
    print(i, REGION_DATA[i])
    fig, ax  = plt.subplots(2, 2)
    fig.suptitle(f"Bllip Particle Filtering Distribution of predicted NTs for {REGION_DATA[i]}")
    where_to_plot = [ax[0,0], ax[0,1], ax[1,0], ax[1,1]]
    where = 0
    for key in sorted(OVERALL_DICT.keys()):
        labels = [x.replace("(", "") for x in list(OVERALL_DICT[key][i].keys())]
        values = list(OVERALL_DICT[key][i].values())
        wp = {'linewidth': 0.5, 'edgecolor': "black"}
        where_to_plot[where].pie(values, labels=labels, shadow=False, startangle=90, autopct=my_pct, wedgeprops=wp)
        where_to_plot[where].set_title(key)
        where += 1
    plt.show()


