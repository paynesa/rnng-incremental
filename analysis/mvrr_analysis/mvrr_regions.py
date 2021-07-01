"""Calculates and plots the mean surprisal at each of the points in the MVRR sentence"""

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

# a list of the values of k used
PARTICLE_NUMBERS = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
# the region we're currently considering
REGION_NUMBER = 6

# load in the meta data about the sentences from the JSON files
META_DATA = []
mvrr_json = json.load(open("mvrr.json"))
for item in mvrr_json["items"]:
    for sub_item in item["conditions"]:
        META_DATA.append(sub_item)

# dictionaries that will store mappings from the conditions to means and stderrs
MEAN_DICT = {}
STDERR_DICT = {}

# number of times we ran the particle filter with each value of k
NUM_RUNS = 10
# iterate through the values of k
# the overall dict will store mappings from the condition to lists of lists of surprisals
overall_dict = {}
# iterate through the distinct runs for each size
for i in range(NUM_RUNS):
    # the temporary dict stores mappings from the condition to the list of surprisals for that file
    temp_dict = {}
    file = pd.read_csv(f"particle_bllip_results/100-mvrr-{i + 1}.txt", sep="\t")
    for j in range(len(META_DATA)):
        sentence = file[file["sentence_id"] == j + 1]
        counter = 0
        condition_name = META_DATA[j]["condition_name"]
        if condition_name not in temp_dict:
            temp_dict[condition_name] = {}
        for region in META_DATA[j]["regions"]:
            counter += len(region["content"].split())
            # get the surprisal in the target region
            region_number = region["region_number"]
            surprisal = np.asarray(sentence["surprisal"])[counter - 1]
            if region_number not in temp_dict[condition_name]:
                temp_dict[condition_name][region_number] = []
            temp_dict[condition_name][region_number].append(surprisal)

    # update the overall dict based on the surprisal values of the file currently under consideration
    for key in temp_dict:
        if key not in overall_dict:
            overall_dict[key] = {}
        for key2 in temp_dict[key]:
            if key2 not in overall_dict[key]:
                overall_dict[key][key2] = []
            overall_dict[key][key2].append(temp_dict[key][key2])
means_for_stderr = {}
for key in overall_dict:
    if key not in means_for_stderr:
        means_for_stderr[key] = {}
    for region_number in overall_dict[key]:
        means = [np.mean(np.asarray([curr_list[i] for curr_list in overall_dict[key][region_number]])) for i in range(len(overall_dict[key][region_number][0]))]
        means_for_stderr[key][region_number] = means
        print(means)

cross_condition_means = {}
for region_number in REGION_DATA:
    things_to_take_mean_of = [means_for_stderr[condition_name][region_number] for condition_name in overall_dict]
    means = [np.mean(np.asarray([curr_list[i] for curr_list in things_to_take_mean_of])) for i in range(len(things_to_take_mean_of[0]))]
    cross_condition_means[region_number] = means
print(cross_condition_means)

fig, ax = plt.subplots()
plt.title("Hello")
for condition_name in means_for_stderr:
    current_means = [np.mean(np.asarray([means_for_stderr[condition_name][i] ])) for i in REGION_DATA]
    new_means = [([means_for_stderr[condition_name][region_number][i] - cross_condition_means[region_number][i] for i in range(len(cross_condition_means[region_number]))]) for region_number in REGION_DATA]
    current_stderrs = [np.std(np.asarray(new_means[i]))/np.sqrt(len(new_means[i])) for i in range(len(new_means))]
    print(new_means)
    print(current_means, condition_name)
    ax.errorbar(list(REGION_DATA.keys()), current_means,
                yerr=current_stderrs, label=condition_name)
plt.legend()
plt.show()





