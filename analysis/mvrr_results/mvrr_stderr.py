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
#PARTICLE_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 30, 40]
PARTICLE_NUMBERS = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90]
# the region we're currently considering
REGION_NUMBER = 5

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
for num_particle in PARTICLE_NUMBERS:
    # the overall dict will store mappings from the condition to lists of lists of surprisals
    overall_dict = {}
    # iterate through the distinct runs for each size
    for i in range(NUM_RUNS):
        # the temporary dict stores mappings from the condition to the list of surprisals for that file
        temp_dict = {}
        #file = pd.read_csv(f"mvrr_{num_particle}_{i + 1}.txt", sep="\t")
        file = pd.read_csv(f"bigger_model/{num_particle}-mvrr-{i + 1}.txt",
                           sep="\t")
        for i in range(len(META_DATA)):
            sentence = file[file["sentence_id"] == i + 1]
            counter = 0
            condition_name = META_DATA[i]["condition_name"]
            for region in META_DATA[i]["regions"]:
                counter += len(region["content"].split())
                # get the surprisal in the target region
                if region["region_number"] == REGION_NUMBER:
                    surprisal = np.asarray(sentence["surprisal"])[counter - 1]
                    if condition_name not in temp_dict:
                        temp_dict[condition_name] = []
                    else:
                        temp_dict[condition_name].append(surprisal)
        # update the overall dict based on the surprisal values of the file currently under consideration
        for key in temp_dict:
            if key not in overall_dict:
                overall_dict[key] = []
            overall_dict[key].append(temp_dict[key])

    # now compute overall means and standard error
    means_for_stderr = {}
    # get the mean for each item for each condition
    for key in overall_dict:
        means = [np.mean(np.asarray([curr_list[i] for curr_list in overall_dict[key]])) for i in range(len(overall_dict[key][0]))]
        means_for_stderr[key] = means
        # the mean for this size will be the average of the means for each item
        if key not in MEAN_DICT:
            MEAN_DICT[key] = []
        MEAN_DICT[key].append(np.mean(np.asarray(means)))
    # subtract the cross-condition mean surprisal for each item and compute the standard error
    overall_means = [np.mean(np.asarray([curr_list[i] for curr_list in means_for_stderr.values()])) for i in range(len(overall_dict[key][0]))]
    for mean in means_for_stderr:
        new_mean = [means_for_stderr[mean][i] - overall_means[i] for i in range(len(overall_means))]
        if mean not in STDERR_DICT:
            STDERR_DICT[mean] = []
        STDERR_DICT[mean].append(np.std(np.asarray(new_mean))/np.sqrt(len(new_mean)))

# graph the results_bllip
fig, ax = plt.subplots()
plt.title(f"Particle Filter Surprisals for MVRR at {REGION_DATA[REGION_NUMBER]}")
for key in MEAN_DICT:
    ax.errorbar(PARTICLE_NUMBERS, MEAN_DICT[key], yerr=STDERR_DICT[key], label=key)
plt.ylabel("mean surprisal")
plt.xlabel("number of particles")
plt.legend()
plt.show()
